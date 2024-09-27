export class HttpClient {
    public async sendRequest(url: string, method: string, headers: Record<string, string>, body?: string) {
        try {
            const options: RequestInit = {
                method,
                headers,
            };

            // Only add body for methods that typically have a body
            if (body && !['GET', 'HEAD'].includes(method.toUpperCase())) {
                options.body = body;
            }

            const response = await fetch(url, options);

            // Convert headers to a plain object
            const responseHeaders: Record<string, string> = {};
            response.headers.forEach((value, key) => {
                responseHeaders[key] = value;
            });

            return {
                status: response.status,
                headers: responseHeaders,
                body: await response.text(),
            };
        } catch (error) {
            console.error('Error sending request:', error);
            throw error;
        }
    }
}