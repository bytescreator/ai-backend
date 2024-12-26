from .messaging import ActionError, Message, register_param_transformer


@register_param_transformer("list-sound-devices")
def list_sound_output_devices(_: Message):
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
    if text is None:
        raise ActionError("text is missing from action")
    if not isinstance(text, str):
        raise ActionError("text is not string")
    return ((text,), {})


@register_param_transformer("toggle-listen")
def toggle_listen(msg: Message):
    status = msg.get("status")
    if status is None:
        raise ActionError("status is missing from action")
    return ((status,), {})
