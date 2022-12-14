from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from plataformaSms.models import Usuario, CadModules, CadServers, CadOperadoras, phone_data, cadEstados, cadCidades
from flask_login import current_user

# A classe abaixo é utilizada para controlar os campos que terá no formulário
class FormCriarConta(FlaskForm):
    username                = StringField('Nome de usuário', validators=[DataRequired()])
    email                   = StringField('E-mail', validators=[DataRequired(), Email()])
    senha                   = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha       = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_CriarConta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError(f'O e-mail acima do usuário {usuario.username}  já está cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')

# A classe dos campos do Formulário de Login
class FormLogin(FlaskForm):
    email           = StringField('E-mail', validators=[DataRequired(), Email()])
    senha           = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados   =   BooleanField('Lembrar dados e acesso')
    botao_submit_Login = SubmitField('Fazer Login')


# A classe dos campos de edição do Formulário do Perfil do Usuário
class FormEditarPerfil(FlaskForm):
    username        = StringField('Nome de Usuário', validators=[DataRequired()])
    email           = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    # ---------------------------------------------------
    # ------               Cursos                  ------
    # ---------------------------------------------------
    curso_Excel     = BooleanField('Excel Impressionador')
    curso_Vba       = BooleanField('VBA Impressionador')
    curso_Python    = BooleanField('Python Impressionador')
    curso_PowerBi   = BooleanField('Power BI Impressionador')
    curso_ppt       = BooleanField('Apresentações Impressionadoras')
    curso_Sql       = BooleanField('SQL Impressionador')
    # ---------------------------------------------------
    botao_submit_EditarPerfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError(f'Já existe o usuário com esse e-mail. Cadastre outro e-mail')

# A classe dos campos para criação / Edição de Posts de Usuários
class FormCriarPost(FlaskForm):
    titulo          = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 140)])
    corpo           = TextAreaField('Escreva o seu Post Aqui', validators=[DataRequired()])
    botao_submit    = SubmitField('Criar Post')

"""
*********************************************************************************
-----                       Novos Formularios para a Optin                  ----- 
*********************************************************************************
"""
"""
-------------------------------------------
-----   CADASTRO DE SERVIDORES        ----- 
-------------------------------------------
"""
class FormCadastroServers(FlaskForm):
    descrServer = StringField('Informar a descrição do Servidor', validators=[DataRequired(), Length(3, 20)])
    fixed_ip = StringField('Informar o IP do Servidor', validators=[DataRequired(), Length(7, 15)])
    udp_Port = StringField('Informar a Porta UDP', validators=[DataRequired(), Length(2, 4)])
    activeServer = BooleanField('Servidor Ativo ?')
    botao_submit_Salvar_CadServers = SubmitField('Salvar')
# ---------------------------------------
    def validate_salvar_server(self, descrServer):
        # 1o Validate - descrServer
        cadServersDB = CadServers.query.filter_by(descrServer=descrServer.data).first()
        if cadServersDB:
            raise ValidationError(f'Este servidor: {descrServer.data} já esta cadastrado com esta descrição')
# ---------------------------------------

"""
--------------------------------------------------------
-----   CADASTRO DE OPERADORAS DE TELEFONIA        ----- 
--------------------------------------------------------
"""
class FormCadastroOperadoras(FlaskForm):
    descrOperadora = StringField('Informar a descrição da Operadora', validators=[DataRequired(), Length(3, 20)])
    foto_logo = StringField('Informar o Logo da Operadora', validators=[DataRequired(), Length(1, 100)])
    ativa = BooleanField('Operadora Ativa ?')
    botao_submit_Salvar_CadOperadoras = SubmitField('Salvar')
# ---------------------------------------
    def validate_salvar_Operadora(self, descrOperadora):
        # 1o Validate - descrOperadora
        cadOperadorasDB = CadOperadoras.query.filter_by(descrOperadora=descrOperadora.data).first()
        if cadOperadorasDB:
            raise ValidationError(f'Esta Operadora: {descrOperadora.data} já esta cadastrada com esta descrição')
# ---------------------------------------


"""
------------------------------------------
-----    CADASTRO DE MODULOS         ----- 
------------------------------------------
"""


def buscar_lista_Operadoras():
    # 1o Validate - descrOperadora
    listaOperadorasDB = CadOperadoras.query.all()
    listaOperadoras = [('0', 'Escolha uma Operadora')]
    if listaOperadorasDB:
        # print(f"Registros Encontrados:")
        for item in listaOperadorasDB:
            # print(f"ID Operadora: {item.id}\nNome Operadora: {item.descrOperadora}")
            # print("-"*30)
            newoperadora = (str(item.id), item.descrOperadora)
            # print(f"Operadora: {newoperadora}")
            listaOperadoras.append(newoperadora)
            # print(f"listaOperadoras: {listaOperadoras}")
        return listaOperadoras


