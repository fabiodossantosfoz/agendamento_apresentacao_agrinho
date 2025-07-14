import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from .models.user import db

def create_app():
    # Cria a instância da aplicação Flask
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
    app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
    CORS(app)

    # --- CONFIGURAÇÃO DO BANCO DE DADOS ---
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o banco de dados com a aplicação
    db.init_app(app)

    # --- IMPORTAÇÃO E REGISTRO DAS ROTAS (BLUEPRINTS) ---
    # As importações são feitas AQUI, dentro da função, para evitar importação circular.
    from .routes.user import user_bp
    from .routes.agendamento import agendamento_bp

    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(agendamento_bp, url_prefix='/api')

    # --- CRIAÇÃO DAS TABELAS E ROTAS ESTÁTICAS ---
    with app.app_context():
        db.create_all()

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        # ... (código para servir arquivos estáticos)
        return send_from_directory(app.static_folder, 'index.html')

    return app

# Cria a aplicação usando a factory function
app = create_app()
