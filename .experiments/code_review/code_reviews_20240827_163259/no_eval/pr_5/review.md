PR URL: https://github.com/sauravpanda/applicant-screening/pull/5

# 🔍 Code Review Summary

❗ **Attention Required:** This push has potential issues. 🚨

## 📊 Stats
- Total Issues: 7
- Critical: 1
- Important: 0
- Minor: 0
- Files Affected: 1
## 🏆 Code Quality
[███████████████░░░░░] 75% (Fair)

## 🚨 Critical Issues

<details>
<summary><strong>Division by Zero Risk (1 issues)</strong></summary>

### 1. Potential division by zero if total_tokens is zero.
📁 **File:** `main.py:159`
⚖️ **Severity:** 9/10
🔍 **Description:** Potential division by zero if total_tokens is zero.
💡 **Solution:** 

**Current Code:**
```python
print(f"Total tokens used:{total_tokens:,}")
```

**Suggested Code:**
```python

```

</details>

## 📝 Minor Notes
Additional small points that you might want to consider:

<details>
<summary><strong>Click to expand (2 issues)</strong></summary>

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


----- Cost Usage (gpt-4o-mini)
{"prompt_tokens": 6403, "completion_tokens": 1126, "total_tokens": 7529}