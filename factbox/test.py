from actors import *
from verbs import *
from physical import *
from datetime import datetime

import unittest

class ActorTest(unittest.TestCase):
    
    def test_actor(self):
        a = Actor(name="test")
        self.assertEqual(a.name, "test")
        
        b = Actor()
        self.assertNotEqual(b.name, None)
        
    def test_locationactor(self):
        here = NamedLocation(name="home", loc=(2, 1, 0))
        a = LocationActor(name="test", location=here)
        self.assertEqual(a.name, "test")
        self.assertEqual(a.location.loc, (2, 1, 0))

    def test_observer(self):
        t = datetime.utcnow()
        obs1 = Observer()
        obs2 = Observer()
        obj = Observable()
        sub = Observable()
        verb = Verb("thing")

        obs1.observe(sub)
        obs2.observe(sub)
        sub.notify_observers(verb, sub, obj)

        self.assertEqual(len(sub.observers), 2)
        self.assertEqual(len(obs1.seen), 1)
        self.assertEqual(len(obs2.seen), 1)


    def test_selfobserver(self):
        t = datetime.utcnow()
        sub = TwoWaySelfObserver()
        obj = Observable()

        self.assertEqual(len(sub.observers), 1)
        self.assertEqual(len(sub.seen), 0)
        self.assertEqual(len(sub.done), 0)

        verb1 = Verb("something")        
        sub.notify_observers(verb1, sub, obj)

        self.assertEqual(len(sub.observers), 1)
        self.assertEqual(len(sub.seen), 0)
        self.assertEqual(len(sub.done), 1)
        self.assertEqual(sub.done[0].verb, verb1)
        
        obs = Observer()
        obs.observe(sub)
        
        verb2 = Verb("something else")
        sub.notify_observers(verb2, sub, obj)
        
        self.assertEqual(len(sub.observers), 2)
        self.assertEqual(len(sub.seen), 0)
        self.assertEqual(len(sub.done), 2)
        self.assertEqual(len(obs.seen), 1)
        self.assertEqual(sub.done[1].verb, verb2)
        self.assertEqual(obs.seen[0].verb, verb2)
        
        
    def test_thing(self):
        t = datetime.utcnow()
        here = NamedLocation("here", (2, 1, 0))
        there = NamedLocation("here", (3, 4, 5))
        sub = Thing("test", location=here)
        obj = Thing("test2", location=there)
        
        self.assertEqual(sub.name, "test")
        self.assertEqual(sub.location.loc, (2, 1, 0))


        self.assertEqual(len(sub.observers), 1)
        self.assertEqual(len(sub.seen), 0)
        self.assertEqual(len(sub.done), 0)

        verb1 = Verb("stuff")        
        sub.notify_observers(verb1, sub, obj)

        self.assertEqual(len(sub.observers), 1)
        self.assertEqual(len(sub.seen), 0)
        self.assertEqual(len(sub.done), 1)
        self.assertEqual(sub.done[0].verb, verb1)
        
        obs = Observer()
        obs.observe(sub)
        
        verb2 = Verb("other stuff")
        sub.notify_observers(verb2, sub, obj)
        
        self.assertEqual(len(sub.observers), 2)
        self.assertEqual(len(sub.seen), 0)
        self.assertEqual(len(sub.done), 2)
        self.assertEqual(len(obs.seen), 1)
        self.assertEqual(sub.done[1].verb, verb2)
        self.assertEqual(obs.seen[0].verb, verb2)
        
    #def test_location_scenario(self):
    #    a = LocationActor(name="test", loc=(2, 1, 0))
    #    self.assertEqual(a.name, "test")
    #    self.assertEqual(a.loc, (2, 1, 0))
    #    
        
    def test_scenario(self):
        
        park = NamedLocation("park", (20, 20, 0))
        home = NamedLocation("home", (0, 0, 0))
        
        alice = Humanoid("Alice", home)
        bob = Humanoid("Bob", home)
        cath = Humanoid("Cath", home)
        dog = Creature("Dog", home)
        ball = Thing("ball", home)
        
        greet = Verb("greet")
        watch = Verb("watch")
        listen = Verb("listen")
        chase = Verb("chase")
        give = Verb("give")
        reply = Verb("reply")
        kiss = Verb("kiss")
        avoid = Verb("avoid")
        
        cath.observe(alice)
        cath.observe(bob)
        cath.observe(dog)
        
        alice.do(greet, obj=bob, oth="'how do you do?'")        
        bob.do(listen, obj=alice)
        bob.do(reply, obj=alice, oth="'how do you do?'")
        alice.goto(park)
        bob.goto(park)
        cath.goto(park)
        dog.goto(park)
        bob.do(give, obj=dog, oth=ball)
        dog.do(chase, obj=ball)
        alice.do(watch, obj=dog, oth=dog.done[-1])
        
        alice.goto(home)
        bob.goto(home)
        
        bob.do(kiss, obj=alice, oth="at home alone")
        
        cath.goto(home)
        
        bob.hide_from(cath)
        alice.hide_from(cath)
        
        bob.do(kiss, obj=alice, oth="in secret")
        
        print "Cath saw:"
        for mem in cath.seen:
            print cath.describe(mem)
        print

        self.assertEqual(len(cath.seen), 6)
        
        
        print "Alice saw and did:"
        for mem in alice.seen + alice.done:
            print alice.describe(mem)
        print
        
        self.assertEqual(len(alice.seen), 4)
        self.assertEqual(len(alice.done), 2)
        
        print "Alice saw Bob:"
        for mem in alice.query_seen(bob):
            print alice.describe(mem)
        print
        
        self.assertEqual(len(alice.seen), 4)

        print "Alice saw kissing:"
        for mem in alice.query_seen(None, kiss):
            print alice.describe(mem)
        print

        self.assertEqual(len(alice.query_seen(None, kiss)), 2)
        
        self.assertEqual(len(alice.query_seen(dog)), 0)
        
        
        
if __name__ == '__main__':
    unittest.main()