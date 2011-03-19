from actors import *

import unittest

class EmotionalActorTest(unittest.TestCase):
    
    def test_actor(self):
        volatilities = {
            'manicdepressive': 0.6
        }
        
        intrinsics = {
            'intelligence': 0.9,
            'virtue': 0.8,
            'integrity': 0.8,
            'power': 0.5,
            'attractiveness': 0.75
        }
        
        a = EmotionalActor(
            name="test", 
            volatilities=volatilities,
            intrinsics=intrinsics
        )
        self.assertEqual(a.name, "test")
    
    def test_actor_relationship(self):
        volatilities = {
            'manicdepressive': 0.6
        }
        
        intrinsics = {
            'intelligence': 0.9,
            'virtue': 0.8,
            'integrity': 0.8,
            'power': 0.5,
            'attractiveness': 0.75
        }
        
        a = RelatingEmotionalActor(
            name="test", 
            volatilities=volatilities,
            intrinsics=intrinsics
        )
        self.assertEqual(a.name, "test")

        b = RelatingEmotionalActor(
            name="test2",
            volatilities=volatilities,
            intrinsics=intrinsics,            
        )
        self.assertEqual(b.name, "test2")
        
        a.relate_to(b)
        
        print
        print a.relationships[b.guid].describe()
            
if __name__ == '__main__':
    unittest.main()
