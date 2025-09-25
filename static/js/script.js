// static/js/script.js - VERSÃO FINAL E CORRIGIDA

document.addEventListener('DOMContentLoaded', () => {
    const emailForm = document.getElementById('email-form');
    const submitButton = document.getElementById('submit-button');
    const buttonText = document.getElementById('button-text');
    const buttonIcon = document.getElementById('button-icon');
    const statusText = document.getElementById('status-text');
    const vortexContainer = document.querySelector('.vortex-container');
    const resultArea = document.getElementById('result-area');
    const resultContent = document.getElementById('result-content');
    const errorAlert = document.getElementById('error-alert');
    const welcomeArea = document.getElementById('welcome-area');
    const fileInput = document.getElementById('email_file');
    const fileLabel = document.getElementById('file-label');

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileLabel.textContent = fileInput.files[0].name;
            fileLabel.classList.add('selected');
        } else {
            fileLabel.textContent = 'ou envie um arquivo';
            fileLabel.classList.remove('selected');
        }
    });

    emailForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        // Prepara a UI para o estado de "processando"
        welcomeArea.classList.add('d-none');
        resultArea.classList.add('d-none');
        errorAlert.classList.add('d-none');
        resultContent.classList.remove('d-none'); // Garante que a área de resultados normais esteja visível
        vortexContainer.classList.add('processing');
        submitButton.disabled = true;
        buttonText.textContent = 'Processando...';
        statusText.textContent = 'Analisando com IA...';
        buttonIcon.className = 'spinner';
        
        const formData = new FormData(event.target);

        try {
            const response = await fetch('/processar', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.erro || `Erro ${response.status}`);
            }

            const data = await response.json();
            
            resultArea.classList.remove('d-none'); // Mostra a "sala" de resultados
            renderizarResultados(data);

        } catch (error) {
            // CORREÇÃO AQUI: Mostra a "sala" de resultados antes de mostrar a "lâmpada" de erro.
            resultArea.classList.remove('d-none');
            // E esconde a grade de resultados de sucesso, para mostrar SÓ o erro.
            resultContent.classList.add('d-none');

            errorAlert.textContent = `Erro: ${error.message}`;
            errorAlert.classList.remove('d-none');
        } finally {
            // Restaura a UI ao estado inicial, independentemente de sucesso ou falha
            vortexContainer.classList.remove('processing');
            submitButton.disabled = false;
            buttonText.textContent = 'Analisar';
            statusText.textContent = '';
            buttonIcon.className = 'bi bi-arrow-right-circle';
        }
    });

    // As funções de renderização continuam exatamente iguais
    function renderizarResultados(data) {
        setTimeout(() => renderizarClassificacao(data), 0);
        setTimeout(() => renderizarEntidades(data), 200);
        setTimeout(() => renderizarResposta(data), 400);
    }

    function renderizarClassificacao(data) {
        const card = document.getElementById('card-classificacao');
        const confiancaPercent = (data.confianca * 100).toFixed(0);
        card.style.animationDelay = '0s';
        card.innerHTML = `
            <h4><i class="bi bi-tags-fill"></i> Classificação</h4>
            <p><strong>Categoria:</strong> <span class="badge" style="background-color: ${getColor(data.categoria, 'cat')}">${data.categoria}</span></p>
            <p><strong>Urgência:</strong> <span class="badge" style="background-color: ${getColor(data.urgencia, 'urg')}">${data.urgencia}</span></p>
            <p><strong>Confiança:</strong> ${confiancaPercent}%</p>
            <div class="progress">
                <div class="progress-bar" style="width: ${confiancaPercent}%"></div>
            </div>
        `;
    }

    function renderizarEntidades(data) {
        const card = document.getElementById('card-entidades');
        card.style.animationDelay = '0.2s';
        let itemsHTML = '';
        const entidades = data.entidades || {};
        const nomeMap = { remetente: 'Remetente', numero_ticket: 'Nº do Ticket', empresa: 'Empresa' };
        
        for (const [chave, valor] of Object.entries(entidades)) {
            if (valor) {
                itemsHTML += `<p><strong>${nomeMap[chave] || chave}:</strong> ${valor}</p>`;
            }
        }
        if (itemsHTML === '') itemsHTML = '<p class="text-muted">Nenhuma entidade extraída.</p>';
        
        card.innerHTML = `<h4><i class="bi bi-bounding-box-circles"></i> Dados Extraídos</h4>${itemsHTML}`;
    }

    function renderizarResposta(data) {
        const card = document.getElementById('card-resposta');
        card.style.animationDelay = '0.4s';
        card.innerHTML = `
            <h4><i class="bi bi-reply-fill"></i> Resposta Sugerida</h4>
            <textarea class="email-textarea" rows="5" readonly>${data.resposta_sugerida}</textarea>
        `;
    }
    
    function getColor(value, type) {
        const colors = {
            cat: { 'Suporte Técnico': '#3B82F6', 'Questão Financeira': '#10B981', 'Geral': '#6B7280', 'Improdutivo': '#9CA3AF' },
            urg: { 'Alta': '#EF4444', 'Média': '#F59E0B', 'Baixa': '#3B82F6' }
        };
        return colors[type][value] || '#1F2937';
    }
});