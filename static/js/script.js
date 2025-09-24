document.addEventListener('DOMContentLoaded', () => {
    const emailForm = document.getElementById('email-form');
    const submitButton = document.getElementById('submit-button');
    const buttonText = document.getElementById('button-text');
    const buttonIcon = document.getElementById('button-icon');
    const statusText = document.getElementById('status-text');

    const vortexContainer = document.querySelector('.vortex-container');
    const resultArea = document.getElementById('result-area');
    const errorAlert = document.getElementById('error-alert');
    const fileInput = document.getElementById('email_file');
    const fileLabel = document.getElementById('file-label');

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileLabel.textContent = fileInput.files[0].name; 
            fileLabel.classList.add('selected'); 
        } else {
            fileLabel.textContent = 'or upload a file';
            fileLabel.classList.remove('selected');
        }
    });


    emailForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        vortexContainer.classList.add('processing');
        submitButton.disabled = true;
        buttonText.textContent = 'Processing...';
        statusText.textContent = 'Analyzing with AI...';
        buttonIcon.className = 'spinner-border spinner-border-sm';
        resultArea.classList.add('d-none');
        errorAlert.classList.add('d-none');
        
        const formData = new FormData(event.target);

        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Server error occurred.');
            }
            
            resultArea.classList.remove('d-none');
            renderResults(data);

        } catch (error) {
            errorAlert.textContent = `Error: ${error.message}`;
            errorAlert.classList.remove('d-none');
        } finally {
            vortexContainer.classList.remove('processing');
            submitButton.disabled = false;
            buttonText.textContent = 'Analyze';
            statusText.textContent = '';
            buttonIcon.className = 'bi bi-arrow-right-circle';
        }
    });

    function renderResults(data) {
        setTimeout(() => renderClassification(data), 0);
        setTimeout(() => renderEntities(data), 200);
        setTimeout(() => renderResponse(data), 400);
    }

    function renderClassification(data) {
        const card = document.getElementById('card-classification');
        const confidencePercent = (data.confidence * 100).toFixed(0);
        card.style.animationDelay = '0s';
        card.innerHTML = `
            <h4><i class="bi bi-tags-fill"></i> Classification</h4>
            <p><strong>Category:</strong> <span class="badge" style="background-color: ${getColor(data.category, 'cat')}">${data.category}</span></p>
            <p><strong>Urgency:</strong> <span class="badge" style="background-color: ${getColor(data.urgency, 'urg')}">${data.urgency}</span></p>
            <p><strong>Confidence:</strong> ${confidencePercent}%</p>
            <div class="progress">
                <div class="progress-bar" style="width: ${confidencePercent}%"></div>
            </div>
        `;
    }

    function renderEntities(data) {
        const card = document.getElementById('card-entities');
        card.style.animationDelay = '0.2s';
        let itemsHTML = '';
        const entities = data.entities || {};
        const nameMap = { sender_name: 'Sender', ticket_number: 'Ticket #', company: 'Company' };
        
        for (const [key, value] of Object.entries(entities)) {
            itemsHTML += `<p><strong>${nameMap[key] || key}:</strong> ${value || '<em>Not found</em>'}</p>`;
        }
        if (itemsHTML === '') itemsHTML = '<p class="text-muted">No extracted entities.</p>';
        
        card.innerHTML = `<h4><i class="bi bi-bounding-box-circles"></i> Extracted Data</h4>${itemsHTML}`;
    }

    function renderResponse(data) {
        const card = document.getElementById('card-response');
        card.style.animationDelay = '0.4s';
        card.innerHTML = `
            <h4><i class="bi bi-reply-fill"></i> Suggested Response</h4>
            <textarea class="email-textarea" rows="5">${data.suggested_response}</textarea>
        `;
    }
    
    function getColor(value, type) {
        const colors = {
            cat: { 'Technical Support': '#3B82F6', 'Financial Inquiry': '#10B981', 'General': '#6B7280', 'Unproductive': '#9CA3AF' },
            urg: { 'High': '#EF4444', 'Medium': '#F59E0B', 'Low': '#3B82F6' }
        };
        return colors[type][value] || '#1F2937';
    }
});
