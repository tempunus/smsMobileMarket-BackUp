-- Na tabela abaixo foi alterado o id da Referencia do Cad_Estados pq estava errado e invalidando a
-- foreign key estando id_Estado erroneamente. OBs já foi corrigido na Base de Dados.
CREATE TABLE cad_Cidades (
id_Cidade       INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
nome 		    VARCHAR(200),
id_Estado 	    INTEGER,
cd_mun_Ibge 	INTEGER,
CONSTRAINT fk_CadCidEstado FOREIGN KEY(id_Estado) REFERENCES cad_Estados(id))
-------------------------------------------------------------------

CREATE TABLE cad_modules (
	id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
	descrModule     VARCHAR NOT NULL,
	modoDeOperacao  VARCHAR NOT NULL,
	fixed_ip        VARCHAR UNIQUE NOT NULL, 
	udpPort         INTEGER NOT NULL,
	ativo           BOOLEAN NOT NULL, 
	connected       BOOLEAN NOT NULL
);

-------------------------------------------------------------------
CREATE TABLE operadorasModulo (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
id_Modulo           INTEGER NOT NULL,
id_Operadora        INTEGER NOT NULL,
CONSTRAINT fk_IdModuloOperadorasPorModulo FOREIGN KEY(id_Modulo) REFERENCES cad_modules(id)
CONSTRAINT fk_idOperadoraPorModulo FOREIGN KEY(id_Operadora) REFERENCES cad_operadoras(id)
);

-------------------------------------------------------------------
DROP TABLE cadXmlGsm;
CREATE TABLE cadXmlGsm
(id         INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
rxGain      INTEGER NOT NULL,
txPwr       INTEGER NOT NULL,
id_Cidade   INTEGER NOT NULL,
id_Modulo   INTEGER NOT NULL,
CONSTRAINT fk_CadCidCadXmlGsm FOREIGN KEY(id_Cidade) REFERENCES cad_Cidades(id_Cidade),
CONSTRAINT fk_IdCadModuloCadXmlGsm FOREIGN KEY(id_Modulo) REFERENCES cad_modules(id)
);
-------------------------------------------------------------------
DROP TABLE itensCadXmlGsm;
CREATE TABLE itensCadXmlGsm (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
id_ItemCadXmlGsm    INTEGER NOT NULL,
arfcn               INTEGER NOT NULL,
mcc                 INTEGER NOT NULL,
mnc                 INTEGER NOT NULL,
lai                 INTEGER NOT NULL,
sib3CellId          INTEGER NOT NULL,
bsic                INTEGER NOT NULL,
cro                 INTEGER NOT NULL,
rxLevAccMin         INTEGER NOT NULL,
reselctHyst         INTEGER NOT NULL,
nbFreq              INTEGER NOT NULL,
CONSTRAINT fk_itensCadXmlGsm FOREIGN KEY(id_ItemCadXmlGsm) REFERENCES cadXmlGsm(id)
);
-------------------------------------------------------------------
--*****************************************************************
CREATE TABLE cadXml_Lte
(id         INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
id_Cidade   INTEGER NOT NULL,
id_Modulo   INTEGER NOT NULL,
CONSTRAINT fk_CadCidCadXmlLte FOREIGN KEY(id_Cidade) REFERENCES cad_Cidades(id_Cidade),
CONSTRAINT fk_IdCadModuloCadXmlLte FOREIGN KEY(id_Modulo) REFERENCES cad_modules(id)
);
-------------------------------------------------------------------
-- Fequencias das Operadoras --
CREATE TABLE itensFreqXmlLteOperadoras (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
id_cadXml_Lte   INTEGER NOT NULL,
id_Operadora    INTEGER NOT NULL,
fcn             INTEGER NOT NULL,
mcc             INTEGER NOT NULL,
mnc             INTEGER NOT NULL,
tac             INTEGER NOT NULL,
nrfcn           INTEGER NOT NULL,
CONSTRAINT fk_idCadXml_Lte FOREIGN KEY(id_cadXml_Lte) REFERENCES cadXml_Lte(id),
CONSTRAINT fk_idOperitensFreqLteOperadoras FOREIGN KEY(id_Operadora) REFERENCES cad_operadoras(id)
);
------------------------------------------------------------------------
-- CRIAR A TABELA DE MENSAGENS A SEREM ENVIADAS --
CREATE TABLE cad_Mensagens_Marketing(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
"mensagem"      VARCHAR,
"dataCadastro"  CURRENT_DATE,
ativa 			BOOLEAN NOT NULL);
-------------------------------------------------------------------
