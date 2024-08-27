PR URL: https://github.com/Cloud-Code-AI/kaizen/pull/252

# 🔍 Code Review Summary

✅ **All Clear:** This commit looks good! 👍

## 📊 Stats
- Total Issues: 2
- Critical: 0
- Important: 0
- Minor: 2
- Files Affected: 2
## 🏆 Code Quality
[██████████████████░░] 90% (Excellent)

## 📝 Minor Notes
Additional small points that you might want to consider:

<details>
<summary><strong>Click to expand (2 issues)</strong></summary>

<details>
<summary><strong>Linkedin Post Generation (2 issues)</strong></summary>

### 1. The LinkedIn post generation code is not formatted correctly.
📁 **File:** `examples/work_summarizer/main.py:60`
⚖️ **Severity:** 3/10
🔍 **Description:** The LinkedIn post generation code is spread across multiple lines, making it less readable and maintainable.
💡 **Solution:** Condense the LinkedIn post generation code into a single line, similar to the Twitter post generation.

**Current Code:**
```python
linkedin_post = work_summary_generator.generate_linkedin_post(
    summary, user="oss_example"
)
```

**Suggested Code:**
```python
linkedin_post = work_summary_generator.generate_linkedin_post(summary, user="oss_example")
```

### 2. The TWITTER_POST_PROMPT and LINKEDIN_POST_PROMPT could be improved for better readability.
📁 **File:** `kaizen/llms/prompts/work_summary_prompts.py:44`
⚖️ **Severity:** 4/10
🔍 **Description:** The prompts are currently formatted as a single long string, making them difficult to read and maintain.
💡 **Solution:** Consider breaking the prompts into multiple lines, using string formatting, and adding comments to explain the different sections.

</details>

</details>

---

> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️

<details>
<summary>Useful Commands</summary>

- **Feedback:** Reply with `!feedback [your message]`
- **Ask PR:** Reply with `!ask-pr [your question]`
- **Review:** Reply with `!review`
- **Explain:** Reply with `!explain [issue number]` for more details on a specific issue
- **Ignore:** Reply with `!ignore [issue number]` to mark an issue as false positive
- **Update Tests:** Reply with `!unittest` to create a PR with test changes
</details>


----- Cost Usage (anthropic.claude-3-haiku-20240307-v1:0)
{"prompt_tokens": 4436, "completion_tokens": 465, "total_tokens": 4901}