from .. import mailsender, db
from flask import current_app, render_template, Blueprint
from flask_mail import Message
from smtplib import SMTPException
from main.models import UsuarioModel, ProductoModel
from main.auth.decorators import rol_required

def send_mail(to, subject, template, **kwargs):

    msg = Message(subject, sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=to)
    try:
        msg.body = render_template(f'{template}.txt', **kwargs)
        mailsender.send(msg)

    except SMTPException as error:
        return 'Mail deliver failed'
    return True

mail = Blueprint('mail', __name__, url_prefix='/mail')

#Funcion para hacer el newsletter
@mail.route('/newsletter', methods=['POST'])
@rol_required(['admin'])
def newsletter():
    usuarios = db.session.query(UsuarioModel).filter(UsuarioModel.rol == 'cliente').all()
    Productos = db.session.query(ProductoModel).all()
    try:
        for usuario in usuarios:
            send_mail([usuario.email], "Productos en Ventas", 'newsletter', usuario = usuario, productos = [producto.nombre for producto in Productos])
    except SMTPException as error:
        return 'Mail deliver failed'
    return 'mails sent', 200

