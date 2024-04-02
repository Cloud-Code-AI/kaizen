from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from api.github_helper.pull_requests import (
    process_pull_request,
    ACTIONS_TO_PROCESS_PR
)
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


app = FastAPI()


@app.post("/github-webhook")
async def handle_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    event = request.headers.get("X-GitHub-Event")
    if event == "pull_request" and payload["action"] in ACTIONS_TO_PROCESS_PR:
        background_tasks.add_task(process_pull_request, payload)
    else:
        print("Ignored event: ", event)
    return JSONResponse(content={"message": "Webhook received"})


@app.get("/")
def github_app_auth():
    return JSONResponse(content={"message": "API is Working!"})
