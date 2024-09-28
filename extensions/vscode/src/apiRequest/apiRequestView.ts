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
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; display: flex; height: 100vh; color: #e0e0e0; background-color: #1e1e1e; }
        .sidebar { width: 200px; background-color: #252526; padding: 10px; }
        .main { flex-grow: 1; display: flex; flex-direction: column; }
        .request-bar { display: flex; padding: 10px; background-color: #333333; }
        .content { display: flex; flex-grow: 1; }
        .request-panel { flex: 1; padding: 10px; display: flex; flex-direction: column; }
        .response-panel { flex: 1; padding: 10px; background-color: #2d2d2d; }
        select, input, button { margin-right: 5px; background-color: #3c3c3c; color: #e0e0e0; border: 1px solid #555; }
        .collections { margin-top: 20px; }
        .collection-item { cursor: pointer; padding: 5px; }
        .collection-item:hover { background-color: #2a2a2a; }
        .tab { display: inline-block; padding: 5px 10px; cursor: pointer; }
        .tab.active { border-bottom: 2px solid #007acc; }
        .tab-content { display: none; overflow-y: auto; }
        .tab-content.active { display: block; }
        #response { white-space: pre-wrap; }
        .params-table { width: 100%; border-collapse: collapse; }
        .params-table th, .params-table td { border: 1px solid #555; padding: 5px; }
        .params-table input { width: 100%; box-sizing: border-box; }
        .params-section { margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div>
            <button id="new-request">New Request</button>
        </div>
        <div class="collections">
            <h3>Collections</h3>
            <div id="collection-list"></div>
        </div>
    </div>
    <div class="main">
        <div class="request-bar">
            <select id="method">
                <option value="GET">GET</option>
                <option value="POST">POST</option>
                <option value="PUT">PUT</option>
                <option value="DELETE">DELETE</option>
                <option value="PATCH">PATCH</option>
            </select>
            <input type="text" id="url" placeholder="Enter URL" style="flex-grow: 1;">
            <button id="send">Send</button>
        </div>
        <div class="content">
            <div class="request-panel">
                <div class="params-section">
                    <h3>Query Params</h3>
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
                <div class="tabs">
                    <span class="tab active" data-tab="headers">Headers</span>
                    <span class="tab" data-tab="body">Body</span>
                    <span class="tab" data-tab="auth">Auth</span>
                </div>
                <div id="headers" class="tab-content active">
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
                <div id="body" class="tab-content">
                    <textarea id="body-content" rows="10" style="width: 100%;"></textarea>
                </div>
                <div id="auth" class="tab-content">
                    <!-- Add authentication options here -->
                </div>
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
            <div class="response-panel">
                <div id="response-stats"></div>
                <div class="tabs">
                    <span class="tab active" data-tab="response">Response</span>
                    <span class="tab" data-tab="response-headers">Headers</span>
                </div>
                <div id="response" class="tab-content active"></div>
                <div id="response-headers" class="tab-content"></div>
            </div>
        </div>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        
        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                const tabName = tab.getAttribute('data-tab');
                document.querySelectorAll('.tab, .tab-content').forEach(el => el.classList.remove('active'));
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

        // Send request
        document.getElementById('send').addEventListener('click', () => {
            const method = document.getElementById('method').value;
            const url = document.getElementById('url').value;
            const headers = collectTableData('headers-table');
            const queryParams = collectTableData('query-params');
            const formData = collectTableData('form-data');
            const body = document.getElementById('body-content').value;
            
            vscode.postMessage({ 
                command: 'sendRequest', 
                method, 
                url, 
                headers, 
                queryParams,
                formData,
                body 
            });
        });

        // Receive response
        window.addEventListener('message', event => {
            const message = event.data;
            switch (message.command) {
                case 'receiveResponse':
                    document.getElementById('response-stats').textContent = \`Status: \${message.response.status} | Size: \${message.size} Bytes | Time: \${message.time} ms\`;
                    document.getElementById('response').textContent = message.response.body;
                    document.getElementById('response-headers').textContent = JSON.stringify(message.response.headers, null, 2);
                    break;
            }
        });

        // New request button
        document.getElementById('new-request').addEventListener('click', () => {
            document.getElementById('url').value = '';
            document.getElementById('body-content').value = '';
            document.getElementById('response').textContent = '';
            document.getElementById('response-headers').textContent = '';
            document.getElementById('response-stats').textContent = '';
            ['query-params', 'headers-table', 'form-data'].forEach(tableId => {
                const table = document.getElementById(tableId);
                table.querySelectorAll('tr:not(:first-child):not(:nth-child(2))').forEach(row => row.remove());
                table.querySelector('tr:nth-child(2)').querySelectorAll('input').forEach(input => input.value = '');
            });
        });
    </script>
</body>
</html>`;
    }

}
