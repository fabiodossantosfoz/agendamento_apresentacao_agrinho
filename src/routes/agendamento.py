from flask import Blueprint, request, jsonify
from ..models.user import db  # Importa 'db' do pacote de modelos
from ..models.agendamento import Agendamento # Importa o modelo Agendamento

# Cria o Blueprint para as rotas de agendamento
agendamento_bp = Blueprint('agendamento_bp', __name__)

@agendamento_bp.route('/agendamentos', methods=['POST'])
def create_agendamento():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados não fornecidos"}), 400

    novo_agendamento = Agendamento(
        nome_professor=data.get('nome_professor'),
        nome_colegio=data.get('nome_colegio'),
        categoria=data.get('categoria'),
        data_apresentacao=data.get('data_apresentacao'),
        periodo=data.get('periodo'),
        horario=data.get('horario')
    )

    db.session.add(novo_agendamento)
    db.session.commit()

    return jsonify({"message": "Agendamento criado com sucesso!", "id": novo_agendamento.id}), 201

@agendamento_bp.route('/agendamentos', methods=['GET'])
def get_agendamentos():
    agendamentos = Agendamento.query.all()
    lista_agendamentos = []
    for agendamento in agendamentos:
        lista_agendamentos.append({
            "id": agendamento.id,
            "nome_professor": agendamento.nome_professor,
            "nome_colegio": agendamento.nome_colegio,
            "categoria": agendamento.categoria,
            "data_apresentacao": agendamento.data_apresentacao,
            "periodo": agendamento.periodo,
            "horario": agendamento.horario
        })
    return jsonify(lista_agendamentos), 200
