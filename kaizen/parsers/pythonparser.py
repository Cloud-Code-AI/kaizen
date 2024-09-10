import ast
import black
from kaizen.helpers.parser import extract_code_from_markdown


class PythonParser:
    def __init__(self):
        self.source = ""
        self.imports = []
        self.global_vars = []

    def parse(self, source):
        self.source = source
        tree = ast.parse(source)
        self.extract_imports_and_globals(tree)
        return self.parse_node(tree)

    def extract_imports_and_globals(self, tree):
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Import):
                self.imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                self.imports.extend(f"{module}.{alias.name}" for alias in node.names)
            elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                self.global_vars.append(node.targets[0].id)

    def parse_node(self, node):
        if isinstance(node, ast.Module):
            return [
                self.parse_node(child)
                for child in node.body
                if isinstance(child, (ast.ClassDef, ast.FunctionDef))
            ]
        elif isinstance(node, ast.ClassDef):
            return {
                "type": "class",
                "name": node.name,
                "methods": [
                    self.parse_node(child)
                    for child in node.body
                    if isinstance(child, ast.FunctionDef)
                ],
                "source": ast.get_source_segment(self.source, node),
                "imports": self.imports,
                "global_vars": self.global_vars,
            }
        elif isinstance(node, ast.FunctionDef):
            return {
                "type": "function",
                "name": node.name,
                "args": [arg.arg for arg in node.args.args if arg.arg != "self"],
                "source": ast.get_source_segment(self.source, node),
                "imports": self.imports,
                "global_vars": self.global_vars,
            }

    def format_python_markdown_snippet(self, code_snippet):
        code_snippet = extract_code_from_markdown(code_snippet)
        return black.format_str(code_snippet, mode=black.Mode())
