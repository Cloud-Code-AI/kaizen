const vscode = acquireVsCodeApi();

function main() {

    const buttons = document.querySelectorAll('.webview-button');

    buttons.forEach((button) => {
        button.addEventListener('click', () => {
            console.log('Button clicked');
            if (button instanceof HTMLElement) {
                const text = button.textContent;
                if (text === 'API Management') {
                    vscode.postMessage({
                        type: 'openApiManagement',
                        value: 'apiManagement'
                    });
                }
                // Handle other buttons if needed
            }
        });
    });
}

main();