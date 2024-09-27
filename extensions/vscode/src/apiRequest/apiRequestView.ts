import * as vscode from 'vscode';

export class ApiRequestView {
    private panel: vscode.WebviewPanel | undefined;
    private context: vscode.ExtensionContext;
    private handleApiRequest: (method: string, url: string, headers: string, body: string) => void;

    constructor(context: vscode.ExtensionContext, handleApiRequest: (method: string, url: string, headers: string, body: string) => void) {
        this.context = context;
        this.handleApiRequest = handleApiRequest;
    }

    public show() {
        if (this.panel) {
            this.panel.reveal();
        } else {
            this.panel = vscode.window.createWebviewPanel(
                'apiRequest',
                'API Request',
                vscode.ViewColumn.One,
                {
                    enableScripts: true,
                    retainContextWhenHidden: true,
                }
            );

            this.panel.webview.html = this.getWebviewContent();

            this.panel.webview.onDidReceiveMessage(
                message => {
                    switch (message.command) {
                        case 'sendRequest':
                            this.handleApiRequest(message.method, message.url, message.headers, message.body);
                            return;
                    }
                },
                undefined,
                this.context.subscriptions
            );

            this.panel.onDidDispose(() => {
                this.panel = undefined;
            });
        }
    }

    public postMessage(message: any) {
        this.panel?.webview.postMessage(message);
    }

    private getWebviewContent() {
        // Return the HTML content for the webview
        // This should match the HTML file we created earlier
        return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>API Request</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                select, input, textarea { width: 100%; margin-bottom: 10px; }
                button { padding: 10px; }
                #response { background-color: #f0f0f0; padding: 10px; white-space: pre-wrap; }
                #stats { margin-top: 10px; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>API Request</h1>
            <select id="method">
                <option value="GET">GET</option>
                <option value="POST">POST</option>
                <option value="PUT">PUT</option>
                <option value="DELETE">DELETE</option>
            </select>
            <input type="text" id="url" placeholder="Enter URL">
            <textarea id="headers" placeholder="Headers (JSON format)"></textarea>
            <textarea id="body" placeholder="Request Body"></textarea>
            <button id="send">Send Request</button>
            <div id="stats"></div>
            <pre id="response"></pre>

            <script>
                const vscode = acquireVsCodeApi();
                const statsDiv = document.getElementById('stats');
                const responseDiv = document.getElementById('response');

                document.getElementById('send').addEventListener('click', () => {
                    const method = document.getElementById('method').value;
                    const url = document.getElementById('url').value;
                    const headers = document.getElementById('headers').value;
                    const body = document.getElementById('body').value;
                    
                    statsDiv.textContent = 'Sending request...';
                    responseDiv.textContent = '';
                    
                    vscode.postMessage({ command: 'sendRequest', method, url, headers, body });
                });

                window.addEventListener('message', event => {
                    const message = event.data;
                    switch (message.command) {
                        case 'receiveResponse':
                            statsDiv.textContent = \`Time: \${message.time}ms | Size: \${message.size} bytes\`;
                            responseDiv.textContent = JSON.stringify(message.response, null, 2);
                            break;
                    }
                });
            </script>
        </body>
        </html>`;
    }
}
