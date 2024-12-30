import logging
import threading

import pyaudio

__audio = pyaudio.PyAudio()
__output_lock = threading.Lock()
__input_lock = threading.Lock()
__output: pyaudio.Stream = __audio.open(
    rate=16000,
    channels=1, format=pyaudio.paFloat32, output=True)
__input: pyaudio.Stream = __audio.open(
    rate=16000,
    channels=1, format=pyaudio.paFloat32, input=True)


def terminate():
    __audio.terminate()


def dump_devices():
    logging.debug("dumping sound devices")
    output = {}
    wasapi = __audio.get_host_api_info_by_type(13)  # WASAPI
    output["default_input"] = wasapi.get("defaultInputDevice")
    output["default_output"] = wasapi.get("defaultOutputDevice")
    devices = []
    for index in range(wasapi["deviceCount"]):
        device_info = __audio.get_device_info_by_host_api_device_index(
            host_api_index=wasapi["index"], host_api_device_index=index
        )
        devices.append(device_info)
    output["devices"] = devices
    logging.debug(f"sound devices dumped as {output}")
    return output


def select_output_device(id: int):
    logging.info(f"requested output device change to {id}")
    global __output
    with __output_lock:
        device_info = __audio.get_device_info_by_index(id)
        if device_info["maxOutputChannels"] == 0:
            raise Exception("device does not have any output")
        new_output = __audio.open(
            rate=22500,
            channels=1,
            output=True,
            input_device_index=id,
            format=pyaudio.paInt16,
        )
        if __output != None:
            __output.close()
        __output = new_output
    logging.info(f"output device changed to {id}")


def select_input_device(id: int):
    logging.info(f"requested input device change to {id}")
    global __input
    with __input_lock:
        device_info = __audio.get_device_info_by_index(id)
        if device_info["maxInputChannels"] == 0:
            raise Exception("device does not have any input")
        new_input = __audio.open(
            rate=16000,
            channels=1,
            input=True,
            output=False,
            input_device_index=id,
            format=pyaudio.paFloat32,
        )
        if __input != None:
            __input.close()
        __input = new_input
    logging.info(f"input device changed to {id}")


def read_input(num_frames: int, exception_on_overflow: bool = False):
    with __input_lock:
        return __input.read(num_frames, exception_on_overflow=exception_on_overflow)


def write_output(frames: bytes, num_frames: int = None, exception_on_underflow: bool = False):
    with __output_lock:
        __output.write(frames, num_frames=num_frames,
                       exception_on_underflow=exception_on_underflow)
