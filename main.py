import datetime

def datetime_response(date_some):
    d1 = datetime.datetime.strptime(date_some,"%Y-%m-%dT%H:%M:%SZ")
    return d1

print(datetime_response("2013-07-12T07:00:00Z"))