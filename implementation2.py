from qu_fsm import *

fsm = Qu_fsm("comm.json")

fsm.set_default_attrs(com_name = "/empty", stage = "default")

def prepare_command(inp):
    inp = inp.split(" ")
    meth = fsm.get_method(com_name = inp[0])
    if meth:
        meth(*inp[1::])
    else:
        print("An error has occured!")
  
@fsm.method()
def empty_com(*args):
    print("Command is not found")

@fsm.method(com_name = "/help")
def help_com(*args):
    print("How can i help you?")

@fsm.method(com_name = "/play", stage = "game")
def play_com(*args):
    print("You won")

@fsm.method(com_name = "/asdf", stage = "menu")
@fsm.methods(com_name = ["/qwe", "/rty"], stage = "game")
def easter_com(*args):
    print("An Easter egg!")

@fsm.method(com_name = "/stage")
def stage_com(*args):
    if args:
        fsm.change_attrs(stage = args[0])
    print("stage:", fsm.get_attr("stage"))

while True:
    prepare_command(input(">>> ").strip())
