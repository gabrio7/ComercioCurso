import os
from flask import Flask
from dotenv import load_dotenv

# Importamos el modulo para la creacion de la API
from flask_restful import Api
# Importo el modulo para conectarme con una base de datos SQL
from flask_sqlalchemy import SQLAlchemy
# Importo el modulo para trabajar con JWT
from flask_jwt_extended import JWTManager
# Importo el modulo para trabajar con mail
from flask_mail import Mail

# Lo instanciamos la API
api = Api()

# Lo instanciamos SQLAlchemy
db = SQLAlchemy()

# Lo instanciamos JWTManager
jwt = JWTManager()

# Lo instanciamos MAIL
mailsender = Mail()



# Funcion para levantar el servidor
def create_app():

    app = Flask(__name__)

    # Cargamos todas las variables de entorno
    load_dotenv()

    # Configuracion de la base de datos 
    PATH = os.getenv("DATABASE_PATH")
    DB_NAME = os.getenv("DATABASE_NAME")
    if not os.path.exists(f'{PATH}{DB_NAME}'):
        os.chdir(f'{PATH}')
        file = os.open(f'{DB_NAME}', os.O_CREAT)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PATH}{DB_NAME}'
    # Inicializamos el db.alchemy
    db.init_app(app)

    import main.resources as resources
    api.add_resource(resources.ClientesResource, '/clientes')
    api.add_resource(resources.ClienteResource, '/cliente/<id>')
    api.add_resource(resources.UsuariosResource, '/usuarios')
    api.add_resource(resources.UsuarioResource, '/usuario/<id>')
    api.add_resource(resources.ComprasResource, '/compras')
    api.add_resource(resources.CompraResource, '/compra/<id>')
    api.add_resource(resources.ProductosResource, '/productos')
    api.add_resource(resources.ProductoResource, '/producto/<id>')
    api.add_resource(resources.ProductosComprasResource, '/productos-compras')
    api.add_resource(resources.ProductoCompraResource, '/producto-compra/<id>')


# Agregamos este init_app a las app -> Aplicacion de Flask
    api.init_app(app)

    # Configurar JWT
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES")) #tiene que recibir un entero
    jwt.init_app(app)

    # Blueprints
    from main.auth import routes
    app.register_blueprint(auth.routes.auth)
    from main.mail import functions
    app.register_blueprint(mail.functions.mail)

    # Configurar mail
    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')

    mailsender.init_app(app)

    return app