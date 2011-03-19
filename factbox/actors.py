from datetime import datetime

from base import guidobject
from physical import NamedLocation

class Observable(guidobject.GUIDObject):
    
    def __init__(self, observers=None):
        super(Observable, self).__init__()
        if observers is None:
            observers = []
        self.observers = set(observers)
        self.invisible_to = set()

    def add_observer(self, obs):
        if obs not in self.observers:
            self.observers.add(obs)
            
    def remove_observer(self, obs):
        if obs in self.observers:
            self.observers.remove(obs)

    def notify_observers(self, verb, sub=None, obj=None, oth=None, invisibles=False, when=None, **kwargs):
        if sub is None:
            sub = self
        dt = kwargs.get("date", datetime.utcnow())
        action = verb.to_action(sub, obj, oth, dt)
        to_notify = self.observers
        if not invisibles:
            to_notify = set(to_notify) - set(self.invisible_to)
        for obs in to_notify:
            if obs.can_see(self):
                obs.notify(action)
            
    def hide_from(self, obs):
        if obs not in self.invisible_to:
            self.invisible_to.add(obs)
    
    
class Observer(guidobject.GUIDObject):
    
    def __init__(self, observing=None):
        super(Observer, self).__init__()
        if observing is None:
            observing = []
        self.observing = set(observing)
        self.seen = []
        
    def notify(self, action):
        self.seen.append(action)
        
    def observe(self, subject):
        subject.add_observer(self)
        
    def stop_observing(self, subject):
        subject.remove_observer(self)
        
    def describe(self):
        return u'observed %s actions' % (len(self.seen),)
        
    def can_see(self, other):
        return True
        

class Actor(guidobject.GUIDObject):
    
    def __init__(self, name=None, *args, **kwargs):
        super(Actor, self).__init__(*args, **kwargs)
        if not name:
            name = self.guid
        self._name = name
            
    def describe(self):
        return unicode(self.name)

    @property
    def name(self):
        return self._name
        
    def __unicode__(self):
        return self.name


class TwoWaySelfObserver(Observer, Observable):
    
    def __init__(self, observing=None, observers=None):
        super(TwoWaySelfObserver, self).__init__()
        self.done = []
        Observable.__init__(self, observers)
        Observer.__init__(self, observing)
        self.observe(self)
        
    def notify(self, action):
        if action.subject is self:
            if action not in self.done:
                self.done.append(action)
        else:
            if action not in self.seen:
                self.seen.append(action)
            
    def describe(self):
        return u'done %s actions, observed %s actions' % (
            len(self.done), 
            len(self.seen)
        )
        
    def query_seen(self, subject=None, verb=None):
        subject = getattr(subject, 'name', subject)
        verb = getattr(verb, 'name', verb)
        filtered = []
        if not (subject or verb):
            return filtered
        for mem in self.seen:
            if subject and subject != mem.subject.name:
                continue
            if verb and verb != mem.verb.name:
                continue
            filtered.append(mem)
        return filtered
        

class LocationActor(Actor):
    
    def __init__(self, location=None, *args, **kwargs):
        super(LocationActor, self).__init__(*args, **kwargs)
        self.location = location
        self.position = self.location and self.location.loc or (0, 0, 0)
                
    def goto(self, location, **kwargs):
        self.location = location
        self.position = self.location.loc
        
    def whereami(self):
        return self.location.describe()
        
    def can_see(self, other):
        if self == other:
            return True
        if other.location == self.location:
            return True
        if other.location in self.location.connected_locations:
            return True
        else:
            return False
            


class Thing(LocationActor, TwoWaySelfObserver):
    
    def __init__(self, name=None, location=None, observing=None, observers=None):
        super(Thing, self).__init__(observing=observing, observers=observers, name=name, location=location)
        
    def describe(self):
        return '%s, %s' % (
            self.describe(),
            self.whereami()
        )
        

class Humanoid(Thing):
    
    def do(self, verb, obj=None, **kwargs):
        dt = datetime.utcnow()
        func = getattr(self, verb.name, None)
        if func is not None:
            func(verb, obj, **kwargs)
        self.notify_observers(verb, obj=obj, date=dt, **kwargs)
        obj.notify_observers(verb, sub=self, obj=obj, date=dt, **kwargs)
    
    def describe(self, memory):
        return memory.describe()
        
    def greet(self, verb, obj=None, **kwargs):
        print "%s: %s %s" % (self.name, kwargs.get("oth", "hello"), obj.name)
        
        
class Creature(Humanoid):
    pass