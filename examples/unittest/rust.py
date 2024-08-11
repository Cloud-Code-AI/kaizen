from kaizen.generator.unit_test import UnitTestGenerator

generator = UnitTestGenerator()
code = """
struct Calculator {
    result: i32,
}

impl Calculator {
    fn new() -> Calculator {
        Calculator { result: 0 }
    }

    fn add(&mut self, a: i32, b: i32) -> i32 {
        self.result = a + b;
        self.result
    }

    fn subtract(&mut self, a: i32, b: i32) -> i32 {
        self.result = a - b;
        self.result
    }

    fn get_result(&self) -> i32 {
        self.result
    }
}

fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

fn main() {
    let mut calc = Calculator::new();
    println!("{}", calc.add(5, 3));  // Should print 8
    println!("{}", calc.subtract(10, 4));  // Should print 6
    println!("{}", calc.get_result());  // Should print 6
    println!("{}", greet("Alice"));  // Should print "Hello, Alice!"
}
"""

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
