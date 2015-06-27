import os
import warnings
from pipestat import pipestat
from djra import settings
import itertools

from ipip import IP

IP_DB_FILE = getattr(settings, 'IP_DB_FILE', None)
if IP_DB_FILE is None: 
    warnings.warn('''not found IP_DB_FILE, geo report will not work, please set IP_DB_FILE in settings.
    You can download the ipdb file from http://www.ipip.net/
    ''')
else:
    IP.load(IP_DB_FILE)

geo_report_pipe = [
    {
        "$group": {
            "_id": {
                "location": "$location",
            },
            "count": {"$sum": 1},
            "sum_input": {"$min": "$acctinputoctets"},
            "sum_output": {"$max": "$acctoutputoctets"},
        },
    },
    {
        "$project" : {
            "location" : "$_id.location",
            "count" : "$count",
            "sum_input" : "$sum_input",
            "sum_output" : "$sum_output",
        },
    },
    {
        "$sort" : {
            "count" : -1
        }
    }
]

def build_geo_report(sessions):
    def prepare(x):
        ip = x.callingstationid
        #real world data is dirty
        if '=' in ip:
            ip = ip.split('=', 1)[0]
        try:
            location = IP.find(ip)
        except:
            location = None
        return {
            'location' : location,
            'acctinputoctets' : x.acctinputoctets,
            'acctoutputoctets' : x.acctoutputoctets
        }

    sessions = itertools.imap(prepare, sessions)
    items = pipestat(sessions, geo_report_pipe)
    return items
