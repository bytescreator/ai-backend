"""
this file defines system audit function for gemini
"""

import logging

import psutil


# TODO: parcalanacak bu cok yavas pid, status falan bolunecek
# TODO: ayrica cachelemek iyi olabilir
def invokable_get_all_processes():
    """
    Gets all processes in current running system.
    Gets all processes cpu and memory information. Can be used to list processes
    by cpu usage or memory usage.

    Returns:
    list[dict]: all processes with supplementary info as name, exe, cwd, status, create_time, cpu_times, cpu_percent, memory_info
    """

    logging.debug("get_all_processes called")

    output = []

    for process in psutil.process_iter():
        try:
            output.append(
                {
                    "pid": process.pid,
                    "name": process.name(),
                    "exe": process.exe(),
                    "cwd": process.cwd(),
                    "status": process.status(),
                    "create_time": process.create_time(),
                    "cpu_times": process.cpu_times(),
                    "cpu_percent": process.cpu_percent(),
                    "memory_info": process.memory_info(),
                }
            )
        except:
            logging.error(
                f"failed to get information of process {process.pid}")
            pass

    logging.debug(f"get_all_processes done, output: {output}")
    return output


def invokable_get_current_cpu_percentage():
    """
    Gets current cpu usage of the system

    Returns:
    float: current cpu usage of the system
    """
    cpu_percent = psutil.cpu_percent()
    logging.debug(f"get_current_cpu_percentage returned {cpu_percent}")
    return cpu_percent


def invokable_get_current_mem_usage():
    """
    Gets current mem usage of the system

    Returns:
    float: current memory stats of the system e.g.
        total is the system's total memory
        available is the current usable memory including freeable buffers
        percent is the total's percantage
        used is the memory currently in use
        free is the actually free memory directly usable by the system

        all units are in kilobytes
    """

    output = {"virtual_memory": psutil.virtual_memory(
    ), "swap_memory": psutil.swap_memory()}
    logging.debug(f"get_current_mem_usage called returned {output}")
    return output
