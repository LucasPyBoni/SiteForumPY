from comunidadeimpressionadora import app
from flask import Flask, render_template, url_for, request, redirect, flash, abort
from comunidadeimpressionadora.forms import FormCriarConta, FormLogin, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.models import Usuario, Post
from comunidadeimpressionadora import database, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import os
from PIL import Image
import secrets

@app.route("/")
def homepage():
    posts = Post.query.order_by(Post.id.desc())
    return render_template("homepage.html", posts=posts)

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template("usuarios.html", lista_usuarios=lista_usuarios)

@app.route("/login", methods=["GET", "POST"])
def login():
  # traduzir = Translator(from_lang="English", to_lang="Portuguese")
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_criarconta.email.data}', 'alert-success')
            parametro_next = request.args.get('next')
            urls_seguras = ['/','/contato','/usuarios','/login','/perfil','/post/criar']
            if parametro_next in urls_seguras:
                return redirect(parametro_next)
            else:
                return redirect(url_for('homepage'))
        else:
            flash('Falha no login, e-mail ou senhas incorretos','alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada com sucesso no e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('homepage'))
    return render_template("login.html", form_login=form_login, form_criarconta=form_criarconta)

@app.route("/sair")
@login_required
def sair():
    logout_user()
    flash("Logout feito com sucesso","alert-success")
    return redirect(url_for("homepage"))

@app.route("/perfil")
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template("perfil.html", foto_perfil=foto_perfil)

@app.route("/post/criar", methods=["GET", "POST"])
@login_required
def criar_post():
    form_criar_post = FormCriarPost()
    if form_criar_post.validate_on_submit():
        post = Post(titulo=form_criar_post.titulo.data, corpo=form_criar_post.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash("Post criado com sucesso","alert-success")
        return redirect(url_for("homepage"))
    return render_template("criarpost.html", form_criar_post=form_criar_post)

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def atualizar_cursos(form_editar_perfil):
    lista_cursos = []
    for campo in form_editar_perfil:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ";".join(lista_cursos)

@app.route("/perfil/editar", methods=["GET", "POST"])
@login_required
def editar_perfil():
    form_editar_perfil = FormEditarPerfil()
    if form_editar_perfil.validate_on_submit():
        current_user.email = form_editar_perfil.email.data
        current_user.username = form_editar_perfil.username.data
        if form_editar_perfil.foto_perfil.data:
            nome_imagem = salvar_imagem(form_editar_perfil.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form_editar_perfil)
        database.session.commit()
        flash("Edição finalizada","alert-success")
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form_editar_perfil.email.data = current_user.email
        form_editar_perfil.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template("editarperfil.html", form_editar_perfil=form_editar_perfil, foto_perfil=foto_perfil)

@app.route("/post/<post_id>", methods=["GET", "POST"])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form_criar_post = FormCriarPost()
        if request.method == "GET":
            form_criar_post.titulo.data = post.titulo
            form_criar_post.corpo.data = post.corpo
        elif form_criar_post.validate_on_submit():
            post.titulo = form_criar_post.titulo.data
            post.corpo = form_criar_post.corpo.data
            database.session.commit()
            flash("Post editado com sucesso", "alert-success")
            return redirect(url_for("homepage"))
    else:
        form_criar_post = None
    return render_template("post.html", post=post, form_criar_post=form_criar_post)

@app.route("/post/<post_id>/excluir", methods=["GET", "POST"])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash("Post excluido com sucesso", "alert-danger")
        return redirect(url_for("homepage"))
    else:
        abort(403)
