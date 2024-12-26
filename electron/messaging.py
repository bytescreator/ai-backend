import json
import logging
import sys
import threading
from typing import Any, Callable

stdout_lock = threading.Lock()


def json_dump(obj):
    with stdout_lock:
        json.dump(obj, sys.stdout)
        print()


# type declerations for clarity
Message = dict
CallParams = Any


class ActionError(Exception):
    pass

# Exception thrown from handle_message


class MessageError(Exception):
    pass


_actions: dict[str, Callable[[Message], dict | None]] = {}
_param_transformers: dict[str, Callable[[Message], tuple[tuple, dict]]] = {}


def register_action(name: str):
    def tmp(f: Callable):
        if name in _actions:
            raise ValueError("name already exists in actions")
        _actions[name] = f
    return tmp


def register_param_transformer(name: str):
    def tmp(f: Callable[[Message], tuple[Any, Any]]):
        if name in _param_transformers:
            raise ValueError("name already exists in transformers")
        _param_transformers[name] = f
        return f
    return tmp


def load_actions():
    import electron.actions
    import electron.transformers

    for key in _actions:
        if not key in _param_transformers:
            raise RuntimeError(f"param transformer for {key} is not found")
    logging.info("all actions validated")
    logging.info(f"actions: {_actions}")


def run_action(msg: Message):
    # this is validated by messaging
    # message contains id and action fields
    action = msg["action"]
    logging.debug(f"action {action} requested")

    mapped_action = _actions.get(action)
    if mapped_action is None:
        logging.debug(f"no action '{action}' found")
        raise ActionError("unknown message action")
    logging.debug(f"action {action} is found")
    transformer = _param_transformers.get(action)
    logging.debug(
        f"action {action} transformer {transformer} is found")
    transformed = transformer(msg)
    logging.debug(f"transformed params: {transformed}")

    mapped_action(*transformed[0], **transformed[1])


def handle_message(msg: Message):
    '''
    loads the message and calls appropriate action.
    '''
    if not isinstance(msg, dict):
        logging.error("message is not a dict")
        raise MessageError("message root is not an object")

    logging.debug("message handled, action calling in progress...")
    run_action(msg)


def handle_stdin():
    '''
    Parses messages from stdin. Messages are formatted as newline delimited json
    messages. An empty line stops the handler causing the program to exit normally
    '''
    logging.info("reading stdin started")
    while True:
        try:
            rd = input()
            logging.debug(f"got new line from stdin {rd}")
            if rd == "":
                return
            msg = json.loads(rd)

        except json.decoder.JSONDecodeError:
            logging.fatal(f"invalid message received")
            return

        logging.debug(f"received message {msg}")
        handle_message(msg)
