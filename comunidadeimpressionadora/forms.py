from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, length
from comunidadeimpressionadora.models import Usuario



class FormCriarConta(FlaskForm):
    username = StringField("Nome do Usuário", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta =SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já existente. Cadastre-se com outro e-mail ou faça login")

class FormLogin(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    botao_submit_login = SubmitField("Fazer Login")
    lembrar_dados = BooleanField("Lembrar Dados de Acesso")

class FormEditarPerfil(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    foto_perfil = FileField("Atualizar Foto de Perfil", validators=[FileAllowed(['jpeg','png'])])
    curso_excel = BooleanField("Excel impressionador")
    curso_vba = BooleanField("VBA impressionador")
    curso_bi = BooleanField("Power BI impressionador")
    curso_sql = BooleanField("SQL impressionador")
    curso_py = BooleanField("Python impressionador")
    username = StringField("Nome do Usuário", validators=[DataRequired()])
    botao_editar_perfil = SubmitField("Confirmar Edição")

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError("Já existe usuário com esse e-mail. Cadastre-se com outro e-mail")

class FormCriarPost(FlaskForm):
    botao_criar_post = SubmitField("Criar Post")
    titulo = StringField("Título", validators=[DataRequired(), length(3, 50)])
    corpo = TextAreaField("Assunto", validators=[DataRequired()])
