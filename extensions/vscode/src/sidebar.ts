

const vscode = acquireVsCodeApi();
console.log('sidebar.js is being executed');

function main() {
    console.log('Main function in sidebar.ts called');

    const buttons = document.querySelectorAll('.webview-button');
    console.log(`Found ${buttons.length} buttons`);

    buttons.forEach((button) => {
        button.addEventListener('click', () => {
            console.log('Button clicked');
            if (button instanceof HTMLElement) {
                const text = button.textContent;
                if (text === 'API Management') {
                    console.log('Sending message to open API Management');
                    vscode.postMessage({
                        type: 'openApiManagement'
                    });
                }
                // Handle other buttons if needed
            }
        });
    });
}

console.log('Main function in sidebar.js called');
main();