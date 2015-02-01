#!/usr/bin/env python
#-*- coding: utf-8 -*-

from requests.auth import HTTPBasicAuth
from operator import itemgetter
import datetime
import requests
import time
import json
import sys
import os


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
            "current": self.get_current,
            "list_aliases": self.list_aliases,
            "add": self.add_alias,
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


    def _list_projects(self, args):
        result = self._beebole_request(api_request="project.list", form={
            "company": {"id": int(args[2])}}
            ).json()
        if result['status'] == "ok":
            for project in result['projects']:
                print "company: {}\n\t{} [SUBPROJECTS] {} [ID] {}".format(project['company']['name'], project['name'], project['subprojects']['count'], project['id'])
                tasks = self._beebole_request(api_request="time_entry.get_tasks", form={
                    "project": {"id": int(project['id'])},"date": now()
                    }).json()
                tasks = tasks['tasks']
                for task in tasks:
                    print "\t\t{} [ID] {}".format(task['name'], task['id'])

    def _list_companies(self, args):
        result =  self._beebole_request(api_request="company.list").json()
        if result['status'] == "ok":
            companies = sorted(result['companies'], key=itemgetter(u'name'))
            for company in companies:
                if len(args) > 1 and args[1] == "-s":
                    if company['name'].find(args[2]) != -1:
                        print u"{} [PROJECTS] {} [ID] = {}".format(company['name'],company['projects']['count'], company['id'])
                else: print u"{} [PROJECTS] {} [ID] = {}".format(company['name'],company['projects']['count'], company['id'])

            
    def list(self, args):
        """\tlist     
        \t'return list of all companies'\n\n\tlist -s <string>
        \t'search in all companies'"""
        if len(args) > 1 and args[1] == "-p":
           self._list_projects(args)
        else:
           self._list_companies(args)

    def register(self, project_id, task_id, project_comment):
        json.dump({
            "project_id": int(project_id),
            "task_id": int(task_id),
            "project_comment": project_comment,
            "ts_start": time.time()
        }, open(rel_path('activity.json'), 'wb'))

    def set(self, args):
        """\tset <project_alias>
        \t'set your current work to a project'"""
        if args[1] == "-r":
            activity = json.load(open(rel_path('activity.json'), 'rb'))
            activity_time = int(round(((time.time() - activity['ts_start']) / 3600), 0))
            self.get_current(None)
            print "TIME ~: {} hours".format(activity_time)
            request = {
                "project": {
                    "id": activity['project_id']
                },
                "task": {
                    "id": activity['task_id']
                },
                "date": now(),
                "hours": activity_time,
                "comment": activity['project_comment']
            }
            result = self._beebole_request(api_request="time_entry.create", form=request).json()
            return
        projects_name = args[1]
        aliases = json.load(open(rel_path('aliases.json'), 'rb'))
        if projects_name in aliases:
            project = aliases[projects_name]
            # register task activity
            self.register(project['project_id'], project['task_id'], project['project_comment'])

    def add_alias(self, args):
        """\tadd <alias_name> <project id> <task_id> <comment_optional>
        \t'add alias to set with alias_name the current project'"""
        name = args[1]
        project_id = int(args[2])
        task_id = int(args[3])
        project_comment = ""
        if len(args) > 3 : project_comment = " ".join(args[4:])
        aliases = json.load(open(rel_path('aliases.json'), 'rb'))
        aliases[name] = {
            "project_id": project_id,
            "task_id": task_id,
            "project_comment": project_comment
        }
        json.dump(aliases, open(rel_path('aliases.json'), 'wb'))

    def list_aliases(self, args):
        """\tlist _aliases
        \t'all aliases set with beebole add'"""
        aliases = json.load(open(rel_path('aliases.json'), 'rb'))
        for k,v in aliases.items():
            project = self._beebole_request(api_request="project.get", form={"id":v['project_id']}).json()['project']
            task = self._beebole_request(api_request="task.get", form={"id":v['task_id']}).json()['task']
            print "{} ==> {} {}".format(k, project['name'], task['name'])

    def get_current(self, args):
        """\tcurrent
        \t'get current project'"""
        current = json.load(open(rel_path('activity.json'), 'rb'))
        project = self._beebole_request(api_request="project.get", form={"id":current['project_id']}).json()
        task = self._beebole_request(api_request="task.get", form={"id":current['task_id']}).json()
        print "{} TASK: {}".format(project['project']['name'], task['task']['name'])

    def set_token(self, args):
        """\tset-token <token> <account_name>
        \t'set beebole token to authentication'"""
        save_token(args[1], args[2])

    def set_date(self, args):
        """\tset-date <start-date> <finish-date>
        \t'set your work date range hh:mm'"""
        pass



def now():
    now_time = datetime.datetime.now()
    return "{}-{}-{}".format(now_time.year, now_time.month, now_time.day)


def rel_path(path):
    return os.path.join( os.path.dirname(os.path.abspath(__file__)), path)


def load_token():
    with open(rel_path('app-token.json'), 'rb') as f:
        token = json.load(f)
        global TOKEN
        global ACCOUNT_NAME
        if token and 'app-token' in token:
            TOKEN = token['app-token']
            ACCOUNT_NAME = token['account_name']
            beebole.__init__()
            return True


def save_token(token, account_name):
    with open(rel_path('app-token.json'), 'wb') as f:
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
