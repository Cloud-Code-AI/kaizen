import * as vscode from 'vscode';
import { ApiRequestView } from './apiRequestView';
import { HttpClient } from '../utils/httpClient';
import * as fs from 'fs';
import * as path from 'path';
import * as msgpack from 'msgpack-lite'; 

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
    private apiHistory: ApiRequest[] = []; 

    constructor(context: vscode.ExtensionContext) {
        this.context = context;
        this.httpClient = new HttpClient();
        this.handleApiRequest = this.handleApiRequest.bind(this);
        this.loadCollections();
        this.loadEnvironment();
        this.loadApiHistory(); // Load existing API history
    }

    public openApiRequestView() {
        if (!this.view) {
            this.view = new ApiRequestView(this.context, this.handleApiRequest);
        }
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

            // Create an API request object
            const apiRequest: ApiRequest = {
                name: `${method} ${url}`,
                method,
                url,
                headers,
                body,
            };

            // Add to API history and save it
            this.apiHistory.push(apiRequest);
            await this.saveApiHistory(); // Save in MessagePack format

            this.view?.postMessage({
                command: 'receiveResponse',
                response,
                time: responseTime,
                size: responseSize
            });
        } catch (error) {
            vscode.window.showErrorMessage(`Error sending request: ${error}`);
        }
    }

    private loadApiHistory() {
        // Load existing API history from global state if needed
        this.apiHistory = this.context.globalState.get('apiHistory', []);
    }

    private async saveApiHistory() {
        try {
            console.log("Saving API History...");

            // Update global state with current API history
            await this.context.globalState.update('apiHistory', this.apiHistory);

            // Define file path for saving the API history
            const folderPath = path.join(this.context.extensionPath, 'api_history');
            
            // Create directory if it doesn't exist
            if (!fs.existsSync(folderPath)) {
                fs.mkdirSync(folderPath);
                console.log(`Created folder at ${folderPath}`);
            }

            // Define file path for the MessagePack file
            const filePath = path.join(folderPath, 'history.msgpack');

            // Write API history to MessagePack file
            const packedData = msgpack.encode(this.apiHistory); // Encode data using MessagePack
            fs.writeFileSync(filePath, packedData); // Write packed data to file
            
            vscode.window.showInformationMessage('API history saved successfully in MessagePack format!');
        } catch (error) {
            console.error('Error saving API history:', error); // Log any errors encountered
            vscode.window.showErrorMessage(`Failed to save API history: ${error.message}`);
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