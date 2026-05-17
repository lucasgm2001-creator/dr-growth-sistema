-- ============================================================
--  DR Growth Sistema — Setup completo do banco de dados
--  Execute TUDO isso no Supabase: Dashboard > SQL Editor > New Query
-- ============================================================

-- ---- Tabela: profiles (perfis dos usuários) ----
CREATE TABLE IF NOT EXISTS profiles (
  id           UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  name         TEXT NOT NULL,
  role         TEXT NOT NULL CHECK (role IN ('admin','comercial','trafego','financeiro')),
  avatar_color TEXT DEFAULT '#6366f1',
  created_at   TIMESTAMPTZ DEFAULT now()
);

-- ---- Tabela: leads ----
CREATE TABLE IF NOT EXISTS leads (
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
  country      TEXT DEFAULT 'br',
  created_at   TIMESTAMPTZ DEFAULT now(),
  updated_at   TIMESTAMPTZ DEFAULT now()
);

-- ---- Tabela: lead_history ----
CREATE TABLE IF NOT EXISTS lead_history (
  id         BIGSERIAL PRIMARY KEY,
  lead_id    BIGINT REFERENCES leads(id) ON DELETE CASCADE,
  user_name  TEXT,
  action     TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ---- Tabela: tasks ----
CREATE TABLE IF NOT EXISTS tasks (
  id           BIGSERIAL PRIMARY KEY,
  title        TEXT NOT NULL,
  description  TEXT,
  responsible  TEXT,
  due_date     DATE,
  priority     TEXT DEFAULT 'medium' CHECK (priority IN ('high','medium','low')),
  status       TEXT DEFAULT 'pending' CHECK (status IN ('pending','in_progress','done')),
  created_at   TIMESTAMPTZ DEFAULT now()
);

-- ---- Tabela: clients ----
CREATE TABLE IF NOT EXISTS clients (
  id             BIGSERIAL PRIMARY KEY,
  name           TEXT NOT NULL,
  service        TEXT,
  responsible    TEXT,
  start_date     DATE,
  renewal_date   DATE,
  monthly_value  NUMERIC(12,2),
  health         TEXT DEFAULT 'green' CHECK (health IN ('green','yellow','red')),
  active         BOOLEAN DEFAULT true,
  country        TEXT DEFAULT 'br',
  created_at     TIMESTAMPTZ DEFAULT now()
);

-- ---- Tabela: payments ----
CREATE TABLE IF NOT EXISTS payments (
  id           BIGSERIAL PRIMARY KEY,
  client_id    BIGINT REFERENCES clients(id) ON DELETE SET NULL,
  client_name  TEXT,
  description  TEXT,
  amount       NUMERIC(12,2) NOT NULL,
  due_date     DATE,
  paid_date    DATE,
  status       TEXT DEFAULT 'pending' CHECK (status IN ('paid','pending','overdue')),
  created_at   TIMESTAMPTZ DEFAULT now()
);

-- ============================================================
--  Row Level Security (RLS)
--  Permite leitura/escrita por usuários autenticados E pelo
--  webhook do Magnetic Funnels (que usa service_role key)
-- ============================================================

ALTER TABLE leads        ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks        ENABLE ROW LEVEL SECURITY;
ALTER TABLE clients      ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments     ENABLE ROW LEVEL SECURITY;

-- Remove policies antigas se existirem
DROP POLICY IF EXISTS "auth_full"    ON leads;
DROP POLICY IF EXISTS "auth_full"    ON lead_history;
DROP POLICY IF EXISTS "auth_full"    ON tasks;
DROP POLICY IF EXISTS "auth_full"    ON clients;
DROP POLICY IF EXISTS "auth_full"    ON payments;
DROP POLICY IF EXISTS "anon_full"    ON leads;
DROP POLICY IF EXISTS "anon_full"    ON lead_history;
DROP POLICY IF EXISTS "anon_full"    ON tasks;
DROP POLICY IF EXISTS "anon_full"    ON clients;
DROP POLICY IF EXISTS "anon_full"    ON payments;

-- Políticas: permite autenticados E anon (para o site funcionar sem login Supabase)
CREATE POLICY "allow_all" ON leads        FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "allow_all" ON lead_history FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "allow_all" ON tasks        FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "allow_all" ON clients      FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "allow_all" ON payments     FOR ALL USING (true) WITH CHECK (true);

-- ============================================================
--  Função para atualizar updated_at automaticamente
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS leads_updated_at ON leads;
CREATE TRIGGER leads_updated_at
  BEFORE UPDATE ON leads
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
--  Pronto! Tabelas criadas e RLS configurado.
-- ============================================================
