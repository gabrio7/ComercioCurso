from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CompraModel
from main.auth.decorators import rol_required
from flask_jwt_extended import get_jwt_identity

class Compra(Resource):

    @rol_required(['admin', 'cliente'])
    def get(self, id):
        compra = db.session.query(CompraModel).get_or_404(id)
        current_user = get_jwt_identity()
        if current_user['usuarioId'] == compra.usuarioId or current_user['rol'] == 'admin':
            try: 
                return compra.to_json()
            except:
                return '', 404
        else:
            return 'Unauthorized', 401
        
    @rol_required(['admin', 'cliente'])
    def put(self,id):
        compra = db.session.query(CompraModel).get_or_404(id)
        current_user = get_jwt_identity()
        if current_user['usuarioId'] == compra.usuarioId or current_user['rol'] == 'admin':
            data = request.get_json().items()
            for key, value in data:
                setattr(compra, key, value)
            try:
                db.session.add(compra)
                db.session.commit()
                return compra.to_json(), 201
            except:
                return '', 404
        else:
            return 'Unauthorized', 401
        
    def delete(self, id):
        compra = db.session.query(CompraModel).get_or_404(id)
        current_user = get_jwt_identity()
        if current_user['usuarioId'] == compra.usuarioId or current_user['rol'] == 'admin':
            try:
                db.session.delete(compra)
                db.session.commit()
                return '', 204
            except:
                return '', 404
        else:
            return 'Unauthorized', 401

class Compras(Resource):

    @rol_required(['admin'])
    def get(self):
        page = 1
        per_page = 5
        compras = db.session.query(CompraModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                elif key == 'per_page':
                    per_page = int(value)
        compras = compras.paginate(page=page, per_page=per_page, error_out=True)
        return jsonify({
            'compras': [compra.to_json() for compra in compras.items],
            'total': compras.total,
            'pages': compras.pages,
            'page': page
        })

    @rol_required(['admin', 'cliente'])
    def post(self):
        compra = CompraModel.from_json(request.get_json())
        db.session.add(compra)
        db.session.commit()
        return compra.to_json(), 201