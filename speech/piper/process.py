import json
import logging
import subprocess


class WrappedSynth:
    process: subprocess.Popen = None

    def synth(text: str) -> None:
        logging.debug(f"WrappedSynth.synth is called with {text}")
        WrappedSynth.process.stdin.write(
            b'{"text": '+json.dumps(text).encode("utf-8")+b'}\n')
        WrappedSynth.process.stdin.flush()
        logging.debug(f"stdin write done")


def start_piper_process() -> subprocess.Popen:
    process = subprocess.Popen([
        "speech/piper_exe/piper/piper.exe",
        "--model",
        "speech/synth_model/tr_TR-fahrettin-medium.onnx",
        "--config",
        "speech/synth_model/tr_TR-fahrettin-medium.onnx.json",
        "--output_raw",
        "--json-input",
        "--debug",  # debug flag
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    if WrappedSynth.process is not None:
        WrappedSynth.process.terminate()
    WrappedSynth.process = process
    return process


def bind_audio_player(writer: callable, process: subprocess.Popen):
    logging.info("listening stdout of piper process")
    while len(chunk := process.stdout.read(512)) != 0:
        # logging.debug(f"received audio chunk of size {len(chunk)}")
        writer(chunk)
    logging.info("player process exit")
