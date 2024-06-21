import ast
import esprima

def chunk_python_code(code):
    tree = ast.parse(code)
    functions = {}
    classes = {}
    other_blocks = []
    current_block = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            functions[node.name] = ast.unparse(node)
        elif isinstance(node, ast.ClassDef):
            methods = {}
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods[item.name] = ast.unparse(item)
            classes[node.name] = {
                'definition': ast.unparse(node),
                'methods': methods
            }
        elif isinstance(node, (ast.If, ast.For, ast.While)):
            other_blocks.append(ast.unparse(node))
        else:
            current_block.append(ast.unparse(node))

    if current_block:
        other_blocks.append('\n'.join(current_block))

    return functions, classes, other_blocks

def chunk_javascript_code(code):
    tree = esprima.parseModule(code, jsx=True, tolerant=True)
    functions = {}
    classes = {}
    other_blocks = []

    def process_node(node):
        if node.type == 'FunctionDeclaration':
            functions[node.id.name] = esprima.generate(node)
        elif node.type == 'ClassDeclaration':
            methods = {}
            for item in node.body.body:
                if item.type == 'MethodDefinition':
                    methods[item.key.name] = esprima.generate(item)
            classes[node.id.name] = {
                'definition': esprima.generate(node),
                'methods': methods
            }
        elif node.type in ['IfStatement', 'ForStatement', 'WhileStatement']:
            other_blocks.append(esprima.generate(node))
        else:
            other_blocks.append(esprima.generate(node))

    for node in tree.body:
        process_node(node)

    return functions, classes, other_blocks

def chunk_code(code, language):
    if language.lower() == 'python':
        return chunk_python_code(code)
    elif language.lower() in ['javascript', 'js']:
        return chunk_javascript_code(code)
    else:
        raise ValueError("Unsupported language. Please use 'python' or 'javascript'.")

# Example usage
python_code = """
import math

def square(x):
    return x * x

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return math.pi * square(self.radius)

if __name__ == "__main__":
    c = Circle(5)
    print(f"Area: {c.area()}")
"""

javascript_code = """
import Math from 'math';

function square(x) {
    return x * x;
}

class Circle {
    constructor(radius) {
        this.radius = radius;
    }
    
    area() {
        return Math.PI * square(this.radius);
    }
}

const c = new Circle(5);
console.log(`Area: ${c.area()}`);
"""

def print_chunks(language, chunks):
    functions, classes, other_blocks = chunks
    print(f"\n{language.capitalize()} Chunks:")
    
    print("\nFunctions:")
    for name, func in functions.items():
        print(f"\n{name}:\n{func}")

    print("\nClasses:")
    for name, class_info in classes.items():
        print(f"\n{name}:")
        print(f"Definition:\n{class_info['definition']}")
        print("Methods:")
        for method_name, method in class_info['methods'].items():
            print(f"\n  {method_name}:\n{method}")

    print("\nOther Blocks:")
    for i, block in enumerate(other_blocks, 1):
        print(f"\nBlock {i}:\n{block}")

print_chunks("Python", chunk_code(python_code, 'python'))
print_chunks("JavaScript", chunk_code(javascript_code, 'javascript'))