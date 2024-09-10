import re


class ReactParser:
    def __init__(self):
        self.source = ""

    def parse(self, source):
        self.source = source
        component_pattern = r"(?:export\s+)?(?:const|class)\s+(\w+)\s*(?:extends\s+React\.Component)?\s*(?:=\s*(?:\([^)]*\))?\s*=>)?\s*{([^}]*)}"
        function_pattern = (
            r"(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\((.*?)\)\s*{([^}]*)}"
        )
        hook_pattern = r"const\s+\[(\w+),\s*set(\w+)\]\s*=\s*useState\((.*?)\)"
        import_pattern = r"import\s+.*?(?:from\s+['\"](.*?)['\"]|\s*;)"
        global_var_pattern = r"(?:const|let|var)\s+(\w+)\s*=\s*([^;]+);"

        parsed_data = []
        imports = re.findall(import_pattern, source)
        global_vars = re.findall(global_var_pattern, source)

        for component_match in re.finditer(component_pattern, source):
            parsed_data.append(
                {
                    "type": "component",
                    "name": component_match.group(1),
                    "body": component_match.group(2),
                    "source": component_match.group(0),
                    "imports": imports,
                    "global_vars": global_vars,
                }
            )

        for func_match in re.finditer(function_pattern, source):
            parsed_data.append(
                {
                    "type": "function",
                    "name": func_match.group(1),
                    "args": func_match.group(2).split(","),
                    "body": func_match.group(3),
                    "source": func_match.group(0),
                    "imports": imports,
                    "global_vars": global_vars,
                }
            )

        hooks = re.findall(hook_pattern, source)
        for hook in hooks:
            parsed_data.append(
                {
                    "type": "hook",
                    "state_var": hook[0],
                    "setter": f"set{hook[1]}",
                    "initial_value": hook[2],
                    "imports": imports,
                    "global_vars": global_vars,
                }
            )

        return parsed_data
