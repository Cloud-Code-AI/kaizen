import * as vscode from 'vscode';
import { ApiRequestView } from './apiRequestView';
import { HttpClient } from '../utils/httpClient';

export class ApiRequestProvider {
    private context: vscode.ExtensionContext;
    private view: ApiRequestView | undefined;
    private httpClient: HttpClient;

    constructor(context: vscode.ExtensionContext) {
        this.context = context;
        this.httpClient = new HttpClient();
    }

    public openApiRequestView() {
        if (!this.view) {
            this.view = new ApiRequestView(this.context, this.handleApiRequest.bind(this));
        }
        this.view.show();
    }

    private async handleApiRequest(method: string, url: string, headers: string, body: string) {
        try {
            const parsedHeaders = JSON.parse(headers);
            const startTime = Date.now();
            const response = await this.httpClient.sendRequest(url, method, parsedHeaders, body);
            const endTime = Date.now();
            const responseTime = endTime - startTime;
            const responseSize = JSON.stringify(response).length;

            this.view?.postMessage({
                command: 'receiveResponse',
                response: response,
                time: responseTime,
                size: responseSize
            });
        } catch (error) {
            vscode.window.showErrorMessage(`Error sending request: ${error}`);
        }
    }
}