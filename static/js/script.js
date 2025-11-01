// Create this file at /Users/ananth.anto/CascadeProjects/hello-curl/static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('extractForm');
    const fileInput = document.getElementById('file');
    const fileNameDisplay = document.querySelector('.file-name');
    const imagePreview = document.getElementById('imagePreview');
    const previewSection = document.querySelector('.preview-section');
    const loadingIndicator = document.getElementById('loading');
    const resultSection = document.getElementById('result');
    const resultContent = document.getElementById('resultContent');
    
    // Authentication elements
    const authIcon = document.getElementById('auth-icon');
    const authMessage = document.getElementById('auth-message');
    const configLink = document.getElementById('config-link');
    const analyzeBtn = document.getElementById('analyze-btn');
    const copyJsonBtn = document.getElementById('copy-json-btn');
    let lastJsonResult = null;

    // Camera elements
    const cameraBtn = document.getElementById('camera-btn');
    const cameraPreview = document.getElementById('camera-preview');
    const cameraCanvas = document.getElementById('camera-canvas');
    const cameraControls = document.getElementById('camera-controls');
    const capturePhotoBtn = document.getElementById('capture-photo-btn');
    const cancelCameraBtn = document.getElementById('cancel-camera-btn');
    let cameraStream = null;
    let capturedFile = null;

    // Check authentication status on page load
    checkAuthStatus();
    
    // Copy JSON button functionality
    if (copyJsonBtn) {
        copyJsonBtn.addEventListener('click', async function() {
            if (lastJsonResult) {
                try {
                    // Extract clean data
                    const cleanData = {};
                    for (const [key, value] of Object.entries(lastJsonResult)) {
                        cleanData[key] = extractValue(value);
                    }
                    
                    const jsonString = JSON.stringify(cleanData, null, 2);
                    await navigator.clipboard.writeText(jsonString);
                    
                    // Visual feedback
                    const originalText = this.textContent;
                    this.textContent = '✓ Copied!';
                    this.style.background = '#4CAF50';
                    
                    setTimeout(() => {
                        this.textContent = originalText;
                        this.style.background = '#667eea';
                    }, 2000);
                    
                    console.log('Clean JSON copied to clipboard!');
                } catch (err) {
                    console.error('Failed to copy:', err);
                    alert('Failed to copy to clipboard. Check console for the JSON data.');
                }
            }
        });
    }

    // Camera functionality
    cameraBtn.addEventListener('click', async function() {
        try {
            cameraStream = await navigator.mediaDevices.getUserMedia({ 
                video: { facingMode: 'environment' }
            });
            cameraPreview.srcObject = cameraStream;
            cameraPreview.style.display = 'block';
            cameraControls.style.display = 'block';
            cameraBtn.style.display = 'none';
            previewSection.style.display = 'none';
        } catch (error) {
            alert('Unable to access camera: ' + error.message);
        }
    });

    capturePhotoBtn.addEventListener('click', function() {
        const context = cameraCanvas.getContext('2d');
        cameraCanvas.width = cameraPreview.videoWidth;
        cameraCanvas.height = cameraPreview.videoHeight;
        context.drawImage(cameraPreview, 0, 0);
        
        cameraCanvas.toBlob(function(blob) {
            capturedFile = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
            
            // Create a data transfer to set the file input
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(capturedFile);
            fileInput.files = dataTransfer.files;
            
            // Show preview
            imagePreview.src = cameraCanvas.toDataURL('image/jpeg');
            previewSection.style.display = 'block';
            fileNameDisplay.textContent = 'camera-capture.jpg';
            
            // Stop camera
            stopCamera();
        }, 'image/jpeg', 0.9);
    });

    cancelCameraBtn.addEventListener('click', function() {
        stopCamera();
    });

    function stopCamera() {
        if (cameraStream) {
            cameraStream.getTracks().forEach(track => track.stop());
            cameraStream = null;
        }
        cameraPreview.style.display = 'none';
        cameraControls.style.display = 'none';
        cameraBtn.style.display = 'inline-block';
    }

    // Update file name display when file is selected
    fileInput.addEventListener('change', function() {
        if (capturedFile) {
            // If we just set a captured file, don't override
            capturedFile = null;
            return;
        }
        
        const fileName = this.files[0]?.name || 'No file chosen - or use camera above';
        fileNameDisplay.textContent = fileName;

        // Show preview for images only
        if (this.files && this.files[0]) {
            const file = this.files[0];
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    previewSection.style.display = 'block';
                };
                reader.readAsDataURL(file);
            } else {
                // Hide preview for non-image files
                previewSection.style.display = 'none';
            }
        }
    });

    // Authentication functions
    async function checkAuthStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            if (data.authenticated) {
                authIcon.textContent = '✅';
                authMessage.textContent = 'Ready to process documents';
                configLink.style.display = 'none';
                analyzeBtn.disabled = false;
            } else {
                authIcon.textContent = '⚠️';
                authMessage.textContent = 'Not authenticated. Please configure and authenticate first.';
                configLink.style.display = 'inline-block';
                analyzeBtn.disabled = true;
            }
        } catch (error) {
            console.error('Error checking auth status:', error);
            authIcon.textContent = '❌';
            authMessage.textContent = 'Error checking authentication status';
            configLink.style.display = 'inline-block';
            analyzeBtn.disabled = true;
        }
    }

    // Function to decode HTML entities
    function decodeHtmlEntities(str) {
        const textarea = document.createElement('textarea');
        textarea.innerHTML = str;
        return textarea.value;
    }

    // Function to extract values from nested type/value structure
    function extractValue(obj) {
        if (obj && typeof obj === 'object' && 'type' in obj && 'value' in obj) {
            if (obj.type === 'array' && Array.isArray(obj.value)) {
                return obj.value.map(item => extractValue(item));
            } else if (obj.type === 'object' && typeof obj.value === 'object') {
                const extracted = {};
                for (const [key, val] of Object.entries(obj.value)) {
                    extracted[key] = extractValue(val);
                }
                return extracted;
            } else {
                return obj.value;
            }
        }
        return obj;
    }

    // Function to format results as table
    function formatResults(data) {
        const container = document.createElement('div');
        container.style.padding = '10px';
        
        // Extract values from type/value structure
        const cleanData = {};
        for (const [key, value] of Object.entries(data)) {
            cleanData[key] = extractValue(value);
        }
        
        // Create main table
        const mainTable = document.createElement('table');
        mainTable.style.width = '100%';
        mainTable.style.borderCollapse = 'collapse';
        mainTable.style.marginBottom = '20px';
        mainTable.style.background = 'white';
        mainTable.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
        
        const tbody = document.createElement('tbody');
        
        // Separate arrays from simple fields
        const simpleFields = {};
        const arrayFields = {};
        
        for (const [key, value] of Object.entries(cleanData)) {
            if (Array.isArray(value)) {
                arrayFields[key] = value;
            } else {
                simpleFields[key] = value;
            }
        }
        
        // Display simple fields first
        for (const [key, value] of Object.entries(simpleFields)) {
            const row = document.createElement('tr');
            
            const keyCell = document.createElement('td');
            keyCell.style.padding = '12px';
            keyCell.style.border = '1px solid #000';
            keyCell.style.fontWeight = '700';
            keyCell.style.background = '#f8f9fa';
            keyCell.style.width = '200px';
            keyCell.textContent = key;
            
            const valueCell = document.createElement('td');
            valueCell.style.padding = '12px';
            valueCell.style.border = '1px solid #000';
            valueCell.colSpan = 10;
            valueCell.textContent = value || '';
            
            row.appendChild(keyCell);
            row.appendChild(valueCell);
            tbody.appendChild(row);
        }
        
        mainTable.appendChild(tbody);
        container.appendChild(mainTable);
        
        // Display array fields as separate tables
        for (const [tableName, items] of Object.entries(arrayFields)) {
            if (!Array.isArray(items) || items.length === 0) continue;
            
            // Table title
            const titleDiv = document.createElement('div');
            titleDiv.style.fontSize = '18px';
            titleDiv.style.fontWeight = '600';
            titleDiv.style.color = '#667eea';
            titleDiv.style.marginTop = '20px';
            titleDiv.style.marginBottom = '10px';
            titleDiv.style.paddingBottom = '5px';
            titleDiv.style.borderBottom = '2px solid #667eea';
            titleDiv.textContent = tableName;
            container.appendChild(titleDiv);
            
            // Create table
            const table = document.createElement('table');
            table.style.width = '100%';
            table.style.borderCollapse = 'collapse';
            table.style.background = 'white';
            table.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
            
            // Get headers from first item
            const firstItem = items[0];
            const headers = Object.keys(firstItem);
            
            // Create header row
            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');
            headers.forEach(header => {
                const th = document.createElement('th');
                th.style.padding = '12px';
                th.style.border = '1px solid #000';
                th.style.background = '#667eea';
                th.style.color = 'white';
                th.style.fontWeight = '600';
                th.style.textAlign = 'left';
                th.textContent = header;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            table.appendChild(thead);
            
            // Create data rows
            const tableBody = document.createElement('tbody');
            items.forEach((item, index) => {
                const row = document.createElement('tr');
                if (index % 2 === 1) {
                    row.style.background = '#f9f9f9';
                }
                
                headers.forEach(header => {
                    const td = document.createElement('td');
                    td.style.padding = '10px 12px';
                    td.style.border = '1px solid #ddd';
                    const value = item[header];
                    td.textContent = value !== null && value !== undefined ? value : '';
                    row.appendChild(td);
                });
                
                tableBody.appendChild(row);
            });
            table.appendChild(tableBody);
            
            container.appendChild(table);
        }
        
        // Add raw JSON view option
        const jsonToggle = document.createElement('details');
        jsonToggle.style.marginTop = '20px';
        
        const summary = document.createElement('summary');
        summary.style.cursor = 'pointer';
        summary.style.padding = '10px';
        summary.style.background = '#f0f0f0';
        summary.style.borderRadius = '4px';
        summary.style.fontWeight = '600';
        summary.textContent = '📄 View Raw JSON';
        jsonToggle.appendChild(summary);
        
        const pre = document.createElement('pre');
        pre.style.background = '#2d2d2d';
        pre.style.color = '#f8f8f2';
        pre.style.padding = '20px';
        pre.style.borderRadius = '8px';
        pre.style.overflow = 'auto';
        pre.style.fontSize = '13px';
        pre.style.lineHeight = '1.5';
        pre.style.fontFamily = "'Courier New', Courier, monospace";
        pre.style.maxHeight = '400px';
        pre.style.marginTop = '10px';
        pre.textContent = JSON.stringify(cleanData, null, 2);
        jsonToggle.appendChild(pre);
        
        container.appendChild(jsonToggle);
        
        return container;
    }

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Check authentication before proceeding
        if (analyzeBtn.disabled) {
            alert('Please configure and authenticate with Salesforce first. Click the Configuration button.');
            return;
        }
        
        loadingIndicator.style.display = 'flex';
        resultSection.style.display = 'none';

        try {
            const formData = new FormData(this);
            const response = await fetch('/extract-data', {
                method: 'POST',
                body: formData
            });

            if (response.status === 401) {
                // Authentication error - recheck status
                await checkAuthStatus();
                alert('Authentication required. Please go to Configuration page and authenticate.');
                return;
            }

            let result = await response.text();
            
            try {
                // Try to parse as JSON
                const jsonData = JSON.parse(result);
                
                // Store for copy button
                lastJsonResult = jsonData;
                
                // Log to console for debugging
                console.log('=== Document Analysis Results (Original) ===');
                console.log(JSON.stringify(jsonData, null, 2));
                
                // Extract and log clean data
                const cleanData = {};
                for (const [key, value] of Object.entries(jsonData)) {
                    cleanData[key] = extractValue(value);
                }
                console.log('=== Extracted Clean Data ===');
                console.log(JSON.stringify(cleanData, null, 2));
                console.log('================================');
                console.log('💡 Tip: Use the "Copy JSON" button to copy clean data to clipboard.');
                
                // Clear previous results
                resultContent.innerHTML = '';
                
                // Format and display results
                const formattedContent = formatResults(jsonData);
                resultContent.appendChild(formattedContent);
                
            } catch (e) {
                // If parsing fails, display as text
                console.error('JSON parsing failed:', e);
                console.log('Raw response:', result);
                resultContent.textContent = result;
            }
            
            resultSection.style.display = 'block';
        } catch (error) {
            resultContent.textContent = 'Error: ' + error.message;
            resultSection.style.display = 'block';
        } finally {
            loadingIndicator.style.display = 'none';
        }
    });
});