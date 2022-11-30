import flask_bcrypt
from flask import render_template, redirect, url_for, flash, request, abort
from plataformaSms import app, database, bcrypt
from plataformaSms.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCadastroModulos,\
     FormCadastroServers, FormCadastroOperadoras, FormCadConfiguraXmls, \
    FormConsultarDadosCentral, FormCriarPost
from plataformaSms.models import Usuario, Post, CadServers, CadModules, CadOperadoras, phone_data
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image  # Biblioteca para compactar Imagem


# Configuração Inicial
@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc()) # ordernar os registros pela Ordem Decrente
    return render_template('home.html', posts=posts)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    listaUsuarios = Usuario.query.all()
    return render_template('usuarios.html', listaUsuarios=listaUsuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_Login' in request.form:
        #Verificar se o usuário existe
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            # Exibir msg de Login Bem Sucedido
            print(f"Login Realizado com sucesso pelo email: {form_login.email.data}")
            flash(f"Login feito com sucesso no email: {form_login.email.data}", "alert-success")
            param_next = request.args.get('next')
            if param_next:
                return redirect(param_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f"Falha no Login: {form_login.email.data} ou Senha errada !!", "alert-danger")


    if form_criarconta.validate_on_submit() and 'botao_submit_CriarConta' in request.form:
        # Criar o Usuario
        # Critografar a senha do Usuário antes de Gravar na base de dados
        senha_criptog = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data,
                          email=form_criarconta.email.data,
                          senha=senha_criptog)

        # Adicionar a Sessão e commitar o Registro
        database.session.add(usuario)
        database.session.commit()

        print(f"Criada a conta do email: {form_login.email.data} com sucesso")
        flash(f"Conta criada para o email: {form_login.email.data}", "alert-success")
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/cadUsers', methods=['GET', 'POST'])
def cad_Users():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_Login' in request.form:
        #Verificar se o usuário existe
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            # Exibir msg de Login Bem Sucedido
            print(f"Login Realizado com sucesso pelo email: {form_login.email.data}")
            flash(f"Login feito com sucesso no email: {form_login.email.data}", "alert-success")
            param_next = request.args.get('next')
            if param_next:
                return redirect(param_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f"Falha no Login: {form_login.email.data} ou Senha errada !!", "alert-danger")


    if form_criarconta.validate_on_submit() and 'botao_submit_CriarConta' in request.form:
        # Criar o Usuario
        # Critografar a senha do Usuário antes de Gravar na base de dados
        senha_criptog = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data,
                          email=form_criarconta.email.data,
                          senha=senha_criptog)

        # Adicionar a Sessão e commitar o Registro
        database.session.add(usuario)
        database.session.commit()

        print(f"Criada a conta do email: {form_login.email.data} com sucesso")
        flash(f"Conta criada para o email: {form_login.email.data}", "alert-success")
        return redirect(url_for('home'))

    return render_template('cadUsers.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com Sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


def salvar_imagem(imagem):
    # Adicionar um código aleatorio no nome da imagem
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo_foto = nome + codigo + extensao
    print (f'Nome Arquivo de Foto {nome_arquivo_foto}')
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo_foto)
    # Reduzir o tamanho da Imagem
    tamanho = (200,200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # Salvar a imagem
    imagem_reduzida.save(caminho_completo)
    # Mudar o campo foto_perfil do usuário para o novo nome da imagem
    return nome_arquivo_foto

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        # Configurar a validação Foto Selecionada para gravar
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        
        database.session.commit()
        flash('Perfil atualizado com Sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data     = current_user.email
        form.username.data  = current_user.username

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post  = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)

        # Adicionar a Sessão e commitar o Registro
        database.session.add(post)
        database.session.commit()

        print(f"Criado o Post com o título: {form.titulo.data} com sucesso")
        flash(f"Criado o Post com o título: {form.corpo.data}", "alert-success")
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)

@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    # Verificar se o Usuário que esta chamando se ele é o dono do Post
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            # Atualizar os dados do Post do dono do Post
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído com Sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)

