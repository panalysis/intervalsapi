__author__ = 'rodj'

import requests
from .taskstatus import TaskStatus
from .task import Task
from .time import Time
from .project import Project
from .project_note import ProjectNote
from .project_worktype import ProjectWorktype
from .milestone import Milestone

class Intervals():

    def __init__(self):
        self.uri = 'https://api.myintervals.com'
        self.user = '34w8rkqkyid'
        self.password = 'X'
        self.data = None
        self.__task_statuses = {}

        # update the list of task statuses
        self.get_task_statuses()

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

    def get_tasks(self,query=None):
        tasks = []
        req = "task/"
        if query is not None:
            req += "?" + query
        results = self.get_data(req)
        if "task" in results:
            for t in results['task']:
                tasks.append(Task(t))

        return tasks

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
                times.append(Time(t))

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