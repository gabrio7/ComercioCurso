from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel

class Usuario(Resource):
    def get(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        return usuario.to_json()
    
    def delete (self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204
    
    def put(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key, value)
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201

class Usuarios(Resource):
    def get(self):
        page = 1
        per_page = 5
        usuarios = db.session.query(UsuarioModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                elif key == 'per_page':
                    per_page = int(value)
        usuarios = usuarios.paginate(page=page, per_page=per_page, error_out=True)
        return jsonify({
            'usuarios': [usuario.to_json() for usuario in usuarios.items],
            'total': usuarios.total,
            'pages': usuarios.pages,
            'page': page 
        })