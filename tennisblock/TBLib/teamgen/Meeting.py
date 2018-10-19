from .MeetingStats import MeetingStats


class Meeting(MeetingStats):
    def __init__(self, n_courts, n_sets, men, women):
        super().__init__(n_courts, n_sets, men, women)
        self.sets = []
        self.n_curr_set_count = 0

    def restart(self):
        self.sets = []
        super().restart()

    def add_set(self, new_set):
        self.sets.append(new_set)
        super().add_set(new_set)

    def display(self):
        for index, blockset in enumerate(self.get_sets()):
            print("Set {index+1}")
            blockset.display()

    def set_count(self):
        return len(self.sets)

    def get_new_set(self, diff_max):
        self.n_curr_set_count = 0
        return super().get_new_set(diff_max)

    def get_sets(self):
        return self.sets

