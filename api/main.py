from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from api.github_helper.pull_requests import process_pull_request

app = FastAPI()


@app.post("/github-webhook")
async def handle_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    event = request.headers.get("X-GitHub-Event")
    if event == "pull_request":
        background_tasks.add_task(process_pull_request, payload)
    else:
        print("Ignored event: ", event)
    return JSONResponse(content={"message": "Webhook received"})


@app.get("/")
def github_app_auth():
    return JSONResponse(content={"message": "API is Working!"})
