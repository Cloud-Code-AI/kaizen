import re


class TypeScriptParser:
    def __init__(self):
        self.source = ""
        self.imports = []
        self.global_vars = []

    def parse(self, source):
        self.source = source
        self.extract_imports_and_globals()

        class_pattern = r"class\s+(\w+).*?{([^}]*)}"
        function_pattern = r"(?:async\s+)?function\s+(\w+)\s*\((.*?)\).*?{([^}]*)}"
        interface_pattern = r"interface\s+(\w+).*?{([^}]*)}"
        type_pattern = r"type\s+(\w+)\s*=\s*([^;]+);"

        parsed_data = []

        for class_match in re.finditer(class_pattern, self.source):
            class_name = class_match.group(1)
            class_body = class_match.group(2)
            methods = re.findall(r"(\w+)\s*\((.*?)\).*?{([^}]*)}", class_body)
            parsed_data.append(
                {
                    "type": "class",
                    "name": class_name,
                    "methods": [
                        {
                            "type": "function",
                            "name": m[0],
                            "args": m[1].split(","),
                            "source": f"{m[0]}({m[1]}) {{{m[2]}}}",
                        }
                        for m in methods
                    ],
                    "source": class_match.group(0),
                    "imports": self.imports,
                    "global_vars": self.global_vars,
                }
            )

        for func_match in re.finditer(function_pattern, self.source):
            parsed_data.append(
                {
                    "type": "function",
                    "name": func_match.group(1),
                    "args": func_match.group(2).split(","),
                    "source": func_match.group(0),
                    "imports": self.imports,
                    "global_vars": self.global_vars,
                }
            )

        for interface_match in re.finditer(interface_pattern, self.source):
            parsed_data.append(
                {
                    "type": "interface",
                    "name": interface_match.group(1),
                    "properties": [
                        prop.strip()
                        for prop in interface_match.group(2).split(";")
                        if prop.strip()
                    ],
                    "source": interface_match.group(0),
                    "imports": self.imports,
                    "global_vars": self.global_vars,
                }
            )

        for type_match in re.finditer(type_pattern, self.source):
            parsed_data.append(
                {
                    "type": "type",
                    "name": type_match.group(1),
                    "definition": type_match.group(2),
                    "source": type_match.group(0),
                    "imports": self.imports,
                    "global_vars": self.global_vars,
                }
            )

        return parsed_data

    def extract_imports_and_globals(self):
        import_pattern = r"import\s+.*?(?:from\s+['\"](.*?)['\"]|\s*;)"
        global_var_pattern = r"(?:const|let|var)\s+(\w+)\s*=\s*([^;]+);"

        self.imports = re.findall(import_pattern, self.source)
        self.global_vars = [
            match[0] for match in re.findall(global_var_pattern, self.source)
        ]
