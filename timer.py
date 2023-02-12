# timer class, makes managing a bunch of game timers much easier
# A timer can be started, stopped, and checked for current status
class timer:
    def __init__(self, actor, count):
        self.actor = actor
        self.count = count
        self.init_count = count
        self.active = 0

    def start(self):
        self.active = 1
        self.count = self.init_count

    def stop(self):
        self.active = 0

    def reset(self):
        self.active = 0
        self.count = self.init_count

    def pause(self):
        self.active = 0

    def is_active(self):
        return self.active ==1

    def is_expired(self):
        return (self.count == 0)

    def advance(self):
        if (self.active and self.count>0):
            self.count -= 1
        elif (self.count == 0):
            self.active = 0
