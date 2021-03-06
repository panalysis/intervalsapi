__author__ = 'Rod Jacka, Leo Dunn'
__copyright__ = 'Copyright 2017, Panalysis PTY LTD'

import requests
from taskstatus import TaskStatus
from task import Task
from taskpriority import TaskPriority
from tasktime import TaskTime
# from project import Project
### Project object requires "performance_report" module ?

from project_note import ProjectNote
from project_worktype import ProjectWorktype
from milestone import Milestone

class Intervals():

    def __init__(self):
        self.uri = 'https://api.myintervals.com'
        self.user = '34w8rkqkyid'
        self.password = 'X'
        self.data = None
        self.__task_statuses = {}
        self.task_priority = {}
        self.get_task_statuses()
        self.get_task_priorities()

    def get_data(self, query):
        url = '/'.join([self.uri, query])
        print("Fetching " + url)
        response = requests.get(url, auth=(self.user, self.password))
        self.data = response.json()

        return self.data

    def get_task_statuses(self):
        results = self.get_data("taskstatus")
        if "taskstatus" in results:
            for t in results['taskstatus']:
                ts = TaskStatus(t)
                self.__task_statuses[ts.name] = ts
                 
    def get_task_priorities(self):
        results = self.get_data("taskpriority")
        if "taskpriority" in results:
            for t in results['taskpriority']:
                num_str = str(t['priority'])
                self.task_priority[num_str] = {
                    'name': t['name'],
                    'color': t['color']
                }

    def get_tasks(self,query=None):
        tasks = []
        req = "task/"
        if query is not None:
            req += "?" + query + '&limit=100'
        results = self.get_data(req)
        if "task" in results:
            for t in results['task']:
                tasks.append(Task(t))

        return tasks
        
    def get_last_date(self,task_id):
        req = "time/?taskid=%s&sortfield=t.date&sortdir=DESC" % task_id
        res = self.get_data(req)
        if (len(res['time'])> 0):
            raw_date = res['time'][0]['date']
            m,d,y = raw_date.split('/')
            return '-'.join((y,m,d))
        else:
            return 0
        
    def get_last_comment(self,task_id):
        req = "tasknote/?taskid=%s&sortfield=date&sortdir=DESC" % task_id
        res = self.get_data(req)
        if ('tasknote' in res):
            raw_date = res['tasknote'][0]['date']
            return raw_date.split(' ')[0]
        else:
            return 0

    def get_people(self,query=None):
        persons = []
        req = "person/"
        if query is not None:
            req += "?" + query
        results = self.get_data(req)
        if "person" in results:
            for t in results['person']:
                persons.append(t)
            return persons
        else:
            return 0
            
    def get_projects(self,query=None):
        projects = []
        req = "project/"
        if query is not None:
            req += "?" + query
        results = self.get_data(req)
        if "project" in results:
            for t in results['project']:
                projects.append(Project(t))

        return projects

    def get_project_notes(self,query=None):
        project_notes = []
        req = "projectnote/"
        if query is not None:
            req += "?" + query
        results = self.get_data(req)
        if "projectnote" in results:
            for t in results['projectnote']:
                project_notes.append(ProjectNote(t))

        return project_notes

    def get_project_worktypes(self,query=None):
        project_worktypes = []
        req = "projectworktype/"
        if query is not None:
            req += "?" + query
        results = self.get_data(req)
        if "projectworktype" in results:
            for t in results['projectworktype']:
                project_worktypes.append(ProjectWorktype(t))

        return project_worktypes

    def get_time(self,query=None):
        times = []
        req = "time/"
        if query is not None:
            req += "?" + query
        results = self.get_data(req)
        if "time" in results:
            for t in results['time']:
                times.append(TaskTime(t))

        return times

    def get_milestones(self,query=None):
        milestones = []
        req = "milestone/"
        if query is not None:
            req += "?" + query
        results = self.get_data(req)
        if "milestone" in results:
            for m in results['milestone']:
                milestones.append(Milestone(m))

        return milestones    