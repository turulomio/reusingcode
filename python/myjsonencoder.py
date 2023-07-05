from datetime import datetime, date, timedelta, time
from decimal import Decimal
from json import JSONEncoder
from base64 import b64encode


class MyJSONEncoder(JSONEncoder):
    """
       Part of this code is from https://github.com/django/django/blob/main/django/core/serializers/json.py
       JSONEncoder subclass that knows how to encode date/time, decimal types, and UUIDs.
    """
    
    
    def _get_duration_components(self, duration):
        days = duration.days
        seconds = duration.seconds
        microseconds = duration.microseconds

        minutes = seconds // 60
        seconds %= 60


        hours = minutes // 60
        minutes %= 60

        return days, hours, minutes, seconds, microseconds
    
    def _duration_iso_string(self, duration):
        if duration < timedelta(0):
            sign = "-"
            duration *= -1
        else:
            sign = ""

        days, hours, minutes, seconds, microseconds = self._get_duration_components(duration)
        ms = ".{:06d}".format(microseconds) if microseconds else ""
        return "{}P{}DT{:02d}H{:02d}M{:02d}{}S".format(
            sign, days, hours, minutes, seconds, ms
        )
    
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith("+00:00"):
                r = r.removesuffix("+00:00") + "Z"
            return r
        elif isinstance(o, date):
            return o.isoformat()
        elif isinstance(o, time):
            if o.utcoffset() is not None: #If it's aware
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, timedelta):
            return self._duration_iso_string(o)
        elif isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, bytes):
            return b64encode(o).decode("UTF-8")
        elif o.__class__.__name__=="Percentage":
            return o.value
        elif o.__class__.__name__=="Currency":
            return o.amount
        else:
            return super().default(o)
            
            
if __name__ == '__main__':
    from json import dumps
    from datetime import timezone
    d={}
    d["Integer"]=12112
    d["Float"]=12121.1212
    d["Date"]=date.today()
    d["Datetime"]=datetime.now()
    d["Timedelta"]=timedelta(hours=4, days=2, minutes=12,  seconds=12)
    d["Time"]=time(12, 12, 12, 123456)
    d["Datetime aware"]=d["Datetime"].replace(tzinfo=timezone.utc)
    d["Bytes"]=b"Byte array"
    d["Decimal"]=Decimal("12.12123414")
    print (dumps(d, cls=MyJSONEncoder, indent=4))
