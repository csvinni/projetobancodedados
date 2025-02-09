from flask import Flask, render_template, url_for, request, redirect
from controllers.campanha import campanha_bp
from controllers.doacao import doacao_bp
from controllers.doador import doador_bp
from auth.bp import auth_bp, login_manager
from database.config import Session, engine, Base

app = Flask(__name__)
app.secret_key = 'dificil'
login_manager.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(doacao_bp)
app.register_blueprint(doador_bp)
app.register_blueprint(campanha_bp)
Base.metadata.create_all(engine)

@app.route('/')
def index():
    return render_template('index.html')
