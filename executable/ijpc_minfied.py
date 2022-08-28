_E='delc'
_D='ncs'
_C='#/ijp python\n'
_B='--med'
_A='--slow'
import subprocess,sys,time as tm
from rich.console import *
from datetime import time
help_info='usage: IJP [-h] ijp_file compilation_py\nVERSION INFO: Varson Alpha Next 1\npositional arguments:\n  ijp_file          What file to read IJP code from\n  compilation_py    Compilation target, what file to compile to?\noptional arguments:\n  -h, --help    show this help message and exit\n  -v --version  show version info\n'
console=Console()
lines=[]
PYTHON_TARGET=sys.executable
agrs=sys.argv
logs=open('logs.log','w')
class err:
	def __init__(self,type,line_num,content):pass
	def invalidLangError(type,line_num,content):error_line=f"{type} on line {line_num}: {content}";console.rule(f"[italic blue]{type} + Tips");console.print(f"[red bold]{error_line}");console.print('[italic blue]You can use [italic green]#/ijp python[italic blue] to help you fix this error.');sys.exit()
	def flexibleError(type,content,tips):error_line=f"{type}: {content}";console.rule(f"[italic blue]{type} + Tips");console.print(f"[red bold]{error_line}");console.print(f"[italic blue]{tips}")
try:
	filename=agrs[1];compile_py=agrs[2]
	try:
		speed=agrs[3]
		if filename.endswith('.ijp')or filename.endswith('.ijpc'):pass
		else:err.flexibleError('WrongFileType',filename,'The filename of source IJP or IJPC file must be .ijp or .ijpc');sys.exit()
	except Exception as em:speed=_A
except Exception:print('usage: IJP [-h] ijp_file compilation_py\nVERSION INFO: Varson Alpha Next 1\npositional arguments:\n  ijp_file          What file to read IJP code from\n  compilation_py    Compilation target, what file to compile to?\noptional arguments:\n  -h, --help    show this help message and exit\n  -v --version  show version info\n  -d --docs     load mkdocs server for documentation\n  ');sys.exit()
code=open(filename,'r')
codes=code.readlines()
imports='from tkinter import *\nfrom tkinter import colorchooser\nfrom tkinter import messagebox\nfrom tkinter import filedialog\nfrom tkinter import ttk'
lines=[]
console=Console()
class error:
	def __init__(self,type,line_num,content):pass
	def invalidLangError(type,line_num,content):error_line=f"{type} on line {line_num}: {content}";console.rule(f"[italic blue]{type} + Tips");console.print(f"[red bold]{error_line}");console.print('[italic blue]You can use [italic green]#/ijp python[italic blue] [italic red](or "py" or "python" based on what the python command is on your laptop)[italic blue] to help you fix this error.');sys.exit()
	def MissingArgument(type,content):error_line=f"{type}: {content}";console.rule(f"[italic blue]{type} + Tips");console.print(f"[red bold]{error_line}");console.print('[italic blue]Please define a [italic green]variable name and "=" and content[italic blue] [italic red]for example: var name = "Joe"');sys.exit()
	def tksuper(type,content):error_line=f"{type}: {content}";console.rule(f"[italic blue]{type} + Tips");console.print(f"[red bold]{error_line}");console.print('[italic green]Example: tksuper root title geometry color');sys.exit()
