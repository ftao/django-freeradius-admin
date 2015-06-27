from django.db import models
from pipestat import pipestat
import itertools

# Create your models here.

from ipip import IP

import os
path = os.path.dirname(os.path.dirname(__file__))
IP.load(os.path.join(path, "ipdb.dat"))

def ip2area(ip):
    return IP.find(ip)


#        <td>{{ acct.acctinputoctets|filesizeformat }}</td>
#        <td>{{ acct.acctoutputoctets|filesizeformat }}</td>

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
            location = ip2area(ip)
        except:
            location = None
        return {
            'location' : location,
            'acctinputoctets' : x.acctinputoctets,
            'acctoutputoctets' : x.acctoutputoctets
        }

    sessions = itertools.imap(prepare, sessions)
    items = pipestat(sessions, geo_report_pipe)

    print items[0]
    return items
