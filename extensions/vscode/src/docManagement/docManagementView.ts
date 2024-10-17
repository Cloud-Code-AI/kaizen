import * as vscode from 'vscode';

type DocManagementCallback = (command: string, docName?: string, content?: string) => Promise<void>;

interface DocMessage {
    command: 'loadDoc' | 'saveDoc';
    docName?: string;
    content?: string;
}

export class DocManagementView {
    private panel: vscode.WebviewPanel | undefined;
    private context: vscode.ExtensionContext;
    private docManagementCallback: DocManagementCallback;

    constructor(context: vscode.ExtensionContext, docManagementCallback: DocManagementCallback) {
        this.context = context;
        this.docManagementCallback = docManagementCallback;
    }

    public show() {
        if (this.panel) {
            this.panel.reveal();
        } else {
            this.panel = vscode.window.createWebviewPanel(
                'docManagement',
                'Documentation Management',
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
                (message: DocMessage) => {
                    switch (message.command) {
                        case 'loadDoc':
                            this.docManagementCallback(message.command, message.docName).catch(err => 
                                vscode.window.showErrorMessage(`Error loading document: ${err.message}`)
                            );
                            return;
                        case 'saveDoc':
                            this.docManagementCallback(message.command, message.docName, message.content).catch(err => 
                                vscode.window.showErrorMessage(`Error saving document: ${err.message}`)
                            );
                            return;
                    }
                },
                undefined,
                this.context.subscriptions
            );

            this.panel.onDidDispose(() => {
                this.panel = undefined; // Cleanup if needed
            });
        }
    }

    public postMessage(message: any) {
        this.panel?.webview.postMessage(message);
    }

    private async getWebviewContent(): Promise<string> {
        const htmlPath = vscode.Uri.joinPath(this.context.extensionUri, 'webview', 'docManagement', 'index.html');
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