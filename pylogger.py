import os
from inspect import currentframe
from time import strftime
from types import FrameType  # using for pylint
from typing import Union  # using for pylint
from rich.console import Console
console = Console()
class Logger_InternalError(SyntaxError):pass
loggers:dict[str,dict] = {
    "message": {
        "fore_color": "rgb(0, 255, 255)",
        "back_color": '',
        "extend_settings": "",
        "available": True,
    },
    "info": {
        "fore_color": "rgb(0, 255, 0)",
        "back_color": '',
        "extend_settings": "",
        "available": True,
    },
    "warning": {
        "fore_color": "rgb(255, 255, 0)",
        "back_color": '',
        "extend_settings": "",
        "available": True,
    },
    "error": {
        "fore_color": "rgb(255, 0, 0)",
        "back_color": '',
        "extend_settings": "",
        "available": True,
    },
    "final": {
        "fore_color": "rgb(255, 0, 0)",
        "back_color": "rgb(255, 255, 0)",
        "extend_settings": "bold",
        "available": True,
    },
    "off": {
        "fore_color": "rgb(100, 100, 100)",
        "back_color": '',
        "extend_settings": "",
        "available": True,
    },
}
def message(_string:str,*,no_print:bool=False,auto_highlight:bool=False) -> None:raise Logger_InternalError
def info(_string:str,*,no_print:bool=False,auto_highlight:bool=False) -> None:raise Logger_InternalError
def warning(_string:str,*,no_print:bool=False,auto_highlight:bool=False) -> None:raise Logger_InternalError
def error(_string:str,*,no_print:bool=False,auto_highlight:bool=False) -> None:raise Logger_InternalError
def final(_string:str,*,no_print:bool=False,auto_highlight:bool=False) -> None:raise Logger_InternalError
def off(_string:str,*,no_print:bool=False,auto_highlight:bool=False) -> None:raise Logger_InternalError

for mode in loggers:
    exec(f"def {mode}(_string:str,*,no_print:bool=False,auto_highlight:bool=False):log(__logMode(),_string,no_print=no_print,auto_highlight=auto_highlight)")
if not os.path.exists("logs"):
    os.mkdir("logs")
minLength = 0
update_LOCK = False


def __logMode() -> str:
    return currentframe().f_back.f_code.co_name #type:ignore[union-attr]



def __save():
    global update_LOCK,loggers
    while update_LOCK:
        pass
    update_LOCK = True
    logger_extensions = f"class Logger_InternalError(SyntaxError):pass\n{loggers}\n\n"
    for mode in loggers:
        logger_extensions += f"def {mode}(_string:str,*,no_print:bool=False,auto_highlight:bool=False):raise Logger_InternalError"
        logger_extensions += "\n"
    with open("./logger_extensions.py",'w') as f:
        f.write(logger_extensions)
    update_LOCK = False


def changeStatus(changes: Union[dict, None] = None, save: bool = False, **kwargs: bool):
    __all_changes = dict(changes , **kwargs) if changes else kwargs
    for log_mode, new_status in __all_changes.items():
        loggers[log_mode]["available"] = new_status
    if save:
        __save()
    return


def setNewMinLength(new_MinLength: int) -> None:
    global minLength
    minLength = new_MinLength
    return


def __name():
    global loggers
    using: FrameType = currentframe().f_back.f_back # type:ignore[union-attr,assignment]
    if using.f_code.co_name in loggers:
        using = using.f_back # type:ignore[assignment]
    filename = os.path.basename(using.f_code.co_filename)
    func_name = using.f_code.co_name
    line = using.f_lineno
    return f"<{func_name}> in {filename},line {line}"


def __writeIn(_string: str):
    try:
        with open("./logs/"+strftime("%Y-%m-%d")+".log", "a", encoding="utf-8") as f:
            f.write(_string)
    except:
        with open("./logs/"+strftime("%Y-%m-%d")+".log", "x", encoding="utf-8") as f:
            f.write(_string)


def create(name: str, fore_color: str = "rgb(255, 255, 255)", back_color: str | None = None, available: bool = True, *, save: bool = False):
    global loggers
    loggers[name] = {
        "fore_color": fore_color,
        "back_color": back_color,
        "available": available
    }
    if save:
        __save()
    return


def log(mode: str, _string: str, *, no_print=False, auto_highlight: bool = False):
    global loggers, minLength
    if loggers[mode]["available"]:
        writeIn_log_mode = mode.upper()+" "*(minLength-len(mode))
        time = strftime("%H:%M:%S")
        value = f"{time} [{writeIn_log_mode}] {__name()}: {_string}"
        __writeIn(value)
        if no_print == False:
            fore_color:str =loggers[mode]['fore_color'].replace(' ','')
            back_color:str = loggers[mode]['back_color'].replace(' ','')
            extend_settings:str = loggers[mode]['extend_settings']
            console.print(
                value,
                highlight=auto_highlight,
                style=f"{fore_color} on {back_color} {extend_settings}" if back_color 
                else f"{fore_color} {extend_settings}",
            )

def logCleaner(logNum:int):
    logs = os.listdir('./logs')[::-1]
    while len(logs) > logNum:
        os.remove(logs.pop())

def init(logNum:int = 30,minLength:int = 7) -> None:
    logCleaner(logNum)
    setNewMinLength(minLength)
    return