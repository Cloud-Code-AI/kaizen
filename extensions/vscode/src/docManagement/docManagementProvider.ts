import * as vscode from 'vscode';
import { DocManagementView } from './docManagementView';

export class DocManagementProvider {
    private context: vscode.ExtensionContext;
    private view: DocManagementView | undefined;

    constructor(context: vscode.ExtensionContext) {
        this.context = context;
    }

    public openDocManagementView() {
        if (!this.view) {
            this.view = new DocManagementView(this.context, this.handleDocAction.bind(this));
        }
        this.view.show();
    }

    private async handleDocAction(command: string, docName?: string, content?: string) {
        try {
            switch (command) {
                case 'loadDoc':
                    if (docName) {
                        const docContent = await this.loadDocument(docName); // Load document content
                        this.view?.postMessage({ command: 'displayDoc', content: docContent });
                    }
                    break;
                case 'saveDoc':
                    if (docName && content) {
                        await this.saveDocument(docName, content); // Save document content
                        vscode.window.showInformationMessage(`Document "${docName}" saved successfully.`);
                    }
                    break;
                default:
                    vscode.window.showErrorMessage(`Unknown command: ${command}`);
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Error handling document action: ${error.message}`);
        }
    }

    private async loadDocument(docName: string): Promise<string> {
        // Simulate loading a document (replace with actual logic)
        return `Content of ${docName}`; // Placeholder content
    }

    private async saveDocument(docName: string, content: string): Promise<void> {
        // Simulate saving a document (replace with actual logic)
        console.log(`Saving Document "${docName}": ${content}`);
        // Here you would typically save to a file or database.
    }
}