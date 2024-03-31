from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse


app = FastAPI()


@app.post('/webhook')
async def handle_webhook(request: Request):
    payload = await request.json()
    event = request.headers.get('X-GitHub-Event')
    if event == 'pull_request':
        pass
    else:
        print("Ignored event: ", event)
    return JSONResponse(content={'message': 'Webhook received'})


@app.get('/')
def github_app_auth():
    return JSONResponse(content={'message': "API is Working!"})
