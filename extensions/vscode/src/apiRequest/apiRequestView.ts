import * as vscode from 'vscode';
import { ApiEndpoint } from '../types';

type ApiRequestCallback = (
    method: string,
    url: string,
    headers: Record<string, string>,
    queryParams: Record<string, string>,
    formData: Record<string, string>,
    body: string,
    bodyType: string
) => Promise<void>;

export class ApiRequestView {
    private panel: vscode.WebviewPanel | undefined;
    private context: vscode.ExtensionContext;
    private apiRequestCallback: ApiRequestCallback;

    constructor(context: vscode.ExtensionContext, apiRequestCallback: ApiRequestCallback) {
        this.context = context;
        this.apiRequestCallback = apiRequestCallback;
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

            // Load the webview content asynchronously
            this.getWebviewContent().then(html => {
                this.panel!.webview.html = html; // Use non-null assertion since we just created the panel
            }).catch(error => {
                console.error("Failed to load webview content:", error);
                this.panel!.webview.html = "<h1>Error loading content</h1>"; // Fallback content
            });

            this.panel.webview.onDidReceiveMessage(
                message => {
                    switch (message.command) {
                        case 'sendRequest':
                            this.apiRequestCallback(
                                message.method,
                                message.url,
                                message.headers,
                                message.queryParams,
                                message.formData,
                                message.body,
                                message.bodyType
                            ).catch(err => console.error("Error in API request callback:", err));
                            return;
                        case 'saveEndpoint':
                            this.saveEndpoint(message.method, message.url);
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

    private saveEndpoint(method: string, url: string) {
        // Check if the URL is blank
        if (!url.trim()) {
            vscode.window.showErrorMessage("URL is blank. Cannot save endpoint.");
            return;
        }

        const endpoint: ApiEndpoint = {
            method: method,
            name: url,
            lastUsed: new Date().toISOString()
        };

        vscode.commands.executeCommand('vscode-api-client.updateApiHistory', endpoint);
    }
    
    private async getWebviewContent(): Promise<string> {
        const htmlPath = vscode.Uri.joinPath(this.context.extensionUri, 'webview', 'apiRequest', 'index.html');
        console.log("Loading HTML from:", htmlPath.toString());
        
        try {
            // Read the HTML file
            const htmlContentBuffer = await vscode.workspace.fs.readFile(htmlPath);
            
            // Convert the buffer to a string using TextDecoder for proper encoding
            return new TextDecoder('utf-8').decode(htmlContentBuffer);
        } catch (error) {
            console.error("Error loading HTML:", error);
            throw error; // Re-throw the error to handle it in show()
        }
    }
}