PR URL: https://github.com/Cloud-Code-AI/kaizen/pull/222

# 🔍 Code Review Summary

❗ **Attention Required:** This push has potential issues. 🚨

## 📊 Stats
- Total Issues: 25
- Critical: 7
- Important: 0
- Minor: 0
- Files Affected: 12
## 🏆 Code Quality
[█████████████████░░░] 85% (Good)

## 🚨 Critical Issues

<details>
<summary><strong>Security (7 issues)</strong></summary>

### 1. Hardcoded API keys in config.json
📁 **File:** `config.json:13`
⚖️ **Severity:** 9/10
🔍 **Description:** Hardcoded API keys in config.json
💡 **Solution:** 

**Current Code:**
```python
"api_key": "os.environ/AZURE_API_KEY"
```

**Suggested Code:**
```python

```

### 2. Potential SQL injection vulnerability in `store_abstraction_and_embedding` method.
📁 **File:** `kaizen/retriever/llama_index_retriever.py:158`
⚖️ **Severity:** 9/10
🔍 **Description:** Potential SQL injection vulnerability in `store_abstraction_and_embedding` method.
💡 **Solution:** 

**Current Code:**
```python
embedding_query = text(
    """
    INSERT INTO function_embeddings (function_id, vector)
    VALUES (:function_id, :vector)
    ON CONFLICT (function_id) DO UPDATE SET vector = EXCLUDED.vector
    """
)
```

**Suggested Code:**
```python

```

### 3. Changes made to sensitive file
📁 **File:** `config.json:4`
⚖️ **Severity:** 10/10
🔍 **Description:** Changes made to sensitive file
💡 **Solution:** 

**Current Code:**
```python
NA
```

**Suggested Code:**
```python

```

### 4. Changes made to sensitive file
📁 **File:** `Dockerfile:4`
⚖️ **Severity:** 10/10
🔍 **Description:** Changes made to sensitive file
💡 **Solution:** 

**Current Code:**
```python
NA
```

**Suggested Code:**
```python

```

### 5. Changes made to sensitive file
📁 **File:** `docker-compose.yml:15`
⚖️ **Severity:** 10/10
🔍 **Description:** Changes made to sensitive file
💡 **Solution:** 

**Current Code:**
```python
NA
```

**Suggested Code:**
```python

```

### 6. Changes made to sensitive file
📁 **File:** `.gitignore:164`
⚖️ **Severity:** 10/10
🔍 **Description:** Changes made to sensitive file
💡 **Solution:** 

**Current Code:**
```python
NA
```

**Suggested Code:**
```python

```

### 7. Changes made to sensitive file
📁 **File:** `db_setup/init.sql:1`
⚖️ **Severity:** 10/10
🔍 **Description:** Changes made to sensitive file
💡 **Solution:** 

**Current Code:**
```python
NA
```

**Suggested Code:**
```python

```

</details>

## 📝 Minor Notes
Additional small points that you might want to consider:

<details>
<summary><strong>Click to expand (9 issues)</strong></summary>

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


----- Cost Usage (gpt-4o-2024-05-13)
{"prompt_tokens": 22541, "completion_tokens": 4406, "total_tokens": 26947}