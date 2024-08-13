from kaizen.generator.unit_test import UnitTestGenerator

generator = UnitTestGenerator()

# You can run it for one file at a time
generator.generate_tests(
    file_path="examples/unittest/typescript_code/home.page.tsx", enable_critique=True, verbose=True
)

# test_results = generator.run_tests()

# for file_path, result in test_results.items():
#     print(f"Results for {file_path}:")
#     if "error" in result:
#         print(f"  Error: {result['error']}")
#     else:
#         print(f"  Tests run: {result.get('tests_run', 'N/A')}")
#         print(f"  Failures: {result.get('failures', 'N/A')}")
#         print(f"  Errors: {result.get('errors', 'N/A')}")
#     print()
