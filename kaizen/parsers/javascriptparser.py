import re


class JavaScriptParser:
    def parse(self, source):
        self.source = source
        class_pattern = r"class\s+(\w+)\s*{([^}]*)}"
        function_pattern = r"(async\s+)?function\s+(\w+)\s*\((.*?)\)\s*{([^}]*)}"

        parsed_data = []

        for class_match in re.finditer(class_pattern, source):
            class_name = class_match.group(1)
            class_body = class_match.group(2)
            methods = re.findall(r"(\w+)\s*\((.*?)\)\s*{([^}]*)}", class_body)
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
                }
            )

        for func_match in re.finditer(function_pattern, source):
            parsed_data.append(
                {
                    "type": "function",
                    "name": func_match.group(2),
                    "args": func_match.group(3).split(","),
                    "source": func_match.group(0),
                }
            )

        return parsed_data
