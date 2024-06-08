# Arquitectura REST
from flask_restful import Resource
from flask import jsonify, request
from .. import db
from main.models import UsuarioModel
from main.auth.decorators import rol_required
from flask_jwt_extended import get_jwt_identity

class Cliente(Resource):

    @rol_required(['admin', 'cliente'])
    def get(self, id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        current_user = get_jwt_identity()
        if cliente.rol == 'cliente':
            if current_user['usuarioId'] == cliente.id or current_user['rol'] == 'admin':
                return cliente.to_json()
            else:
                return 'Unauthorized', 401
        else:
            return '', 404
        
    @rol_required(['cliente'])
    def delete(self, id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        current_user = get_jwt_identity()
        if cliente.rol == 'cliente' and current_user['usuarioId'] == cliente.id:
            try:
                db.session.delete(cliente)
                db.session.commit()
                return '', 204
            except:
                db.session.rollback()
                return '', 500
        else:
            return 'Unauthorized', 401    

    @rol_required(['cliente'])
    def put(self, id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        current_user = get_jwt_identity()
        if cliente.rol == 'cliente' and current_user['usuarioId'] == cliente.id:        
            data = request.get_json().items()
            for key, value in data:
                setattr(cliente, key, value)
            try:
                db.session.add(cliente)
                db.session.commit()
                return cliente.to_json()
            except:
                db.session.rollback()
                return '', 500
        else:
            return 'Unauthorized', 401 
        
                    
class Clientes(Resource):

    @rol_required(['admin'])
    def get(self):
        # Valores predeterminados para la paginacion
        page = 1 
        per_page = 5
        # Consulta para filtrar clientes
        clientes = db.session.query(UsuarioModel).filter(UsuarioModel.rol == 'cliente')

        # Procesar datos de la solicitud si estan presentes
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                elif key == 'per_page':
                    per_page = int(value)
        # Paginacion de la consulta
        clientes = clientes.paginate(page=page, per_page=per_page, error_out=True)
        return jsonify({
            'clientes': [cliente.to_json() for cliente in clientes.items],
            'total': clientes.total,
            'pages': clientes.pages,
            'page': page
        })

    @rol_required(['admin'])
    def post(self):
        cliente = UsuarioModel.from_json(request.get_json())
        cliente.rol = 'cliente'
        try:
            db.session.add(cliente)
            db.session.commit()
            return cliente.to_json(), 201
        except:
            db.session.rollback()
            return '', 500