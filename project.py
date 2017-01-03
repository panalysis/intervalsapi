__author__ = 'rodj'
import datetime
from distutils.util import strtobool
from performance_report import ProjectTypes, BillingTypes


class Project(object):
    projects = {}

    def __init__(self, data={}):
        self.id = 0
        self.local_id = None
        self.ownerid = 0
        self.name = None
        self.billable = True
        self.active = True
        self.date_start = None
        self.date_end = None
        self.budget = None
        self.client_id = None
        self.client = None
        self.project_type = None
        self.billing = None
        self.notes = []
        self.project_worktypes={}
        self.tasks = {}
        self.milestones = {}


        if 'id' in data and data['id'] is not None:
            self.id = int(data['id'])

        if 'localid' in data and data['localid'] is not None:
            self.local_id = int(data['localid'])

        if 'name' in data and data['name'] is not None:
            self.name = data['name']

        if 'billable' in data and data['billable'] is not None:
            self.billable = strtobool(data['billable'])

        if 'active' in data and data['active'] is not None:
            self.active = strtobool(data['active'])

        if 'datestart' in data and data['datestart'] is not None:
            self.date_start = self.__get_date__(data['datestart'])

        if 'dateend' in data and data['dateend'] is not None:
            self.date_end = self.__get_date__(data['dateend'])

        if 'clientid' in data and data['clientid'] is not None:
            self.client_id = data['clientid']

        if 'client' in data and data['client'] is not None:
            self.client = data['client']

        if 'budget' in data and data['budget'] is not None:
            self.budget = data['budget']

        Project.projects[self.id] = self



    def __get_date__(self,dateStr):
        my_dt = datetime.datetime.strptime(dateStr,"%Y-%m-%d")
        return datetime.date(my_dt.year,my_dt.month,my_dt.day)

    def add_note(self,note):
        self.notes.append(note)

        #if the project note title is Project Data then parse the record for settings.
        if note.title.lower() == "project data":
            self._parse_project_data(note.note)

    def add_worktype(self,worktype):
        self.project_worktypes[worktype.work_type_id] = worktype

    def get_worktype(self, work_type_id):
        if work_type_id in self.project_worktypes.keys():
            return self.project_worktypes[work_type_id]
        else:
            return None

    def _parse_project_data(self,text):
        lines = text.splitlines()
        for i in lines:
            parts = i.split(':')
            if len(parts)==2:
                if parts[0].lower() == 'type':
                    self.project_type = ProjectTypes.fromstring(parts[1].strip())
                if parts[0].lower() == 'billing':
                    self.billing = BillingTypes.fromstring(parts[1].strip())


    def get_projects_by_type(self,type):
        results = {}
        if len(Project.projects.keys()) > 0:
            for i,p in Project.projects.items():
                if p.project_type == type:
                    results[p.id] = p

        return results