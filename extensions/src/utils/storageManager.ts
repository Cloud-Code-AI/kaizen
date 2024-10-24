import * as vscode from 'vscode';

export class StorageManager {
    private context: vscode.ExtensionContext;

    constructor(context: vscode.ExtensionContext) {
        this.context = context;
    }

    public getValue(key: string): any {
        return this.context.globalState.get(key);
    }

    public setValue(key: string, value: any) {
        this.context.globalState.update(key, value);
    }
}