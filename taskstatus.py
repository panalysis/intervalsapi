__author__ = 'rodj'

class TaskStatus(object):

    def __init__(self, data=None):
        self.priority = None
        self.__frozen = None
        self.__active = None
        self.id = 0
        self.name = None

        if 'id' in data:
            self.id = data['id']
        if 'name' in data:
            self.name = data['name']


    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self,val):
        if val == 't':
            self.__active = True
        else:
            self.__active = False