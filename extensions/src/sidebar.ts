(function() {
    const vscode = acquireVsCodeApi();

    // Add this function to handle delete button clicks
    function handleDeleteClick(event: MouseEvent) {
        const target = event.target as HTMLElement;
        if (target.classList.contains('delete-btn')) {
            const name = target.getAttribute('data-name');
            const method = target.getAttribute('data-method');
            vscode.postMessage({
                type: 'deleteEndpoint',
                name: name,
                method: method
            });
        }
    }

    // Add this to your existing event listener setup
    document.addEventListener('click', handleDeleteClick);

    document.addEventListener('click', (event: MouseEvent) => {
        const target = event.target as HTMLElement;
        
        if (target.classList.contains('webview-button')) {
            const webviewType = target.getAttribute('data-webview');
            vscode.postMessage({ type: 'openApiManagement', value: webviewType });
        } else if (target.id === 'back-button') {
            vscode.postMessage({ type: 'backButton' });
        } else if (target.id === 'new-request-btn') {
            vscode.postMessage({ type: 'newRequest' });
        } else if (target.closest('.api-endpoint')) {
            const endpoint = target.closest('.api-endpoint') as HTMLElement;
            const method = endpoint.querySelector('.method')?.textContent;
            const name = endpoint.querySelector('.name')?.textContent;
            vscode.postMessage({ type: 'selectEndpoint', value: { method, name } });
        } else if (target.id === 'export-history-btn') {
            vscode.postMessage({ type : 'exportApiHistory'});
        }
    });

    // Add filter functionality
    document.addEventListener('input', (event: Event) => {
        const target = event.target as HTMLInputElement;
        if (target.id === 'filter-history') {
            const filter = target.value.toLowerCase();
            document.querySelectorAll('.api-endpoint').forEach((endpoint: Element) => {
                const name = (endpoint.querySelector('.name') as HTMLElement)?.textContent?.toLowerCase();
                (endpoint as HTMLElement).style.display = name?.includes(filter) ? 'flex' : 'none';
            });
        }
    });
})();