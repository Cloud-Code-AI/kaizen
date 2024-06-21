import logging
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup, Comment
import asyncio
import nest_asyncio
import subprocess
import os
import json
from kaizen.helpers import general

logger = logging.getLogger(__name__)


PR_COLLAPSIBLE_TEMPLATE = """
<details>
<summary><strong>[{confidence}]<strong> -> {comment}</summary> \n
</strong> Potential Solution:</strong> \n\n{solution}
\n
<blockquote>  
    <p><code>{file_name} | {start_line} - {end_line}</code></p>
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
