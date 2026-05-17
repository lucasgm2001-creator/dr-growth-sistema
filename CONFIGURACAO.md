# Configuração: Integração Magnetic Funnels → DR Growth Sistema

## Visão geral do fluxo

```
Lead vê anúncio no Facebook
         ↓
Preenche formulário (Magnetic Funnels)
         ↓
Magnetic Funnels dispara Webhook
         ↓
Supabase Edge Function recebe e salva
         ↓
Lead aparece automaticamente no site (Funil Kanban)
```

---

## PASSO 1 — Criar as tabelas no Supabase

1. Acesse https://supabase.com/dashboard
2. Selecione seu projeto `hevtlwnyarthvqmihsuk`
3. Vá em **SQL Editor** → **New Query**
4. Cole TODO o conteúdo do arquivo `supabase/setup.sql`
5. Clique em **Run** (ou Ctrl+Enter)

Você verá a mensagem de sucesso. As tabelas `leads`, `tasks`, `clients`, `payments` serão criadas.

---

## PASSO 2 — Fazer deploy da Edge Function

### Opção A: Via Supabase Dashboard (mais fácil)

1. No Dashboard do Supabase, vá em **Edge Functions**
2. Clique em **New Function**
3. Nome da função: `magnetic-webhook`
4. Cole o conteúdo do arquivo `supabase/functions/magnetic-webhook/index.ts`
5. Clique em **Deploy**

### Opção B: Via CLI (avançado)

```bash
npm install -g supabase
supabase login
supabase link --project-ref hevtlwnyarthvqmihsuk
supabase functions deploy magnetic-webhook --no-verify-jwt
```

### URL da função após deploy:
```
https://hevtlwnyarthvqmihsuk.supabase.co/functions/v1/magnetic-webhook
```

---

## PASSO 3 — Configurar Webhook no Magnetic Funnels

1. Acesse sua conta do **Magnetic Funnels**
2. Vá em **Automações** (ou Workflows)
3. Abra o workflow do seu formulário de captação
4. Adicione uma ação **Webhook**
5. Configure assim:
   - **Método**: POST
   - **URL**: `https://hevtlwnyarthvqmihsuk.supabase.co/functions/v1/magnetic-webhook`
   - **Content-Type**: application/json
6. Salve e ative o workflow

**Importante**: O webhook deve ser adicionado logo após a etapa de captura do formulário, para que o lead seja enviado imediatamente.

---

## PASSO 4 — Testar

1. Preencha seu formulário do Magnetic Funnels com dados de teste
2. Aguarde ~5 segundos
3. Abra `comercial.html` no site → o lead deve aparecer no funil (coluna "Novo Lead")

Para verificar se o webhook chegou:
- No Supabase Dashboard → **Logs** → **Edge Function Logs**
- Você verá a mensagem: `Lead salvo: [nome] ([telefone])`

---

## Dados que chegam automaticamente do Magnetic Funnels

| Campo no formulário | Campo no site |
|---|---|
| nome / name | Nome do lead |
| email | Email |
| telefone / phone | Telefone |
| empresa / company | Empresa |
| Origem do anúncio | Origem (Facebook, Instagram, etc.) |

Se o formulário tiver outros campos, eles aparecem em **Notas** do lead.

---

## Responsável padrão

Leads vindos do Magnetic chegam com responsável **"Equipe"**. Para mudar isso, edite a linha no arquivo `supabase/functions/magnetic-webhook/index.ts`:

```typescript
responsible: 'Equipe',  // ← mude para o nome desejado, ex: 'Lucas'
```

E refaça o deploy da Edge Function.

---

## Problemas comuns

**Lead não aparece no site:**
- Verifique se o SQL do Passo 1 foi executado (tabelas criadas)
- Verifique os logs da Edge Function no Supabase
- Confirme a URL do webhook no Magnetic Funnels

**Erro "relation leads does not exist":**
- Execute o SQL do Passo 1 novamente

**Erro 401 / Unauthorized:**
- A função deve ser deployada com `--no-verify-jwt` (ou desmarque JWT verification no dashboard)
