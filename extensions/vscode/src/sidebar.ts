(function() {
    const vscode = acquireVsCodeApi();

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