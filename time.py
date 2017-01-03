__author__ = 'rodj'
import datetime
from distutils.util import strtobool


class Time(object):

    times = {}
    transaction_register = None

    def __init__(self, data={}):
        self.id = 0
        self.project_id = None
        self.task_id = None
        self.ownerid = 0
        self.date = None
        self.billable = False
        self.first_name = None
        self.last_name = None
        self.full_name = None
        self.task = None
        self.client = None
        self.project = None
        self.time = 0
        self.module = None
        self.work_type_id = None
        self.work_type = None
        self.description = None
        self.__allocated = False


        if 'id' in data and data['id'] is not None:
            self.id = int(data['id'])

        if 'projectid' in data and data['projectid'] is not None:
            self.project_id = int(data['projectid'])

        if 'taskid' in data and data['taskid'] is not None:
            self.task_id = int(data['taskid'])

        if 'task' in data and data['task'] is not None:
            self.task = data['task']

        if 'project' in data and data['project'] is not None:
            self.project = data['project']

        if 'client' in data and data['client'] is not None:
            self.client = data['client']

        if 'person' in data and data['person'] is not None:
            self.full_name = data['person']

        if 'firstname' in data and data['firstname'] is not None:
            self.first_name = data['firstname']

        if 'lastname' in data and data['lastname'] is not None:
            self.last_name = data['lastname']

        if 'dateiso' in data and data['dateiso'] is not None:
            self.date = self.__get_date__(data['dateiso'])

        if 'time' in data and data['time'] is not None:
            self.time = float(data['time'])

        if 'module' in data and data['module'] is not None:
            self.module = data['module']

        if 'billable' in data and data['billable'] is not None:
            self.billable = strtobool( data['billable'])

        if 'description' in data and data['description'] is not None:
            self.description = data['description']

        if 'worktypeid' in data and data['worktypeid'] is not None:
            self.work_type_id = int(data['worktypeid'])

        Time.times[self.id] = self


    def __get_date__(self,dateStr):
        my_dt = datetime.datetime.strptime(dateStr,"%Y-%m-%d")
        return datetime.date(my_dt.year,my_dt.month,my_dt.day)



    def get_times(consultant="",date_from=None, date_to=None, project_id=0, task_id=0):

        time_by_date = []
        set_s = []
        if date_from is not None and date_to is not None:
            for i,t in Time.times.items():
                if t.date >= date_from and t.date <= date_to:
                    time_by_date.append(t.id)
            set_s.append(set(time_by_date))

        time_by_consultant = []
        if consultant != "":
            for i,t in Time.times.items():
                if t.full_name.lower() == consultant.lower():
                    time_by_consultant.append(t.id)
            set_s.append(set(time_by_consultant))

        time_by_project = []
        if project_id != 0:
            for i,t in Time.times.items():
                if t.project_id == project_id:
                    time_by_project.append(t.id)
            set_s.append(set(time_by_project))

        time_by_task = []
        if task_id != 0:
            for i,t in Time.times.items():
                if t.task_id == task_id:
                    time_by_task.append(t.id)
            set_s.append(set(time_by_task))

        res = None
        for i in range(0, len(set_s)):
            if len(set_s)==1:
                res = set_s[0]
            elif i==0 and len(set_s)>1:
                res = set_s[0].intersection(set_s[1])
            elif i < len(set_s):
                res = res.intersection(set_s[i])

        result = []
        if res is not None and len(res)>0:
            for i in list(res):
                result.append(Time.times[i])

        return result

    def get_time_summary(consultant="",date_from=None, date_to=None, project_id=0, task_id=0):
        times = Time.get_times(consultant=consultant,date_from=date_from, date_to=date_to, project_id=project_id, task_id=task_id)
        result = {}

        for t in times:
            # set the allocated time
            #Time.times[t.id].__allocated=True
            # if Time.transaction_register is not None:
            #     billable_hours = 0
            #     non_billable_hours = 0
            #     if t.billable:
            #         billable_hours = t.time
            #     else:
            #         non_billable_hours = t.time
            #     insert_id = Time.transaction_register.register_time(date=t.date,
            #                                                         consultant=t.full_name,
            #                                                         timesheet_id=t.id,
            #                                                         task=t.task,
            #                                                         project=t.project,
            #                                                         description=t.description,
            #                                                         billable_hours=billable_hours,
            #                                                         non_billable_hours=non_billable_hours)

            if t.full_name not in result.keys():
                if t.work_type is not None:
                    rate = t.work_type.hourly_rate
                else:
                    rate = 0

                result[t.full_name] = {
                    'billable'      : 0,
                    'non-billable'  : 0,
                    'rate'          : rate,
                    'allocation'    : 0,
                    'timesheet_ids' : []
                }

            result[t.full_name]['timesheet_ids'].append(t.id)
            if t.billable:
                result[t.full_name]['billable'] = result[t.full_name]['billable'] + t.time
            else:
                result[t.full_name]['non-billable'] = result[t.full_name]['billable'] + t.time

        return result

    def get_unallocated_time(date_from=None, date_to=None, project_id=0):

        times = Time.get_times(date_from=date_from, date_to=date_to, project_id=project_id)

        res = []
        for t in times:
            if not t.__allocated:
                res.append(t)

        return res
