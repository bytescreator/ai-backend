from messaging import (ActionError, Message, register_action,
                       register_param_transformer)
from speech.piper.process import WrappedSynth

@register_action("gemini")
def f():
    pass

@register_param_transformer("gemini")
def transformer():
    pass

@register_action("synth")
def synth(text: str):
    WrappedSynth.synth(text)

@register_param_transformer("synth")
def synth_transform(msg: Message):
    txt = msg.get("text")
    if txt is None:
        raise ActionError("no text given")
    return ((txt,), {})