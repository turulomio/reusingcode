import datetime
from collections import OrderedDict
from colorama import Fore
import cx_Oracle
import os
import time
import sys

## Esta clase realiza una conexión a Oracle y prevee de cursores y utilidades para gestionarla
class Connection:
    def __init__(self):
        self.con=None
        self.delay=0
        self.args=None
        self.connectiontime=None
        
    ## To avoid pickling problems
    def __getstate__(self):
#        print("I'm being pickled")
        r=self.__dict__.copy()
        del r["con"]#ERA LO QUE ME FALLABA
        return r


    def connect(self, user, password, service_name, server, port):
        self.user=user
        self.password=password
        self.service_name=service_name
        self.server=server
        self.port=port
        self.connectiontime=datetime.datetime.now()
        os.environ["NLS_LANG"]="AMERICAN_AMERICA.UTF8"
        dsnStr=cx_Oracle.makedsn(server, port, service_name)
        dsnStr=dsnStr.replace("SID", "SERVICE_NAME")
        self.con=cx_Oracle.connect(user=user, password=password, dsn=dsnStr)


    def disconnect(self):
        self.con.close()

    def version(self):
        return self.con.version

    def reconnect(self):
        """Used to reconnect to avoid long conexion with timeout"""
        print ("Reconecting after {}.".format(Fore.YELLOW + str(datetime.datetime.now()-self.connectiontime)))
        self.connectiontime=datetime.datetime.now()
        self.disconnect()
        self.connect(self.user, self.password, self.service_name, self.server, self.port)

    def cursor(self):
        time.sleep(self.delay)
        return self.con.cursor()
    
    def cursor_one_number(self,sql, params=[]):
        try:
            cur=self.cursor()
            time.sleep(self.delay)
            cur.execute(sql, params)
            data=[]
            for row in cur:
                data.append(row)
            cur.close()
            if len(data)!=1:
                print ("Used cursor_one_number and returned {} rows".format(len(data)))
            return data[0][0]
        except cx_Oracle.DatabaseError as e:
            print ("Se ha producido un error en la base de datos {}".format(e))
            print ("Función invocadora Connection.cursor_one_row: {}".format(sql))
            error,=e.args
            print (error.message)
            print (error.context)
            cur.close()
            self.con.disconnect()
            sys.exit(0)

    def cursor_one_row(self,sql, params=[]):
        try:
            cur=self.cursor()
            time.sleep(self.delay)
            cur.execute(sql, params)
            data=self.rows_to_dict_list(cur)
            cur.close()
            if len(data)!=1:
                print ("Used cursor one_ row and returned {}".format(cur.rowcount))
            return data[0]
        except cx_Oracle.DatabaseError as e:
            print ("Se ha producido un error en la base de datos {}".format(e))
            print ("Función invocadora Connection.cursor_one_row: {}".format(sql))
            error,=e.args
            print (error.message)
            print (error.context)
            cur.close()
            self.con.disconnect()
            sys.exit(0)
            
    ## Devuelve una lista con el valor solicitado  de la columna sql
    def cursor_one_column(self,sql, params=[]):
        try:
            cur=self.cursor()
            time.sleep(self.delay)
            cur.execute(sql, params)
            r=[]
            for row in cur:
                r.append(row[0])
            cur.close()
            return r
        except cx_Oracle.DatabaseError as e:
            print ("Se ha producido un error en la base de datos {}".format(e))
            print ("Función invocadora Connection.cursor_one_row: {}".format(sql))
            error,=e.args
            print (error.message)
            print (error.context)
            cur.close()
            self.con.disconnect()
            sys.exit(0)
            
    def cursor_rows(self,sql, params=[]):
        try:
            cur=self.cursor()
            time.sleep(self.delay)
            cur.execute(sql, params)
            data=self.rows_to_dict_list(cur)
            cur.close()
            return data
        except cx_Oracle.DatabaseError as e:
            print ("Se ha producido un error en la base de datos {}".format(e))
            print ("Función invocadora Connection.cursor_one_row: {}".format(sql))
            error,=e.args
            print (error.message)
            print (error.context)
            cur.close()
            self.con.disconnect()
            sys.exit(0)
    
    def rows_to_dict_list(self, cursor):
        columns=[i[0] for i in cursor.description]
        return [OrderedDict(zip(columns, row)) for row in cursor]
        
    ## Returns if the connection is active
    def is_active(self):
        try:
            return self.con.ping() is None
        except:
            return False


    def unogenerator_values_in_sheet(self,doc, coord_start, sql, params=[], columns_header=0, color_row_header=0xffdca8, color_column_header=0xc0FFc0, color=0xFFFFFF, styles=None):
        from unogenerator.commons import Coord as C
        from unogenerator.helpers import helper_list_of_ordereddicts
        cur=self.cursor()
        time.sleep(self.delay)
        cur.execute(sql,params)
        rows=self.rows_to_dict_list(cur)
        cur.close()

        coord_start=C.assertCoord(coord_start)

        helper_list_of_ordereddicts(doc, coord_start, rows, None, columns_header, color_row_header, color_column_header, color, styles)

    ## @params columns_widths must be a list
    def unogenerator_ods_sheet(self, doc, sheet_name,  sql, params=[], columns_widths=None, columns_header=0, color_row_header=0xffdca8, color_column_header=0xc0FFc0, color=0xFFFFFF, styles=None):
        if len(sheet_name)>32:
            print(f"Hoja {sheet_name} tiene {len(sheet_name)} caracteres")
        doc.createSheet(sheet_name)
        if columns_widths is not None:
            doc.setColumnsWidth(columns_widths)

        self.unogenerator_values_in_sheet(doc, "A1", sql, params,columns_header, color_row_header, color_column_header,  color, styles)

    ## @params columns_widths must be a list
    def unogenerator_ods_document(self, filename,  sql, params=[], sheet_name="Data", columns_widths=None, columns_header=0, color_row_header=0xffdca8, color_column_header=0xc0FFc0, color=0xFFFFFF, styles=None):
        from unogenerator import ODS_Standard, __version__
        doc=ODS_Standard()
        doc.setMetadata(
            "Query result",  
            "Query result", 
            "Connection_pg from https://github.com/turulomio/reusingcode/", 
            f"This file have been generated with ConnectionPg and UnoGenerator-{__version__}. You can see UnoGenerator main page in http://github.com/turulomio/unogenerator/",
            ["unogenerator", "sql", "query"]
        )
        self.unogenerator_ods_sheet(doc, sheet_name, sql, params, columns_widths, columns_header, color_row_header, color_column_header, color, styles)
        doc.removeSheet(0)
        doc.save(filename)
        doc.close()

