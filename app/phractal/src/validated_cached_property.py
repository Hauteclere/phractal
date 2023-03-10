from functools import cached_property
import inspect

_NOT_FOUND = object()

def _get_handy_context(func: callable) -> tuple[str, int, str]:
    """Grabs the filename, line number, and code-block in which a function is defined.
    
    Args:
        func - the function being interrogated.
    """
    filename = inspect.getfile(func)
    code, lineno = inspect.getsourcelines(func)
    context = "".join(code)

    return filename, lineno, context

class ValidatedCachedProperty(cached_property):
    """A decorator which turns a function into a property on a class which is cached and validated. 
    
    Validation is based on return type hints (type hints are compulsory).
    Does not currently support parameterised generics (ex: `list[int]` is not a valid type hint - use `list` instead) -> This is an open issue!
    Value is calculated and cached at first access.
    Subclassed from the inbuilt functools.cached_property.      
    """
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if self.attrname is None:
            raise TypeError(
                "Cannot use cached_property instance without calling __set_name__ on it.")
        try:
            cache = instance.__dict__
        except AttributeError:  # not all objects have __dict__ (e.g. class defines slots)
            msg = (
                f"No '__dict__' attribute on {type(instance).__name__!r} "
                f"instance to cache {self.attrname!r} property."
            )
            raise TypeError(msg) from None
        val = cache.get(self.attrname, _NOT_FOUND)
        if val is _NOT_FOUND:
            with self.lock:
                # check if another thread filled cache while we awaited lock
                val = cache.get(self.attrname, _NOT_FOUND)
                if val is _NOT_FOUND:
                    val = self.func(instance)
                    try:
                        cache[self.attrname] = val
                    except TypeError:
                        msg = (
                            f"The '__dict__' attribute on {type(instance).__name__!r} instance "
                            f"does not support item assignment for caching {self.attrname!r} property."
                        )
                        raise TypeError(msg) from None
                    
        if not 'return' in self.func.__annotations__:
            filename, lineno, context = _get_handy_context(self.func)
            raise ValueError(f"No type hint supplied for ValidatedCachedProperty {self.attrname}. Context: \n {filename} ({lineno}): \n {context}")
        if not isinstance(val, self.func.__annotations__['return']):
            filename, lineno, context = _get_handy_context(self.func)
            raise ValueError(f"ValidatedCachedProperty {self.attrname} returned a value that did not match its type hint. Hinted type: {self.func.__annotations__['return']}. Returned type: {type(val)}.Context: \n {filename} ({lineno}): \n {context}")
        return val
    