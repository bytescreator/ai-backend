import subprocess
import pyaudio
import threading
import logging
import json

class WrappedSynth:
    process: subprocess.Popen = None

    def synth(text: str) -> None:
        logging.debug(f"WrappedSynth.synth is called with {text}")
        WrappedSynth.process.stdin.write(b'{"text": '+json.dumps(text).encode("utf-8")+b'}\n')
        WrappedSynth.process.stdin.flush()
        logging.debug(f"stdin write done")

def start_piper_process() -> tuple[subprocess.Popen, threading.Thread]:
    process = subprocess.Popen([
        "speech/piper_exe/piper/piper.exe",
        "--model",
        "speech/synth_model/tr_TR-fahrettin-medium.onnx",
        "--config",
        "speech/synth_model/tr_TR-fahrettin-medium.onnx.json",
        "--output_raw",
        "--json-input",
        "--debug", # debug flag
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    thread = threading.Thread(None, lambda: audio_player_thread(process))
    thread.start()
    return (process, thread)

def wrap_process_stdin(process: subprocess.Popen):
    if WrappedSynth.process != None:
        raise RuntimeError("synth set twice")
    WrappedSynth.process = process

def audio_player_thread(process: subprocess.Popen):
    logging.info("starting player thread")
    p = pyaudio.PyAudio()
    stream = p.open(rate=22050, channels=1, output=True, format=pyaudio.paInt16)
    logging.info("audio stream opened, listening stdout of piper process")
    while len(chunk:=process.stdout.read(512)) != 0:
        # logging.debug(f"received audio chunk of size {len(chunk)}")
        stream.write(chunk)
    logging.info("player process exit")
    stream.stop_stream()
    stream.close()
    p.terminate()
    logging.info("player terminated")
