import * as vscode from 'vscode';

export class ApiRequestView {
    private panel: vscode.WebviewPanel | undefined;
    private context: vscode.ExtensionContext;
    private handleApiRequest: (
        method: string, 
        url: string, 
        headers: Record<string, string>, 
        queryParams: Record<string, string>, 
        formData: Record<string, string>, 
        body: string
    ) => Promise<void>;

    constructor(
        context: vscode.ExtensionContext, 
        handleApiRequest: (
            method: string, 
            url: string, 
            headers: Record<string, string>, 
            queryParams: Record<string, string>, 
            formData: Record<string, string>, 
            body: string
        ) => Promise<void>
    ) {
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
                            this.handleApiRequest(message.method, message.url, message.headers,message.queryParams, message.formData, message.body);
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
        return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Client</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; display: flex; height: 100vh; color: var(--vscode-foreground); background-color: var(--vscode-editor-background); }
        .main-container { display: flex; width: 100%; height: 100vh; }
        .request-panel { flex: 2; padding: 20px; display: flex; flex-direction: column; }
        .response-panel { flex: 1; padding: 20px; border-left: 1px solid var(--vscode-panel-border); display: flex; flex-direction: column; }
        .request-bar { display: flex; padding: 10px; background-color: var(--vscode-editor-background); }
        select, input, button { margin-right: 5px; background-color: var(--vscode-input-background); color: var(--vscode-input-foreground); border: 1px solid var(--vscode-input-border); }
        .tab { display: inline-block; padding: 5px 10px; cursor: pointer; }
        .tab.active { border-bottom: 2px solid var(--vscode-focusBorder); }
        .tab-content { display: none; overflow-y: auto; flex-grow: 1; }
        .tab-content.active { display: block; }
        #response, #response-headers { white-space: pre-wrap; }
        .params-table { width: 100%; border-collapse: collapse; }
        .params-table th, .params-table td { border: 1px solid var(--vscode-panel-border); padding: 5px; }
        .params-table input { width: 100%; box-sizing: border-box; }
        .status-bar { display: flex; justify-content: space-between; align-items: center; padding: 10px; background-color: var(--vscode-statusBar-background); border-bottom: 1px solid var(--vscode-panel-border); }
        .placeholder { display: flex; justify-content: center; align-items: center; height: 100%; color: var(--vscode-descriptionForeground); }
        .params-section { margin-top: 20px; }
        .params-section h3 { margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="request-panel">
            <div class="request-bar">
                <select id="method" class="method-select">
                    <option value="GET">GET</option>
                    <option value="POST">POST</option>
                    <option value="PUT">PUT</option>
                    <option value="DELETE">DELETE</option>
                    <option value="PATCH">PATCH</option>
                </select>
                <input type="text" id="url" class="url-input" placeholder="Enter URL">
                <button id="send" class="send-button">Send</button>
            </div>
            <div class="tabs request-tabs">
                <span class="tab active" data-tab="query">Query</span>
                <span class="tab" data-tab="headers">Headers</span>
                <span class="tab" data-tab="auth">Auth</span>
                <span class="tab" data-tab="body">Body</span>
            </div>
            <div id="query" class="tab-content request-tab-content active">
                <table class="params-table" id="query-params">
                    <tr>
                        <th>Key</th>
                        <th>Value</th>
                        <th>Actions</th>
                    </tr>
                    <tr>
                        <td><input type="text" placeholder="Key"></td>
                        <td><input type="text" placeholder="Value"></td>
                        <td><button onclick="addRow(this, 'query-params')">+</button></td>
                    </tr>
                </table>
            </div>
            <div id="headers" class="tab-content request-tab-content">
                <table class="params-table" id="headers-table">
                    <tr>
                        <th>Key</th>
                        <th>Value</th>
                        <th>Actions</th>
                    </tr>
                    <tr>
                        <td><input type="text" placeholder="Key"></td>
                        <td><input type="text" placeholder="Value"></td>
                        <td><button onclick="addRow(this, 'headers-table')">+</button></td>
                    </tr>
                </table>
            </div>
            <div id="auth" class="tab-content request-tab-content">
                <!-- Add authentication options here -->
                <select id="auth-type" style="margin-bottom: 10px;">
                    <option value="none">No Auth</option>
                    <option value="basic">Basic Auth</option>
                    <option value="bearer">Bearer Token</option>
                </select>
                <div id="basic-auth" style="display: none;">
                    <input type="text" id="username" placeholder="Username" style="width: 100%; margin-bottom: 5px;">
                    <input type="password" id="password" placeholder="Password" style="width: 100%;">
                </div>
                <div id="bearer-auth" style="display: none;">
                    <input type="text" id="token" placeholder="Token" style="width: 100%;">
                </div>
            </div>
            <div id="body" class="tab-content request-tab-content">
                <textarea id="body-content" rows="10" style="width: 100%;"></textarea>
                <div class="params-section">
                    <h3>Form Data</h3>
                    <table class="params-table" id="form-data">
                        <tr>
                            <th>Key</th>
                            <th>Value</th>
                            <th>Actions</th>
                        </tr>
                        <tr>
                            <td><input type="text" placeholder="Key"></td>
                            <td><input type="text" placeholder="Value"></td>
                            <td><button onclick="addRow(this, 'form-data')">+</button></td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>
        <div class="response-panel">
            <div id="response-placeholder" class="placeholder">Send a request to see the response</div>
            <div id="response-content" style="display: none; height: 100%;">
                <div class="status-bar">
                    <span id="response-status"></span>
                    <span id="response-time"></span>
                    <span id="response-size"></span>
                </div>
                <div class="tabs response-tabs">
                    <span class="tab active" data-tab="response">Response</span>
                    <span class="tab" data-tab="response-headers">Headers</span>
                </div>
                <div id="response" class="tab-content response-tab-content active"></div>
                <div id="response-headers" class="tab-content response-tab-content"></div>
            </div>
        </div>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        
        // Tab switching for request panel
        document.querySelectorAll('.request-tabs .tab').forEach(tab => {
            tab.addEventListener('click', () => {
                const tabName = tab.getAttribute('data-tab');
                document.querySelectorAll('.request-tabs .tab, .request-tab-content').forEach(el => el.classList.remove('active'));
                tab.classList.add('active');
                document.getElementById(tabName).classList.add('active');
            });
        });

        // Tab switching for response panel
        document.querySelectorAll('.response-tabs .tab').forEach(tab => {
            tab.addEventListener('click', () => {
                const tabName = tab.getAttribute('data-tab');
                document.querySelectorAll('.response-tabs .tab, .response-tab-content').forEach(el => el.classList.remove('active'));
                tab.classList.add('active');
                document.getElementById(tabName).classList.add('active');
            });
        });

        // Add row to table
        function addRow(button, tableId) {
            const table = document.getElementById(tableId);
            const row = button.closest('tr');
            const newRow = row.cloneNode(true);
            newRow.querySelectorAll('input').forEach(input => input.value = '');
            table.appendChild(newRow);
            button.textContent = '-';
            button.onclick = function() { removeRow(this); };
        }

        // Remove row from table
        function removeRow(button) {
            button.closest('tr').remove();
        }

        // Collect data from table
        function collectTableData(tableId) {
            const data = {};
            const table = document.getElementById(tableId);
            table.querySelectorAll('tr:not(:first-child)').forEach(row => {
                const inputs = row.querySelectorAll('input');
                if (inputs[0].value && inputs[1].value) {
                    data[inputs[0].value] = inputs[1].value;
                }
            });
            return data;
        }

        // Auth type selection
        document.getElementById('auth-type').addEventListener('change', function() {
            document.getElementById('basic-auth').style.display = this.value === 'basic' ? 'block' : 'none';
            document.getElementById('bearer-auth').style.display = this.value === 'bearer' ? 'block' : 'none';
        });

        // Modify the send request function to include auth and form data
        document.getElementById('send').addEventListener('click', () => {
            const method = document.getElementById('method').value;
            const url = document.getElementById('url').value;
            const headers = collectTableData('headers-table');
            const queryParams = collectTableData('query-params');
            const formData = collectTableData('form-data');
            const body = document.getElementById('body-content').value;
            
            // Collect auth data
            const authType = document.getElementById('auth-type').value;
            let authData = {};
            if (authType === 'basic') {
                authData = {
                    username: document.getElementById('username').value,
                    password: document.getElementById('password').value
                };
            } else if (authType === 'bearer') {
                authData = {
                    token: document.getElementById('token').value
                };
            }
            
            document.getElementById('response-placeholder').style.display = 'none';
            document.getElementById('response-content').style.display = 'flex';
            document.getElementById('response-content').style.flexDirection = 'column';
            
            vscode.postMessage({ 
                command: 'sendRequest', 
                method, 
                url, 
                headers, 
                queryParams,
                formData,
                body,
                auth: {
                    type: authType,
                    data: authData
                }
            });
        });

        // Receive response
        window.addEventListener('message', event => {
            const message = event.data;
            switch (message.command) {
                case 'receiveResponse':
                    document.getElementById('response-status').textContent = \`Status: \${message.response.status}\`;
                    document.getElementById('response-time').textContent = \`Time: \${message.time} ms\`;
                    document.getElementById('response-size').textContent = \`Size: \${message.size} Bytes\`;
                    document.getElementById('response').textContent = message.response.body;
                    document.getElementById('response-headers').textContent = JSON.stringify(message.response.headers, null, 2);
                    break;
            }
        });
    </script>
</body>
</html>`;
    }

}