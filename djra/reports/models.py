import datetime
import time
from djra.freeradius.models import Radacct
import warnings
from pipestat import pipestat
from djra import settings
import itertools

from ipip import IP

def to_timestamp(d):
    return time.mktime(d.timetuple()) 

IP_DB_FILE = getattr(settings, 'IP_DB_FILE', None)
if IP_DB_FILE is None: 
    warnings.warn('''not found IP_DB_FILE, geo report will not work, please set IP_DB_FILE in settings.
    You can download the ipdb file from http://www.ipip.net/
    ''')
else:
    IP.load(IP_DB_FILE)

def pick(x, fields):
    return {
        field: getattr(x, field) for field in fields
    }

def build_server_report(begin_date, end_date, options):
    fields = ['username', 'nasipaddress', 'acctinputoctets', 'acctoutputoctets'] 
    sessions = Radacct.objects.filter(
        acctstarttime__gte=begin_date, acctstarttime__lt=end_date
    ).only(*fields)
    sessions = itertools.imap(lambda x: pick(x, fields), sessions)
    report_pipe = [
        {
            "$group": {
                "_id": {
                    "nasipaddress": "$nasipaddress",
                    "username": "$username",
                },
                "session_count": {"$sum": 1},
                "sum_input": {"$sum": "$acctinputoctets"},
                "sum_output": {"$sum": "$acctoutputoctets"},
            },
        },
        {
            "$group": {
                "_id": {
                    "nasipaddress": "$_id.nasipaddress",
                },
                "user_count" : {"$sum" : 1},
                "session_count": {"$sum": "$session_count"},
                "sum_input": {"$sum": "$sum_input"},
                "sum_output": {"$sum": "$sum_output"},
            },
        },
        {
            "$project" : {
                "nasipaddress" : "$_id.nasipaddress",
                "user_count" : "$user_count",
                "session_count" : "$session_count",
                "sum_input" : "$sum_input",
                "sum_output" : "$sum_output",
            },
        },
        {
            "$sort" : {
                "session_count" : -1
            }
        }
    ]

    return pipestat(sessions, report_pipe)
 
def build_user_report(begin_date, end_date, options):
    fields = ['username', 'acctinputoctets', 'acctoutputoctets'] 
    sessions = Radacct.objects.filter(
        acctstarttime__gte=begin_date, acctstarttime__lt=end_date
    ).only(*fields)
    sessions = itertools.imap(lambda x: pick(x, fields), sessions)
    threshold = options.get('threshold', 30)
    report_pipe = [
        {
            "$group": {
                "_id": {
                    "username": "$username",
                },
                "session_count": {"$sum": 1},
                "sum_input": {"$sum": "$acctinputoctets"},
                "sum_output": {"$sum": "$acctoutputoctets"},
            },
        },
        {  
            "$match" : {
                "session_count" : {"$lt" : threshold},
            }
        },
        {
            "$project" : {
                "username" : "$_id.username",
                "session_count" : "$session_count",
                "sum_input" : "$sum_input",
                "sum_output" : "$sum_output",
            },
        },
        {
            "$sort" : {
                "session_count" : 1
            }
        }
    ]

    return pipestat(sessions, report_pipe)
 
def build_geo_report(begin_date, end_date, options):
    report_pipe = [
        {
            "$group": {
                "_id": {
                    "location": "$location",
                    "username": "$username",
                },
                "session_count": {"$sum": 1},
                "session_time" : {"$sum": {"$substract" : ["$acctstoptime", "$acctstarttime"]}},
                "sum_input": {"$sum": "$acctinputoctets"},
                "sum_output": {"$sum": "$acctoutputoctets"},
            },
        },
        {
            "$group": {
                "_id": {
                    "location": "$_id.location",
                },
                "user_count" : {"$sum" : 1},
                "session_count": {"$sum": "$session_count"},
                "session_time": {"$sum": "$session_time"},
                "sum_input": {"$sum": "$sum_input"},
                "sum_output": {"$sum": "$sum_output"},
            },
        },
        {
            "$project" : {
                "location" : "$_id.location",
                "user_count" : "$user_count",
                "session_avg_time" : {"$divide" : ["$session_time", "$session_count"]},
                "session_count" : "$session_count",
                "sum_input" : "$sum_input",
                "sum_output" : "$sum_output",
            },
        },
        {
            "$sort" : {
                "user_count" : -1
            }
        }
    ]

    fields = [
        'username', 'callingstationid', 
        'acctinputoctets', 'acctoutputoctets',
        'acctstarttime', 'acctstoptime'
    ] 
    def prepare(x):
        ip = x.callingstationid
        #real world data is dirty
        if '=' in ip:
            ip = ip.split('=', 1)[0]
        try:
            location = IP.find(ip)
            location = " ".join(location.split()[:2])
        except:
            location = 'Unknow'
        y = pick(x, fields)
        y['location'] = location
        y['acctstarttime'] = to_timestamp(y['acctstarttime'] or datetime.datetime.now())
        y['acctstoptime'] = to_timestamp(y['acctstoptime'] or datetime.datetime.now())
        return y
    sessions = Radacct.objects.filter(
        acctstarttime__gte=begin_date, acctstarttime__lt=end_date
    ).only(*fields)
    sessions = itertools.imap(prepare, sessions)
    return pipestat(sessions, report_pipe)
