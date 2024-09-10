from kaizen.actors.unit_test_runner import UnitTestRunner
import logging
import json

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
runner = UnitTestRunner()
res = runner.discover_and_run_tests(test_file=".kaizen/unit_test/test_create_folder.py")
print(json.dumps(res, indent=2))
