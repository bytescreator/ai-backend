from typing import Any, Callable
import logging

# type declerations for clarity
Message = dict
CallParams = Any

class ActionError(Exception):
    pass

actions: dict[str,Callable[[Message], None]] = {}
param_transformers: dict[str, Callable[[Message], tuple[tuple, dict]]] = {}

def register_action(name: str):
    def tmp(f: Callable):
        if name in actions:
            raise ValueError("name already exists in actions")
        actions[name] = f
    return tmp

def register_param_transformer(name: str):
    def tmp(f: Callable[[Message], tuple[Any, Any]]):
        if name in param_transformers:
            raise ValueError("name already exists in transformers")
        param_transformers[name] = f
    return tmp

def validate_actions():
    for key in actions:
        if not key in param_transformers:
            raise RuntimeError(f"param transformer for {key} is not found")
    logging.info("all actions validated")
    logging.info(f"actions: {actions}")

def run_action(msg: Message):
    # this is validated by messaging
    # message contains id and action fields
    action = msg["action"]
    logging.debug(f"action {action} requested for msg id {msg['id']}")

    mapped_action = actions.get(action)
    if mapped_action is None:
        logging.debug(f"no action '{action}' found for msg id {msg['id']}")
        raise ActionError("unknown message action")
    logging.debug(f"action {action} is found for msg id {msg['id']}")
    transformer = param_transformers.get(action)
    logging.debug(f"action {action} transformer {transformer} is found for msg id {msg['id']}")
    transformed = transformer(msg)
    logging.debug(f"transformed params for msg id {msg['id']}: {transformed}")

    mapped_action(*transformed[0], **transformed[1])

# Exception thrown from handle_message
class MessageError(Exception):
    pass

def handle_message(msg: Message):
    '''
    loads the message and calls appropriate action.
    '''
    if not isinstance(msg, dict):
        logging.error("message is not a dict")
        raise MessageError("message root is not an object")

    id = msg.get("id")
    if id is None:
        logging.error("message does not contain id")
        raise MessageError("message root does not contain id")
    if not isinstance(id, int):
        logging.error("message id is not int")
        raise MessageError("message id is not int")

    logging.debug("message handled, action calling in progress...")
    run_action(msg)
