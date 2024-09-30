from kaizen.generator.unit_test import UnitTestGenerator

generator = UnitTestGenerator()

# You can run it for one file at a time
# generator.generate_tests(
#     file_path="kaizen/helpers/output.py", enable_critique=True, verbose=True, max_critique=1
# )

# OR for a directory
result = generator.generate_tests_from_dir(
    dir_path="kaizen/llms/",
    output_path=".kaizen/unit_test/",
    enable_critique=True,
    verbose=True,
    max_critique=1,
)
print(result)

# Run all tests
test_results = generator.run_tests()

# Run a single test file:
# test_results = generator.run_tests(file_path="test_create_folder.py")

for file_path, result in test_results.items():
    print(f"Results for {file_path}:")
    if "error" in result:
        print(f"  Error: {result['error']}")
    else:
        print(f"  Tests run: {result.get('tests_run', 'N/A')}")
        print(f"  Failures: {result.get('failed_tests', 'N/A')}")
        print(f"  Errors: {result.get('error_tests', 'N/A')}")
    print()


# You can also directly pass code to generator to generate tests
code = '''
class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, a, b):
        """Add two numbers and store the result."""
        self.result = a + b
        return self.result

    def subtract(self, a, b):
        """Subtract b from a and store the result."""
        self.result = a - b
        return self.result

    def get_result(self):
        """Return the last calculated result."""
        return self.result

def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    calc = Calculator()
    print(calc.add(5, 3))  # Should print 8
    print(calc.subtract(10, 4))  # Should print 6
    print(calc.get_result())  # Should print 6
    print(greet("Alice"))  # Should print "Hello, Alice!"
'''
# generator.generate_tests(file_path="sample.py", content=code)  # Replace with the actual file path
