from argparse import ArgumentParser, RawTextHelpFormatter
from os import system, makedirs
from shutil import rmtree

def command(s):
    print (s)
    system(s)

def wdgDatetime():
    command("cp {0}.py /tmp/{0}.py".format(args.example))
    command("cp datetime_functions.py /tmp/datetime_functions.py")
    command("sed -i -e 's/\.Ui/Ui/' /tmp/{0}.py".format(args.example))
    command("sed -i -e 's/ \.\. / /' /tmp/{0}.py".format(args.example))
    command("pyuic5 {0}.ui -o /tmp/Ui_{0}.py".format(args.example))
    command("python /tmp/{0}.py".format(args.example))

def frmSelector():
    dir="/tmp/reusingcode_frmselector"
    
    rmtree(dir, ignore_errors=True)
    makedirs(dir, exist_ok=True)
    command("cp ui/{0}.py {1}/{0}.py".format(args.example, dir))
    command("cp ui/myqtablewidget.py {0}".format(dir))
    command("cp libmanagers.py {0}".format(dir))
    command("cp datetime_functions.py {0}/datetime_functions.py".format(dir))
    command("sed -i -e 's/\.Ui/Ui/' {1}/{0}.py".format(args.example, dir))
    command("sed -i -e 's/ \.\. / /' {1}/{0}.py".format(args.example, dir))
    command("sed -i -e 's/\.myqtablewidget/myqtablewidget/' {0}/frmSelector.py".format(dir))
    command("sed -i -e 's/ \.\. / /' {0}/myqtablewidget.py".format(dir))
    command("sed -i -e 's/\.datetime_functions/datetime_functions/' {}/libmanagers.py".format(dir))
    command("python {1}/{0}.py".format(args.example, dir))


parser=ArgumentParser(description='Program to allow see reusingcode modules as standalone scripts', formatter_class=RawTextHelpFormatter)
parser.add_argument('--example', action='store', choices=['wdgDatetime', 'frmSelector' ], required=True)
args=parser.parse_args()

if args.example=="wdgDatetime":
    wdgDatetime()
elif args.example=="frmSelector":
    frmSelector()
