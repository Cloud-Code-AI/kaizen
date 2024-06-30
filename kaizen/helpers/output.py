import logging
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup, Comment
import asyncio
import nest_asyncio
import subprocess
import os
import json
from kaizen.helpers import general
from typing import List, Dict

logger = logging.getLogger(__name__)


PR_COLLAPSIBLE_TEMPLATE = """
<details>
<summary><strong>[{confidence}]<strong> -> {comment}</summary> \n
</strong> Potential Solution:</strong> \n\n{solution}
\n
<blockquote>  
    <p><code>{file_name} | {position}</code></p>
    <p>request_for_change: {request_for_change}</p>  
</blockquote>  
</details> \n

"""

DESC_COLLAPSIBLE_TEMPLATE = """
<details>
<summary>Original Description</summary>
{desc}
</details>

"""


def create_pr_description(desc, original_desc):
    markdown_output = desc
    markdown_output += "\n\n> ✨ Generated with love by Kaizen ❤️"
    markdown_output += "\n\n" + DESC_COLLAPSIBLE_TEMPLATE.format(desc=original_desc)
    return markdown_output


async def get_html(url):
    async with async_playwright() as p:
        subprocess.run(["playwright", "install", "--with-deps"], check=True)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        html = await page.content()
        await browser.close()
        return html


def get_web_html(url):
    nest_asyncio.apply()
    html = asyncio.run(get_html(url))
    soup = BeautifulSoup(html, "html.parser")

    for svg in soup.find_all("svg"):
        svg.decompose()

    # Delete each comment
    for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    for style_block in soup.find_all("style"):
        style_block.decompose()

    pretty_html = soup.prettify()
    return pretty_html


def get_parent_folder():
    return os.getcwd()


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logger.debug(f"Folder '{folder_path}' created successfully.")
    else:
        logger.debug(f"Folder '{folder_path}' already exists.")


def create_test_files(json_tests, folder_path):
    with open(f"{folder_path}/tests.json", "w") as f:
        f.write(json.dumps(json_tests))

    for module in json_tests:
        temp_folder_path = os.path.join(folder_path, module["folder_name"])
        create_folder(temp_folder_path)

        for test in module["tests"]:
            file_path = os.path.join(
                temp_folder_path,
                "test_" + "_".join(test["test_name"].lower().split(" ")) + ".py",
            )
            with open(file_path, "w") as f:
                cleaned_code = general.clean_python_code(test["code"])
                if not cleaned_code:
                    logger.info(f"Failed to clean code")
                else:
                    cleaned_code = (
                        f"'''Importance: {module['importance']}\
                            \nModule Name: {module['module_title']}\
                            \nDescription: {test['test_description']}\n'''\n\n"
                        + cleaned_code
                    )
                    f.write(cleaned_code)


def create_pr_review_text(topics: Dict[str, List[Dict]]) -> str:
    markdown_title = "## Code Review\n\n"
    markdown_output = ""
    high_ranked_issues = 0

    for topic, reviews in topics.items():
        if reviews:
            markdown_output += f"### {topic}\n\n"
            for review in reviews:
                if review.get("confidence", "") == "critical":
                    high_ranked_issues += 1
                ct = PR_COLLAPSIBLE_TEMPLATE.format(
                    comment=review.get("comment", "NA"),
                    reasoning=review.get("reasoning", "NA"),
                    solution=review.get("solution", "NA"),
                    confidence=review.get("confidence", "NA"),
                    position=review.get("position", "NA"),
                    end_line=review.get("end_line", "NA"),
                    file_name=review.get("file_name", "NA"),
                    request_for_change=review.get("request_for_change", "NA"),
                )
                markdown_output += ct + "\n"

    status_msg = (
        "❗ **Attention Required:** This PR has potential issues. 🚨\n\n"
        if high_ranked_issues > 0
        else "✅ **All Clear:** This PR is ready to merge! 👍\n\n"
    )
    return markdown_title + status_msg + markdown_output
