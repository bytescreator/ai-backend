import logging
import threading
from signal import CTRL_C_EVENT

import sound
import speech.piper
from electron.messaging import handle_stdin, load_actions

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    load_actions()

    if not speech.piper.check_windows_exe():
        speech.piper.del_windows_exe()
        speech.piper.download_windows_release()

    process = speech.piper.process.start_piper_process()
    piper_pipe = threading.Thread(
        target=lambda: speech.piper.process.bind_audio_player(sound.write_output, process))
    piper_pipe.start()

    try:
        handle_stdin()
    except KeyboardInterrupt:
        logging.error("keyboard interrupt, exiting.")
    except Exception as e:
        logging.error(e)

    logging.info("waiting threads to terminate")
    sound.terminate()
    process.send_signal(CTRL_C_EVENT)
    try:
        process.wait(timeout=10)
    except KeyboardInterrupt:
        logging.info("subprocess responded to interrupt")
    except:
        logging.info("subprocess didn't repond to interrupt, terminating...")
        process.terminate()
        process.wait()
    piper_pipe.join()
    logging.info("all threads are terminated")
