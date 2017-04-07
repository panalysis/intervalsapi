__author__ = 'Rod Jacka'
__copyright__ = 'Copyright 2017, Panalysis PTY LTD'

import datetime
from distutils.util import strtobool

class Milestone(object):
    milestones = {}

    def __init__(self, data={}):
        self.id = 0
        self.local_id=0
        self.project_id=0
        self.title = ""
        self.date_due = None
        self.description = ""
        self.complete = False
        self.tasks = {}

        if 'id' in data and data['id'] is not None:
            self.id = int(data['id'])

        if 'localid' in data and data['localid'] is not None:
            self.local_id = int(data['localid'])

        if 'projectid' in data and data['projectid'] is not None:
            self.project_id = int(data['projectid'])

        if 'complete' in data:
            self.complete = strtobool(data['complete'])

        if 'title' in data:
            self.title = data['title']

        if 'description' in data:
            self.description = data['description']

        Milestone.milestones[self.id] = self

    def get_time_summary_by_consultant(self):
        data = {}
        for k,task in self.tasks.items():
            for p,t in task.consultant_time.items():
                if p not in data.keys(): data[p] = {'billable': 0, 'non-billable': 0}
                for i in t:
                    if i.billable:
                        data[p]['billable'] = data[p]['billable'] + i.time
                    else:
                        data[p]['non-billable'] = data[p]['non-billable'] + i.time

        return data