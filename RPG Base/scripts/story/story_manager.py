from scripts.story.trigger import Trigger
from scripts.story.text_box import TextBox

class StoryManager():
    def __init__(self):
        self.event = None
        self.spent_events = []

    def update_triggers(self, triggers, player):
        for trigger in triggers:
            if trigger not in self.spent_events:
                if player.rect.colliderect(trigger.rect): # only deal with 1 trigger at a time
                    self.do_event(trigger.pass_event())
                    self.spent_events.append(trigger) # or just delete spent events, or use hashmap lookup
                    print(self.event)
                    break


    def do_event(self, event):
        pass

class Event():
    def __init__(self):
        pass
        


