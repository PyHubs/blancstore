import subprocess, sys
import time as tm
from rich.console import *
from datetime import time

"""
UPDATE INFO
- Now fiexd some bugs
- if line starts with ~ = print
- if line startswith with ! = input 
- typing ncs as the compilation_target actually means that the python compiled target does not live for long.
- Switched to pypy

This is the readable source, for building and modifying to fit your own custom syntax! 
"""

# Variables
help_info = """usage: IJP [-h] ijp_file compilation_py
VERSION INFO: Varson Alpha Next 1
positional arguments:
  ijp_file          What file to read IJP code from
  compilation_py    Compilation target, what file to compile to?
optional arguments:
  -h, --help    show this help message and exit
  -v --version  show version info
"""

console = Console() # Initalize rich console
lines = [] # List to append all compiled code to

# Get python target an args
PYTHON_TARGET = sys.executable
agrs = sys.argv

# Create a logger
logs = open('logs.log', 'w')

#? Create an error handler (FLEXIBLE)
class err():
    def __init__(self, type, line_num, content) -> None: pass

    #! Invalid Language error
    def invalidLangError(type, line_num, content):
        """
        #! An InvalidLanguageError occours when you use the wrong header. The header must be #/ijp python to indicate that this is indeed an .ijp file
        """
        error_line = f"{type} on line {line_num}: {content}"
        console.rule(f"[italic blue]{type} + Tips")
        console.print(f"[red bold]{error_line}")
        console.print('[italic blue]You can use [italic green]#/ijp python[italic blue] to help you fix this error.')
        sys.exit()

    def flexibleError(type, content, tips):
        """
        #? Use flexibleError to create a custom error class, its own type, content and tips, no bulitin ones for you. Recommended for most uses as a flexibleError is easier for almost all posible needs
        """
        error_line = f"{type}: {content}"
        console.rule(f"[italic blue]{type} + Tips")
        console.print(f"[red bold]{error_line}")
        console.print(f"[italic blue]{tips}")

#* DIFFERENCES
#* write("hello world") ~~> print("hello world")
#* fun name(): ~~> def name():
#* imp ~~> import
#* fr ~~> from
#* write ~~> print
#* tksuper root title geometry color

# Try to get filename and compilation_py (target)
try:
    filename = agrs[1]
    compile_py = agrs[2]
    try:
        speed = agrs[3]

        # Check if filename ends with .ijp or .ijpc
        if filename.endswith(".ijp") or filename.endswith(".ijpc"): pass
        else:
            err.flexibleError("WrongFileType", filename, "The filename of source IJP or IJPC file must be .ijp or .ijpc")
            sys.exit()

    # If slow is equal to nothing, set it to slow
    except Exception as em: speed = "--slow"

# If no filename and compilation target
except Exception:
    print("""usage: IJP [-h] ijp_file compilation_py
VERSION INFO: Varson Alpha Next 1
positional arguments:
  ijp_file          What file to read IJP code from
  compilation_py    Compilation target, what file to compile to?
optional arguments:
  -h, --help    show this help message and exit
  -v --version  show version info
  -d --docs     load mkdocs server for documentation
  """)
    sys.exit()

# Open FILENAME
code = open(filename, "r")
codes = code.readlines()

# TKALL
imports = "from tkinter import *\nfrom tkinter import colorchooser\nfrom tkinter import messagebox\nfrom tkinter import filedialog\nfrom tkinter import ttk"

# Some variables
lines = []
console = Console()

# Error class
class error:
    def __init__(self, type, line_num, content) -> None: pass

    # Invalid Language error
    def invalidLangError(type, line_num, content):
        error_line = f"{type} on line {line_num}: {content}"
        console.rule(f"[italic blue]{type} + Tips")
        console.print(f"[red bold]{error_line}")
        console.print('[italic blue]You can use [italic green]#/ijp python[italic blue] [italic red](or "py" or "python" based on what the python command is on your laptop)[italic blue] to help you fix this error.')
        sys.exit()

    # Wrong variable definiton
    def MissingArgument(type, content):
        error_line = f"{type}: {content}"
        console.rule(f"[italic blue]{type} + Tips")
        console.print(f"[red bold]{error_line}")
        console.print('[italic blue]Please define a [italic green]variable name and "=" and content[italic blue] [italic red]for example: var name = "Joe"')
        sys.exit()

    #TK Super error
    def tksuper(type, content):
        error_line = f"{type}: {content}"
        console.rule(f"[italic blue]{type} + Tips")
        console.print(f"[red bold]{error_line}")
        console.print('[italic green]Example: tksuper root title geometry color')
        sys.exit()

