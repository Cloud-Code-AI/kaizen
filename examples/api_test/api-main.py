from kaizen.generator.api_test import APITestGenerator

generator = APITestGenerator()

generator.generate_tests(
     file_path="./examples/api_test/api-schema.json", 
     base_url="http://api.weatherbit.io/v2.0/",
     enable_critique=True, 
     verbose=True,
     max_critique=1
)

test_results = generator.run_tests()

for file_path, result in test_results.items():
    print(f"Results for {file_path}:")
    if "error" in result:
        print(f"  Error: {result['error']}")
    else:
        print(f"  Tests run: {result.get('tests_run', 'N/A')}")
        print(f"  Failures: {result.get('failures', 'N/A')}")
        print(f"  Errors: {result.get('errors', 'N/A')}")
    print()
