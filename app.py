from flask import Flask
import os,database
from controllers import auth,catalogo,pedidos
app=Flask(__name__,template_folder='views')
app.secret_key=os.environ.get('SECRET_KEY','troque')
app.teardown_appcontext(database.close_db)
for m in (auth,catalogo,pedidos):app.register_blueprint(m.bp)
def init():database.init_db()
init()
if __name__=='__main__':
    app.run(debug=True)
