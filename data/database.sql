;CREATE TABLE tabela_projetos
(
  id INTEGER PRIMARY KEY,
  nome_do_projeto VARCHAR(100) NOT NULL,
  data_de_inicio DATE NOT NULL,
  data_de_fim DATE NOT NULL
)

;CREATE TABLE IF NOT EXISTS tabela_atividades
(
  id_atividade INTEGER PRIMARY KEY,
  id_do_projeto VARCHAR(100),
  nome_da_atividade VARCHAR(100) NOT NULL,
  data_de_inicio DATE NOT NULL,
  data_de_fim DATE NOT NULL,
  finalizada TINYINT NULL,
  CONSTRAINT id
    FOREIGN KEY (id_do_projeto)
    REFERENCES tabela_projetos (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
