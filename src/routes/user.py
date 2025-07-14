from flask import Blueprint

# Este é o blueprint para as rotas de usuário.
# Mesmo que não tenhamos nenhuma rota aqui ainda, o objeto precisa existir para ser importado.
user_bp = Blueprint('user_bp', __name__)

# Aqui você poderia adicionar rotas no futuro, como:
# @user_bp.route('/users', methods=['GET'])
# def get_users():
#     return "Lista de usuários"
