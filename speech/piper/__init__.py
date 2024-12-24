# this module is for managing the piper subprocess

from urllib.request import urlopen
from io import BytesIO
import os
import zipfile
import shutil
import logging
import hashlib

from . import process

def download_windows_release():
    '''downloads the windows release from github'''
    logging.info("downloading piper windows release...")
    with urlopen("https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_windows_amd64.zip") as response:
        logging.info("downloading piper windows release is completed.")
        v = response.read()
        logging.info("extracting piper windows release...")
        with zipfile.ZipFile(BytesIO(v)) as z:
            z.extractall("speech/piper_exe/")
        logging.info("extracted piper release")

    if not os.path.exists("speech/synth_model"):
        os.mkdir("speech/synth_model")

    logging.info("downloading voice model...")
    with urlopen("https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/tr/tr_TR/fahrettin/medium/tr_TR-fahrettin-medium.onnx?download=true") as modelcfg:
        logging.info("voice model downloaded")
        with open("speech/synth_model/tr_TR-fahrettin-medium.onnx", "wb") as model:
            shutil.copyfileobj(modelcfg, model)
        logging.debug("voice model written")

    logging.info("downloading voice model config...")
    with urlopen("https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/tr/tr_TR/fahrettin/medium/tr_TR-fahrettin-medium.onnx.json?download=true.json") as modelcfg:
        logging.info("voice model config downloaded")
        with open("speech/synth_model/tr_TR-fahrettin-medium.onnx.json", "wb") as model:
            shutil.copyfileobj(modelcfg, model)
        logging.debug("voice model config written")

    if not check_windows_exe():
        raise RuntimeError("failed to match checksums of new download")

def check_windows_exe() -> bool:
    '''checks windows executable of piper exists'''
    exists = os.path.exists("speech/piper_exe")
    logging.debug(f"piper exists: {exists}")
    if not exists:
        return False

    logging.debug("checking piper checksums")
    with open("speech/piper/chk.sum", "r") as sumfile:
        for line in sumfile:
            fsp = line.find(" ")
            line = (line[:fsp], line[fsp+1:])
            sum, path = line[0], line[1][:-1]
            logging.debug(f"checking file {path}")
            try:
                with open(os.path.join("speech/", path), "rb") as f:
                    h = hashlib.sha256(b"")
                    while (chunk := f.read(1024)) != b'':
                        h.update(chunk)
                    if h.hexdigest() != sum:
                        logging.error(f"{path}: FAILED")
                        return False
            except FileNotFoundError:
                logging.error(f"{path}: NOT FOUND")
                return False
            logging.debug(f"{path}: OK")

    logging.info("piper checksum is validated")
    return True

def del_windows_exe():
    '''deletes executable from path if exists'''
    if os.path.exists("speech/piper_exe"):
        logging.debug("deleting piper_exe")
        shutil.rmtree("speech/piper_exe")
    else:
        logging.debug("piper_exe is missing, skipping delete.")

    if os.path.exists("speech/synth_model"):
        logging.debug("deleting synth_model")
        shutil.rmtree("speech/synth_model")
    else:
        logging.debug("synth_model is missing, skipping delete.")
