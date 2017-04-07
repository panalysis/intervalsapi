__author__ = 'Rod Jacka'
__copyright__ = 'Copyright 2017, Panalysis PTY LTD'

class ProjectNote(object):

    def __init__(self, data={}):
        self.id = 0
        self.local_id = None
        self.client_id = None
        self.project_id = None
        self.title = ""
        self.note = ""

        if 'id' in data:
            self.id = int(data['id'])
        if 'localid' in data:
            self.local_id = data['localid']
        if 'clientid' in data:
            self.client_id = data['clientid']
        if 'projectid' in data:
            self.project_id = int(data['projectid'])
        if 'title' in data:
            self.title = data['title']
        if 'note' in data:
            self.note = data['note']