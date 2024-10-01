import * as vscode from 'vscode';
import { ApiRequestProvider } from './apiRequest/apiRequestProvider';
import { log } from './extension';
import { ApiEndpoint } from './types';

export class SidebarProvider implements vscode.WebviewViewProvider {
  _view?: vscode.WebviewView;
  _doc?: vscode.TextDocument;
  private apiRequestProvider: ApiRequestProvider;
  private apiHistory: ApiEndpoint[] = [];
  private showHistory: boolean = false;

  constructor(private readonly _extensionUri: vscode.Uri, context: vscode.ExtensionContext) {
    this.apiRequestProvider = new ApiRequestProvider(context);

    // Register command to update API history
    context.subscriptions.push(
      vscode.commands.registerCommand('vscode-api-client.updateApiHistory', (endpoint: ApiEndpoint) => {
        this.updateApiHistory(endpoint);
      })
    );
  }

  public refresh() {
    if (this._view) {
      console.log('Refreshing webview content');
      this._view.webview.html = this._getHtmlForWebview(this._view.webview);
    }
  }

  public resolveWebviewView(webviewView: vscode.WebviewView) {
    this._view = webviewView;
    webviewView.webview.options = {
      enableScripts: true,
      localResourceRoots: [this._extensionUri],
    };

    webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

    webviewView.webview.onDidReceiveMessage(async (data) => {
      log("Received message on sidebar");
      switch (data.type) {
        case "onInfo": {
          if (!data.value) {
            return;
          }
          vscode.window.showInformationMessage(data.value);
          break;
        }
        case "onError": {
          if (!data.value) {
            return;
          }
          vscode.window.showErrorMessage(data.value);
          break;
        }
        case "openApiManagement": {
          if (!data.value) {
            return;
          }
          this.openWebview(data.value);
          break;
        }
        case "backButton": {
          this.showHistory = false;
          this.refresh();
          break;
        }
        case "newRequest": {
          this.openApiRequestView();
          break;
        }
        case "deleteEndpoint": {
          this.deleteEndpoint(data.name, data.method);
          break;
        }
      }
    });
  }

  public revive(panel: vscode.WebviewView) {
    this._view = panel;
  }

