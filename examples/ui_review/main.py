from kaizen.reviewer.ui_review import UIReviewer

url = "https://cloudcode.ai"
ui_review = UIReviewer()
reviews = ui_review.generate_ui_review(url=url)["reviews"]

print_block = """
-----------------------------------------------
Topic: {topic}
Review: {review}
Confidence: {confidence}
Solution: {solution}

Code Block:
```html
{code_block}
```\n\n
"""

for review in reviews:
    content = print_block.format(
        topic=review["topic"],
        review=review["comment"],
        confidence=review["confidence"],
        code_block=review["code_block"],
        solution=review["solution"],
    )
    print(content)
