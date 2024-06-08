from main import create_app, db
import os

app = create_app()

# hacer push del contexto de la aplicacion
app.app_context().push()

# verificacion para ver que mi app se esta ejecutando en este archivo
if __name__ == '__main__':
# Se crean todas la tablas 
    db.create_all()

    app.run(port=os.getenv("PORT"), debug=True)