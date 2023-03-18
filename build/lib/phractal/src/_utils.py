import inspect

def _get_handy_context(func: callable) -> tuple[str, int, str]:
    """Grabs the filename, line number, and code-block in which a function is defined.
    
    Args:
        func - the function being interrogated.
    """
    filename = inspect.getfile(func)
    code, lineno = inspect.getsourcelines(func)
    context = "".join(code)

    return filename, lineno, context