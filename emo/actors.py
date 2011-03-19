from base import guidobject

class EmotionalState(guidobject.GUIDObject):

    MOODS = [
        'joy',
        'anger',
        'fear',
        'arousal',
        'intrigue',
    ]
    
    def __init__(self, owner, perceived_of=None, reaction_to=None, **kwargs):
        super(EmotionalState, self).__init__(**kwargs)
        self.owner = owner
        self.perceived_of = perceived_of
        self.reaction_to = reaction_to
        for mood in EmotionalState.MOODS:
            setattr(self, mood, kwargs.get(mood, 0.0))
            
    def describe(self, include_owner=False, joinchar=u", "):
        emos = [u"%s (%2f)" % (mood, getattr(self, mood)) for mood in EmotionalState.MOODS]
        if include_owner:
            resp = u"%s feels %s" % (self.owner, ", ". join(emos))
        else:
            resp = joinchar.join(emos)

        if self.perceived_of:
            resp = resp + u" about %s" % (self.perceived_of,)
        if self.reaction_to:
            resp = resp + u" about %s" % (self.reaction_to,)
        return resp
        
    def __unicode__(self):
        return self.describe(include_owner=True)
        

class IntrinsicState(guidobject.GUIDObject):
    
    INTRINSICS = [
        'intelligence',
        'integrity',
        'power',
        'attractiveness',
        'virtue',
    ]

    def __init__(self, owner, perceived_of=None, **kwargs):
        super(IntrinsicState, self).__init__(**kwargs)      
        self.owner = owner
        self.perceived_of = perceived_of
        for attr in IntrinsicState.INTRINSICS:
            setattr(self, attr, kwargs.get(attr, 0.0))

    def describe(self, include_owner=False, joinchar=u", "):
        emos = [u"%s (%2f)" % (mood, getattr(self, mood)) for mood in IntrinsicState.INTRINSICS]
        if include_owner:
            resp = u"%s feels %s" % (self.owner, ", ". join(emos))
        else:
            resp = joinchar.join(emos)            
        if self.perceived_of:
            resp = resp + u" about %s" % (self.perceived_of,)
        return resp
        
    def __unicode__(self):
        return self.describe(include_owner=True)        


class VolatilityState(guidobject.GUIDObject):

    VOLATILITIES = [
        'adrenaline', # modulates anger and fear responses
        'manicdepressive', # modulates joy responses
        'sensuality', # modulates arousal responses
        'curiosity', # modulates intrigue responses
    ]
    
    def __init__(self, owner, perceived_of=None, **kwargs):
        super(VolatilityState, self).__init__(**kwargs) 
        self.owner = owner
        self.perceived_of = perceived_of
        for vol in VolatilityState.VOLATILITIES:
            setattr(self, vol, kwargs.get(vol, 0.0))

    def describe(self, include_owner=False, joinchar=u", "):
        emos = [u"%s (%2f)" % (mood, getattr(self, mood)) for mood in VolatilityState.VOLATILITIES]
        if include_owner:
            resp = u"%s feels %s" % (self.owner, ", ". join(emos))
        else:
            resp = joinchar.join(emos)
        if self.perceived_of:
            resp = resp + u" about %s" % (self.perceived_of,)
        return resp
        
    def __unicode__(self):
        return self.describe(include_owner=True)

            
class BaseEmotionalActor(guidobject.GUIDObject):
    
    def __init__(self, **kwargs):
        super(BaseEmotionalActor, self).__init__(**kwargs)
        base_mood = kwargs.get('base_mood', {})
        intrinsics = kwargs.get('intrinsics', {})
        volatilities = kwargs.get('volatilities', {})
        accord_intrinsics = kwargs.get('accord_intrinsics', {})

        
        self.base_mood = EmotionalState(self, **base_mood)
        self.current_mood = EmotionalState(self, **base_mood)
        self.intrinsics = IntrinsicState(self, **intrinsics)
        self.volatilities = VolatilityState(self, **volatilities)
        self.accord_intrinsics = IntrinsicState(self, **accord_intrinsics)


class EmotionalActor(BaseEmotionalActor):

    template = """My name is %s.
My attributes are:
    %s.
Currently I feel:
    %s.
My moods are changeable based on:
    %s."""
    
    def __init__(self, name, *args, **kwargs):
        super(EmotionalActor, self).__init__(*args, **kwargs)
        self.name = name

    def describe(self):            
        output = self.template % (
            self.name,
            self.intrinsics.describe(joinchar=u",\n    "),
            self.current_mood.describe(joinchar=u",\n    "),
            self.volatilities.describe(joinchar=u",\n    ")
        )
        
        return output

    def __unicode__(self):
        return self.name
        
        
class MentalModel(BaseEmotionalActor):
    
    template = """This is what {owner} thinks of {modelled}.
{modelled}'s attributes are:
    {intrinsics}
{modelled} probably feels:
    {current_mood}
{modelled} changes their moods based on:
    {volatilities}"""
    
    def __init__(self, owner, modelled, *args, **kwargs):
        super(MentalModel, self).__init__(*args, **kwargs)
        self.owner = owner
        self.modelled = modelled
        
    def describe(self):            
        output = self.template.format(
            owner=self.owner.name,
            modelled=self.modelled.name,
            intrinsics=self.intrinsics.describe(joinchar=u",\n    "),
            current_mood=self.current_mood.describe(joinchar=u",\n    "),
            volatilities=self.volatilities.describe(joinchar=u",\n    ")
        )
        
        return output

    def __unicode__(self):
        return self.name
        
        
class RelatingEmotionalActor(EmotionalActor):
    
    def __init__(self, *args, **kwargs):
        super(RelatingEmotionalActor, self).__init__(*args, **kwargs)
        self.relationships = {}
    
    def relate_to(self, other, model=None):
        if model is None:
            model = MentalModel(self, other)
        self.relationships[other.guid] = model
        

# end
