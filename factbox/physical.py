import itertools

from base import guidobject

class LocationObject(guidobject.GUIDObject):
    
    def __init__(self, loc=None):
        super(LocationObject, self).__init__()
        if loc is None:
            loc = (0, 0, 0)
        self.loc = loc
        
    def describe(self):
        return unicode(self.loc)

        
class NamedLocation(LocationObject):

    def __init__(self, name, loc=None, parent=None):
        super(NamedLocation, self).__init__(loc)
        self.name = unicode(name)
        self.children = set()
        self.connections = set()
        #self.parent = parent
        #self.parent.children.add(self)
        
    def describe(self, show_parents=False):
        if not show_parents:
            return self.name
        else:
            return u"%s (%s)" % (
                self.name, 
                self.parent.describe(show_parents=True)
            )

    #@property
    #def siblings(self, visible=None):
    #    return self.parent.children
    
    @property
    def connected_locations(self):
        return itertools.chain([c.locations for c in self.connections])
            

class LocationConnection(guidobject.GUIDObject):
    
    def __init__(self, connection_type=None, *locs):
        super(LocationConnection, self).__init__()
        self.locations = locs
        self.connection_type = connection_type and connection_type or 'open'
        for loc in locs:
            loc.connections.add(self)
