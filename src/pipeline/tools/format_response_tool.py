class FormatResponseTool:
    def run(self, context: dict) -> str:
        return self.format_context(context)

    def format_context(self, context: dict) -> str:
        if "error" in context:
            return f"Error: {context['error']}"

        result = context.get("result", [])
        if not result:
            return "No relevant data was found in the database."

        response = "Here is the detailed information:\n\n"
        for item in result:
            if isinstance(item, dict):
                response += "\n".join([f"{key.capitalize()}: {value}" for key, value in item.get('p', {}).items()])
            else:
                response += str(item)
            response += "\n\n"
        return response.strip()
