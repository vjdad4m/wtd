#!/usr/bin/env python3

import os
import sys
from datetime import datetime

_VERSION = "0.1"

FILE_NAME = ".wtd"
CURRENT_DIR = os.getcwd()

_iota = 0
def iota(reset=False):
    global _iota
    if reset: _iota = 0
    val = _iota
    _iota += 1 
    return val

def not_implemented():
    assert False, "Not implemented."

def exists_file():
    return os.path.exists(os.path.join(CURRENT_DIR, FILE_NAME))

OP_PRINT    = iota(reset=True)  # Print the current to-do list.
OP_NEW      = iota()            # Create a new to-do list.
OP_DELETE   = iota()            # Remove the to-do list.
OP_ADD      = iota()            # Add a task to the to-do list.
OP_COMP     = iota()            # Mark a task completed in the to-do list.
OP_HELP     = iota()            # Display help message.
_N_OPS      = iota()

CMD_LIST = ["print", "new", "delete", "add", "comp", "help",    # main command
            "p", "n", "d", "a", "c", "h"]                       # command alias

if _N_OPS != len(CMD_LIST) // 2: # every command has 2 aliases.
    assert False, "Incorrect command list"

def print_usage():
    print("Usage: wtd <SUBCOMMAND> [ARGS]")
    print("Subcommands:")
    print("     print / p   Print the to-do list of the current directory.")
    print("     new / n     Create a to-do list in the current directory.")
    print("     delete / d  Delete the to-do list of the current directory.")
    print("     add / a     Add a to-do to the to-do list.")
    print("     comp / c    Complete a to-do in the list.")
    print("Default: Print")

def OP_print(args=[]):
    if exists_file():
        with open(os.path.join(CURRENT_DIR, FILE_NAME), "r") as todo_file:
            TODOS = todo_file.readlines()
    
        banner = "-- WTD | What To Do? --"
        header = "Comp. \t|  Date \t\t| Id\t\t | TODO"
        print(' '*(len(header) - len(banner) // 2) +banner)
        print('-'*2*len(header))
        print(header)
        print('-'*2*len(header))


        if TODOS == []:
            print("Nothing... Hooray!!")
        else:
            for _idx, _todo in enumerate(TODOS):
                elements = _todo.split()
                if len(elements) < 2:
                    print("[wtd] ERROR: Invalid line in file.")
                    exit(1)

                print("[ ]" if elements[0] == "0" else "[x]", end="\t| ")
                d_element = elements[1].replace('-', ' ')
                print(d_element, end=" | ")
                print(_idx, "\t\t", end=" | ")
                print(" ".join(elements[2:]))

    else:
        print("[wtd] ERROR: To-do file does not exist.")
        exit(1)

def OP_new(args=[]):
    print("[wtd] Creating to-do file.")
    if not exists_file():
        f = open(".wtd","w+")
        f.close()
        if exists_file():
            print("[wtd] Succesfully created to-do file.")
        else:
            print("[wtd] ERROR: Failed to create to-do file.")
            exit(1)
    else:
        print("[wtd] ERROR: To-do file already exists.")
        exit(1)

def OP_delete(args=[]):
    if exists_file():
        confirm = input("[wtd] Are you sure you want to delete your to-do file (y/n)? ").lower()
        if confirm in ["y", "yes", ""]:
            os.remove(os.path.join(CURRENT_DIR, FILE_NAME))
            print("[wtd] File deleted successfully")
        else:
            print("[wtd] Deletion cancelled.")
    else:
        print("[wtd] ERROR: To-do file does not exist.")
        exit(1)

def OP_add(args=[]):
    if exists_file():
        if len(args) == 0:
            print("[wtd] ERROR: No arguments provided.")
            exit(1)

        with open(os.path.join(CURRENT_DIR, FILE_NAME), "a") as todo_file:
            now = datetime.now()
            now_str = now.strftime("[%d/%m/%Y-%H:%M:%S]")
            todo_str = ' '.join(args).replace('\n', ' ')
            todo_file.write(f"0 {now_str} {todo_str}\n")
        
        print("[wtd] To-do added successfully.")            

    else:
        print("[wtd] ERROR: To-do file does not exist.")
        exit(1)

def OP_comp(args=[]):
    not_implemented()

def OP_help(args=[]):
    print("[wtd] Version %s." % _VERSION)
    print_usage()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        args = []
        if len(sys.argv) > 2:
            args = sys.argv[2:]
    
        try:
            cmd_idx = CMD_LIST.index(cmd) % _N_OPS
        except ValueError: 
            print("[wtd] ERROR: Invalid subcommand %s." % cmd)
            print_usage()
            exit(1)

        if   cmd_idx == OP_PRINT:
            OP_print(args)
        elif cmd_idx == OP_NEW:
            OP_new(args)
        elif cmd_idx == OP_DELETE:
            OP_delete(args)
        elif cmd_idx == OP_ADD:
            OP_add(args)
        elif cmd_idx == OP_COMP:
            OP_comp(args)
        elif cmd_idx == OP_HELP:
            OP_help(args)
        else: # impossible to get here, but just in case.
            print("[wtd] ERROR: Invalid subcommand %s." % cmd)
            print_usage()
            exit(1)

    else:
        OP_print()
