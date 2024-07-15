from kaizen.generator.unit_test import UnitTestGenerator

generator = UnitTestGenerator()
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
generator.generate_tests(file_path="kaizen/helpers/output.py")
