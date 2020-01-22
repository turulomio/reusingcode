from argparse import ArgumentParser, RawTextHelpFormatter
from os import system

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


parser=ArgumentParser(description='Program to allow see reusingcode modules as standalone scripts', formatter_class=RawTextHelpFormatter)
parser.add_argument('--example', action='store', choices=['wdgDatetime', ], required=True)
args=parser.parse_args()

if args.example=="wdgDatetime":
    wdgDatetime()