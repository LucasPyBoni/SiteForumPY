Sobre o projeto:
Projeto baseado em um fórum, onde você pode fazer seus posts sobre algum tópico. Pode editar seu perfil, atualizando foto e cursos. Todos usuários podem ver seus posts, mas só você pode edita-los.

Principais Bibliotecas:
Flask, Flask-Login, flask_bcrypt, flask_wtf, wtforms, Pillow, SQLAlchemy e as criadas.

Explicação da linha de raciocínio:
O diretório principal contém todos arquivos como init.py, rotas, formulários, estrutura do banco de dados, e arquivos front html.

init.py - ativa por meio do Flask(name), assim como a base de dados, chave de segurança e uma pasta que armazena os posts postados pelos usuários.

models.py - é a estrutura da base de dados, armazena todas informações que o usuário preenche.

forms.py - contém os formulários de login, criar conta, editar perfil, e criar post os quais tem consulta e validação no banco de dados.

routes.py - são os links que ativam os formulários p/ o site através do @app.route: homepage para os posts, estando logado aparece os botões criar post, perfil e sair, estando deslogado aparece login e criar conta. O iniciar, homepage e usuários aparecem em ambos casos.

As páginas html foram feitas com ajuda do bootstrap.
