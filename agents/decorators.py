# agents/decorators.py

def tool(name: str, description: str):
    def decorator(func):
        func.tool_name = name
        func.description = description
        return func
    return decorator
