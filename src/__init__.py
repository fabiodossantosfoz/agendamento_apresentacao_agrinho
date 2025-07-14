import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from .models.user import db # Importa a instância 'db'

# Cria a instância da aplicação Flask
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
CORS(app)

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
# Lê a URL do banco a partir das variáveis de ambiente do Render
db_url = os.environ.get('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados com a aplicação
db.init_app(app)

# --- IMPORTAÇÃO E REGISTRO DAS ROTAS (BLUEPRINTS) ---
# As importações são feitas AQUI, depois que 'app' e 'db' já existem.
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
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# A seção if __name__ == '__main__' não é usada pelo Gunicorn, mas é bom manter para testes locais.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
