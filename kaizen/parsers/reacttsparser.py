import re


class ReactTSParser:
    def __init__(self):
        self.source = ""
        self.imports = []
        self.global_vars = []

    def parse(self, source):
        self.source = source
        self.extract_imports_and_globals()

        component_pattern = r"(class|function|const)\s+(\w+).*?{([^}]*)}"
        hook_pattern = r"const\s+\[(\w+),\s*set(\w+)\]\s*=\s*useState\((.*?)\)"

        parsed_data = []

        for comp_match in re.finditer(component_pattern, self.source):
            comp_type = comp_match.group(1)
            comp_name = comp_match.group(2)
            comp_body = comp_match.group(3)

            if comp_type == "class":
                methods = re.findall(r"(\w+)\s*\((.*?)\):\s*\w+\s*{([^}]*)}", comp_body)
                parsed_data.append(
                    {
                        "type": "class",
                        "name": comp_name,
                        "methods": [
                            {
                                "type": "function",
                                "name": m[0],
                                "args": m[1].split(","),
                                "source": f"{m[0]}({m[1]}): return_type {{{m[2]}}}",
                            }
                            for m in methods
                        ],
                        "source": comp_match.group(0),
                        "imports": self.imports,
                        "global_vars": self.global_vars,
                    }
                )
            else:
                parsed_data.append(
                    {
                        "type": "function",
                        "name": comp_name,
                        "args": [],
                        "source": comp_match.group(0),
                        "imports": self.imports,
                        "global_vars": self.global_vars,
                    }
                )

        for hook_match in re.finditer(hook_pattern, self.source):
            parsed_data.append(
                {
                    "type": "hook",
                    "state_var": hook_match.group(1),
                    "setter": hook_match.group(2),
                    "initial_value": hook_match.group(3),
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
