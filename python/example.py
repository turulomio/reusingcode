from argparse import ArgumentParser, RawTextHelpFormatter
from logging import info, basicConfig, DEBUG, INFO, CRITICAL, ERROR, WARNING
from os import system, makedirs, chdir
from shutil import rmtree
from sys import path

def command(s):
    print (s)
    system(s)

def frmAccess():
    dir="/tmp/reusingcode_frmaccess"
    rmtree(dir, ignore_errors=True)
    makedirs(dir, exist_ok=True)

    command("cp ui/{0}.py {1}/{0}.py".format(args.example,dir))
    command("cp ui/myqwidgets.py {0}/myqwidgets.py".format(dir))
    command("cp call_by_name.py {0}".format(dir))
    command("cp casts.py {0}".format(dir))
    command("cp admin_pg.py {0}".format(dir))
    command("cp objects/currency.py {0}".format(dir))
    command("cp objects/percentage.py {0}".format(dir))
    command("cp connection_pg.py {0}".format(dir))
    command("cp connection_pg_qt.py {0}".format(dir))
    command("cp translationlanguages.py {0}".format(dir))
    command("cp package_resources.py {0}".format(dir))
    command("cp libmanagers.py {0}".format(dir))
    command("pyuic5 ui/{0}.ui -o {1}/Ui_{0}.py".format(args.example, dir))
    command("sed -i -e 's/\.Ui/Ui/' {1}/{0}.py".format(args.example, dir))
    command("sed -i -e 's/ \.\. / /' {1}/{0}.py".format(args.example, dir))
    command("sed -i -e 's/ \.myqwidgets / myqwidgets /' {1}/{0}.py".format(args.example, dir))
    command("sed -i -e 's/ \.connection/ connection/' {}/connection_pg_qt.py".format(dir))
    command("sed -i -e 's/ \.connection/ connection/' {}/admin_pg.py".format(dir))
    command("sed -i -e 's/ \.libmanagers/ libmanagers/' {}/translationlanguages.py".format(dir))
    command("sed -i -e 's/ \.package/ package/' {}/translationlanguages.py".format(dir))
    command("sed -i -e 's/ \.objects./ /' {0}/casts.py".format(dir))
    command("sed -i -e 's/\.casts/casts/' {}/connection_pg.py".format(dir))
    command("sed -i -e 's/ \.call_by_name/ call_by_name/' {0}/libmanagers.py".format(dir))
    command("cp datetime_functions.py {0}/datetime_functions.py".format(dir))
    command("sed -i -e 's/\.datetime_functions/datetime_functions/' {}/libmanagers.py".format(dir))
    command("python {1}/{0}.py".format(args.example, dir))

def wdgDatetime():
    dir="/tmp/reusingcode_wdgdatetime"
    rmtree(dir, ignore_errors=True)
    makedirs(dir, exist_ok=True)

    command("cp ui/{0}.py {1}/{0}.py".format(args.example, dir))
    command("cp ui/myqdialog.py {}/myqdialog.py".format(dir))
    command("cp datetime_functions.py {0}/datetime_functions.py".format(dir))
    command("sed -i -e 's/\.Ui/Ui/' {1}/{0}.py".format(args.example, dir))
    command("sed -i -e 's/ \.\. / /' {1}/{0}.py".format(args.example, dir))
    command("sed -i -e 's/ \.myqdialog / myqdialog /' {1}/{0}.py".format(args.example, dir))
    command("pyuic5 ui/{0}.ui -o {1}/Ui_{0}.py".format(args.example, dir))
    command("python {1}/{0}.py".format(args.example, dir))

def wdgYearMonth():
    dir="/tmp/reusingcode_wdgyearmonth"
    rmtree(dir, ignore_errors=True)
    makedirs(dir, exist_ok=True)
    path.insert(0, dir)

    command("cp ui/{0}.py {1}/{0}.py".format(args.example,dir))
    command("cp ui/myqwidgets.py {0}/myqwidgets.py".format(dir))
    command("sed -i -e 's/\.Ui/Ui/' {1}/{0}.py".format(args.example, dir))
    command("sed -i -e 's/from \./from  /' {1}/{0}.py".format(args.example, dir))
    command("pyuic5 ui/{0}.ui -o {1}/Ui_{0}.py".format(args.example, dir))

    chdir(dir)
    from wdgYearMonth import example
    example()

def frmSelector():
    dir="/tmp/reusingcode_frmselector"
    rmtree(dir, ignore_errors=True)
    makedirs(dir, exist_ok=True)
    path.insert(0, dir)

    command("cp ui/{0}.py {1}/{0}.py".format(args.example, dir))
    command("cp ui/myqtablewidget.py {0}".format(dir))
    command("cp libmanagers.py {0}".format(dir))
    command("cp objects/currency.py {0}".format(dir))
    command("cp objects/percentage.py {0}".format(dir))
    command("cp call_by_name.py {0}".format(dir))
    command("cp casts.py {0}".format(dir))
    command("cp datetime_functions.py {0}/datetime_functions.py".format(dir))
    command("sed -i -e 's/\.Ui/Ui/' {1}/{0}.py".format(args.example, dir))
    command("sed -i -e 's/ \.\. / /' {1}/{0}.py".format(args.example, dir))
    command("sed -i -e 's/\.myqtablewidget/myqtablewidget/' {0}/frmSelector.py".format(dir))
    command("sed -i -e 's/ \.\. / /' {0}/myqtablewidget.py".format(dir))
    command("sed -i -e 's/ \.call_by_name/ call_by_name/' {0}/libmanagers.py".format(dir))
    command("sed -i -e 's/ \.objects./ /' {0}/casts.py".format(dir))
    command("sed -i -e 's/\.datetime_functions/datetime_functions/' {}/libmanagers.py".format(dir))

    chdir(dir)
    from frmSelector import example
    example()

