def handle_operation(func, context=None):
    try:
        return func()
    except Exception as e:
        return {"error": f"Operation failed: {str(e)}"}