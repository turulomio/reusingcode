## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README
from datetime import timedelta, datetime, date, time
from pytz import timezone
from logging import critical

from PyQt5.QtWidgets import QApplication


## Types for dt strings. Used in dtaware2string function
class eDtStrings:
    ## Parsed for ui
    QTableWidgetItem=1
    
    ## 20190909 0909
    Filename=2
    
    ## 201909090909
    String=3

## Function to create a datetime aware object
## @param date datetime.date object
## @param hour hour object
## @param zonename String with datetime zone name. For example "Europe/Madrid"
## @return datetime aware
def dtaware(date, hour, zonename):
    z=timezone(zonename)
    a=datetime(date.year,  date.month,  date.day,  hour.hour,  hour.minute,  hour.second, hour.microsecond)
    a=z.localize(a)
    return a
    ## Function that converts a number of days to a string showing years, months and days
## @param days Integer with the number of days
## @return String like " 0 years, 1 month and 3 days"
def days2string(days):
    years=days//365
    months=(days-years*365)//30
    days=int(days -years*365 -months*30)
    if years==1:
        stryears=QApplication.translate("Core", "year")
    else:
        stryears=QApplication.translate("Core", "years")
    if months==1:
        strmonths=QApplication.translate("Core", "month")
    else:
        strmonths=QApplication.translate("Core", "months")
    if days==1:
        strdays=QApplication.translate("Core", "day")
    else:
        strdays=QApplication.translate("Core", "days")
    return QApplication.translate("Core", "{} {}, {} {} and {} {}").format(years, stryears,  months,  strmonths, days,  strdays)


def month_end(year, month, zone):
    """datetime último de un mes
    """
    return day_end_from_date(month_last_date(year, month), zone)
    
## Returns a date with the last day of a month
## @return date object
def month_last_date(year, month):
    if month == 12:
        return date(year, month, 31)
    return date(year, month+1, 1) - timedelta(days=1)

## Returns an aware datetime with the start of year
def year_start(year, zone):
    return day_start_from_date(date(year, 1, 1), zone)
    
## Returns an aware datetime with the last of year
def year_end(year, zone):
    return day_end_from_date(date(year, 12, 31), zone)
def day_end(dattime, zone):
    """Saca cuando acaba el dia de un dattime en una zona concreta"""
    return dtaware_changes_tz(dattime, zone.name).replace(hour=23, minute=59, second=59)
    
def day_start(dattime, zone):
    return dtaware_changes_tz(dattime, zone.name).replace(hour=0, minute=0, second=0)
    
def day_end_from_date(date, zone):
    """Saca cuando acaba el dia de un dattime en una zona concreta"""
    return dtaware(date, time(23, 59, 59), zone.name)
    
def day_start_from_date(date, zone):
    return dtaware(date, time(0, 0, 0), zone.name)
    
def month_start(year, month, zone):
    """datetime primero de un mes
    """
    return day_start_from_date(date(year, month, 1), zone)
    
def month2int(s):
    """
        Converts a month string to a int
    """
    if s in ["Jan", "Ene", "Enero", "January", "enero", "january"]:
        return 1
    if s in ["Feb", "Febrero", "February", "febrero", "february"]:
        return 2
    if s in ["Mar", "Marzo", "March", "marzo", "march"]:
        return 3
    if s in ["Apr", "Abr", "April", "Abril", "abril", "april"]:
        return 4
    if s in ["May", "Mayo", "mayo", "may"]:
        return 5
    if s in ["Jun", "June", "Junio", "junio", "june"]:
        return 6
    if s in ["Jul", "July", "Julio", "julio", "july"]:
        return 7
    if s in ["Aug", "Ago", "August", "Agosto", "agosto", "august"]:
        return 8
    if s in ["Sep", "Septiembre", "September", "septiembre", "september"]:
        return 9
    if s in ["Oct", "October", "Octubre", "octubre", "october"]:
        return 10
    if s in ["Nov", "Noviembre", "November", "noviembre", "november"]:
        return 11
    if s in ["Dic", "Dec", "Diciembre", "December", "diciembre", "december"]:
        return 12


## Converts a tring 12:23 to a time object
def string2time(s, type=1):
    if type==1:#12:12
        a=s.split(":")
        return time(int(a[0]), int(a[1]))
    elif type==2:#12:12:12
        a=s.split(":")
        return time(int(a[0]), int(a[1]), int(a[2]))
        
        
            
def string2date(iso, type=1):
    """
        date string to date, with type formats
    """
    if type==1: #YYYY-MM-DD
        d=iso.split("-")
        return date(int(d[0]), int(d[1]),  int(d[2]))
    if type==2: #DD/MM/YYYY
        d=iso.split("/")
        return date(int(d[2]), int(d[1]),  int(d[0]))
    if type==3: #DD.MM.YYYY
        d=iso.split(".")
        return date(int(d[2]), int(d[1]),  int(d[0]))
    if type==4: #DD/MM
        d=iso.split("/")
        return date(date.today().year, int(d[1]),  int(d[0]))

