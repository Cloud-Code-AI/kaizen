import re


class RustParser:
    def __init__(self):
        self.source = ""

    def parse(self, source):
        self.source = source
        struct_pattern = r"struct\s+(\w+)\s*{([^}]*)}"
        enum_pattern = r"enum\s+(\w+)\s*{([^}]*)}"
        function_pattern = r"(async\s+)?fn\s+(\w+)\s*\((.*?)\)\s*{([^}]*)}"
        impl_pattern = r"impl\s*(\w+)\s*{([^}]*)}"
        mod_pattern = r"mod\s+(\w+)\s*{([^}]*)}"
        use_pattern = r"use\s+(.*?);"
        const_pattern = r"const\s+(\w+)\s*:\s*(\w+)\s*=\s*([^;]+);"
        static_pattern = r"static\s+(\w+)\s*:\s*(\w+)\s*=\s*([^;]+);"

        parsed_data = []

        imports = re.findall(use_pattern, source)
        consts = re.findall(const_pattern, source)
        statics = re.findall(static_pattern, source)
        global_vars = consts + statics

        for mod_match in re.finditer(mod_pattern, source):
            mod_name = mod_match.group(1)
            mod_body = mod_match.group(2)
            parsed_data.append(
                {
                    "type": "module",
                    "name": mod_name,
                    "contents": mod_body,
                    "source": mod_match.group(0),
                    "imports": imports,
                    "global_vars": global_vars,
                }
            )

        for struct_match in re.finditer(struct_pattern, source):
            struct_name = struct_match.group(1)
            struct_body = struct_match.group(2)
            fields = [
                field.strip() for field in struct_body.split(";") if field.strip()
            ]
            parsed_data.append(
                {
                    "type": "struct",
                    "name": struct_name,
                    "fields": fields,
                    "source": struct_match.group(0),
                    "imports": imports,
                    "global_vars": global_vars,
                }
            )

        for enum_match in re.finditer(enum_pattern, source):
            enum_name = enum_match.group(1)
            enum_body = enum_match.group(2)
            variants = [
                variant.strip() for variant in enum_body.split(",") if variant.strip()
            ]
            parsed_data.append(
                {
                    "type": "enum",
                    "name": enum_name,
                    "variants": variants,
                    "source": enum_match.group(0),
                    "imports": imports,
                    "global_vars": global_vars,
                }
            )

        for func_match in re.finditer(function_pattern, source):
            async_keyword = func_match.group(1)
            parsed_data.append(
                {
                    "type": "function",
                    "async": bool(async_keyword),
                    "name": func_match.group(2),
                    "args": func_match.group(3).split(","),
                    "body": func_match.group(4).strip(),
                    "source": f"{async_keyword or ''}fn {func_match.group(2)}({func_match.group(3)}) {{{func_match.group(4)}}}",
                    "imports": imports,
                    "global_vars": global_vars,
                }
            )

        for impl_match in re.finditer(impl_pattern, source):
            impl_name = impl_match.group(1)
            impl_body = impl_match.group(2)
            methods = re.findall(
                r"(async\s+)?fn\s+(\w+)\s*\((.*?)\)\s*{([^}]*)}", impl_body
            )
            parsed_data.append(
                {
                    "type": "impl",
                    "for": impl_name,
                    "methods": [
                        {
                            "type": "function",
                            "async": bool(m[0]),
                            "name": m[1],
                            "args": m[2].split(","),
                            "body": m[3].strip(),
                            "source": f"{m[0] or ''}fn {m[1]}({m[2]}) {{{m[3]}}}",
                            "imports": imports,
                            "global_vars": global_vars,
                        }
                        for m in methods
                    ],
                    "source": impl_match.group(0),
                    "imports": imports,
                    "global_vars": global_vars,
                }
            )

        return parsed_data
