from kaizen.helpers.parser import patch_to_separate_chunks

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

print(patch_to_separate_chunks(patch_text=patch_data))
