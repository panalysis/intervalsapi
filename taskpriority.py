__author__ = 'Leo Dunn'
__copyright__ = 'Copyright 2017, Panalysis PTY LTD'
__credits__ = ['Rod Jacka']

class TaskPriority(object):

    def __init__(self, data=None):
        
        self.name = None
        self.number = None
        self.color = None
        
        if ('name' in data):
            self.name = data['name']
        else:
            self.name = 'None: %d' % str(data['priority'])
            
        if ('priority' in data):
            self.number = data['priority']
            
        if ('color' in data):
            self.color = data['color']