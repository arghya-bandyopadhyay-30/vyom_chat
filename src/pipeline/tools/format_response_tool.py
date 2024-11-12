class FormatResponseTool:
    def run(self, context: dict) -> str:
        return self.format_context(context)

    def format_context(self, context: dict) -> str:
        if "error" in context:
            return f"Error: {context['error']}"
        result = context.get("result", [])
        response = "Here is the detailed information:\n\n"
        for item in result:
            response += "\n".join([f"{key.capitalize()}: {value}" for key, value in item.items()])
            response += "\n\n"
        return response.strip()