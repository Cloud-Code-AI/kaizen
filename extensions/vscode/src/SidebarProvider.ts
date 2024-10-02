import * as vscode from 'vscode';
import { ApiRequestProvider } from './apiRequest/apiRequestProvider';
import { log } from './extension';
import { ApiEndpoint } from './types';
import { inspect } from 'util';

export class SidebarProvider implements vscode.WebviewViewProvider {
  _view?: vscode.WebviewView;
  _doc?: vscode.TextDocument;
  private apiRequestProvider: ApiRequestProvider;
  private apiHistory: ApiEndpoint[] = [];
  private showHistory: boolean = false;
  private context: vscode.ExtensionContext;


  constructor(private readonly _extensionUri: vscode.Uri, context: vscode.ExtensionContext) {
    this.apiRequestProvider = new ApiRequestProvider(context);
    this.context = context;
    this.loadApiHistory();

    // Add these lines to the constructor
    this.inspectApiHistory();
    this.cleanupApiHistory();

    // Register command to update API history
    context.subscriptions.push(
      vscode.commands.registerCommand('vscode-api-client.updateApiHistory', (endpoint: ApiEndpoint) => {
        this.updateApiHistory(endpoint);
      })
    );
  }
  private loadApiHistory() {
    try {
      const history = this.context.globalState.get<ApiEndpoint[]>('apiHistory', []);
      this.apiHistory = history;
    } catch (error) {
      console.error('Error loading API history:', error);
      this.apiHistory = [];
    }
  }

  private saveApiHistory() {
    try {
      this.context.globalState.update('apiHistory', this.apiHistory);
    } catch (error) {
      console.error('Error saving API history:', error);
      vscode.window.showErrorMessage('Failed to save API history. Please try again.');
    }
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
           <button class="webview-button" data-webview="apiRequest">API Documentation [Coming Soon]</button>
           <button class="webview-button" data-webview="documentation">Documentation [Coming Soon]</button>
           <button class="webview-button" data-webview="testCase">Test Management [Coming Soon]</button>
           <button class="webview-button" data-webview="codeReview">Code Review [Coming Soon]</button>
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
          ${this.apiHistory.map(endpoint => {
            if (!endpoint || !endpoint.method || !endpoint.name || !endpoint.lastUsed) {
              return ''; // Skip invalid entries
            }
            return `
              <li class="api-endpoint ${endpoint.method.toLowerCase()}">
                <span class="method">${endpoint.method}</span>
                <span class="name">${endpoint.name}</span>
                <span class="last-used">${new Date(endpoint.lastUsed).toLocaleString()}</span>
                <button class="delete-btn" data-name="${endpoint.name}" data-method="${endpoint.method}">X</button>
              </li>
            `;
          }).join('')}
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
      case 'codeReview':
        return 'Code Review';
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
  private updateApiHistory(endpoint: ApiEndpoint) {
    const existingIndex = this.apiHistory.findIndex(
      e => e.name === endpoint.name && e.method === endpoint.method
    );

    if (existingIndex !== -1) {
      this.apiHistory[existingIndex].lastUsed = endpoint.lastUsed;
      const [updatedEndpoint] = this.apiHistory.splice(existingIndex, 1);
      this.apiHistory.unshift(updatedEndpoint);
    } else {
      this.apiHistory.unshift(endpoint);
      this.apiHistory = this.apiHistory.slice(0, 10);
    }

    this.saveApiHistory();
    this.refresh();
  }

  private deleteEndpoint(name: string, method: string) {
    const initialLength = this.apiHistory.length;
    this.apiHistory = this.apiHistory.filter(
      endpoint => endpoint && endpoint.name && endpoint.method &&
      !(endpoint.name === name && endpoint.method === method)
    );
    
    if (this.apiHistory.length < initialLength) {
      this.saveApiHistory();
      this.refresh();
      vscode.window.showInformationMessage(`Endpoint ${method} ${name} deleted successfully.`);
    } else {
      vscode.window.showWarningMessage(`Failed to delete endpoint ${method} ${name}. It may not exist or be invalid.`);
    }
  }

  private inspectApiHistory() {
    console.log('Inspecting API History:');
    this.apiHistory.forEach((item, index) => {
      console.log(`Item ${index}:`, inspect(item, { depth: null, colors: true }));
    });
  }

  private cleanupApiHistory() {
    const initialLength = this.apiHistory.length;
    this.apiHistory = this.apiHistory.filter(endpoint => 
      endpoint && 
      typeof endpoint === 'object' &&
      typeof endpoint.method === 'string' &&
      typeof endpoint.name === 'string' &&
      typeof endpoint.lastUsed === 'string' &&
      !isNaN(Date.parse(endpoint.lastUsed))
    );

    const removedCount = initialLength - this.apiHistory.length;
    if (removedCount > 0) {
      console.log(`Removed ${removedCount} invalid items from API history.`);
      this.saveApiHistory();
      this.refresh();
    } else {
      console.log('No invalid items found in API history.');
    }
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