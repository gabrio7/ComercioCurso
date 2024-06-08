# Rutas para login y registro

from flask import request, Blueprint
from .. import db
from main.models import UsuarioModel
from flask_jwt_extended import create_access_token
from main.auth.decorators import user_identity_lookup
from main.mail.functions import send_mail

auth = Blueprint('auth', __name__, url_prefix='/auth')

# Metodo de login
@auth.route('/login', methods=['POST'])
# funcion para login 
def login():
    # Buscamos el usuario en la db mediante el mail
    usuario = db.session.query(UsuarioModel).filter(UsuarioModel.email == request.get_json().get('email')).first_or_404()

    # Validamos la contraseña de ese usuario
    if usuario.validate_password(request.get_json().get('password')):
        
        # Generamos un nuevo token y le pasamos al usuario como identidad de ese token
        access_token = create_access_token(identity=usuario)

        # Devolvemos los valores y el token
        data = {
            'id': str(usuario.id),
            'email': usuario.email,
            'access_token': access_token,
            'rol': str(usuario.rol)
        }
        return data, 200
    else:
        return 'Incorrect password', 401



@auth.route('/register', methods=['POST'])
# Funcion para registro
def register():
    usuario = UsuarioModel.from_json(request.get_json())
    # Verifica que el email que pasa el usuario no exista en la base de datos 
    exist = db.session.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).scalar() is not None
    if exist:
        return 'Duplicated email', 409
    else:
        try:
            db.session.add(usuario)
            db.session.commit()
            send_mail([usuario.email], "Bienvenido", 'register', usuario = usuario)
        except Exception as error:
            db.session.rollback()
            return str(error), 409
        return usuario.to_json(), 201