"""
Páginas referentes o Sistema de Envio de Mensagens
"""
@app.route('/Modules', methods=['GET', 'POST'])
@login_required
def cad_Modules():
    form_cadastroModulos = FormCadastroModulos()
    if form_cadastroModulos.validate_on_submit() and 'botao_submit_Salvar_CadModulos' in request.form:
        #Verificar se já existe o módulo Cadastrado
        # 1a Validador - descrModule
        cadmodulesDB = CadModules.query.filter_by(descrModule=form_cadastroModulos.descrModule.data).first()

        # 2a Validador - fixed_ip
        validar_fixedIP = CadModules.query.filter_by(fixed_ip=form_cadastroModulos.fixed_ip.data).first()

        if cadmodulesDB and cadmodulesDB.descrModule == form_cadastroModulos.descrModule.data:
            """Exibir mensagem dizendo que o Módulo já esta cadastrado """
            print(f"Atenção este módulo: {form_cadastroModulos.descrModule.data} já esta cadastrado !!! Favor informar outro.")
            flash(f"Atenção esta de decrição: {form_cadastroModulos.descrModule.data} já esta cadastrado !!", 'alert-info')
            # Se ja existe a mesma descrição de módulo, volta para a página
            return redirect( url_for('cad_Modules')) # Ficar na página Atual

        elif validar_fixedIP:
            print(f"Este IP {form_cadastroModulos.fixed_ip.data} já esta cadastrado !! É permitido apenas 1 IP único no sistema")
            flash(f"Este IP {form_cadastroModulos.fixed_ip.data} já esta cadastrado !! É permitido apenas 1 IP único no sistema !", 'alert-info')
            # Se ja existe o IP que esta tentando cadastrar, Recarrega a página atual
            return redirect( url_for('cad_Modules')) # Recarrega a página atual

        else:
            # Salvar os dados do Cadastro de módulo
            cadmodulesDB = CadModules(descrModule=form_cadastroModulos.descrModule.data,
                                      fixed_ip=form_cadastroModulos.fixed_ip.data,
                                      udpPort=int(form_cadastroModulos.udp_Port.data),
                                      ativo=form_cadastroModulos.activeModule.data,
                                      id_Operadora=int(form_cadastroModulos.selectOperadoras.data)
                                      )
            database.session.add(cadmodulesDB)
            database.session.commit()
            print(f"Atenção o módulo {form_cadastroModulos.descrModule.data} foi cadastrado com sucesso.")
            flash(f"Atenção o módulo {form_cadastroModulos.descrModule.data} foi cadastrado com sucesso.", "alert-success")
            # Depois que cadastrar o novo Registro, listar na tabela abaixo do cadastro
            return redirect( url_for('cad_Modules')) # Ficar na página Atual

    return render_template('cadModules.html', form_cadastroModulos=form_cadastroModulos)



"""
Configuração do Cadastro de Servidores
"""
@app.route('/servers', methods=['GET', 'POST'])
@login_required
def cad_Servers():
    form_cadServers = FormCadastroServers()
    if form_cadServers.validate_on_submit() and 'botao_submit_Salvar_CadServers' in request.form:
        #Verificar se já existe o servidor Cadastrado
        # 1a Validador - descrServer
        cadServersDB = CadServers.query.filter_by(descrServer=form_cadServers.descrServer.data).first()

        # 2a Validador - fixed_ip
        validar_fixedIP = CadServers.query.filter_by(fixed_ip=form_cadServers.fixed_ip.data).first()

        if cadServersDB and cadServersDB.descrServer == form_cadServers.descrServer.data:
            """Exibir mensagem dizendo que o Servidor já esta cadastrado """
            print(f"Atenção este servidor: {form_cadServers.descrServer.data} já esta cadastrado !!! Favor informar outro.")
            flash(f"Atenção esta de decrição: {form_cadServers.descrServer.data} já esta cadastrado !!", 'alert-info')
            # Se ja existe a mesma descrição de servidor, volta para a página
            return redirect( url_for('cad_Servers')) # Ficar na página Atual

        elif validar_fixedIP:
            print(f"Este IP {form_cadServers.fixed_ip.data} já esta cadastrado !! É permitido apenas 1 IP único no sistema")
            flash(f"Este IP {form_cadServers.fixed_ip.data} já esta cadastrado !! É permitido apenas 1 IP único no sistema !", 'alert-info')
            # Se ja existe o IP que esta tentando cadastrar, Recarrega a página atual
            return redirect( url_for('cad_Servers')) # Recarrega a página atual

        else:
            # Salvar os dados do Cadastro de servidor
            cadServerDB = CadServers(descrServer=form_cadServers.descrServer.data,
                                      fixed_ip=form_cadServers.fixed_ip.data,
                                      udpPort=int(form_cadServers.udp_Port.data),
                                      ativo=form_cadServers.activeServer.data)
            database.session.add(cadServerDB)
            database.session.commit()
            print(f"Atenção o servidor {form_cadServers.descrServer.data} foi cadastrado com sucesso.")
            flash(f"Atenção o servidor {form_cadServers.descrServer.data} foi cadastrado com sucesso.", "alert-success")
            # Depois que cadastrar o novo Registro, listar na tabela abaixo do cadastro
            return redirect( url_for('cad_Servers')) # Ficar na página Atual

    return render_template('cadServers.html', form_cadServers=form_cadServers)

