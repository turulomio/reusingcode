from argparse import ArgumentParser
from logging import basicConfig, INFO, WARNING,  ERROR,  CRITICAL, DEBUG, info

_=str

class MyArgParser(ArgumentParser):
    def __init__(self ):
        ArgumentParser.__init__(self)
        self.debug_system=False

    def setDescription(self, s):
        self.description=s
        
        
    def addArgumentVersion(self, version):
        self.add_argument('--version', action='version', version=version)
        
    def addArgumentDebug(self, default="WARNING"):
        self.debug_system=True
        self.add_argument('--debug', help=_("Debug program information"), choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"], default=default)

    def __addDebugSystem(self, level):
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
         self.debuglevel=level
         
         
    def addGroupOracle(self):
        group_oracle=self.add_argument_group(_("Parámetros conexión a ORACLE"))
        group_oracle.add_argument( '--user', help='Database user', action='store',  default=None)
        group_oracle.add_argument( '--password', help='Database password', action='store', default=None)
        group_oracle.add_argument( '--server', help='Database host', action='store',  default=None)
        group_oracle.add_argument( '--port', help='Database port', action='store',  default=None)
        group_oracle.add_argument('--service_name',  help="Oracle Service Name", action='store',  default=None)


    def setEpilog(self, s):
        self.epilog=s

    def process(self, args=None):
        self.args=self.parse_args(args)
        if self.debug_system is True:
            self.__addDebugSystem(self.args.debug)

    
