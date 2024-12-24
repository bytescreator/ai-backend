import json
import logging
import sys

# imported for side effects
import actions
import speech.piper
from messaging import handle_message, validate_actions


def handle_stdin():
    '''
    Parses messages from stdin. Messages are formatted as newline delimited json
    messages. An empty line stops the handler causing the program to exit normally
    '''
    logging.info("reading stdin started")
    while True:
        try:
            rd = sys.stdin.readline()[:-1]
            logging.debug(f"got new line from stdin {rd}")
            if rd=="":
                return
            msg = json.loads(rd)

        except json.decoder.JSONDecodeError:
            logging.fatal(f"invalid message received")
            return

        logging.debug(f"received message {msg}")

        handle_message(msg)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    validate_actions()

    if not speech.piper.check_windows_exe():
        speech.piper.del_windows_exe()
        speech.piper.download_windows_release()

    process, thread = speech.piper.process.start_piper_process()
    speech.piper.process.wrap_process_stdin(process)

    try:
        handle_stdin()
    finally:
        logging.info("waiting threads to terminate")
        process.terminate()
        process.wait()
        thread.join()
        logging.info("all threads are terminated")
