from kaizen.helpers.parser import patch_to_numbered_lines

patch_data = '''
From b82fcf4f6392a54bc8bfa6d099fb838f9293f448 Mon Sep 17 00:00:00 2001
From: Saurav Panda <sgp65@cornell.edu>
Date: Tue, 16 Jul 2024 21:56:02 -0700
Subject: [PATCH] fix: updated the work summary prompt to merge multiple
 summaries

---
 examples/work_summarizer/main.py            |  2 +-
 kaizen/llms/prompts/work_summary_prompts.py | 22 ++++++++++++++++++++-
 kaizen/reviewer/work_summarizer.py          |  6 +++++-
 pyproject.toml                              |  2 +-
 4 files changed, 28 insertions(+), 4 deletions(-)

diff --git a/examples/work_summarizer/main.py b/examples/work_summarizer/main.py
index 1436a23..ffd0282 100644
--- a/examples/work_summarizer/main.py
+++ b/examples/work_summarizer/main.py
@@ -8,7 +8,7 @@
 
 # Get the current date and calculate the date 14 days ago
 current_date = datetime.now(timezone.utc).date()
-since_date = current_date - timedelta(days=7)
+since_date = current_date - timedelta(days=14)
 
 # Convert the date to ISO format
 since_date_iso = since_date.isoformat()
diff --git a/kaizen/llms/prompts/work_summary_prompts.py b/kaizen/llms/prompts/work_summary_prompts.py
index acedda0..e35d38c 100644
--- a/kaizen/llms/prompts/work_summary_prompts.py
+++ b/kaizen/llms/prompts/work_summary_prompts.py
@@ -27,7 +27,7 @@
 }}
 
 estimated_time: its the range of time you think the above work might have taken for a developer. example "10-15hrs"
-details: its list of important changes in human readable term so that anyone can understand how the software has been impacted.
+details: its list of changes in human readable term so that anyone can understand how the software has been impacted.
   
 Guidelines:  
 1. Give a high-level overview of the goal.  
@@ -41,6 +41,26 @@
 PATCH DATA: {PATCH_DATA}  
 """
 
+MERGE_WORK_SUMMARY_PROMPT = """  
+Merge all this information into the following output format.
+
+OUTPUT Format:  
+{{
+    "summary": "<SUMMARY_OF_WORK_DONE>",  
+    "details": ["<IMPORTANT_DETAILS>", ...],  
+    "todo": ["<TODO_ITEMS>", ...],  
+    "future_considerations": ["<THINGS_TO_CONSIDER_IN_FUTURE>", ...],  
+    "estimated_time": <ESTIMATED_TIME_IN_HOURS>  
+}}
+
+estimated_time: its the range of time you think the above work might have taken for a developer in hours, be little generous. example "10-15hrs"
+details: its list of changes in human readable term so that anyone can understand how the software has been impacted.
+  
+All the summaries: 
+
+{SUMMARY_JSON}
+"""
+
 TWITTER_POST_PROMPT = """
 Given the following work summary, create a concise and engaging Twitter post (max 280 characters) that highlights the key changes or improvements. Format the post as markdown, enclosed in triple backticks:
 
diff --git a/kaizen/reviewer/work_summarizer.py b/kaizen/reviewer/work_summarizer.py
index ecacc57..df6082e 100644
--- a/kaizen/reviewer/work_summarizer.py
+++ b/kaizen/reviewer/work_summarizer.py
@@ -6,8 +6,10 @@
     WORK_SUMMARY_SYSTEM_PROMPT,
     TWITTER_POST_PROMPT,
     LINKEDIN_POST_PROMPT,
+    MERGE_WORK_SUMMARY_PROMPT
 )
 import logging
+import json
 
 
 class WorkSummaryGenerator:
@@ -55,7 +57,9 @@ def generate_work_summaries(
 
         if len(summaries) > 1:
             # TODO Merge summaries
-            pass
+            prompt = MERGE_WORK_SUMMARY_PROMPT.format(SUMMARY_JSON=json.dumps(summaries))
+            response, usage = self.provider.chat_completion_with_json(prompt, user=user)
+            summaries = [response]
 
         return {"summary": summaries[0], "usage": self.total_usage}
 
diff --git a/pyproject.toml b/pyproject.toml
index 95c754f..4b35bcc 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -1,6 +1,6 @@
 [tool.poetry]
 name = "kaizen-cloudcode"
-version = "0.3.9"
+version = "0.3.10"
 description = "An intelligent coding companion that accelerates your development workflow by providing efficient assistance, enabling you to craft high-quality code more rapidly."
 authors = ["Saurav Panda <saurav.panda@cloudcode.ai>"]
 license = "Apache2.0"
'''

