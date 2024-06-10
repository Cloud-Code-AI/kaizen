from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from github_app.github_helper.pull_requests import (
    process_pull_request,
    ACTIONS_TO_PROCESS_PR,
    ACTIONS_TO_UPDATE_DESC,
    process_pr_desc,
)
from github_app.github_helper.utils import is_github_signature_valid
from kaizen.utils.config import ConfigData
import logging

# from cloudcode.generator.ui import UITester

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/github-webhook")
async def handle_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    body = await request.body()
    event = request.headers.get("X-GitHub-Event")
    # Check if the Signature is valid
    CONFIG_DATA = ConfigData().get_config_data()
    if CONFIG_DATA["github_app"]["check_signature"] and not is_github_signature_valid(
        request.headers, body
    ):
        return HTTPException(status_code=404, detail="Invalid Signature")

    if event == "pull_request":
        if (
            CONFIG_DATA["github_app"]["auto_pr_review"]
            and payload["action"] in ACTIONS_TO_PROCESS_PR
        ):
            background_tasks.add_task(process_pull_request, payload)
        if (
            CONFIG_DATA["github_app"]["edit_pr_desc"]
            and payload["action"] in ACTIONS_TO_UPDATE_DESC
        ):
            background_tasks.add_task(process_pr_desc, payload)
    else:
        logger.info(f"Ignored event: {event}")
    return JSONResponse(content={"message": "Webhook received"})


@app.get("/")
def github_app_auth():
    return JSONResponse(content={"message": "API is Working!"})
