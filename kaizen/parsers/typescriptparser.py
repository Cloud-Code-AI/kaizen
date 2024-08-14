import re


class TypeScriptParser:
    def parse(self, source):
        self.source = source
        class_pattern = (
            r"(export\s+)?(abstract\s+)?class\s+(\w+)(?:\s+extends\s+\w+)?\s*{([^}]*)}"
        )
        function_pattern = r"(export\s+)?(async\s+)?(function\s+)?(\w+)\s*(\(.*?\))(?::\s*\w+)?\s*(?:=>|{)([^}]*)}?"
        interface_pattern = r"(export\s+)?interface\s+(\w+)\s*{([^}]*)}"

        parsed_data = []

        for class_match in re.finditer(class_pattern, source):
            class_name = class_match.group(3)
            class_body = class_match.group(4)
            methods = re.findall(
                r"((?:public|private|protected)?\s*(?:async\s+)?(?:static\s+)?)\s*(\w+)\s*(\(.*?\))(?::\s*\w+)?\s*{([^}]*)}",
                class_body,
            )
            parsed_data.append(
                {
                    "type": "class",
                    "name": class_name,
                    "methods": [
                        {
                            "type": "method",
                            "name": m[1],
                            "args": self._parse_args(m[2]),
                            "source": f"{m[0]}{m[1]}{m[2]}: return_type {{{m[3]}}}",
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
                    "name": func_match.group(4),
                    "args": self._parse_args(func_match.group(5)),
                    "source": func_match.group(0),
                }
            )

        for interface_match in re.finditer(interface_pattern, source):
            interface_name = interface_match.group(2)
            interface_body = interface_match.group(3)
            properties = re.findall(r"(\w+)\s*:\s*(\w+)", interface_body)
            parsed_data.append(
                {
                    "type": "interface",
                    "name": interface_name,
                    "properties": [
                        {"name": prop[0], "type": prop[1]} for prop in properties
                    ],
                    "source": interface_match.group(0),
                }
            )

        return parsed_data

    def _parse_args(self, args_string):
        args = args_string.strip("()").split(",")
        return [arg.strip() for arg in args if arg.strip()]
