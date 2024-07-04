import ast


class PythonParser:
    def parse(self, source):
        tree = ast.parse(source)
        parsed_data = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                parsed_data.append(self.parse_class(node))
            elif isinstance(node, ast.FunctionDef) and node.parent_field == "body":
                parsed_data.append(self.parse_function(node))

        return parsed_data

    def parse_class(self, node):
        return {
            "type": "class",
            "name": node.name,
            "methods": [
                self.parse_function(method)
                for method in node.body
                if isinstance(method, ast.FunctionDef)
            ],
        }

    def parse_function(self, node):
        return {
            "type": "function",
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
        }
