import * as vscode from 'vscode';
import { ApiManagementView } from './apiManagementView';
import { ApiEndpoint } from '../types';

export class ApiManagementProvider {
    private context: vscode.ExtensionContext;
    private view: ApiManagementView | undefined;

    constructor(context: vscode.ExtensionContext) {
        this.context = context;
    }

    public openApiManagementView() {
        if (!this.view) {
            this.view = new ApiManagementView(this.context, this.handleApiManagementAction.bind(this));
        }
        this.view.show();
    }

    private async handleApiManagementAction(action: string, endpoint?: ApiEndpoint) {
        switch (action) {
            case 'addApi':
                if (endpoint) {
                    // Handle the addition of the API (for now, just log it)
                    console.log(`API Added: ${endpoint.method} - ${endpoint.name}`);
                    vscode.window.showInformationMessage(`Added API: ${endpoint.method} - ${endpoint.name}`);
                }
                break;
            // You can add more actions here in the future
            default:
                console.error(`Unknown action: ${action}`);
        }
    }
}