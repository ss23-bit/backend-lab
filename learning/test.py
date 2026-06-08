class LoginTracker:
    def __init__(self):
        
        self.counts = {}
    def failed_login(self, name):
        self.counts[name] = self.counts.get(name, 0) + 1
        return self.counts[name]

tracker = LoginTracker()

tracker.failed_login("alice")
tracker.failed_login("alice")
tracker.failed_login("bob")

print(tracker.failed_login("joe"), tracker.failed_login("joe"))