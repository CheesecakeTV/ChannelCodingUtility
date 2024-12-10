import FreeSimpleGUI as sg
import numpy as np

import Calculations as calc
from functools import partial

# Main layout
# Start here if you are running as a python script

def layout_oneLine(text:str,key:str,in_size:int=22,default_text:str|float="",enable_events:bool=False) -> list[sg.Element]:
    """
    One standard input line for the layout
    :param enable_events: If the input element should throw an event
    :param default_text: Default text for the input element
    :param in_size: Size of the input element
    :param text:
    :param key:
    :return:
    """
    return [
        sg.T(
            text,
            size=(20,0),
        ),
        sg.In(
            key=key,
            size=(in_size,0),
            default_text=default_text,
            enable_events=enable_events,
        )
    ]


def convert(x:any,default:any,to_type:"type|callable") -> any:
    """
    Tries to convert x to to_type.
    If that doesn't work, returns default
    :param x:
    :param default:
    :param to_type:
    :return:
    """
    try:
        return to_type(x)
    except ValueError:
        return default

to_int = partial(convert,to_type = int)
to_float = partial(convert,to_type = float)

def call_multiple(*calls,args=tuple()):
    """
    Calls multiple functions
    :param args: Arguments passed to every function
    :param calls:
    :return:
    """
    for i in calls:
        i(*args)

def layout_numberButtons(key:str,to_type:type=float,additional_call:"callable"=None) -> list[sg.Element]:
    """
    Returns standard numberButtons to refer to 'key'.
    Only for main Window!
    :param additional_call: Will be added to the key so it is also called
    :param to_type: Type the value should be converted to
    :param key: key of the corresponding sg.Input
    :return: Layout-Row
    """
    if not additional_call:
        additional_call = lambda *_:0

    return [
        sg.Button(
            "* 2",
            key=(
                lambda w,e,v:w[key](convert(v[key],0,to_type=to_type) * 2),
                additional_call
            )
        ),
        sg.Button(
            "/ 2",
            key=(
                lambda w,e,v:w[key](convert(v[key],0,to_type=to_type) / 2),
                additional_call
            )
        ),
        sg.Button(
            "* 10",
            key=(
                lambda w,e,v:w[key](convert(v[key],0,to_type=to_type) * 10),
                additional_call
            )
        ),
        sg.Button(
            "/ 10",
            key=(
                lambda w,e,v:w[key](convert(v[key],0,to_type=to_type) / 10),
                additional_call
            )
        ),
        sg.Button(
            "+ 1",
            key=(
                lambda w,e,v:w[key](convert(v[key],0,to_type=to_type) + 1),
                additional_call
            )
        ),
        sg.Button(
            "- 1",
            key=(
                lambda w,e,v:w[key](convert(v[key],0,to_type=to_type) - 1),
                additional_call
            )
        ),
    ]

def array_to_formatted_list(array:np.ndarray,to_type:"callable|type" = float) -> list[any]:
    """
    Returns the array as a list while converting all values to the specified type
    :param array:
    :param to_type:
    :return:
    """
    return list(map(to_type,array))

def refresh_table(w,_,v):
    """
    Refreshes the main table
    :param w:
    :param v:
    :return:
    """
    num_symbols = 0 # So the IDE doesn't complain...
    max_k = 0

    if not (
        (err_rate := to_float(v["SymbolErrorRate"],0)) and
        (num_symbols := to_int(v["NumSymbols"], 0)) and
        (max_k := to_int(v["MaxErrorcount"], 0))
    ):
        return

    calculated:np.ndarray = calc.get_table(
        err_rate,
        num_symbols,
        max_k,
        rounding=8,
        to_array=True,
    ).T

    formatted = [
        array_to_formatted_list(calculated[0], int),
        array_to_formatted_list(calculated[1]),
        array_to_formatted_list(calculated[2]),
        array_to_formatted_list(calculated[3]),
        array_to_formatted_list(calculated[4], lambda a:f"{int(a):_}"),
    ]
    formatted = list(zip(*formatted)) # Transpose for non-Numpy fans

    w["mainTable"](formatted)


def main():

    layout = [
        layout_oneLine("Symbol-error probability:","SymbolErrorRate",default_text="1e-7",enable_events=True) +
        layout_numberButtons("SymbolErrorRate",float,refresh_table),
        layout_oneLine("Symbol-count:", "NumSymbols",default_text=1000,enable_events=True) +
        layout_numberButtons("NumSymbols",float,refresh_table),
        layout_oneLine("Max error Count:","MaxErrorcount",default_text=10,enable_events=True) +
        layout_numberButtons("MaxErrorcount",int,refresh_table),
        [
            sg.Table(
                [],
                headings=["Errors (k)","P(= k)","P(<= k)","P(> k)","1 // P(> k)    Period of P(> k)"],
                size=(0,10), # 10 rows
                col_widths=[10,25,25,25,25],
                auto_size_columns=False,
                key="mainTable",
            )
        ],
    ]

    w = sg.Window("Channel Coding Utility",layout=layout,finalize=True)

    e,v = w.read(timeout=10)

    refresh_table(w,e,v)

    while True:
        e,v = w.read()

        if e is None:
            w.close()
            break

        print(e)

        if callable(e): # So you can do calls just from the key
            e(w,e,v)

        if isinstance(e,tuple) and e and callable(e[0]): # You can call multiple functions simultaniously
            for i in e:
                i(w,e,v)

        if e in ["SymbolErrorRate","NumSymbols","MaxErrorcount"]:
            refresh_table(w,e,v)

if __name__ == "__main__":
    main()


