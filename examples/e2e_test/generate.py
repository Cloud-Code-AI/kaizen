from kaizen.generator.e2e_tests import E2ETestGenerator
import time
import sys
import traceback

generator = E2ETestGenerator()

WEBPAGE_URL = "https://cloudcode.ai"

print(f"Generating UI tests for `{WEBPAGE_URL}`, please wait...")
start_time = time.time()

try:
    tests, _ = generator.generate_e2e_tests(WEBPAGE_URL)
except Exception as e:
    print(f"Error: {e}")
    print(traceback.format_exc())
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

results = generator.run_tests()
print(f"Test Execution results: \n {results}")
