from .messaging import ActionError, Message, register_param_transformer


@register_param_transformer("list_sound_devices")
def list_sound_output_devices(_: Message):
    return (tuple(), {})


@register_param_transformer("select_sound_input")
@register_param_transformer("select_sound_output")
def device_id_transformer(msg: Message):
    device_id = msg.get("sound_device")
    if device_id is None:
        raise ActionError("sound_device is missing from action")
    if not isinstance(device_id, int):
        raise ActionError("sound_device should be an integer")
    return ((device_id,), {})
