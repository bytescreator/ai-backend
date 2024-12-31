import logging
import mmap
from os import SEEK_SET

import gemini
import numpy as np
import sound
import torch
import whisper
from silero_vad import VADIterator, load_silero_vad

from .messaging import json_dump, register_action

# from speech.piper.process import WrappedSynth

vad_model = load_silero_vad(onnx=True)
vad_iter = VADIterator(model=vad_model, sampling_rate=16000)
stt_model = whisper.load_model("base")
MMAP_SIZE = 16000*4*1*30
m = mmap.mmap(-1, MMAP_SIZE)


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
def submit_text(text: str, speak: bool):
    gemini.send_text(text, speak)


@register_action("new-session")
def new_session():
    gemini.new_session()


@register_action("rewind-session")
def rewind_session():
    gemini.rewind_session()


@register_action("toggle-listen")
def toggle_listen():
    json_dump({"action": "listening-armed"})

    m.seek(0, SEEK_SET)
    size = 0
    silence_cnt = 0
    while len(chunk := sound.read_input(512)) > 0:
        buf = np.frombuffer(chunk, dtype=np.float32)
        tensor = torch.Tensor(buf)
        d = vad_model(tensor, 16000).item()

        # whisper cannot handle chopped audio, it spits out utter garbage
        m.write(chunk)
        size += len(chunk)
        if size >= MMAP_SIZE:
            logging.info(
                "listening buffer filled up, passing to transcribe")
            break

        if d > 0.6:
            silence_cnt = 0
        else:
            silence_cnt += 1
            if silence_cnt > 50:
                logging.info(
                    "silence threshold exceeded, passing to transcribe")
                break

    vad_iter.reset_states()
    transcribe_aud = np.frombuffer(m[:size], dtype=np.float32)
    tr = stt_model.transcribe(
        transcribe_aud, language="tr", word_timestamps=True, hallucination_silence_threshold=0.3)
    json_dump({"action": "transcript-ready",
              "transcript": "".join(tr.get("text"))})
