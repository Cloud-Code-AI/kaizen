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

            this.panel.webview.html = await this.getWebviewContent();

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
        const htmlContent = await vscode.workspace.fs.readFile(htmlPath);
        return htmlContent.toString();
    }
}
