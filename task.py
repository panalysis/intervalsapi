__author__ = 'rodj'
import datetime

class Task(object):

    tasks = {}

    def __init__(self, data={}):
        self.id = 0
        self.queueid = None
        self.color = None
        self.project_id = None
        self.clientid = None
        self.dateclosed = None
        self.ownerid = 0
        self.billable = 0.0
        self.unbillable = 0.0
        self.statusid = 0
        self.severity = None
        self.title = None
        self.priority = 0
        self.followers = []
        self.status = 0
        self.assigneeid = []
        self.clientlocalid = 0
        self.datedue = None
        self.dateopen = None
        self.module = None
        self.milestone = None
        self.estimate = 0.0
        self.followerid = []
        self.datemodified = None
        self.owners = []
        self.actual = 0
        self.local_id = 0
        self.projectlocalid = 0
        self.summary = None
        self.project = None
        self.assignees = []
        self.client = None
        self.milestone_id = 0
        self.moduleid = None
        self.statusorder = None
        self.consultant_time = {}

        if 'id' in data and data['id'] is not None:
            self.id = int(data['id'])

        if 'queueid' in data and data['queueid'] is not None:
            self.queueid = int(data['queueid'])

        if 'colour' in data:
            self.color  = data['color']

        if 'projectid' in data and data['projectid'] is not None:
            self.project_id = int(data['projectid'])

        if 'clientid' in data and data['clientid'] is not None:
            self.clientid = int(data['clientid'])

        if 'dateclosed' in data and data['dateclosed'] is not None:
            self.dateclosed = self.__get_date__(data['dateclosed'])

        if 'ownerid' in data and data['ownerid'] is not None:
            self.ownerid = data['ownerid']

        if 'billable' in data and data['billable'] is not None:
            self.billable = float(data['billable'])

        if 'unbillable' in data and data['unbillable'] is not None:
            self.unbillable = float(data['unbillable'])

        if 'statusid' in data and data['statusid'] is not None:
            self.statusid = int(data['statusid'])

        if 'severity' in data:
            self.severity = data['severity']

        if  'title' in data:
            self.title = data['title']

        if  'priority' in data and data['priority'] is not None:
            self.priority = int(data['priority'])

        if  'followers' in data and data['followers'] is not None:
            self.followers = data['followers'].split(',')

        if  'status' in data:
            self.status = data['status']

        if  'assigneeid' in data and data['assigneeid'] is not None:
            self.assigneeid = data['assigneeid'].split(',')

        if  'assignees' in data and data['assignees'] is not None:
            self.assignees = data['assignees'].split(',')

        if  'clientlocalid' in data and data['clientlocalid'] is not None:
            self.clientlocalid = int(data['clientlocalid'])

        if  'datedue' in data and data['datedue'] is not None:
            self.datedue = self.__get_date__(data['datedue'])

        if  'dateopen' in data and data['dateopen'] is not None:
            self.dateopen = self.__get_date__(data['dateopen'])

        if  'datemodified' in data and data['datemodified'] is not None:
            self.datemodified = datetime.datetime.strptime(data['datemodified'],"%Y-%m-%d %H:%M:%S")

        if  'module' in data:
            self.module = data['module']

        if  'milestone' in data:
            self.milestone = data['milestone']

        if  'milestoneid' in data and data['milestoneid'] is not None:
            self.milestone_id = int(data['milestoneid'])

        if  'estimate' in data and data['estimate'] is not None:
            self.estimate = float(data['estimate'])

        if  'actual' in data and data['actual'] is not None:
            self.actual = float(data['actual'])

        if  'followerid' in data and data['followerid'] is not None:
            self.followerid = data['followerid'].split(',')

        if  'owners' in data and data['owners'] is not None:
            self.owners = data['owners'].split(',')

        if  'localid' in data and data['localid'] is not None:
            self.local_id = int(data['localid'])

        if  'localprojectid' in data and data['localprojectid'] is not None:
            self.localprojectid = int(data['localprojectid'])

        if  'summary' in data:
            self.summary = data['summary']

        if  'project' in data:
            self.project = data['project']

        if  'client' in data:
            self.client = data['client']

        if  'status_order' in data:
            self.statusorder = data['status_order']

        Task.tasks[self.id] = self

    def add_time(self,t):
        if t.full_name not in self.consultant_time.keys():
            self.consultant_time[t.full_name] = []

        self.consultant_time[t.full_name].append(t)

    def get_time_summary_by_consultant(self):
        data = {}

        for p,t in self.consultant_time.items():
            if p not in data.keys(): data[p] = {'billable': 0, 'non-billable': 0}
            for i in t:
                if i.billable:
                    data[p]['billable'] = data[p]['billable'] + i.time
                else:
                    data[p]['non-billable'] = data[p]['non-billable'] + i.time

        return data

    def get_remaining_time(self):
        remaining = 0
        if self.estimate > self.actual:
            remaining = self.estimate - self.actual

        return remaining

    def get_remaining_time_per_consultant(self):
        remaining = self.get_remaining_time()
        num_assignees =  len(self.assignees)
        if num_assignees > 1:
            remaining = remaining/len(self.assignees)

        return remaining

    def get_average_hours_per_day(self):
        remaining = self.get_remaining_time()
        if isinstance(self.datedue,datetime.date):
            days = self.get_num_work_days()
            if days >0:
                return remaining/days
            return remaining
        else:
            return None

    def get_average_hours_per_day_per_consultant(self):
        remaining = self.get_remaining_time_per_consultant()
        if isinstance(self.datedue, datetime.date):
            days = self.get_num_work_days()
            if days > 0:
                return remaining/days
            else:
                return remaining
        else:
            return None

    def get_num_work_days(self):
        start_date = datetime.date.today()
        if isinstance(self.dateopen, datetime.date) and self.dateopen>datetime.date.today():
            start_date = self.dateopen

        # if the due date has past then calculate based on the next 7 days
        if self.datedue < datetime.date.today():
            self.datedue = datetime.date.today()+ datetime.timedelta(days=7)

        if isinstance(self.datedue, datetime.date):
            daygenerator = (start_date + datetime.timedelta(x + 1) for x in range((self.datedue - start_date).days))
            num_days = sum(1 for day in daygenerator if self.__is_work_day__(day))
            return num_days
        else:
            return 0

    def get_work_days(self):
        start_date = datetime.date.today()

        if isinstance(self.dateopen, datetime.date) and self.dateopen > datetime.date.today():
            start_date = self.dateopen

        if isinstance(self.datedue, datetime.date) and self.datedue > datetime.date.today():
            end_date = self.datedue
        else:
            end_date = start_date + datetime.timedelta(days=7)

        res = {}
        daily_hours_consultant = self.get_average_hours_per_day_per_consultant()
        daily_hours = self.get_average_hours_per_day()

        if isinstance(self.dateopen, datetime.date) and self.dateopen>datetime.date.today():
            start_date = self.dateopen

        if end_date < datetime.date.today():
            end_date = datetime.date.today()+ datetime.timedelta(days=7)

        if isinstance(self.datedue, datetime.date):
            daygenerator = (start_date + datetime.timedelta(x + 1) for x in range((end_date - start_date).days))
            for day in daygenerator:
                if self.__is_work_day__(day):
                    res[day] = {
                        "date": day,
                        "task_id": self.id,
                        "task_name": self.title,
                        "hours_per_day": daily_hours,
                        "hours_per_consultant": daily_hours_consultant
                    }

        return res

    def __is_work_day__(self,day):
        if day.weekday() < 5:
            return True
        else:
            return False


    def __get_date__(self,dateStr):
        my_dt = datetime.datetime.strptime(dateStr,"%Y-%m-%d")
        return datetime.date(my_dt.year,my_dt.month,my_dt.day)