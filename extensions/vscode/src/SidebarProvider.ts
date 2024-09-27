import * as vscode from 'vscode';
import { ApiRequestProvider } from './apiRequest/apiRequestProvider';
import { log } from './extension';

console.log("Sidebar.ts is loaded");


export class SidebarProvider implements vscode.WebviewViewProvider {
  _view?: vscode.WebviewView;
  _doc?: vscode.TextDocument;
  private apiRequestProvider: ApiRequestProvider;

  constructor(private readonly _extensionUri: vscode.Uri, context: vscode.ExtensionContext) {
    this.apiRequestProvider = new ApiRequestProvider(context);
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
        case "openWebview": {
          console.log("Received openWebview event", data);
          if (!data.value) {
            console.log("No value provided for openWebview");
            return;
          }
          this.openWebview(data.value);
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
      <div id="buttons">
        <button class="webview-button" data-webview="apiManagement">API Management</button>
        <button class="webview-button" data-webview="apiRequest">API Request</button>
        <button class="webview-button" data-webview="chatRepo">Chat Repo</button>
        <button class="webview-button" data-webview="documentation">Documentation</button>
        <button class="webview-button" data-webview="testCase">Test Case</button>
      </div>
      <script nonce="${nonce}" src="${scriptUri}"></script>
      <script nonce="${nonce}">
        console.log('Script after sidebar.js');
        window.onerror = function(message, source, lineno, colno, error) {
          console.error('An error occurred:', message, 'at', source, lineno, colno, error);
        };
      </script>
    </body>
    </html>`;
  }

  private async openWebview(webviewType: string) {
    log("Webview Opened");
    if (webviewType === 'apiManagement') {
      if (this.apiRequestProvider) {
        this.apiRequestProvider.openApiRequestView();
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
}

function getNonce() {
  let text = '';
  const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  for (let i = 0; i < 32; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}