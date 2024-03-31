from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from github_helper.pull_requests import process_pull_request

app = FastAPI()


@app.post('/github-webhook')
async def handle_webhook(request: Request):
    payload = await request.json()
    event = request.headers.get('X-GitHub-Event')
    if event == 'pull_request':
        BackgroundTasks.create_task(process_pull_request, payload)
    else:
        print("Ignored event: ", event)
    return JSONResponse(content={'message': 'Webhook received'})


@app.get('/')
def github_app_auth():
    return JSONResponse(content={'message': "API is Working!"})
