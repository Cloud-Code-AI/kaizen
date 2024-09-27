"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.HttpClient = void 0;
class HttpClient {
    async sendRequest(url, method, headers, body) {
        try {
            const response = await fetch(url, {
                method,
                headers,
                body,
            });
            return {
                status: response.status,
                headers: { ...response.headers },
                body: await response.text(),
            };
        }
        catch (error) {
            console.error('Error sending request:', error);
            throw error;
        }
    }
}
exports.HttpClient = HttpClient;
//# sourceMappingURL=httpClient.js.map