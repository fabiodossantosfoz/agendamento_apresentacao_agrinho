document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('agendamentoForm');
    const dataApresentacaoSelect = document.getElementById('dataApresentacao');
    const periodoSelect = document.getElementById('periodo');
    const horarioSelect = document.getElementById('horario');
    const messageDiv = document.getElementById('message');

    async function updateHorarios() {
        horarioSelect.innerHTML = '<option value="">Selecione</option>';
        
        const data = dataApresentacaoSelect.value;
        const periodo = periodoSelect.value;

        if (!data || !periodo) {
            return;
        }

        try {
            const response = await fetch(`/api/agendamentos/horarios-disponiveis?data=${data}&periodo=${periodo}`);
            const result = await response.json();

            if (response.ok) {
                const horariosDisponiveis = result.horarios_disponiveis;
                
                if (horariosDisponiveis.length === 0) {
                    const option = document.createElement('option');
                    option.value = '';
                    option.textContent = 'Nenhum horário disponível';
                    option.disabled = true;
                    horarioSelect.appendChild(option);
                } else {
                    horariosDisponiveis.forEach(horario => {
                        const option = document.createElement('option');
                        option.value = horario;
                        option.textContent = horario;
                        horarioSelect.appendChild(option);
                    });
                }
            } else {
                console.error('Erro ao carregar horários:', result.error);
            }
        } catch (error) {
            console.error('Erro de conexão ao carregar horários:', error);
        }
    }

    // Atualizar horários quando data ou período mudarem
    dataApresentacaoSelect.addEventListener('change', updateHorarios);
    periodoSelect.addEventListener('change', updateHorarios);

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const agendamentoData = {
            nome_professor: document.getElementById('nomeProfessor').value,
            nome_colegio: document.getElementById('nomeColegio').value,
            categoria: document.getElementById('categoria').value,
            data_apresentacao: dataApresentacaoSelect.value,
            periodo: periodoSelect.value,
            horario: horarioSelect.value
        };

        try {
            const response = await fetch('/api/agendamentos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(agendamentoData)
            });

            const result = await response.json();

            if (response.ok) {
                messageDiv.className = 'message success';
                messageDiv.textContent = result.message;
                form.reset();
                // Limpar horários após reset
                horarioSelect.innerHTML = '<option value="">Selecione</option>';
            } else {
                messageDiv.className = 'message error';
                messageDiv.textContent = result.message || 'Erro ao agendar apresentação.';
                
                // Se o horário estava ocupado, atualizar a lista de horários
                if (response.status === 409) {
                    updateHorarios();
                }
            }
        } catch (error) {
            messageDiv.className = 'message error';
            messageDiv.textContent = 'Erro de conexão: ' + error.message;
        }
    });
});

