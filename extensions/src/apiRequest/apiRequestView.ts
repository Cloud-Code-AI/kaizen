import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { ApiEndpoint } from '../types';

// Update the type definition for the callback
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
    
    public async show() {
        console.log("Show from View");
            this.panel = vscode.window.createWebviewPanel(
                'apiRequest',
                'API Request',
                vscode.ViewColumn.One,
                {
                    enableScripts: true,
                    retainContextWhenHidden: true,
                }
            );
            const content = await this.getWebviewContent();
            console.log("Webview Content:", content);
            this.panel.webview.html = content;

            this.panel.webview.onDidReceiveMessage(
                message => {
                    console.log("Message received from webview:", message); // Log incoming messages
                    switch (message.command) {
                        case 'sendRequest':
                            this.apiRequestCallback(message.method, message.url, message.headers,message.queryParams, message.formData, message.body, message.bodyType);
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
                console.log("Webview panel disposed");
                this.panel = undefined;
            });
    }

    public postMessage(message: any) {
        this.panel?.webview.postMessage(message);
    }
    private saveEndpoint(method: string, url: string) {
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
        const htmlFilePath = path.join(this.context.extensionPath, 'webview', 'apiRequest', 'index.html');
        
        return new Promise((resolve, reject) => {
            fs.readFile(htmlFilePath, 'utf8', (err, data) => {
                if (err) {
                    console.error("Failed to read HTML file:", err);
                    reject(`<html><body><h1>Error loading content</h1><p>${err.message}</p></body></html>`); // Fallback content
                } else {
                    resolve(data); // Return the HTML content
                }
            });
        });
    }

    public loadEndpoint(endpoint: ApiEndpoint) {
        console.log("Loading Endpoint");
        if (this.panel) {
            this.panel.webview.postMessage({
                command: 'loadEndpoint',
                endpoint: endpoint
            });
            console.log(this.panel.webview.postMessage);
        }
    }

}