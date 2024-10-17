import * as vscode from 'vscode';

type TestManagementCallback = (action: string, data?: any) => Promise<void>;

export class TestManagementView {
    private panel: vscode.WebviewPanel | undefined;
    private context: vscode.ExtensionContext;
    private testManagementCallback: TestManagementCallback;

    constructor(context: vscode.ExtensionContext, testManagementCallback: TestManagementCallback) {
        this.context = context;
        this.testManagementCallback = testManagementCallback;
    }

    public async show() {
        if (this.panel) {
            this.panel.reveal();
        } else {
            this.panel = vscode.window.createWebviewPanel(
                'testManagement',
                'Test Management',
                vscode.ViewColumn.One,
                {
                    enableScripts: true,
                    retainContextWhenHidden: true,
                }
            );

            try {
                // Load the webview content asynchronously
                this.panel.webview.html = await this.getWebviewContent();
            } catch (error) {
                console.error("Failed to load webview content:", error);
                this.panel.webview.html = "<h1>Error loading content</h1>"; // Fallback content
            }

            this.panel.webview.onDidReceiveMessage(
                message => {
                    this.testManagementCallback(message.command, message.value);
                },
                undefined,
                this.context.subscriptions
            );

            this.panel.onDidDispose(() => {
                this.panel = undefined;
            });
        }
    }

    private async getWebviewContent(): Promise<string> {
        const htmlPath = vscode.Uri.joinPath(this.context.extensionUri, 'webview', 'testManagement', 'index.html');
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