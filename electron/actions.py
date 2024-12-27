import gemini
import sound

from .messaging import json_dump, register_action

# from speech.piper.process import WrappedSynth


@register_action("list-sound-devices")
def list_sound_output_devices():
    json_dump({"action": "sound-devices-list",
              "devices": sound.dump_devices()})


@register_action("select-sound-output")
def select_sound_output(device_id: int):
    try:
        sound.select_output_device(device_id)
        json_dump({"action": "selected-sound-output",
                  "ok": True, "device": device_id})
    except:
        json_dump({"action": "selected-sound-output", "ok": False})


@register_action("select-sound-input")
def select_sound_input(device_id: int):
    try:
        sound.select_input_device(device_id)
        json_dump({"action": "selected-sound-input",
                  "ok": True, "device": device_id})
    except:
        json_dump({"action": "selected-sound-input", "ok": False})


@register_action("submit-text")
def submit_text(text: str):
    gemini.send_text(text, False)


@register_action("new-session")
def new_session():
    gemini.new_session()


@register_action("rewind-session")
def rewind_session():
    gemini.rewind_session()


@register_action("toggle-listen")
def toggle_listen(status: bool):
    pass
