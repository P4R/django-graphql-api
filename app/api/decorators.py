from functools import wraps


def login_required_mutation(fn):
    @wraps(fn)
    def wrapper(cls, root, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Not logged in!')
        return fn(cls, root, info, **kwargs)
    return wrapper


def login_required_query(fn):
    @wraps(fn)
    def wrapper(root, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Not logged in!')
        return fn(root, info, **kwargs)
    return wrapper
