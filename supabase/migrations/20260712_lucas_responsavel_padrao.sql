-- Projeto escritorio-digital: Lucas vendedor como responsável de novos registros.
CREATE OR REPLACE FUNCTION set_lucas_as_default_owner()
RETURNS trigger AS $$
BEGIN
  IF TG_TABLE_NAME = 'leads' THEN
    NEW.assigned_to := '623dd724-ddeb-426c-956a-4c71f6653fa5'::uuid;
    NEW.assigned_name := 'Lucas';
  ELSIF TG_TABLE_NAME = 'tasks' THEN
    NEW.responsavel_id := '623dd724-ddeb-426c-956a-4c71f6653fa5'::uuid;
    NEW.responsavel_nome := 'Lucas';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS leads_default_lucas ON leads;
CREATE TRIGGER leads_default_lucas
  BEFORE INSERT ON leads
  FOR EACH ROW EXECUTE FUNCTION set_lucas_as_default_owner();

DROP TRIGGER IF EXISTS tasks_default_lucas ON tasks;
CREATE TRIGGER tasks_default_lucas
  BEFORE INSERT ON tasks
  FOR EACH ROW EXECUTE FUNCTION set_lucas_as_default_owner();
