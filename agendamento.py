from src.models.user import db

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_professor = db.Column(db.String(100), nullable=False)
    nome_colegio = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    data_apresentacao = db.Column(db.String(50), nullable=False)
    periodo = db.Column(db.String(50), nullable=False)
    horario = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Agendamento {self.nome_professor} - {self.nome_colegio}>'


