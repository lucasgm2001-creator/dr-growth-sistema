// ============================================================
//  DR Growth Sistema — Supabase Configuration
//  Substitua SUPABASE_URL e SUPABASE_ANON_KEY com os seus dados
//  Acesse: https://supabase.com/dashboard → seu projeto → Settings → API
// ============================================================

const SUPABASE_URL  = 'https://qofzhpksvuqxzjqhwcpr.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_BMjHeQeryER_PDMe8En9NQ_ft0H9NP-';

// Inicializa o cliente Supabase (usando CDN via index.html)
const supabase = window.supabase
  ? window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY)
  : null;

// ============================================================
//  ESTRUTURA DAS TABELAS (execute no SQL Editor do Supabase)
// ============================================================
/*

-- Usuários do sistema (perfis)
CREATE TABLE profiles (
  id         UUID PRIMARY KEY REFERENCES auth.users(id),
  name       TEXT NOT NULL,
  role       TEXT NOT NULL CHECK (role IN ('admin','comercial','trafego','financeiro')),
  avatar_color TEXT DEFAULT '#6366f1',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Leads
CREATE TABLE leads (
  id           BIGSERIAL PRIMARY KEY,
  name         TEXT NOT NULL,
  company      TEXT,
  email        TEXT,
  phone        TEXT,
  stage        TEXT DEFAULT 'novo' CHECK (stage IN ('novo','contato','reuniao','proposta','fechado','perdido')),
  value        NUMERIC(12,2),
  responsible  TEXT,
  origin       TEXT,
  notes        TEXT,
  created_at   TIMESTAMPTZ DEFAULT now(),
  updated_at   TIMESTAMPTZ DEFAULT now()
);

-- Histórico de interações dos leads
CREATE TABLE lead_history (
  id         BIGSERIAL PRIMARY KEY,
  lead_id    BIGINT REFERENCES leads(id) ON DELETE CASCADE,
  user_name  TEXT,
  action     TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Tarefas
CREATE TABLE tasks (
  id           BIGSERIAL PRIMARY KEY,
  title        TEXT NOT NULL,
  description  TEXT,
  responsible  TEXT,
  due_date     DATE,
  priority     TEXT DEFAULT 'medium' CHECK (priority IN ('high','medium','low')),
  status       TEXT DEFAULT 'pending' CHECK (status IN ('pending','in_progress','done')),
  created_at   TIMESTAMPTZ DEFAULT now()
);

-- Clientes ativos
CREATE TABLE clients (
  id                BIGSERIAL PRIMARY KEY,
  name              TEXT NOT NULL,
  service           TEXT,
  responsible       TEXT,
  start_date        DATE,
  renewal_date      DATE,
  monthly_value     NUMERIC(12,2),
  health            TEXT DEFAULT 'green' CHECK (health IN ('green','yellow','red')),
  active            BOOLEAN DEFAULT true,
  created_at        TIMESTAMPTZ DEFAULT now()
);

-- Contratos e recebimentos
CREATE TABLE payments (
  id           BIGSERIAL PRIMARY KEY,
  client_id    BIGINT REFERENCES clients(id),
  client_name  TEXT,
  description  TEXT,
  amount       NUMERIC(12,2) NOT NULL,
  due_date     DATE,
  paid_date    DATE,
  status       TEXT DEFAULT 'pending' CHECK (status IN ('paid','pending','overdue')),
  created_at   TIMESTAMPTZ DEFAULT now()
);

-- RLS Policies (habilite Row Level Security)
ALTER TABLE leads        ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks        ENABLE ROW LEVEL SECURITY;
ALTER TABLE clients      ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments     ENABLE ROW LEVEL SECURITY;

-- Policy: usuários autenticados leem e escrevem tudo
CREATE POLICY "auth_full" ON leads        FOR ALL USING (auth.role() = 'authenticated');
CREATE POLICY "auth_full" ON lead_history FOR ALL USING (auth.role() = 'authenticated');
CREATE POLICY "auth_full" ON tasks        FOR ALL USING (auth.role() = 'authenticated');
CREATE POLICY "auth_full" ON clients      FOR ALL USING (auth.role() = 'authenticated');
CREATE POLICY "auth_full" ON payments     FOR ALL USING (auth.role() = 'authenticated');

-- Vendedores do comercial
CREATE TABLE sellers (
  id         BIGSERIAL PRIMARY KEY,
  name       TEXT NOT NULL,
  short      TEXT NOT NULL,
  color      TEXT DEFAULT '#6366f1',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Comissões
CREATE TABLE commissions (
  id                BIGSERIAL PRIMARY KEY,
  lead_id           BIGINT REFERENCES leads(id) ON DELETE SET NULL,
  lead_name         TEXT,
  lead_company      TEXT,
  lead_value        NUMERIC(12,2),
  seller            TEXT,
  commission_amount NUMERIC(12,2),
  notes             TEXT,
  created_at        TIMESTAMPTZ DEFAULT now()
);

-- Despesas
CREATE TABLE expenses (
  id         BIGSERIAL PRIMARY KEY,
  descricao  TEXT NOT NULL,
  tipo       TEXT DEFAULT 'outro',
  valor      NUMERIC(12,2),
  data       DATE,
  status     TEXT DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Campanhas de tráfego
CREATE TABLE campaigns (
  id          BIGSERIAL PRIMARY KEY,
  name        TEXT NOT NULL,
  client      TEXT,
  platform    TEXT,
  status      TEXT DEFAULT 'active',
  budget      NUMERIC(12,2) DEFAULT 0,
  spend       NUMERIC(12,2) DEFAULT 0,
  impressions BIGINT DEFAULT 0,
  clicks      BIGINT DEFAULT 0,
  leads       BIGINT DEFAULT 0,
  objective   TEXT,
  notes       TEXT,
  country     TEXT DEFAULT 'br',
  created_at  TIMESTAMPTZ DEFAULT now()
);

-- Conteúdo programado
CREATE TABLE content_pieces (
  id         BIGSERIAL PRIMARY KEY,
  title      TEXT NOT NULL,
  client     TEXT,
  platform   TEXT,
  format     TEXT,
  date       DATE,
  status     TEXT DEFAULT 'draft',
  desc       TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Add country to existing tables (run these ALTER statements)
ALTER TABLE leads   ADD COLUMN IF NOT EXISTS country TEXT DEFAULT 'us';
ALTER TABLE clients ADD COLUMN IF NOT EXISTS country TEXT DEFAULT 'us';

-- RLS for new tables
ALTER TABLE sellers        ENABLE ROW LEVEL SECURITY;
ALTER TABLE commissions    ENABLE ROW LEVEL SECURITY;
ALTER TABLE expenses       ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaigns      ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_pieces ENABLE ROW LEVEL SECURITY;

CREATE POLICY "auth_full" ON sellers        FOR ALL USING (auth.role() = 'authenticated');
CREATE POLICY "auth_full" ON commissions    FOR ALL USING (auth.role() = 'authenticated');
CREATE POLICY "auth_full" ON expenses       FOR ALL USING (auth.role() = 'authenticated');
CREATE POLICY "auth_full" ON campaigns      FOR ALL USING (auth.role() = 'authenticated');
CREATE POLICY "auth_full" ON content_pieces FOR ALL USING (auth.role() = 'authenticated');

*/

