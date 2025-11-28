from routes.cliente import cliente_route
from database.database import db
from database.models.cliente import Cliente , Produtos




def configure_all(app):
    configure_routes(app)
    configure_database()
    lembrar_usuario(app)
   

def configure_routes(app):
    app.register_blueprint(cliente_route )

def configure_database():
    db.connect()
    db.create_tables([Cliente, Produtos])
    


def lembrar_usuario(app):
    app.secret_key = 'pB9a86*&%89yfdafJDRTh'  


