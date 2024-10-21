from kaizen.retriever.code_chunker import chunk_code
import json


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

# Example usage
react_nextjs_code = """
import React, { useState, useEffect } from 'react';
import Head from 'next/head';

function useCustomHook() {
    const [value, setValue] = useState(0);
    return [value, setValue];
}

function HomePage() {
    const [count, setCount] = useCustomHook();

    useEffect(() => {
        document.title = `Count: ${count}`;
    }, [count]);

    return (
        <div>
            <Head>
                <title>Home Page</title>
            </Head>
            <h1>Welcome to Next.js!</h1>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>Increment</button>
        </div>
    );
}

export default HomePage;
"""


def print_chunks(language, chunks):
    print(f"\n{language.capitalize()} Chunks:")
    print(json.dumps(chunks, indent=2))
    # print("\nFunctions:")
    # for name, func in chunks["functions"].items():
    #     print(f"\n{name}:\n{func}")

    # print("\nClasses:")
    # for name, class_info in chunks["classes"].items():
    #     print(f"\n{name}:")
    #     print(f"Definition:\n{class_info['definition']}")
    #     print("Methods:")
    #     for method_name, method in class_info["methods"].items():
    #         print(f"\n  {method_name}:\n{method}")

    # print("\nOther Blocks:")
    # for i, block in enumerate(chunks["other_blocks"], 1):
    #     print(f"\nBlock {i}:\n{block}")


print_chunks("Python", chunk_code(python_code, "python"))
print_chunks("JavaScript", chunk_code(javascript_code, "javascript"))
print_chunks("JavaScript", chunk_code(javascript_code, "javascript"))
print_chunks("React", chunk_code(react_nextjs_code, "javascript"))
