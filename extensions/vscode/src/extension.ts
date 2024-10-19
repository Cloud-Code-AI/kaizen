// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
// import * as vscode from 'vscode';
// import { SidebarProvider } from './SidebarProvider';
// import { ApiRequestProvider } from './apiRequest/apiRequestProvider';
// import { ApiManagementProvider } from './apiManagement/apiManagementProvider';
// import { ChatRepoProvider } from './chatRepo/chatRepoProvider';
// import { DocManagementProvider } from './docManagement/docManagementProvider';
// import { TestManagementProvider } from './testManagement/testManagementProvider';

// let outputChannel: vscode.OutputChannel;

// export function activate(context: vscode.ExtensionContext) {
// 	outputChannel = vscode.window.createOutputChannel("Kaizen CloudCode");

// 	outputChannel.appendLine("Kaizen CloudCode extension is activating!!!");
// 	console.log("Kaizen CloudCode extension is activating");


// 	const sidebarProvider = new SidebarProvider(context.extensionUri, context);
// 	const apiRequestProvider = new ApiRequestProvider(context);
// 	const testManagementProvider = new TestManagementProvider(context);
// 	const apiManagementProvider = new ApiManagementProvider(context);

// 	context.subscriptions.push(
// 		vscode.window.registerWebviewViewProvider(
// 			"kaizen-cloudcode-sidebar",
// 			sidebarProvider
// 		)
// 	);

// 	context.subscriptions.push(
// 		vscode.commands.registerCommand('kaizen-cloudcode.openTestManagement', () => {
// 			testManagementProvider.openTestManagementView();
// 		})
// 	);

// 	// You might want to add a command to open the API Request view directly
// 	let disposable = vscode.commands.registerCommand('kaizen-cloudcode.openApiRequest', () => {
// 		apiRequestProvider.openApiRequestView();
// 	});
// 	context.subscriptions.push(disposable);

// 	context.subscriptions.push(
// 		vscode.commands.registerCommand('kaizen-cloudcode.openSidebar', () => {
// 			vscode.commands.executeCommand('workbench.view.extension.kaizen-cloudcode-view');
// 		})
// 	);
// }

// export function log(message: string) {
// 	if (outputChannel) {
// 		outputChannel.appendLine(message);
// 	}
// 	console.log(message);
// }
// export function deactivate() { }
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below""
import * as vscode from 'vscode';
import { SidebarProvider } from './SidebarProvider';
import { ApiRequestProvider } from './apiRequest/apiRequestProvider';
import { ApiManagementProvider } from './apiManagement/apiManagementProvider';
import { ChatRepoProvider } from './chatRepo/chatRepoProvider';
import { DocManagementProvider } from './docManagement/docManagementProvider';
import { TestManagementProvider } from './testManagement/testManagementProvider';

let outputChannel: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext) {
    outputChannel = vscode.window.createOutputChannel("Kaizen CloudCode");

    outputChannel.appendLine("Kaizen CloudCode extension is activating!!!");
    console.log("Kaizen CloudCode extension is activating");

    const sidebarProvider = new SidebarProvider(context.extensionUri, context);
    const apiRequestProvider = new ApiRequestProvider(context);
    const apiManagementProvider = new ApiManagementProvider(context);
    const chatRepoProvider = new ChatRepoProvider(context);
    const docManagementProvider = new DocManagementProvider(context);
    const testManagementProvider = new TestManagementProvider(context);

    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            "kaizen-cloudcode-sidebar",
            sidebarProvider
        )
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('kaizen-cloudcode.openTestManagement', () => {
            testManagementProvider.openTestManagementView();
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('kaizen-cloudcode.openApiRequest', () => {
            apiRequestProvider.openApiRequestView();
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('kaizen-cloudcode.openApiManagement', () => {
            apiManagementProvider.openApiManagementView();
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('kaizen-cloudcode.openChatRepo', () => {
            chatRepoProvider.openChatRepoView();
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('kaizen-cloudcode.openDocManagement', () => {
            docManagementProvider.openDocManagementView();
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('kaizen-cloudcode.openSidebar', () => {
            vscode.commands.executeCommand('workbench.view.extension.kaizen-cloudcode-view');
        })
    );
}

export function log(message: string) {
    if (outputChannel) {
        outputChannel.appendLine(message);
    }
    console.log(message);
}

export function deactivate() {}