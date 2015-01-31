#!/usr/bin/env python
#-*- coding: utf-8 -*-

from requests.auth import HTTPBasicAuth
from operator import itemgetter
import requests
import json
import sys


TOKEN = ""
ACCOUNT_NAME = ""

class BeeboleApiManager(object):
    
    def __init__(self):
        self.auth = HTTPBasicAuth(TOKEN, "x")
        self.beeboleUrl = "https://{}.beebole-apps.com/api/v2".format(ACCOUNT_NAME)
        self.apiService = {
            "list": self.list,
            "set": self.set,
            "set_token": self.set_token,
            "set_date": self.set_date,
            "?": self.help
        }

    def _beebole_request(self, api_request, form={}, success='', error=''):
        """ try a request """
        form['service'] = api_request
        form = json.dumps(form)
        try:
            request_result = requests.post(
                auth=self.auth,
                url=self.beeboleUrl,
                data=form
            )
        except Exception, e:
            sys.exit(e)
        if request_result.status_code in [200, 201]:
            print success
        elif request_result.status_code == 401:
            sys.exit("ERROR: " + request_result.reason + " maybe you are set wrong token or account name, type beebole set_token <your-token> <your_account_name> to change it")
        else:
            sys.exit("ERROR: " + request_result.reason)
        return request_result

    def help(self, args):
        """\t?
        \t'help'"""
        print "Usage:"
        for key, method in self.apiService.items():
            print method.__doc__
            print
        sys.exit()
            
    def list(self, args):
        """\tlist     
        \t'return list of all companies'\n\n\tlist -s <string>
        \t'earch in all companies'"""
        result =  self._beebole_request(api_request="company.list").json()
        if result['status'] == "ok":
            companies = sorted(result['companies'], key=itemgetter(u'name'))
            for company in companies:
                if len(args) > 1 and args[1] == "-s":
                    if company['name'].find(args[2]) != -1:
                        print u"{}".format(company['name'])
                else: print u"{}".format(company['name'])

    def set(self, args):
        """\tset <project_name>
        \t'set your current work to a project'"""
        project_name = " ".join(args[1:])
        print project_name

    def set_token(self, args):
        """\tset-token <token> <account_name>
        \t'set beebole token to authentication'"""
        save_token(args[1], args[2])

    def set_date(self, args):
        """\tset-date <start-date> <finish-date>
        \t'set your work date range hh:mm'"""
        pass


def load_token():
    with open('app-token.json', 'rb') as f:
        token = json.load(f)
        global TOKEN
        global ACCOUNT_NAME
        if token and 'app-token' in token:
            TOKEN = token['app-token']
            ACCOUNT_NAME = token['account_name']
            beebole.__init__()
            return True


def save_token(token, account_name):
    with open('app-token.json', 'wb') as f:
        json.dump({'app-token': token, 'account_name': account_name}, f)
    load_token()


beebole = BeeboleApiManager()
def main():
    cmd = sys.argv[1:]
    

    if len(cmd) < 1:
        beebole.help("")

    if not load_token():
        print "please insert your api token and your account_name to authorize this application"
        token = raw_input("token: ")
        account_name = raw_input("account name: ")
        save_token(token, account_name)
    
    beebole.apiService.get(cmd[0], beebole.help)(cmd)


if __name__ == '__main__':
    main()
