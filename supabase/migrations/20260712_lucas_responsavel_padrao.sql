-- Define Lucas como responsável padrão de novos leads e tarefas.
-- Valores explicitamente escolhidos na interface continuam sendo respeitados.
ALTER TABLE leads ALTER COLUMN responsible SET DEFAULT 'Lucas';
ALTER TABLE tasks ALTER COLUMN responsible SET DEFAULT 'Lucas';

-- Guarda a situação informada ao concluir uma tarefa.
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS completion_note TEXT;
