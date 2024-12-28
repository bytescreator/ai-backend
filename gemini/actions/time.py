import time


def invokable_get_time():
    """
    returns current system time in %H:%M:%S %d/%m/%y format

    Returns:
    str: current time in %H:%M:%S %d/%m/%y format
    """

    return time.strftime("%H:%M:%S %d/%m/%y %A")