  private _getHtmlForWebview(webview: vscode.Webview) {
    log("HTML Web View Loaded");
    
    const scriptUri = webview.asWebviewUri(
      vscode.Uri.joinPath(this._extensionUri, "out", "sidebar.js")
    );

    const styleSidebarUri = webview.asWebviewUri(
      vscode.Uri.joinPath(this._extensionUri, "media", "sidebar.css")
    );

  
    const nonce = getNonce();

    const csp = `
      default-src 'none';
      script-src ${webview.cspSource} 'nonce-${nonce}';
      style-src ${webview.cspSource} 'unsafe-inline';
      img-src ${webview.cspSource} https:;
      font-src ${webview.cspSource};
    `;
  
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="Content-Security-Policy" content="${csp}">
        <link href="${styleSidebarUri}" rel="stylesheet">
    </head>
    <body>
    ${this.showHistory 
      ? `<button id="back-button">Back</button>${this.getHistoryHtml()}`
      : `<div id="buttons">
           <button class="webview-button" data-webview="apiManagement">API Management</button>
           <button class="webview-button" data-webview="apiRequest">API Request</button>
           <button class="webview-button" data-webview="chatRepo">Chat Repo</button>
           <button class="webview-button" data-webview="documentation">Documentation</button>
           <button class="webview-button" data-webview="testCase">Test Case</button>
         </div>`
    }
    <script nonce="${nonce}" src="${scriptUri}"></script>
    </body>
    </html>`;
  }

  private getHistoryHtml() {
    return `
      <div id="sidebar-container">
        <div id="history-header">
          <h3>API History</h3>
          <button id="new-request-btn">New Request</button>
        </div>
        <input type="text" id="filter-history" placeholder="Filter history">
        <ul id="api-history">
          ${this.apiHistory.map(endpoint => `
            <li class="api-endpoint ${endpoint.method.toLowerCase()}">
              <span class="method">${endpoint.method}</span>
              <span class="name">${endpoint.name}</span>
              <span class="last-used">${new Date(endpoint.lastUsed).toLocaleString()}</span>
              <button class="delete-btn" data-name="${endpoint.name}" data-method="${endpoint.method}">X</button>
            </li>
          `).join('')}
        </ul>
      </div>
    `;
  }

  private async openWebview(webviewType: string) {
    if (webviewType === 'apiManagement') {
      if (this.apiRequestProvider) {
        console.log("Opening API Request View");
        this.apiRequestProvider.openApiRequestView();
        this.showHistory = true;
        this.refresh();
      } else {
        console.error("apiRequestProvider is not initialized");
        vscode.window.showErrorMessage("API Management is not available");
      }
    } else {
      const panel = vscode.window.createWebviewPanel(
        webviewType,
        this.getWebviewTitle(webviewType),
        vscode.ViewColumn.One,
        {
          enableScripts: true,
          localResourceRoots: [this._extensionUri],
        }
      );

      panel.webview.html = await this.getWebviewContent(webviewType);
    }
  }

  private openApiRequestView() {
    if (this.apiRequestProvider) {
      console.log("Opening API Request View");
      this.apiRequestProvider.openApiRequestView();
    } else {
      console.error("apiRequestProvider is not initialized");
      vscode.window.showErrorMessage("API Request is not available");
    }
  }

  private getWebviewTitle(webviewType: string): string {
    switch (webviewType) {
      case 'apiManagement':
        return 'API Management';
      case 'apiRequest':
        return 'API Request';
      case 'chatRepo':
        return 'Chat Repo';
      case 'documentation':
        return 'Documentation';
      case 'testCase':
        return 'Test Case';
      default:
        return 'Webview';
    }
  }

  private async getWebviewContent(webviewType: string): Promise<string> {
    const filePath = vscode.Uri.joinPath(this._extensionUri, webviewType, 'index.html');
    const fileContent = await vscode.workspace.fs.readFile(filePath);
    return fileContent.toString();
  }

private updateApiHistory(endpoint: ApiEndpoint){
    // Check if an endpoint with the same name and method already exists
    const existingIndex = this.apiHistory.findIndex(
      e => e.name === endpoint.name && e.method === endpoint.method
    );

    let updatedEndpoint: ApiEndpoint;

    if (existingIndex !== -1){
      // If it exists, update the lastUsed time
      updatedEndpoint ={...this.apiHistory[existingIndex], lastUsed: endpoint.lastUsed};
      this.apiHistory.splice(existingIndex, 1);
}else{
      updatedEndpoint = endpoint;
      // Using a circular buffer implementation
      class CircularBuffer<T>{
          private buffer: T[];
          private pointer: number = 0;
          constructor(private capacity: number){
              this.buffer = new Array<T>(capacity);
      }
          push(item: T): void{
              this.buffer[this.pointer] = item;
              this.pointer = (this.pointer + 1) % this.capacity;
      }
          getItems(): T[]{
              return[...this.buffer.slice(this.pointer), ...this.buffer.slice(0, this.pointer)];
      }
      }

      // Usage
      private apiHistory = new CircularBuffer<ApiEndpoint>(10);

      // In updateApiHistory method
      this.apiHistory.push(endpoint);
}
}

    // Add the updated/new endpoint to the beginning of the array
    this.apiHistory.unshift(updatedEndpoint);

    // Send only the updated history item to the webview
    this._view?.webview.postMessage({
      type: 'updateHistoryItem', 
      endpoint: updatedEndpoint,
      action: existingIndex !== -1 ? 'update' : 'add'
});
}

  private deleteEndpoint(name: string, method: string) {
    this.apiHistory = this.apiHistory.filter(
      endpoint => !(endpoint.name === name && endpoint.method === method)
    );
    this.refresh();
  }
}

function getNonce() {
  let text = '';
  const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  for (let i = 0; i < 32; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}