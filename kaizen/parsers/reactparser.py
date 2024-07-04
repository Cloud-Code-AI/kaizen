import re


class ReactParser:
    def parse(self, source):
        self.source = source
        component_pattern = r"(class|function)\s+(\w+).*?{([^}]*)}"

        parsed_data = []

        for comp_match in re.finditer(component_pattern, source):
            comp_type = comp_match.group(1)
            comp_name = comp_match.group(2)
            comp_body = comp_match.group(3)

            if comp_type == "class":
                methods = re.findall(r"(\w+)\s*\((.*?)\)\s*{([^}]*)}", comp_body)
                parsed_data.append(
                    {
                        "type": "class",
                        "name": comp_name,
                        "methods": [
                            {
                                "type": "function",
                                "name": m[0],
                                "args": m[1].split(","),
                                "source": f"{m[0]}({m[1]}) {{{m[2]}}}",
                            }
                            for m in methods
                        ],
                        "source": comp_match.group(0),
                    }
                )
            else:
                parsed_data.append(
                    {
                        "type": "function",
                        "name": comp_name,
                        "args": [],
                        "source": comp_match.group(0),
                    }
                )

        return parsed_data
