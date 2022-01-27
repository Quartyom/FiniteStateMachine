from qu_fsm import *

com = Qu_fsm("com.json")

com.set_attrs(com_name = "/test", role = "user")

def prepare_command(inp):
    inp = inp.split(" ")
    com.change_attrs(com_name = inp[0])
    if not com.handle_command(*inp[1::]):
        print("An error has occured!")
  
@com.command()
def error_com(*args):
    print("Command is not found")

@com.command(com_name = "/help")
def help_com(*args):
    print("How can i help you?")

@com.command(com_name = "/admin", role = "admin")
def admin_com(*args):
    print("You're admin")

@com.command(com_name = "/admin")
def admin_com(*args):
    print("You have no rights")

@com.command(com_name = "/role")
def admin_com(*args):
    if args:
        com.change_attrs(role = args[0])
    print("role:", com.get_attr("role"))

while True:
    prepare_command(input(">>> "))