patch_data2 = '''
From d3f483e4f6a9d3b6322e0baaeb1d1bc15fed3cc6 Mon Sep 17 00:00:00 2001
From: Saurav Panda <sgp65@cornell.edu>
Date: Thu, 18 Jul 2024 09:42:03 -0700
Subject: [PATCH] feat: added standard output format for description generation

---
 kaizen/generator/pr_description.py         |  51 ++------
 kaizen/llms/prompts/code_review_prompts.py | 140 ---------------------
 kaizen/llms/prompts/pr_desc_prompts.py     |  92 ++++++++++++++
 3 files changed, 105 insertions(+), 178 deletions(-)
 create mode 100644 kaizen/llms/prompts/pr_desc_prompts.py

diff --git a/kaizen/generator/pr_description.py b/kaizen/generator/pr_description.py
index e4f548c..e8a4635 100644
--- a/kaizen/generator/pr_description.py
+++ b/kaizen/generator/pr_description.py
@@ -5,12 +5,11 @@
 
 from kaizen.helpers import output, parser
 from kaizen.llms.provider import LLMProvider
-from kaizen.llms.prompts.code_review_prompts import (
+from kaizen.llms.prompts.pr_desc_prompts import (
     PR_DESCRIPTION_PROMPT,
     MERGE_PR_DESCRIPTION_PROMPT,
     PR_FILE_DESCRIPTION_PROMPT,
-    PR_DESC_EVALUATION_PROMPT,
-    CODE_REVIEW_SYSTEM_PROMPT,
+    PR_DESCRIPTION_SYSTEM_PROMPT,
 )
 
 
@@ -26,7 +25,7 @@ class PRDescriptionGenerator:
     def __init__(self, llm_provider: LLMProvider):
         self.logger = logging.getLogger(__name__)
         self.provider = llm_provider
-        self.provider.system_prompt = CODE_REVIEW_SYSTEM_PROMPT
+        self.provider.system_prompt = PR_DESCRIPTION_SYSTEM_PROMPT
         self.total_usage = {
             "prompt_tokens": 0,
             "completion_tokens": 0,
@@ -40,7 +39,6 @@ def generate_pull_request_desc(
         pull_request_desc: str,
         pull_request_files: List[Dict],
         user: Optional[str] = None,
-        reeval_response: bool = False,
     ) -> DescOutput:
         prompt = PR_DESCRIPTION_PROMPT.format(
             PULL_REQUEST_TITLE=pull_request_title,
@@ -51,14 +49,13 @@ def generate_pull_request_desc(
             raise Exception("Both diff_text and pull_request_files are empty!")
 
         if diff_text and self.provider.is_inside_token_limit(PROMPT=prompt):
-            desc = self._process_full_diff(prompt, user, reeval_response)
+            desc = self._process_full_diff(prompt, user)
         else:
             desc = self._process_files(
                 pull_request_files,
                 pull_request_title,
                 pull_request_desc,
                 user,
-                reeval_response,
             )
 
         body = output.create_pr_description(desc, pull_request_desc)
@@ -77,15 +74,13 @@ def _process_full_diff(
         self,
         prompt: str,
         user: Optional[str],
-        reeval_response: bool,
     ) -> str:
         self.logger.debug("Processing directly from diff")
-        resp, usage = self.provider.chat_completion_with_json(prompt, user=user)
+        resp, usage = self.provider.chat_completion(prompt, user=user)
+        desc = parser.extract_code_from_markdown(resp)
         self.total_usage = self.provider.update_usage(self.total_usage, usage)
 
-        if reeval_response:
-            resp = self._reevaluate_response(prompt, resp, user)
-        return resp["desc"]
+        return desc
 
     def _process_files(
         self,
@@ -93,7 +88,6 @@ def _process_files(
         pull_request_title: str,
         pull_request_desc: str,
         user: Optional[str],
-        reeval_response: bool,
     ) -> List[Dict]:
         self.logger.debug("Processing based on files")
         file_descs = []
@@ -102,15 +96,15 @@ def _process_files(
             pull_request_title,
             pull_request_desc,
             user,
-            reeval_response,
         ):
             file_descs.extend(file_review)
 
         prompt = MERGE_PR_DESCRIPTION_PROMPT.format(DESCS=json.dumps(file_descs))
-        resp, usage = self.provider.chat_completion_with_json(prompt, user=user)
+        resp, usage = self.provider.chat_completion(prompt, user=user)
+        desc = parser.extract_code_from_markdown(resp)
         self.total_usage = self.provider.update_usage(self.total_usage, usage)
 
-        return resp["desc"]
+        return desc
 
     def _process_files_generator(
         self,
@@ -118,7 +112,6 @@ def _process_files_generator(
         pull_request_title: str,
         pull_request_desc: str,
         user: Optional[str],
-        reeval_response: bool,
     ) -> Generator[List[Dict], None, None]:
         combined_diff_data = ""
         available_tokens = self.provider.available_tokens(
@@ -151,7 +144,6 @@ def _process_files_generator(
                     pull_request_title,
                     pull_request_desc,
                     user,
-                    reeval_response,
                 )
                 combined_diff_data = (
                     f"\n---->\nFile Name: {filename}\nPatch Details: {patch_details}"
@@ -163,7 +155,6 @@ def _process_files_generator(
                 pull_request_title,
                 pull_request_desc,
                 user,
-                reeval_response,
             )
 
     def _process_file_chunk(
@@ -172,30 +163,14 @@ def _process_file_chunk(
         pull_request_title: str,
         pull_request_desc: str,
         user: Optional[str],
-        reeval_response: bool,
     ) -> List[Dict]:
         prompt = PR_FILE_DESCRIPTION_PROMPT.format(
             PULL_REQUEST_TITLE=pull_request_title,
             PULL_REQUEST_DESC=pull_request_desc,
             CODE_DIFF=diff_data,
         )
-        resp, usage = self.provider.chat_completion_with_json(prompt, user=user)
+        resp, usage = self.provider.chat_completion(prompt, user=user)
+        desc = parser.extract_code_from_markdown(resp)
         self.total_usage = self.provider.update_usage(self.total_usage, usage)
 
-        if reeval_response:
-            resp = self._reevaluate_response(prompt, resp, user)
-
-        return resp["desc"]
-
-    def _reevaluate_response(self, prompt: str, resp: str, user: Optional[str]) -> str:
-        messages = [
-            {"role": "system", "content": self.provider.system_prompt},
-            {"role": "user", "content": prompt},
-            {"role": "assistant", "content": resp},
-            {"role": "user", "content": PR_DESC_EVALUATION_PROMPT},
-        ]
-        resp, usage = self.provider.chat_completion(
-            prompt, user=user, messages=messages
-        )
-        self.total_usage = self.provider.update_usage(self.total_usage, usage)
-        return resp
+        return desc
diff --git a/kaizen/llms/prompts/code_review_prompts.py b/kaizen/llms/prompts/code_review_prompts.py
index 04c1181..5942fff 100644
--- a/kaizen/llms/prompts/code_review_prompts.py
+++ b/kaizen/llms/prompts/code_review_prompts.py
@@ -166,146 +166,6 @@
 ```{FILE_PATCH}```
 """
 
-PR_DESCRIPTION_PROMPT = """
-As a skilled developer reviewing a pull request, generate a concise and well-formatted description summarizing the main purpose, scope of changes, significant modifications, refactoring, or new features introduced in the pull request.
-
-Provide the output in the following JSON format:
-
-{{
-  "desc": "
-### Summary
-
-<Brief one-line summary of the pull request>
-
-### Details
-
-<Detailed multi-line description in markdown format>
-- List of key changes
-- New features
-- Refactoring details
-  "
-}}
-
-When generating the description:
-
-- Create a concise and clear summary highlighting the main purpose of the pull request.
-- Use markdown formatting in the detailed description for better readability.
-- Organize the details into relevant sections or bullet points.
-- Focus on the most significant aspects of the changes.
-- Avoid repeating information already present in the pull request title or description.
-- Ensure the output is in valid JSON format.
-
-Based on the provided information:
-
-Pull Request Title: {PULL_REQUEST_TITLE}
-Pull Request Description: {PULL_REQUEST_DESC}
-Patch Data:
-{CODE_DIFF}
-
-Analyze the information thoroughly and generate a comprehensive summary and detailed description.
-Use your expertise to identify and highlight the most important aspects of the changes without asking for additional clarification. If certain details are unclear, make reasonable inferences based on the available information and your development experience.
-
-"""
-
-PR_FILE_DESCRIPTION_PROMPT = """
-As a skilled developer reviewing a pull request, generate a concise and well-formatted description summarizing the main purpose, scope of changes, significant modifications, refactoring, or new features introduced in the pull request.
-
-Provide the output in the following JSON format:
-
-{{
-  "desc": "
-### Summary
-
-<Brief one-line summary of the pull request>
-
-### Details
-
-<Detailed multi-line description in markdown format>
-- List of key changes
-- New features
-- Refactoring details
-  "
-}}
-
-When generating the description:
-
-- Create a concise and clear summary highlighting the main purpose of the pull request.
-- Use markdown formatting in the detailed description for better readability.
-- Organize the details into relevant sections or bullet points.
-- Focus on the most significant aspects of the changes.
-- Avoid repeating information already present in the pull request title or description.
-- Ensure the output is in valid JSON format.
-
-Based on the provided information:
-
-Pull Request Title: {PULL_REQUEST_TITLE}
-Pull Request Description: {PULL_REQUEST_DESC}
-Patch Data:
-{CODE_DIFF}
-
-Analyze the information thoroughly and generate a comprehensive summary and detailed description.
-Use your expertise to identify and highlight the most important aspects of the changes without asking for additional clarification. If certain details are unclear, make reasonable inferences based on the available information and your development experience.
-"""
-
-MERGE_PR_DESCRIPTION_PROMPT = """
-As a skilled developer reviewing a pull request, generate a concise and well-formatted description that synthesizes multiple PR descriptions into a single, comprehensive summary. This summary should encapsulate the main purpose, scope of changes, significant modifications, refactoring, and new features introduced in the pull request.
-
-Using the provided PR descriptions in JSON format, create a merged PR Description in the following JSON format:
-
-{{
-  "desc": "
-### Summary
-
-<Brief one-line summary encompassing the overall purpose of the pull request>
-
-### Details
-
-<Detailed multi-line description in markdown format>
-- Consolidated list of key changes
-- Aggregated new features
-- Combined refactoring details
-- Other significant aspects from all descriptions
-  "
-}}
-
-When generating the merged description:
-
-- Create a concise yet comprehensive summary that captures the essence of all provided descriptions.
-- Use markdown formatting in the detailed description for improved readability.
-- Organize the details into relevant sections or bullet points, consolidating similar information from different descriptions.
-- Focus on the most significant aspects of the changes across all descriptions.
-- Eliminate redundancies and repetitions while ensuring all unique and important points are included.
-- Ensure the output is in valid JSON format.
-
-Analyze the provided PR descriptions thoroughly and generate a unified, comprehensive summary and detailed description. Use your expertise to identify, merge, and highlight the most important aspects of the changes across all descriptions. If certain details seem contradictory or unclear, use your best judgment to provide the most accurate and coherent representation of the pull request's purpose and changes.
-
-Here is the information:
-{DESCS}
-"""
-
-PR_DESC_EVALUATION_PROMPT = """
-Please evaluate the accuracy and completeness of your previous responses in this conversation.
-Identify any potential errors or areas for improvement.
-
-Respond the JSON output as:
-{{
-  "desc": "
-### Summary
-
-<Brief one-line summary encompassing the overall purpose of the pull request>
-
-### Details
-
-<Detailed multi-line description in markdown format>
-- Consolidated list of key changes
-- Aggregated new features
-- Combined refactoring details
-- Other significant aspects from all descriptions
-  "
-}}
-
-"""
-
 
 PR_REVIEW_EVALUATION_PROMPT = """
 Please evaluate the accuracy and completeness of your previous responses in this conversation.
diff --git a/kaizen/llms/prompts/pr_desc_prompts.py b/kaizen/llms/prompts/pr_desc_prompts.py
new file mode 100644
index 0000000..3800d67
--- /dev/null
+++ b/kaizen/llms/prompts/pr_desc_prompts.py
@@ -0,0 +1,92 @@
+PR_DESCRIPTION_SYSTEM_PROMPT = """
+As a senior software developer reviewing code submissions, provide thorough, constructive feedback and suggestions for improvements. Consider best practices, error handling, performance, readability, and maintainability. Offer objective and respectful reviews that help developers enhance their skills and code quality. Use your expertise to provide comprehensive feedback without asking clarifying questions.
+"""
+
+PR_DESCRIPTION_PROMPT = """
+Summarize the main purpose, scope of changes, significant modifications, refactoring, or new features in this pull request.
+
+Output Format:
+```markdown
+# {{Generated PR Title}}
+
+## Overview
+{{Brief summary of overall purpose}}
+
+## Changes
+- Key Changes: {{List main modifications}}
+- New Features: {{List key new features}}
+- Refactoring: {{List main refactoring changes}}
+```
+
+Instructions:
+- Create a concise summary of the PR's main purpose.
+- Use markdown formatting for readability.
+- Focus on significant changes and avoid repetition.
+
+Based on:
+Title: {PULL_REQUEST_TITLE}
+Description: {PULL_REQUEST_DESC}
+Patch:
+{CODE_DIFF}
+
+Analyze the information and generate a comprehensive summary. Make reasonable inferences for unclear details based on your development experience.
+"""
+
+PR_FILE_DESCRIPTION_PROMPT = """
+Summarize the main purpose, scope of changes, significant modifications, refactoring, or new features in this pull request file.
+
+Output Format:
+```markdown
+# {{Generated PR Title}}
+
+## Overview
+{{Brief summary of file changes}}
+
+## Details
+- Main Changes: {{List key modifications}}
+- New Features: {{List new features, if any}}
+- Refactoring: {{List refactoring changes, if any}}
+```
+
+Instructions:
+- Create a concise summary of the file changes.
+- Use markdown formatting for readability.
+- Focus on significant changes and avoid repetition.
+
+Based on:
+Title: {PULL_REQUEST_TITLE}
+Description: {PULL_REQUEST_DESC}
+Patch:
+{CODE_DIFF}
+
+Analyze the information and generate a comprehensive summary. Make reasonable inferences for unclear details based on your development experience.
+"""
+
+MERGE_PR_DESCRIPTION_PROMPT = """
+Synthesize multiple PR descriptions into a single, comprehensive summary. Create a markdown-formatted description that captures the main purpose, scope of changes, and significant modifications.
+
+Output Format:
+```markdown
+# {{Generated PR Title}}
+
+## Overview
+{{Brief summary of overall purpose}}
+
+## Changes
+- New Features: {{List key new features}}
+- Refactoring: {{List main refactoring changes}}
+- Other Changes: {{List other significant modifications}}
+```
+
+Instructions:
+- Capture the essence of all descriptions concisely.
+- Use markdown formatting for readability.
+- Organize details into the specified sections.
+- Focus on the most significant aspects across all descriptions.
+- Ensure all unique and important points are included.
+
+Analyze the provided PR descriptions and generate a unified summary. Use your judgment to resolve any contradictions or unclear points.
+
+Here is the information:
+{DESCS}
+"""
'''

print(patch_to_numbered_lines(patch_text=patch_data))