// ============================================================
//  DADOS DE DEMONSTRAÇÃO — chame seedDemoData() uma vez
// ============================================================
async function seedDemoData() {
  if (!supabase) return;

  // Leads de exemplo
  const leads = [
    { name:'Carlos Mendonça', company:'MedTech Brasil', email:'carlos@medtech.com', phone:'(11) 99234-5678', stage:'proposta', value:4500, responsible:'Lucas', origin:'LinkedIn' },
    { name:'Sarah Johnson',   company:'US Digital LLC',  email:'sarah@usdigital.com', phone:'+1 305 555-0192', stage:'reuniao', value:8200, responsible:'Lucas', origin:'Indicação' },
    { name:'Fernanda Lima',   company:'Estudio Criativo',email:'fernanda@estudio.com', phone:'(21) 98765-4321', stage:'contato', value:2800, responsible:'Gabriel', origin:'Instagram' },
    { name:'Robert Davis',    company:'GrowthX Agency',  email:'robert@growthx.io', phone:'+1 212 555-0147', stage:'fechado', value:12000, responsible:'Lucas', origin:'Google Ads' },
    { name:'Paulo Andrade',   company:'E-commerce Plus', email:'paulo@ecomplus.com', phone:'(41) 97654-3210', stage:'novo', value:3200, responsible:'Gabriel', origin:'Referência' },
    { name:'Amanda Torres',   company:'Clínica Saúde+',  email:'amanda@saude.com', phone:'(31) 96543-2109', stage:'perdido', value:1800, responsible:'Gabriel', origin:'Facebook' },
  ];

  const tasks = [
    { title:'Enviar proposta para MedTech Brasil', responsible:'Lucas', due_date:'2026-05-18', priority:'high', status:'pending' },
    { title:'Configurar campanhas de Google Ads', responsible:'Gabriel', due_date:'2026-05-15', priority:'high', status:'in_progress' },
    { title:'Reunião de onboarding — GrowthX', responsible:'Daniel', due_date:'2026-05-16', priority:'medium', status:'pending' },
    { title:'Emitir NFs de maio', responsible:'Thamyris', due_date:'2026-05-20', priority:'medium', status:'pending' },
    { title:'Revisar relatório mensal de clientes', responsible:'Daniel', due_date:'2026-05-22', priority:'low', status:'pending' },
    { title:'Ajustar landing page US Digital', responsible:'Gabriel', due_date:'2026-05-17', priority:'high', status:'in_progress' },
    { title:'Follow-up Sarah Johnson', responsible:'Lucas', due_date:'2026-05-14', priority:'high', status:'done' },
  ];

  const clients = [
    { name:'GrowthX Agency',    service:'Gestão de Tráfego', responsible:'Gabriel', start_date:'2025-11-01', renewal_date:'2026-11-01', monthly_value:12000, health:'green' },
    { name:'MedTech Brasil',    service:'Social Media + Ads', responsible:'Gabriel', start_date:'2026-01-10', renewal_date:'2026-07-10', monthly_value:4500,  health:'green' },
    { name:'US Digital LLC',    service:'Full Marketing',    responsible:'Lucas',   start_date:'2026-02-01', renewal_date:'2026-08-01', monthly_value:8200,  health:'yellow' },
    { name:'Restaurante Sabor', service:'Instagram + Stories',responsible:'Gabriel', start_date:'2025-09-15', renewal_date:'2026-09-15', monthly_value:1800,  health:'red' },
    { name:'Academia Fit',      service:'Google Ads',        responsible:'Gabriel', start_date:'2026-03-01', renewal_date:'2026-09-01', monthly_value:2400,  health:'green' },
  ];

  const payments = [
    { client_name:'GrowthX Agency',    description:'Serviços maio/2026', amount:12000, due_date:'2026-05-10', paid_date:'2026-05-09', status:'paid' },
    { client_name:'MedTech Brasil',    description:'Serviços maio/2026', amount:4500,  due_date:'2026-05-15', status:'pending' },
    { client_name:'US Digital LLC',    description:'Serviços maio/2026', amount:8200,  due_date:'2026-05-12', status:'overdue' },
    { client_name:'Restaurante Sabor', description:'Serviços maio/2026', amount:1800,  due_date:'2026-05-05', status:'overdue' },
    { client_name:'Academia Fit',      description:'Serviços maio/2026', amount:2400,  due_date:'2026-05-20', status:'pending' },
    { client_name:'GrowthX Agency',    description:'Serviços abr/2026', amount:12000, due_date:'2026-04-10', paid_date:'2026-04-08', status:'paid' },
  ];

  await supabase.from('leads').insert(leads);
  await supabase.from('tasks').insert(tasks);
  await supabase.from('clients').insert(clients);
  await supabase.from('payments').insert(payments);

  console.log('✅ Dados de demonstração inseridos!');
}

// Exporta para uso global
window.drSupabase = supabase;
window.seedDemoData = seedDemoData;