"""
Consultar as informações Coletadas da Central Telefonica
"""
@app.route('/consultardados') #, methods=['GET', 'POST'])
@login_required
def consultarDados():
    form_ConsultarDados = FormConsultarDadosCentral()
    # Busca os Dados da Base de Dados
    listarDados = phone_data.query.all()
    listarModulosAtivo = CadModules.query.filter_by(ativo=1).all()

    return render_template('consulta.html', form_ConsultarDados=form_ConsultarDados, listarDados=listarDados, listarModulosAtivo=listarModulosAtivo)

#**********************************************************************************
#**********************************************************************************

"""
Páginas referentes o Sistema de Envio de Mensagens
"""
@app.route('/cadconfigxml', methods=['GET', 'POST'])
@login_required
def cad_conf_xmls():
    form_cad_conf_xmls = FormCadConfiguraXmls()
    return render_template('configXML.html', form_cad_conf_xmls=form_cad_conf_xmls)


print(f'API_KEY do Google: {app.config["GOOGLE_API_KEY"]}')

#********************************************************************************#

@app.route('/msgOperadora', methods=['GET', 'POST'])
@login_required
def msgOperadora():
    if request.method== 'POST':
        mensagem = request.form.get("mensagem")
        dataCadastro = request.form.get("dataCadastro")
    return render_template('msgOperadora.html')


print(f'API_KEY do Google: {app.config["GOOGLE_API_KEY"]}')

#********************************************************************************#

@app.route('/consulta', methods=['GET', 'POST'])
@login_required
def consulta():
    return render_template('consulta.html')


print(f'API_KEY do Google: {app.config["GOOGLE_API_KEY"]}')

#**********************************************************************************#

# Initialize the extension
@app.route('/geolocalizacao')
def minhalocalizacao():
    # Retrieve geoip data for the given requester
    # return render_template('mapearGeoLocalizacao.html')
    return render_template('geolocalizacao.html', GOOGLE_API_KEY=app.config["GOOGLE_API_KEY"])

#**********************************************************************************
#**********************************************************************************

"""
Cadastro de Operadoras de Telefonia
"""
@app.route('/cadoperadoras', methods=['GET', 'POST'])
@login_required
def cad_Operadoras():
    form_cadOperadoras = FormCadastroOperadoras()
    if form_cadOperadoras.validate_on_submit() and 'botao_submit_Salvar_CadOperadoras' in request.form:
        #Verificar se já existe a Operadora Cadastrada
        # 1a Validador - descrOperadora
        cadOperadoraDB = CadOperadoras.query.filter_by(descrOperadora=form_cadOperadoras.descrOperadora.data).first()

        if cadOperadoraDB and cadOperadoraDB.descrOperadora == form_cadOperadoras.descrOperadora.data:
            """Exibir mensagem dizendo que a Operadora já esta cadastrada """
            print(f"Atenção esta operadora : {form_cadOperadoras.descrOperadora.data} já esta cadastrada !!! Favor informar outra.")
            flash(f"Atenção esta de decrição: {form_cadOperadoras.descrOperadora.data} já esta cadastrada !!", 'alert-info')
            # Se ja existe a mesma descrição de Operadora, volta para a página
            return redirect( url_for('cad_Operadoras')) # Ficar na página Atual
        else:
            # Salvar os dados do Cadastro de Operadoras de Telefonia
            cadOperadoraDB = CadOperadoras(descrOperadora=form_cadOperadoras.descrOperadora.data,
                                           ativa=form_cadOperadoras.ativa.data,
                                           foto_logo=form_cadOperadoras.foto_logo.data)
            database.session.add(cadOperadoraDB)
            database.session.commit()
            print(f"Atenção a operadora {form_cadOperadoras.descrOperadora.data} foi cadastrada com sucesso.")
            flash(f"Atenção a operadora {form_cadOperadoras.descrOperadora.data} foi cadastrada com sucesso.", "alert-success")
            # Depois que cadastrar o novo Registro, listar na tabela abaixo do cadastro
            return redirect( url_for('cad_Operadoras')) # Ficar na página Atual

    return render_template('cadOperadoras.html', form_cadOperadoras=form_cadOperadoras)
