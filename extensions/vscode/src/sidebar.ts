import { log } from './extension';

log('sidebar.ts is being executed');

declare const vscode: {
    postMessage: (message: any) => void;
};

function main() {
    log('Main function in sidebar.ts called');
    if (typeof document !== 'undefined') {
        console.log('Document is defined');
        const buttons = document.querySelectorAll('.webview-button');
        console.log(`Found ${buttons.length} buttons`);

        buttons.forEach((button) => {
            button.addEventListener('click', () => {
                console.log('Button clicked');
                if (button instanceof HTMLElement) {
                    const text = button.textContent;
                    if (text === 'API Management') {
                        log('Sending message to open API Management');
                        vscode.postMessage({
                            type: 'openApiManagement'
                        });
                    }
                    // Handle other buttons if needed
                }
            });
        });
    } else {
        log('Document is not defined');
    }
}
log('Main function in sidebar.ts called11');
main();