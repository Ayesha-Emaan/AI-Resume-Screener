// Global functions that might be used across multiple pages

// Initialize tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Format file sizes
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Initialize file upload previews
function initFileUploadPreview(inputElement, messageElement, previewElement) {
    inputElement.addEventListener('change', function(e) {
        if (this.files.length > 0) {
            messageElement.textContent = `${this.files.length} file(s) selected`;
            
            let html = '<div class="list-group">';
            for (let i = 0; i < this.files.length; i++) {
                html += `<div class="list-group-item">
                    <i class="fas fa-file-alt me-2"></i> ${this.files[i].name}
                    <span class="badge bg-secondary float-end">${formatFileSize(this.files[i].size)}</span>
                </div>`;
            }
            html += '</div>';
            previewElement.innerHTML = html;
        } else {
            messageElement.textContent = 'Drag & drop files here or click to browse';
            previewElement.innerHTML = '';
        }
    });
}

// Initialize drag and drop for file upload areas
function initFileDropArea(dropArea, inputElement) {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropArea.classList.add('bg-light');
    }
    
    function unhighlight() {
        dropArea.classList.remove('bg-light');
    }
    
    dropArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        inputElement.files = files;
        const event = new Event('change');
        inputElement.dispatchEvent(event);
    }
}

// Document ready
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
    
    // Initialize file upload preview if elements exist
    const fileInput = document.querySelector('.file-input');
    const fileMsg = document.querySelector('.file-msg');
    const filePreview = document.getElementById('filePreview');
    
    if (fileInput && fileMsg && filePreview) {
        initFileUploadPreview(fileInput, fileMsg, filePreview);
        initFileDropArea(document.querySelector('.file-drop-area'), fileInput);
    }
    
    // Initialize range value display
    const scoreRange = document.getElementById('scoreRange');
    const rangeValue = document.getElementById('rangeValue');
    
    if (scoreRange && rangeValue) {
        scoreRange.addEventListener('input', function() {
            rangeValue.textContent = `${this.value}%`;
        });
    }
    
    // Add any other page-specific initializations here
});