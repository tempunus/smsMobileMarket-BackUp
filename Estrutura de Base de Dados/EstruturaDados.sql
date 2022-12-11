DROP TABLE cad_Cidades;
DROP TABLE cad_Estados;

CREATE TABLE regioesPais
(id     INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
nome   VARCHAR NOT NULL,
sigla  VARCHAR NOT NULL
);

/*
INSERT INTO regioesPais (nome, sigla) values ("NORTE","N");
INSERT INTO regioesPais (nome, sigla) values ("NORDESTE","NE");
INSERT INTO regioesPais (nome, sigla) values ("SUDESTE","SE");
INSERT INTO regioesPais (nome, sigla) values ("SUL","S");
INSERT INTO regioesPais (nome, sigla) values ("CENTRO-OESTE","CO");
*/

------------------------------------------------------------------------
CREATE TABLE cad_Estados (
id       		INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
nome            VARCHAR (64),
sigla 	        VARCHAR (2),
id_Regioes      INTEGER NOT NULL,
CONSTRAINT fk_Est_id_Regioes FOREIGN KEY(id_Regioes) REFERENCES regioesPais(id)
);
------------------------------------------------------------------------

CREATE TABLE cad_Cidades (
id_Cidade       INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
nome 		    VARCHAR(200),
id_Estado 	    INTEGER,
cd_mun_Ibge 	INTEGER,
CONSTRAINT fk_CadCidEstado FOREIGN KEY(id_Estado) REFERENCES cad_Estados(id)
);
------------------------------------------------------------------------

CREATE TABLE cad_operadoras (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
"descrOperadora" VARCHAR NOT NULL, 
foto_logo 	VARCHAR, 
ativa 			BOOLEAN NOT NULL);


-- SELEÇÕES E INCLUSOES, AJUSTES E DELEÇÕES --

--INSERT INTO cad_operadoras1 (descrOperadora, foto_logo, ativa) 
--SELECT descrOperadora, foto_logo, ativa FROM cad_operadoras  ORDER BY ID ASC;

SELECT * FROM cad_operadoras1 ORDER BY ID ASC;


--PRAGMA TABLE_INFO("cad_modules")

--INSERT INTO cad_modules1 (descrModule, fixed_ip, udpPort, ativo, connected )
--SELECT  descrModule, fixed_ip, udpPort, ativo, connected FROM cad_modules ORDER BY ID ASC

--SELECT  descrModule, fixed_ip, udpPort, ativo, connected FROM cad_modules1 ORDER BY ID ASC

