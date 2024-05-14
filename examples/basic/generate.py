from kaizen.generator.ui import UITestGenerator

generator = UITestGenerator()

WEBPAGE_URL = "https://cloudcode.ai"

tests, _ = generator.generate_ui_tests(WEBPAGE_URL)

# print("Generated Tests: ", json.dumps(tests))

for test in tests:
    print(f'#### ======== Module Title: {test["module_title"]} ========== ####')
    for t in test["tests"]:
        print(f'Desc: {t["test_description"]}')
        print(f'Code: \n{t["code"]}')
        print("-----------------------------------------------------------")
