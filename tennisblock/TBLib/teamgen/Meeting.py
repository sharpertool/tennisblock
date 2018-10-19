from typing import List
from .MeetingStats import MeetingStats
from .Set import Set


class Meeting(MeetingStats):
    def __init__(self, n_courts, n_sets, men, women):
        super().__init__(n_courts, n_sets, men, women)
        self.sets: List[Set] = []

    def restart(self):
        self.sets = []
        super().restart()

    def add_set(self, new_set):
        self.sets.append(new_set)
        super().add_set(new_set)

    def set_count(self):
        return len(self.sets)

    def get_sets(self):
        return self.sets

    def display_update(self, n_tries, diff):
        print(f"Assigned men. "
              f"Try to assign women. "
              f"Seqs:{len(self.sets)} "
              f"Try:{n_tries} Diff={diff:4.2}"
              )