## Function to generate a datetime (aware or naive) from a string
## @param s String
## @param type Integer
## @param zone Name of the zone. By default "Europe Madrid" only in type 3and 4
## @return Datetime
def string2datetime(s, type, zone="Europe/Madrid"):
    if type==1:#2017-11-20 23:00:00+00:00  ==> Aware
        s=s[:-3]+s[-2:]
        dat=datetime.strptime( s, "%Y-%m-%d %H:%M:%S%z" )
        return dat
    if type==2:#20/11/2017 23:00 ==> Naive
        dat=datetime.strptime( s, "%d/%m/%Y %H:%M" )
        return dat
    if type==3:#20/11/2017 23:00 ==> Aware, using zone parameter
        dat=datetime.strptime( s, "%d/%m/%Y %H:%M" )
        z=timezone(zone)
        return z.localize(dat)
    if type==4:#27 1 16:54 2017==> Aware, using zone parameter . 1 es el mes convertido con month2int
        dat=datetime.strptime( s, "%d %m %H:%M %Y")
        z=timezone(zone)
        return z.localize(dat)
    if type==5:#2017-11-20 23:00:00.000000+00:00  ==> Aware with microsecond
        s=s[:-3]+s[-2:]#quita el :
        arrPunto=s.split(".")
        s=arrPunto[0]+s[-5:]
        micro=int(arrPunto[1][:-5])
        dat=datetime.strptime( s, "%Y-%m-%d %H:%M:%S%z" )
        dat=dat+timedelta(microseconds=micro)
        return dat
    if type==6:#201907210725 ==> Naive
        dat=datetime.strptime( s, "%Y%m%d%H%M" )
        return dat
    if type==7:#01:02:03 ==> Aware
        tod=date.today()
        a=s.split(":")
        dat=datetime(tod.year, tod.month, tod.day, int(a[0]), int(a[1]), int(a[2]))
        z=timezone(zone)
        return z.localize(dat)

def dtaware2epochms(d):
    """
        Puede ser dateime o date
        Si viene con zona datetime zone aware, se convierte a UTC y se da el valor en UTC
        return now(timezone(self.name))
    """
    if d.__class__==datetime:
        if d.tzname()==None:#unaware datetine
            critical("Must be aware")
        else:#aware dateime changed to unawar
            utc=dtaware_changes_tz(d, 'UTC')
            return utc.timestamp()*1000
    critical("{} can't be converted to epochms".format(d.__class__))
    
## Return a UTC datetime aware
def epochms2dtaware(n):
    utc_unaware=datetime.utcfromtimestamp(n/1000)
    utc_aware=utc_unaware.replace(tzinfo=timezone('UTC'))
    return utc_aware


## Returns a formated string of a dtaware string formatting with a zone name
## @param dt datetime aware object
## @return String
def dtaware2string(dt, type=eDtStrings.QTableWidgetItem):
    if dt==None:
        return "None"
    elif dt.tzname()==None:
        return "Naive date and time"
    else:
        return dtnaive2string(dt, type)

## Returns a formated string of a dtaware string formatting with a zone name
## @param dt datetime aware object
## @return String
def dtnaive2string(dt, type=eDtStrings.QTableWidgetItem):
    if dt==None:
        resultado="None"
    elif type==eDtStrings.QTableWidgetItem:
        if dt.microsecond==4 :
            resultado="{}-{}-{}".format(dt.year, str(dt.month).zfill(2), str(dt.day).zfill(2))
        else:
            resultado="{}-{}-{} {}:{}:{}".format(dt.year, str(dt.month).zfill(2), str(dt.day).zfill(2), str(dt.hour).zfill(2), str(dt.minute).zfill(2),  str(dt.second).zfill(2))
    elif type==eDtStrings.Filename:
            resultado="{}{}{} {}{}".format(dt.year, str(dt.month).zfill(2), str(dt.day).zfill(2), str(dt.hour).zfill(2), str(dt.minute).zfill(2))
    elif type==eDtStrings.String:
        resultado="{}{}{}{}{}".format(dt.year, str(dt.month).zfill(2), str(dt.day).zfill(2), str(dt.hour).zfill(2), str(dt.minute).zfill(2))
    return resultado
    
## Changes zoneinfo from a dtaware object
## For example:
## - datetime.datetime(2018, 5, 18, 8, 12, tzinfo=<DstTzInfo 'Europe/Madrid' CEST+2:00:00 DST>)
## - libcaloriestrackerfunctions.dtaware_changes_tz(a,"Europe/London")
## - datetime.datetime(2018, 5, 18, 7, 12, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
## @param dt datetime aware object
## @tzname String with datetime zone. For example: "Europe/Madrid"
## @return datetime aware object
def dtaware_changes_tz(dt,  tzname):
    if dt==None:
        return None
    tzt=timezone(tzname)
    tarjet=tzt.normalize(dt.astimezone(tzt))
    return tarjet
