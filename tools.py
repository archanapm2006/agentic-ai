# agent_app/tools.py

import math

def calculate(expression: str) -> str:
    """
    Evaluates a mathematical expression safely using Python's math library.
    """
    try:
        # Build a clean safe dictionary containing math functions
        safe_dict = {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "pow": pow,
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "pi": math.pi,
            "e": math.e,
            "math": math
        }
        
        # Strip out any markdown or trailing spaces
        clean_expr = expression.strip().strip("`")
        
        # Execute in restricted global context
        result = eval(clean_expr, {"__builtins__": None}, safe_dict)
        return str(result)
    except Exception as e:
        return f"Error executing calculation: {str(e)}"