class FormCadastroModulos(FlaskForm):
    OPERADORAS = buscar_lista_Operadoras()

    selectOperadoras = SelectField(u'Operadora', choices=OPERADORAS, validators=[DataRequired()])
    descrModule = StringField('Informar a descrição do Módulo', validators=[DataRequired(), Length(3, 20)])
    fixed_ip = StringField('Informar o IP do Módulo', validators=[DataRequired(), Length(7, 15)])
    udp_Port = StringField('Informar a Porta UDP', validators=[DataRequired(), Length(2, 4)])
    # udp_Port = IntegerField('Informar a Porta UDP', validators=[DataRequired(), Length(2, 4)])
    activeModule = BooleanField('Modulo Ativo ?')
    # print(f"Operadora Selecionada: {selectOperadoras}")
    botao_submit_Salvar_CadModulos = SubmitField('Salvar')
# ---------------------------------------
    def validate_salvar_modulo(self, descrModule):
        # 1o Validate - descrModule
        cadmodulesDB = CadModules.query.filter_by(descr_module=descrModule.data).first()
        if cadmodulesDB:
            raise ValidationError(f'Este módulo: {descrModule.data} já esta cadastrado com esta descrição')
# ---------------------------------------
"""
---------------------------------------------
----  MENSAGENS PARA OPERADORAS ----- 
---------------------------------------------
"""
class FormCadastroMensagensMarketing(FlaskForm):
    # Configurar o envio de mensagem para o Equipamento
    dataCadastro = StringField('Data de Cadastro', validators=[DataRequired(), Length(10, 10)])
    mensagem = StringField('Mensagem', validators=[DataRequired(), Length(10, 580)])
    ativa = BooleanField ('Ativa')
    botao_submit_Salvar_CadMensagem = SubmitField('Salvar')
    # ---------------------------------------
    def validate_CadastroMensagensMarketing(self, dataCadastro):
        # 1o Validate - DataCadastro
        pass
        '''
        cadOperadorasDB = CadOperadoras.query.filter_by(descrOperadora=descrOperadora.data).first()
        if cadOperadorasDB:
            raise ValidationError(f'Esta Operadora: {descrOperadora.data} já esta cadastrada com esta descrição')
        '''
    # ---------------------------------------


"""
---------------------------------------------
----  CADASTRO DE CONFIGURAÇÕES DE XMLs ----- 
---------------------------------------------
"""
class FormCadConfiguraXmls(FlaskForm):
    # Configurar o Formato XMLS que vai mandar para o Equipamento
    descrXML = StringField('Descrição do XML', validators=[DataRequired(), Length(3, 20)])
    rxGain = StringField('RX Gain', validators=[DataRequired(), Length(1, 6)])
    txPwr = StringField('TX PWR', validators=[DataRequired(), Length(1, 6)])
    cell = StringField('cell', validators=[DataRequired(), Length(1, 6)])
    arfcn = IntegerField('ARFCN', validators=[DataRequired(), Length(1, 6)])
    mcc = IntegerField('MCC', validators=[DataRequired(), Length(1, 6)])
    mnc = IntegerField('MNC', validators=[DataRequired(), Length(1, 6)])
    lai = IntegerField('LAI', validators=[DataRequired(), Length(1, 6)])
    sib3CellId = IntegerField('Informar Sib3CellId', validators=[DataRequired(), Length(1, 6)])
    bsic = IntegerField('BSIC', validators=[DataRequired(), Length(1, 6)])
    cro = IntegerField('CRO', validators=[DataRequired(), Length(1, 6)])
    rxLevAccMin = IntegerField('RxLevAccMin', validators=[DataRequired(), Length(1, 6)])
    reselctHyst = IntegerField('ReselctHyst', validators=[DataRequired(), Length(1, 6)])
    nbFreq = IntegerField('nbFreq', validators=[DataRequired(), Length(1, 6)])
    botao_Salvar = SubmitField('Salvar')
# ---------------------------------------
    def validate_cadconfxmls(self, rxGain):
        pass
        """"
        cadModule = CadModules.query.filter_by(descr_module=descr_module.data).first()
        if cadModule:
            raise ValidationError(f'Este módulo já esta cadastrado com esta descrição')
        """""

# ---------------------------------------
# A classe dos campos do Formulário de Login
class FormConsultarDadosCentral(FlaskForm):
    #operadora           = StringField('Operadora', validators=[DataRequired()])
    
    senha           = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados   =   BooleanField('Lembrar dados e acesso')
    
    botao_submit_ConsultarDados = SubmitField('Buscar Dados')

# ---------------------------------------
# A classe Cadastro de Estados
class FormCadEstados(FlaskForm):
    nome           = StringField('Nome do Estado', validators=[DataRequired(), Length(3, 20)])
    sigla           = StringField('Sigla UF', validators=[DataRequired(), Length(2, 2)])
    regiao          = StringField('Região UF', validators=[DataRequired(), Length(2, 15)])

# ---------------------------------------
# A classe Cadastro de Cidades
class FormCadCidades(FlaskForm):
    nome           = StringField('Nome da Cidade', validators=[DataRequired(), Length(3, 200)])
    id_Estado       = StringField('Sigla UF', validators=[DataRequired(), Length(1, 2)])
    cod_mun_ibge   = StringField('Sigla UF', validators=[DataRequired(), Length(1, 8)])
# ---------------------------------------
