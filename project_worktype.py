
from distutils.util import strtobool

class ProjectWorktype(object):
    project_worktypes = {}

    def __init__(self, data={}):
        self.id = 0
        self.local_id = None
        self.project_id = None
        self.work_type_id = 0
        self.name = ""
        self.hourly_rate = 0
        self.estimated_time = 0
        self.active = True
        self.total = 0

        if 'id' in data:
            self.id = int(data['id'])
        if 'worktypeid' in data:
            self.work_type_id = int(data['worktypeid'])
        if 'projectid' in data:
            self.project_id = int(data['projectid'])
        if 'worktype' in data:
            self.name = data['worktype']
        if 'hourlyrate' in data:
            self.hourly_rate = float(data['hourlyrate'])
        if 'active' in data:
            self.active = strtobool(data['active'])
        if 'esttime' in data:
            self.estimated_time = float(data['esttime'])
        if 'total' in data:
            self.total = float(data['total'])

        if self.id > 0:
            ProjectWorktype.project_worktypes[self.id] = self