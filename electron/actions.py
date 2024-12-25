import sound

from .messaging import register_action

# from speech.piper.process import WrappedSynth


@register_action("list_sound_devices")
def list_sound_output_devices():
    return sound.dump_devices()


@register_action("select_sound_output")
def select_sound_output(device_id: int):
    return sound.select_output_device(device_id)


@register_action("select_sound_input")
def select_sound_input(device_id: int):
    return sound.select_input_device(device_id)
