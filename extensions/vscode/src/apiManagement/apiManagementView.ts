import * as vscode from 'vscode';
import { ApiEndpoint } from '../types';

type ApiManagementCallback = (
    action: string,
    endpoint?: ApiEndpoint // Made optional for addApi action
) => Promise<void>;

export class ApiManagementView {
    private panel: vscode.WebviewPanel | undefined;
    private context: vscode.ExtensionContext;
    private apiManagementCallback: ApiManagementCallback;

    constructor(context: vscode.ExtensionContext, apiManagementCallback: ApiManagementCallback) {
        this.context = context;
        this.apiManagementCallback = apiManagementCallback;
    }

    public show() {
        if (this.panel) {
            this.panel.reveal();
        } else {
            this.panel = vscode.window.createWebviewPanel(
                'apiManagement',
                'API Management',
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
                        case 'addApi':
                            this.promptForApiDetails();
                            return;
                        case 'performAction':
                            this.apiManagementCallback(
                                message.action,
                                message.endpoint
                            ).catch(err => console.error("Error in API management callback:", err));
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

    private async getWebviewContent(): Promise<string> {
        const htmlPath = vscode.Uri.joinPath(this.context.extensionUri, 'webview', 'apiManagement', 'index.html');
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

    private async promptForApiDetails() {
        const method = await vscode.window.showInputBox({ prompt: "Enter API Method (GET, POST, etc.)" });
        const url = await vscode.window.showInputBox({ prompt: "Enter API URL" });

        if (method && url) {
            const endpoint: ApiEndpoint = { method, name: url, lastUsed: new Date().toISOString() };
            this.apiManagementCallback('addApi', endpoint).catch(err => console.error("Error adding API:", err));
        } else {
            vscode.window.showErrorMessage("API Method and URL are required.");
        }
    }
}