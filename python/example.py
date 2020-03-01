from argparse import ArgumentParser, RawTextHelpFormatter
from logging import info, basicConfig, DEBUG, INFO, CRITICAL, ERROR, WARNING
from os import system, makedirs
from shutil import rmtree

def command(s):
    print (s)
    system(s)

def frmAccess():
    dir="/tmp/reusingcode_frmaccess"
    rmtree(dir, ignore_errors=True)
    makedirs(dir, exist_ok=True)

    command("cp ui/{0}.py {1}/{0}.py".format(args.example,dir))
    command("cp connection_pg.py {0}".format(dir))
    command("cp connection_pg_qt.py {0}".format(dir))
    command("cp translationlanguages.py {0}".format(dir))
    command("cp package_resources.py {0}".format(dir))
    command("cp libmanagers.py {0}".format(dir))
    command("pyuic5 ui/{0}.ui -o {1}/Ui_{0}.py".format(args.example, dir))
    command("sed -i -e 's/\.Ui/Ui/' {1}/{0}.py".format(args.example, dir))
    command("sed -i -e 's/ \.\. / /' {1}/{0}.py".format(args.example, dir))
    command("sed -i -e 's/ \.connection/ connection/' {}/connection_pg_qt.py".format(dir))
    command("sed -i -e 's/ \.libmanagers/ libmanagers/' {}/translationlanguages.py".format(dir))
    command("sed -i -e 's/ \.package/ package/' {}/translationlanguages.py".format(dir))
    command("cp datetime_functions.py {0}/datetime_functions.py".format(dir))
    command("sed -i -e 's/\.datetime_functions/datetime_functions/' {}/libmanagers.py".format(dir))
    command("python {1}/{0}.py".format(args.example, dir))

def wdgDatetime():
    dir="/tmp/reusingcode_wdgdatetime"
    rmtree(dir, ignore_errors=True)
    makedirs(dir, exist_ok=True)

    command("cp ui/{0}.py {1}/{0}.py".format(args.example,dir))
    command("cp datetime_functions.py {0}/datetime_functions.py".format(dir))
    command("sed -i -e 's/\.Ui/Ui/' {1}/{0}.py".format(args.example, dir))
    command("sed -i -e 's/ \.\. / /' {1}/{0}.py".format(args.example, dir))
    command("pyuic5 ui/{0}.ui -o {1}/Ui_{0}.py".format(args.example, dir))
    command("python {1}/{0}.py".format(args.example, dir))

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
    
def libmanagers():
    dir="/tmp/reusingcode_libmanagers"
    rmtree(dir, ignore_errors=True)
    makedirs(dir, exist_ok=True)

    command("cp libmanagers.py {0}".format(dir))
    command("cp datetime_functions.py {0}/datetime_functions.py".format(dir))
#    command("sed -i -e 's/ \.\. / /' {}/myqtablewidget.py".format(dir))
    command("sed -i -e 's/\.datetime_functions/datetime_functions/' {}/libmanagers.py".format(dir))
    command("python {}/libmanagers.py".format(dir))  
    
def myQTableWidget():
    dir="/tmp/reusingcode_myqtablewidget"
    rmtree(dir, ignore_errors=True)
    makedirs(dir, exist_ok=True)

    command("cp ui/myqtablewidget.py {0}".format(dir))
    command("cp libmanagers.py {0}".format(dir))
    command("cp datetime_functions.py {0}/datetime_functions.py".format(dir))
    command("sed -i -e 's/ \.\. / /' {}/myqtablewidget.py".format(dir))
    command("sed -i -e 's/\.datetime_functions/datetime_functions/' {}/libmanagers.py".format(dir))
    command("python {1}/myqtablewidget.py".format(args.example, dir))  

def myqcharts():
    dir="/tmp/reusingcode_myqcharts"
    rmtree(dir, ignore_errors=True)
    makedirs(dir, exist_ok=True)

    command("cp ui/myqcharts.py {0}".format(dir))
    command("cp ui/myqtablewidget.py {0}".format(dir))
    command("cp objects/percentage.py {0}".format(dir))
    command("cp objects/currency.py {0}".format(dir))
    command("cp datetime_functions.py {0}/datetime_functions.py".format(dir))
    command("sed -i -e 's/\.myqtablewidget/myqtablewidget/' {0}/myqcharts.py".format(dir))
    command("sed -i -e 's/ \.\. objects\./ /' {}/myqcharts.py".format(dir))
    command("sed -i -e 's/ \./ /' {0}/percentage.py".format(dir))
    command("sed -i -e 's/ \.\. datetime_functions/ datetime_functions/' {}/myqcharts.py".format(dir))
    command("sed -i -e 's/ \.\. datetime_functions/ datetime_functions/' {}/myqtablewidget.py".format(dir))

    command("python {1}/myqcharts.py".format(args.example, dir))
    
def addDebugSystem( level):
    logFormat = "%(asctime)s.%(msecs)03d %(levelname)s %(message)s [%(module)s:%(lineno)d]"
    dateFormat='%F %I:%M:%S'

    if level=="DEBUG":#Show detailed information that can help with program diagnosis and troubleshooting. CODE MARKS
        basicConfig(level=DEBUG, format=logFormat, datefmt=dateFormat)
    elif level=="INFO":#Everything is running as expected without any problem. TIME BENCHMARCKS
        basicConfig(level=INFO, format=logFormat, datefmt=dateFormat)
    elif level=="WARNING":#The program continues running, but something unexpected happened, which may lead to some problem down the road. THINGS TO DO
        basicConfig(level=WARNING, format=logFormat, datefmt=dateFormat)
    elif level=="ERROR":#The program fails to perform a certain function due to a bug.  SOMETHING BAD LOGIC
        basicConfig(level=ERROR, format=logFormat, datefmt=dateFormat)
    elif level=="CRITICAL":#The program encounters a serious error and may stop running. ERRORS
        basicConfig(level=CRITICAL, format=logFormat, datefmt=dateFormat)
    info("Debug level set to {}".format(level))

parser=ArgumentParser(description='Program to allow see reusingcode modules as standalone scripts', formatter_class=RawTextHelpFormatter)
parser.add_argument('--example', action='store', choices=['wdgDatetime', 'frmSelector', 'libmanagers', 'myQTableWidget' , 'myqcharts', 'frmAccess'], required=True)
parser.add_argument('--debug', help="Debug program information", choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"], default="DEBUG")
args=parser.parse_args()

addDebugSystem(args.debug)
if args.example=="wdgDatetime":
    wdgDatetime()
elif args.example=="frmAccess":
    frmAccess()
elif args.example=="frmSelector":
    frmSelector()
elif args.example=="myQTableWidget":
    myQTableWidget()
elif args.example=="myqcharts":
    myqcharts()
elif args.example=="libmanagers":
    libmanagers()