def libmanagers():
    dir="/tmp/reusingcode_libmanagers"
    rmtree(dir, ignore_errors=True)
    makedirs(dir, exist_ok=True)

    command("cp libmanagers.py {0}".format(dir))
    command("cp datetime_functions.py {0}/datetime_functions.py".format(dir))
    command("sed -i -e 's/\.datetime_functions/datetime_functions/' {}/libmanagers.py".format(dir))
    command("python {}/libmanagers.py".format(dir))  

def connection_pg():
    dir="/tmp/reusingcode_connection_pg"
    rmtree(dir, ignore_errors=True)
    makedirs(dir, exist_ok=True)

    command("cp connection_pg.py {0}".format(dir))
    command("cp casts.py {0}/casts.py".format(dir))
    command("sed -i -e 's/\.casts/casts/' {}/connection_pg.py".format(dir))
    command("python {}/connection_pg.py".format(dir))  
def myconfigparser():
    dir="/tmp/reusingcode_myconfigparser"
    rmtree(dir, ignore_errors=True)
    makedirs(dir, exist_ok=True)

    command("cp myconfigparser.py {0}".format(dir))
    command("cp casts.py {0}/casts.py".format(dir))
    command("cp datetime_functions.py {0}/datetime_functions.py".format(dir))
    command("sed -i -e 's/\.casts/casts/' {}/myconfigparser.py".format(dir))
    command("sed -i -e 's/\.datetime_functions/datetime_functions/' {}/myconfigparser.py".format(dir))
    command("python {}/myconfigparser.py".format(dir))  

def myQTableWidget():
    dir="/tmp/reusingcode_myqtablewidget"
    rmtree(dir, ignore_errors=True)
    makedirs(dir, exist_ok=True)
    path.insert(0, dir)

    command("cp ui/myqtablewidget.py {0}".format(dir))
    command("cp libmanagers.py {0}".format(dir))
    command("cp datetime_functions.py {0}/datetime_functions.py".format(dir))
    command("sed -i -e 's/ \.\. / /' {}/myqtablewidget.py".format(dir))
    command("sed -i -e 's/\.datetime_functions/datetime_functions/' {}/libmanagers.py".format(dir))
    
    chdir(dir)
    from myqtablewidget import example
    example()

def myqcharts():
    dir="/tmp/reusingcode_myqcharts"
    rmtree(dir, ignore_errors=True)
    makedirs(dir, exist_ok=True)
    path.insert(0, dir)

    command("cp ui/myqcharts.py {0}".format(dir))
    command("cp ui/myqtablewidget.py {0}".format(dir))
    command("cp objects/percentage.py {0}".format(dir))
    command("cp objects/currency.py {0}".format(dir))
    command("cp casts.py {0}".format(dir))
    command("cp objects/currency.py {0}".format(dir))
    command("cp datetime_functions.py {0}/datetime_functions.py".format(dir))
    command("cp libmanagers.py {0}/libmanagers.py".format(dir))
    command("sed -i -e 's/\.myqtablewidget/myqtablewidget/' {0}/myqcharts.py".format(dir))
    command("sed -i -e 's/ \.\. objects\./ /' {}/myqcharts.py".format(dir))
    command("sed -i -e 's/ \.\. / /' {}/myqcharts.py".format(dir))
    command("sed -i -e 's/ \.\. / /' {}/myqtablewidget.py".format(dir))
    command("sed -i -e 's/ \./ /' {0}/percentage.py".format(dir))
    command("sed -i -e 's/ \.objects/ objects/' {0}/casts.py".format(dir))
    command("sed -i -e 's/ \./ /' {0}/libmanagers.py".format(dir))
    command("sed -i -e 's/ \.\. datetime_functions/ datetime_functions/' {}/myqcharts.py".format(dir))
    command("sed -i -e 's/ \.\. datetime_functions/ datetime_functions/' {}/myqtablewidget.py".format(dir))

    chdir(dir)
    from myqcharts import example
    example()
    
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
parser.add_argument('--example', action='store', choices=['wdgDatetime', 'wdgYearMonth', 'frmSelector', 'libmanagers', 'myQTableWidget' , 'myconfigparser',  'myqcharts', 'frmAccess', 'connection_pg'], required=True)
parser.add_argument('--debug', help="Debug program information", choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"], default="DEBUG")
args=parser.parse_args()

addDebugSystem(args.debug)
if args.example=="wdgDatetime":
    wdgDatetime()
elif args.example=="wdgYearMonth":
    wdgYearMonth()
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
elif args.example=="connection_pg":
    connection_pg()
elif args.example=="myconfigparser":
    myconfigparser()
