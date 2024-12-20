from messaging import register_action, register_param_transformer


@register_action("gemini")
def f():
    pass

@register_param_transformer("gemini")
def transformer():
    pass