def parse(line):
	U='#/ijp strict_variables';T='!';S='~';R='onexec:';Q='sepr';P='# ';O='// ';N='ijp_version';M='OOP';L='def ';K='print(';J='write ';I='$';H='init(';G='do';F='fun ';E='Missing name, identifier, content';D=')';C=':';B=' ';A=True;line_whitespace=line.lstrip()
	if line_whitespace.startswith(J)==A:line=line.replace(J,K);line+=D
	elif line_whitespace.startswith('write(')==A:
		if line.endswith(D)==A:line=line.replace(f"write",'print',1)
	elif line_whitespace.startswith(F)==A:
		if line.endswith(C)==A:line=line.replace(F,L,1)
		elif line.endswith(G)==A:line=line.replace(F,L,1);line=line.replace(' do',C,1)
	elif line_whitespace.startswith(M)==A:
		if line.endswith(C)==A:line=line.replace(M,'class',1)
	elif N in line_whitespace:line=line.replace(N,"'Version [Alpha] 2.2.1'")
	elif line_whitespace.startswith(O):line=line.replace(O,P)
	elif line_whitespace==Q:line=line.replace(Q,"print('')")
	elif line_whitespace.startswith(H)==A:
		if line.endswith(C)==A:line=line.replace('init','def __init__')
	elif line_whitespace.startswith('imp ')==A:
		if line=='imp tkall':line=line.replace(line,imports)
		line=line.replace('imp','import',1)
	elif line_whitespace.startswith('fr ')==A:line=line.replace('fr','from',1)
	elif line_whitespace.endswith(G)==A:line=line.replace(G,C)
	elif line_whitespace.startswith('cstr')or line_whitespace.startswith('cint')or line_whitespace.startswith('cfloat')or line_whitespace.startswith('cbool'):
		line_list=line.split(B);line_list=[x for x in line_list if x!='']
		try:types=line_list[0];name=line_list[1];identifier=line_list[2];content=B.join(line_list[3:]);prev=f"{types} {name} = {content}";new=f"{name} {identifier} str({content})";line=line.replace(prev,new,1)
		except Exception:error.MissingArgument(E,line)
	elif line_whitespace.startswith(H)==A:line=line.replace(H,'def __init__(:',1)
	elif line_whitespace.startswith(R)==A:line=line.replace(R,'if __name__ == "__main__":',1)
	elif line_whitespace.startswith(S):line=line.replace(S,K,1);line+=D
	elif line_whitespace.startswith(T):line=line.replace(T,'input(',1);line+=D
	elif line_whitespace==U:strict_var='class var(object):\n    def __init__(self): object.__setattr__(self, "_types", {})\n    def set_type(self, name, _type): self._types[name] = _type\n    def __setattr__(self, name, value):\n        _type = self._types.get(name)\n        if _type:\n            if type(value) is not _type:\n                raise ValueError(\n                    "Variable type conflict assigning \'{}\': was {} is {}".format(\n                    name, _type, type(value)))\n        else:\n            self._types[name] = type(value)\n        object.__setattr__(self, name, value)\nv = var()';line=line.replace(U,strict_var)
	elif line_whitespace.startswith(I):
		llist=line.split(B);llist=[x for x in llist if x!='']
		try:
			identifier=I;name=llist[0];name=name.replace(I,'');content=B.join(llist[1:])
			if content=='':error.MissingArgument(E,f"\n{line}")
			line=line.replace(f"${name} {content}",f"v.{name} = {content}")
		except Exception:error.MissingArgument(E,line)
	elif line_whitespace.startswith('var'):
		line_list=line.split(B);line_list=[x for x in line_list if x!='']
		try:types=line_list[0];name=line_list[1];identifier=line_list[2];content=B.join(line_list[3:]);prev=f"{types} {name} = {content}";new=f"v.{name} = {content}";line=line.replace(prev,new)
		except Exception:error.MissingArgument(E,line)
	elif line_whitespace.startswith('tksuper '):
		lists=line.split(B);lists=[x for x in lists if x!='']
		try:var_root=lists[1];var_title=lists[2];var_size=lists[3];var_color=lists[4];line=f"{var_root} = Tk()\nroot.title({var_title})\nroot.geometry({var_size})\nroot.configure(bg={var_color})"
		except Exception:line_num=lists[0];error.TkSuper('Rw, WindowTitle, WindowSize, and WindowColor missing',line)
	line=line.replace('#/ijp python','#/ijp python compiled')
	if line_whitespace.startswith(P)!=A:
		if line_whitespace!='':
			if speed==_A:console.log(line)
			elif speed=='--fast':pass
			elif speed==_B:pass
			else:console.log(line)
			lines.append(line)
start=tm.time()
for line in codes:line=line.replace('\n','');parse(line)
with open(compile_py,'w')as file:file.seek(0);file.truncate();file.close()
for x in lines:files=open(compile_py,'a');files.write(f"{x}\n")
files.close()
my_code=open(compile_py,'r')
my_codes=my_code.read()
my_code.close()
def run_code():
	if speed==_B:console.log(lines)
	end=tm.time();subprocess.run([PYTHON_TARGET,compile_py]);console.log(f"Total compilation time {end-start}, speed: {speed}")
if __name__=='__main__':
	if codes[0]==_C:pass
	elif codes[0]!=_C:error.invalidLangError('Invalid IJP code','1',codes[0]);sys.exit()
	try:
		run_code()
		if compile_py==_D:os.remove(_D)
		if compile_py==_E:os.remove(_E)
	except Exception as pyerror:print(pyerror)