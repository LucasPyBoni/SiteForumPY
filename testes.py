from comunidadeimpressionadora import database, app
from comunidadeimpressionadora.models import Usuario, Foto

with app.app_context():
    database.create_all()

# usuario_1 = Usuario(username="Cuca_Beludo", email="lazadrt@gmail.com", senha="5646465")
# usuario_2 = Usuario(username="Deide_Costa", email="niltinha@gmail.com", senha="4546465")
#
# with app.app_context():
#     database.session.add(usuario_1)
#     database.session.add(usuario_2)
#
#     database.session.commit()

# with app.app_context():
#     meu_post = Post(titulo="Tamo aê", corpo="Vai dar tudo certo", id_usuario=2)
#     database.session.add(meu_post)
#
#     database.session.commit()

# with app.app_context():
#     usuarios = Usuario.query.first()
#     print(usuarios.username)
#     print(usuarios.email)
#     print(usuarios.cursos)
#     print(usuarios.id)
#
# print("------")
#
# with app.app_context():
#     usuarios = Usuario.query.filter_by(id=2).first()
#     print(usuarios.username)
#     print(usuarios.email)
#     print(usuarios.cursos)
#     print(usuarios.id)

# print("------")
#
# with app.app_context():
#     posts = Post.query.first()
#     print(posts.titulo)
#     print(posts.corpo)
#     # pegar info da outra tabela através do autor
#     print(posts.autor.username)
#     print(posts.autor.email)

