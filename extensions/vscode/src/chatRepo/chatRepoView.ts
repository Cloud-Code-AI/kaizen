import * as vscode from 'vscode';

type ChatRepoCallback = (message: string) => Promise<void>;

export class ChatRepoView {
    private panel: vscode.WebviewPanel | undefined;
    private context: vscode.ExtensionContext;
    private chatRepoCallback: ChatRepoCallback;

    constructor(context: vscode.ExtensionContext, chatRepoCallback: ChatRepoCallback) {
        this.context = context;
        this.chatRepoCallback = chatRepoCallback;
    }

    public show() {
        if (this.panel) {
            this.panel.reveal();
        } else {
            this.panel = vscode.window.createWebviewPanel(
                'chatRepo',
                'Chat with Repo',
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
                        case 'sendChatMessage':
                            this.chatRepoCallback(message.message).catch(err => console.error("Error in chat repo callback:", err));
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
        const htmlPath = vscode.Uri.joinPath(this.context.extensionUri, 'webview', 'chatRepo', 'index.html');
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