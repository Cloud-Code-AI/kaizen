from kaizen.generator.ui import UITestGenerator
import time
import sys

generator = UITestGenerator()

WEBPAGE_URL = "https://cloudcode.ai"

print(f"Generating UI tests for `{WEBPAGE_URL}`, please wait...")
start_time = time.time()

try:
    tests, _ = generator.generate_ui_tests(WEBPAGE_URL)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"\nUI tests generated in {elapsed_time:.2f} seconds.")


for test in tests:
    print(
        f'#### ======== Module Title: {test["module_title"]} || Importance: {test["importance"]} ========== ####'
    )
    for t in test["tests"]:
        print(f'Desc: {t["test_description"]}')
        print(f'Code: \n{t["code"]}')
        print("-----------------------------------------------------------")
