import ast
import esprima
import escodegen
import json


ParsedBody = {
    "functions": {},
    "classes": {},
    "hooks": {},
    "components": {},
    "other_blocks": [],
}


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
            classes[node.name] = {"definition": ast.unparse(node), "methods": methods}
        elif isinstance(node, (ast.If, ast.For, ast.While)):
            other_blocks.append(ast.unparse(node))
        else:
            current_block.append(ast.unparse(node))

    if current_block:
        other_blocks.append("\n".join(current_block))

    body = ParsedBody
    body["functions"] = functions
    body["classes"] = classes
    body["other_blocks"] = other_blocks
    return body


def chunk_javascript_code(code):
    tree = esprima.parseModule(code, jsx=True, tolerant=True)
    functions = {}
    classes = {}
    components = {}
    hooks = {}
    other_blocks = []

    def ast_to_source(node):
        try:
            return escodegen.generate(node)
        except Exception:
            return f"// Unable to generate code for {node.type}"

    def process_node(node):
        if node.type == "FunctionDeclaration":
            if is_react_component(node):
                components[node.id.name] = ast_to_source(node)
            else:
                functions[node.id.name] = ast_to_source(node)
        elif node.type == "ClassDeclaration":
            if is_react_component(node):
                components[node.id.name] = ast_to_source(node)
            else:
                methods = {}
                for item in node.body.body:
                    if item.type == "MethodDefinition":
                        methods[item.key.name] = ast_to_source(item)
                classes[node.id.name] = {
                    "definition": ast_to_source(node),
                    "methods": methods,
                }
        elif node.type == "VariableDeclaration":
            for decl in node.declarations:
                if decl.init and decl.init.type == "ArrowFunctionExpression":
                    if is_react_component(decl.init):
                        components[decl.id.name] = ast_to_source(node)
                    elif is_react_hook(decl.id.name):
                        hooks[decl.id.name] = ast_to_source(node)
                    else:
                        functions[decl.id.name] = ast_to_source(node)
                else:
                    other_blocks.append(ast_to_source(node))
        elif node.type in [
            "ImportDeclaration",
            "ExportDefaultDeclaration",
            "ExportNamedDeclaration",
        ]:
            other_blocks.append(ast_to_source(node))
        else:
            other_blocks.append(ast_to_source(node))

    def is_react_component(node):
        # Check if the function/class is likely a React component
        if node.type == "FunctionDeclaration" or node.type == "ArrowFunctionExpression":
            body = node.body.body if node.body.type == "BlockStatement" else [node.body]
            return any(
                stmt.type == "ReturnStatement"
                and stmt.argument
                and stmt.argument.type == "JSXElement"
                for stmt in body
            )
        elif node.type == "ClassDeclaration":
            return any(
                method.key.name == "render"
                for method in node.body.body
                if method.type == "MethodDefinition"
            )
        return False

    def is_react_hook(name):
        # Check if the function name starts with 'use'
        return name.startswith("use") and name[3].isupper()

    for node in tree.body:
        process_node(node)

    # return functions, classes, components, hooks, other_blocks
    body = ParsedBody
    body["functions"] = functions
    body["classes"] = classes
    body["other_blocks"] = other_blocks
    body["components"] = components
    body["hooks"] = hooks
    return body


def chunk_code(code, language):
    if language.lower() == "python":
        return chunk_python_code(code)
    elif language.lower() in ["javascript", "js"]:
        return chunk_javascript_code(code)
    else:
        raise ValueError("Unsupported language. Please use 'python' or 'javascript'.")
