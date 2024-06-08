from .. import jwt  
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def rol_required(roles):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # Verificar que el JWT sea correcto
            verify_jwt_in_request()
            # Obtenemos los claims (peticiones o permisos), que estan dentro de JWT
            claims = get_jwt()  # Reclamos
            
            try:
                user_role = claims['sub']['rol']
                if isinstance(user_role, str) and isinstance(roles, (list, set, tuple)):
                    if user_role in roles:
                        return function(*args, **kwargs)
                    else:
                        return 'Rol not allowed', 403
                else:
                    return 'Invalid role data', 400
            except (KeyError, TypeError):
                return 'Invalid JWT claims structure', 400
        
        return wrapper
    return decorator

# Decoradores que trae JWT, los modificamos, redefinimos 

# Para que el token identifique a un usuario
@jwt.user_identity_loader
def user_identity_lookup(usuario):
    return {
        'usuarioId': usuario.id,
        'rol': usuario.rol
    }

# Para generar Claims
@jwt.additional_claims_loader
def add_claims_to_access_token(usuario):
    claims = {
        'id': usuario.id,
        'rol': usuario.rol,
        'email': usuario.email
    }
    return claims

 