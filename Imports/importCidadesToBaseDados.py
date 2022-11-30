from plataformaSms import database
from plataformaSms.models import cadEstados, cadCidades
# Pandas
import pandas as pd
#OpenpyxL
from openpyxl import Workbook, load_workbook

# tabela = pd.read_excel("./AR_BR_RG_UF_RGINT_RGIM_MES_MIC_MUN_2021.xls")
planilha = load_workbook("AR_BR_RG_UF_RGINT_RGIM_MES_MIC_MUN_2021.xlsx")
aba_ativa = planilha.active

for celula in aba_ativa["F"]:
    linha = celula.row
    if linha > 1 and linha < 5574:
        cd_uf = aba_ativa[f"B{linha}"].value
        nome_Estado = aba_ativa[f"C{linha}"].value
        sigla_Estado = aba_ativa[f"D{linha}"].value
        cod_municipio = aba_ativa[f"E{linha}"].value
        nome_municipio = aba_ativa[f"F{linha}"].value
        print(f"Linha: {celula.row} \ncd_uf: {nome_municipio}\nNome Estado: {nome_Estado}\nSigla Estado: {sigla_Estado}")
        print("-"*40)
        # Buscar ID do Index do Estado Atual da Base
        print(sigla_Estado)
        buscaEstado =  cadEstados.query.filter_by(sigla=sigla_Estado).first()
        print(f"ID Estado..: {buscaEstado.id}")
        print(f"Nome Estado: {buscaEstado.nome}")
        print(f"Sigla UF...: {buscaEstado.sigla}")
        # print(linha)
        # ---------------------------------------------------------------------
        saveCidade = cadCidades(nome=nome_municipio,
                                id_Estado=int(buscaEstado.id),
                                cd_mun_Ibge=int(cod_municipio))
        print(saveCidade)
        # Adicionar a Sessão e commitar o Registro
        database.session.add(saveCidade)
        database.session.commit()

"""
# TO CHOICE SHEET
#source = planilha.get_sheet_by_name("AR_BR_MUN_2021")
#target = planilha.copy_worksheet(source)


for celula in target.cell["F"]:
    print(f"Linha: {celula.row} - Cidade: {celula.value}")
"""