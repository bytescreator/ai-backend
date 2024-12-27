from . import weather


def extract_functions(x):
    return [getattr(x, name) for name in dir(x) if name.startswith("invokable_")]


action_list = [
    extract_functions(weather),
]
