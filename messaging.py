from typing import Any, Callable, number

# type declerations for clarity
Message = Any
CallParams = Any

class ActionError(Exception):
    pass

actions: dict[str,Callable[[Message], None]] = {}
param_transformers: dict[str, Callable[[Message], (tuple, dict)]] = {}

def register_action(name: str):
    def tmp(f: Callable):
        if name in actions:
            raise ValueError("name already exists in actions")
        actions[name] = f
    return tmp

def register_param_transformer(name: str):
    def tmp(f: Callable[[Message], Any]):
        if name in param_transformers:
            raise ValueError("name already exists in transformers")
        param_transformers[name] = f
    return tmp

def run_action(msg: Message):
    # this is validated by messaging
    # message contains id and action fields
    action = msg["action"]

    mapped_action = actions.get(action)
    if mapped_action is None:
        raise ActionError("unknown message action")
    transformer = param_transformers.get(map)
    transformed = transformer(msg)
    mapped_action(*transformed[0], **transformed[1])


# Exception thrown from handle_message
class MessageError(Exception):
    pass

'''
loads the message and calls appropriate action.
'''
def handle_message(msg: Message):
    if not isinstance(msg, dict):
        raise MessageError("message root is not an object")

    id = msg.get("id")
    if id is None:
        raise MessageError("message root does not contain id")
    if not isinstance(id, int):
        raise MessageError("message id is not int")

    run_action(msg)
