import os
import json
from datetime import datetime


# Turns VT output support on
def enable_vt_support():
    if os.name == "nt":
        import ctypes

        hOut = ctypes.windll.kernel32.GetStdHandle(-11)
        out_modes = ctypes.c_uint32()
        ENABLE_VT_PROCESSING = ctypes.c_uint32(0x0004)
        # ctypes.addressof()
        ctypes.windll.kernel32.GetConsoleMode(hOut, ctypes.byref(out_modes))
        out_modes = ctypes.c_uint32(out_modes.value | 0x0004)
        ctypes.windll.kernel32.SetConsoleMode(hOut, out_modes)


def datetime_to_string(dt):
    # type: (datetime.datetime) -> str
    return (dt.isoformat() + "Z") if dt is not None else None


def datetime_from_string(s):
    # type: (str) -> datetime.datetime
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ") if s is not None else None
