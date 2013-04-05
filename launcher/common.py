#
# some common code...
#

import json
import requests
import subprocess
import sys


def get_vo_info():
    # get VO information
    try:
        vo_info = subprocess.check_output('voms-proxy-info -vo -path',
                                          shell=True,
                                          stderr=subprocess.STDOUT)
        proxy, vo_name = vo_info.split()
    except subprocess.CalledProcessError:
        print >> sys.stderr, "Not able to get proxy info..."
        sys.exit(1)
    print "Using proxy file at %s for VO %s" % (proxy, vo_name)
    return proxy, vo_name


def keystone_auth(ks_uri, proxy, vo_name):
    print "Authenticating against %s" % ks_uri
    r = requests.post(ks_uri + 'v2.0/tokens',
                      headers={'content-type': 'application/json',
                               'accept': 'application/json', },
                      data=json.dumps({'auth': {'tenantName': vo_name,
                                                'voms': True}
                                       }),
                      cert=proxy,
                      verify=False)
    if r.status_code != 200:
        print >> sys.stderr, "Something went wrong, out!"
        sys.exit(1)
    try:
        return r.json()['access']['token']['id']
    except KeyError:
        print >> sys.stderr, "Something went wrong, out!"
        sys.exit(1)
