from kaizen.generator.api_test import APITestGenerator

generator = APITestGenerator()

print("Entering api generator function")
generator.generate_tests(
     file_path="F:/Kaizen/kaizen-fork/kaizen/examples/api_test/api-schema.json", enable_critique=True, verbose=True, max_critique=1
)
print("Exited the api gen func")