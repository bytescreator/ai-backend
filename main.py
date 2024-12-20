import json
import logging
import sys

from messaging import handle_message

'''
Parses messages from stdin. Messages are formatted as newline delimited json
messages. An empty line stops the handler causing the program to exit normally
'''
def handle_stdin():
    while True:
        try:
            rd = sys.stdin.readline()[:-1]
            if rd=="":
                return
            msg = json.loads(rd)

        except json.decoder.JSONDecodeError:
            logging.fatal(f"invalid message received")
            # TODO: emit invalid message
            continue

        logging.debug(f"received message {msg}")

        handle_message(msg)

if __name__ == "__main__":
    handle_stdin()
