import ast


class PythonParser:
    def __init__(self):
        self.source = ""

    def parse(self, source):
        self.source = source
        tree = ast.parse(source)
        return self.parse_node(tree)

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
            }
        elif isinstance(node, ast.FunctionDef):
            return {
                "type": "function",
                "name": node.name,
                "args": [arg.arg for arg in node.args.args if arg.arg != "self"],
                "source": ast.get_source_segment(self.source, node),
            }
