import * as vscode from 'vscode';
import { ApiRequestView } from './apiRequestView';
import { HttpClient } from '../utils/httpClient';

interface Collection {
    name: string;
    requests: ApiRequest[];
}

interface ApiRequest {
    name: string;
    method: string;
    url: string;
    headers: Record<string, string>;
    body: string;
}

export class ApiRequestProvider {
    private context: vscode.ExtensionContext;
    private view: ApiRequestView | undefined;
    private httpClient: HttpClient;
    private collections: Collection[] = [];
    private environment: Record<string, string> = {};

    constructor(context: vscode.ExtensionContext) {
        this.context = context;
        this.httpClient = new HttpClient();
        this.handleApiRequest = this.handleApiRequest.bind(this);
        this.loadCollections();
        this.loadEnvironment();
    }

    public openApiRequestView() {
        console.log("API Request View : This is the request view");
        // if (!this.view) {
        //     this.view = new ApiRequestView(this.context, this.handleApiRequest);
        // }
        this.view = new ApiRequestView(this.context, this.handleApiRequest);
        this.view.show();
        this.updateCollectionsView();
    }

    private async handleApiRequest(
        method: string, 
        url: string, 
        headers: Record<string, string>, 
        queryParams: Record<string, string>, 
        formData: Record<string, string>, 
        body: string,
        bodyType: string
    ): Promise<void> {
        console.log("Handle API Request called");
        try {
            // Append query params to URL
            const urlObj = new URL(url);
            Object.entries(queryParams).forEach(([key, value]) => {
                urlObj.searchParams.append(key, value);
            });

            // Prepare body
            let requestBody: string | FormData | undefined;
            if (bodyType === 'form-data') {
                requestBody = new FormData();
                Object.entries(formData).forEach(([key, value]) => {
                    (requestBody as FormData).append(key, value);
                });
            } else if (bodyType === 'raw' && body) {
                requestBody = body;
            }

            const startTime = Date.now();
            const response = await this.httpClient.sendRequest(
                urlObj.toString(), 
                method, 
                headers, 
                requestBody
            );
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

    private replaceEnvironmentVariables(str: string): string {
        return str.replace(/\{\{(\w+)\}\}/g, (_, key) => this.environment[key] || '');
    }

    public addCollection(name: string) {
        console.log("api Request view : AddCollections called");
        this.collections.push({ name, requests: [] });
        this.saveCollections();
        this.updateCollectionsView();
    }

    public addRequestToCollection(collectionName: string, request: ApiRequest) {
        console.log("api Request view : AddRequestToCollections called");
        const collection = this.collections.find(c => c.name === collectionName);
        if (collection) {
            collection.requests.push(request);
            this.saveCollections();
            this.updateCollectionsView();
        }
    }

    private loadCollections() {
        this.collections = this.context.globalState.get('apiCollections', []);
    }

    private saveCollections() {
        this.context.globalState.update('apiCollections', this.collections);
    }

    private updateCollectionsView() {
        this.view?.postMessage({
            command: 'updateCollections',
            collections: this.collections
        });
    }

    public setEnvironmentVariable(key: string, value: string) {
        this.environment[key] = value;
        this.saveEnvironment();
    }

    private loadEnvironment() {
        this.environment = this.context.globalState.get('apiEnvironment', {});
    }

    private saveEnvironment() {
        this.context.globalState.update('apiEnvironment', this.environment);
    }
}