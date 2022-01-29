from qu_fsm import *

com = Qu_fsm("com.json")

com.set_default_attrs(com_name = "/empty", role = "user")

def prepare_command(inp):
    inp = inp.split(" ")
    com.change_attrs(com_name = inp[0])
    if not com.handle_method(*inp[1::]):
        print("An error has occured!")
  
@com.method()
def empty_com(*args):
    print("Command is not found")
    if args: print("args:,", *args)

@com.method(com_name = "/help")
def help_com(*args):
    print("How can i help you?")

@com.methods(com_name = ["/admin", "/manage"], role = ["admin", "superadmin"])
def admin_com(*args):
    print("You're admin")

@com.methods(com_name = ["/admin", "/manage"])
def admin_com(*args):
    print("You have no rights")

@com.method(com_name = "/role")
def admin_com(*args):
    if args:
        com.change_attrs(role = args[0])
    print("role:", com.get_attr("role"))

while True:
    prepare_command(input(">>> "))
