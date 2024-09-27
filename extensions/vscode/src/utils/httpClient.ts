export class HttpClient {
    public async sendRequest(url: string, method: string, headers: Record<string, string>, body?: string) {
        try {
            const response = await fetch(url, {
                method,
                headers,
                body,
            });

            return {
                status: response.status,
                headers: {...response.headers},
                body: await response.text(),
            };
        } catch (error) {
            console.error('Error sending request:', error);
            throw error;
        }
    }
}