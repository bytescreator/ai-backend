from .messaging import ActionError, Message, register_param_transformer


@register_param_transformer("list-sound-devices")
@register_param_transformer("new-session")
@register_param_transformer("rewind-session")
@register_param_transformer("toggle-listen")
def no_input_transformer(_: Message):
    return (tuple(), {})


@register_param_transformer("select-sound-input")
@register_param_transformer("select-sound-output")
def device_id_transformer(msg: Message):
    device_id = msg.get("sound_device")
    if device_id is None:
        raise ActionError("sound_device is missing from action")
    if not isinstance(device_id, int):
        raise ActionError("sound_device should be an integer")
    return ((device_id,), {})


@register_param_transformer("submit-text")
def submit_text_transformer(msg: Message):
    text = msg.get("text")
    speak = msg.get("speak")
    if text is None:
        raise ActionError("text is missing from action")
    if speak is None:
        speak = False
    else:
        if not isinstance(text, bool):
            raise ActionError("speak is not bool")
    if not isinstance(text, str):
        raise ActionError("text is not string")
    return ((text, speak), {})
