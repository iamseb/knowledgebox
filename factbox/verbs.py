from datetime import datetime

from base import guidobject
from utils import timesince

class Verb(guidobject.GUIDObject):
    
    def __init__(self, name):
        super(Verb, self).__init__()
        self._name = name
        
    def describe(self):
        return self.name
        
    def to_action(self, subject, obj, other, date):
        return Action(self, subject, obj, other, date)
        
    @property
    def name(self):
        return self._name
        
    def __unicode__(self):
        return self.name
        
class Action(guidobject.GUIDObject):
    
    def __init__(self, verb, sub=None, obj=None, oth=None, date=None):
        super(Action, self).__init__()
        if date is None:
            date = datetime.utcnow()
        elif type(date) != datetime:
            date = datetime(date)
        self.verb = verb
        self.subject = sub
        self.obj = obj
        self.other = oth
        self.date = date
                
        self.description = u'%s did %s to %s %s%s%s ago' % (
            self.subject,
            self.verb,
            self.obj,
            u"(%s) " % (self.other,) if self.other else '',
            u"at %s, " % (self.subject.whereami(),) if hasattr(self.subject, 'whereami') else '',
            timesince(self.date)
        )
        
    def __eq__(self, other):
        return (
            self.subject == other.subject and 
            self.obj == other.obj and
            self.verb == other.verb and
            self.other == other.other and
            self.date == other.date
        )
        
    def describe(self):
        return self.description
        
    def __unicode__(self):
        return self.describe()
        