# A oarse function
def parse(line):
    line_whitespace = line.lstrip()

    # write
    if line_whitespace.startswith("write ") == True:
        #s:write e:NULL
        line = line.replace("write ", "print(")
        line += ")"

    elif line_whitespace.startswith("write(") == True:
        #s:write( e:)
        if line.endswith(")") == True:
            line = line.replace(f"write", "print", 1)

    elif line_whitespace.startswith("fun ") == True:
        #s:fun e:[:, do]
        if line.endswith(":") == True:
            line = line.replace("fun ", "def ", 1)
        elif line.endswith("do") == True:
            line = line.replace("fun ", "def ", 1)
            line = line.replace(" do", ":", 1)

    elif line_whitespace.startswith("OOP") == True:
        #s:OOP e::
        if line.endswith(":") == True:
            line = line.replace("OOP", "class", 1)

    elif "ijp_version" in line_whitespace:
        #s:ijp_version e:NULL
        line = line.replace("ijp_version", "'Version [Alpha] 2.2.1'")

    elif line_whitespace.startswith("// "):
        #s:// e:NULL
        line = line.replace("// ", '# ')

    elif line_whitespace == "sepr":
        #s:sepr e:NULL
        line = line.replace('sepr', "print('')")

    elif line_whitespace.startswith("init(") == True:
        #s:init( e::
        if line.endswith(":") == True:
            line = line.replace("init", "def __init__")

    elif line_whitespace.startswith("imp ") == True:
        #s:imp  s:imp kall e:NULL
        if line == "imp tkall":
            line = line.replace(line, imports)
        line = line.replace("imp", "import", 1)

    elif line_whitespace.startswith("fr ") == True:
        #s:fr  e:NULL
        line = line.replace("fr", "from", 1)

    elif line_whitespace.endswith("do") == True:
        #s:do e:NULL
        line = line.replace("do", ":")

    elif line_whitespace.startswith("cstr") or line_whitespace.startswith("cint") or line_whitespace.startswith("cfloat") or line_whitespace.startswith("cbool"):
        #s:[cstr, cint, cbool, cfloat] e:NULL
        line_list = line.split(" ")
        line_list = [x for x in line_list if x != ""]
        try:
            # Get types, name, identifier, content
            types = line_list[0]
            name = line_list[1]
            identifier = line_list[2]
            content = " ".join(line_list[3:])

            prev = f"{types} {name} = {content}"
            new = f"{name} {identifier} str({content})"

            line = line.replace(prev, new, 1)

        # Show error
        except Exception: error.MissingArgument("Missing name, identifier, content", line)

    elif line_whitespace.startswith("init(") == True:
        line = line.replace("init(", "def __init__(:", 1)

    elif line_whitespace.startswith("onexec:") == True:
        line = line.replace('onexec:', 'if __name__ == "__main__":', 1)

    # ~ (STANDS FOR PRINT)
    elif line_whitespace.startswith("~"):
        line = line.replace("~", "print(", 1)
        line += ")"

    # ! (STANDS INPUT)
    elif line_whitespace.startswith("!"):
        line = line.replace("!", "input(", 1)
        line += ")"

    elif line_whitespace == "#/ijp strict_variables":
        strict_var = """class var(object):
    def __init__(self): object.__setattr__(self, "_types", {})
    def set_type(self, name, _type): self._types[name] = _type
    def __setattr__(self, name, value):
        _type = self._types.get(name)
        if _type:
            if type(value) is not _type:
                raise ValueError(
                    "Variable type conflict assigning '{}': was {} is {}".format(
                    name, _type, type(value)))
        else:
            self._types[name] = type(value)
        object.__setattr__(self, name, value)
v = var()"""

        line = line.replace("#/ijp strict_variables", strict_var)

    elif line_whitespace.startswith("$"):
        llist = line.split(" ")
        llist = [x for x in llist if x != ""]

        try:
            identifier = "$"
            name = llist[0]
            name = name.replace("$", "")
            content = " ".join(llist[1:])

            if content == "":
                error.MissingArgument("Missing name, identifier, content", f"\n{line}")
            line = line.replace(f"${name} {content}", f"v.{name} = {content}")

        except Exception:
            error.MissingArgument("Missing name, identifier, content", line)

    elif line_whitespace.startswith("var"):
        line_list = line.split(" ")
        line_list = [x for x in line_list if x != ""]
        try:
            # Gt variables
            types = line_list[0]
            name = line_list[1]
            identifier = line_list[2]
            content = " ".join(line_list[3:])

            prev = f"{types} {name} = {content}"
            new = f"v.{name} = {content}"

            line = line.replace(prev, new)

        # Show error
        except Exception: error.MissingArgument("Missing name, identifier, content", line)

    elif line_whitespace.startswith("tksuper "):
        lists = line.split(" ")
        lists = [x for x in lists if x != ""]
        try:
            # Get tksuper arguments
            var_root = lists[1]
            var_title = lists[2]
            var_size = lists[3]
            var_color = lists[4]

            line = f'''{var_root} = Tk()
root.title({var_title})
root.geometry({var_size})
root.configure(bg={var_color})'''

        # Exception
        except Exception:
            line_num = lists[0]
            error.TkSuper("Rw, WindowTitle, WindowSize, and WindowColor missing", line)

    #/ijp python
    line = line.replace("#/ijp python", "#/ijp python compiled")

    if line_whitespace.startswith("# ") != True:
        if line_whitespace != "":
            if speed == "--slow": console.log(line)
            elif speed == "--fast": pass
            elif speed == "--med": pass
            else: console.log(line)
            lines.append(line)

start = tm.time()

# Parse all liens
for line in codes:
    line = line.replace("\n", "")
    parse(line)

# Write to compilation target
with open(compile_py, "w") as file:
    file.seek(0)
    file.truncate()
    file.close()
for x in lines:
    files = open(compile_py, "a")
    files.write(f"{x}\n")
files.close()

my_code = open(compile_py, "r")
my_codes = my_code.read()
my_code.close()

# Run the code
def run_code():
    # Show a list containing all lines
    if speed == "--med": console.log(lines)

    # End variable
    end = tm.time()

    # Run compile_py
    subprocess.run([PYTHON_TARGET, compile_py])
    console.log(f"Total compilation time {end - start}, speed: {speed}")

# Run
if __name__ == '__main__':
    # Raise invalid IJP CODE ERROR
    if codes[0] == "#/ijp python\n": pass
    elif codes[0] != "#/ijp python\n":
        error.invalidLangError("Invalid IJP code", "1", codes[0])
        sys.exit()

    # Run code
    try: 
        run_code()
        if compile_py == "ncs": os.remove('ncs')
        if compile_py == "delc": os.remove('delc')
    except Exception as pyerror: print(pyerror)