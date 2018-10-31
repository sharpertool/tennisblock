from typing import List
from .MeetingStats import MeetingStats
from .round import MatchRound


class Meeting(MeetingStats):
    def __init__(self, n_courts, n_sets, men, women):
        super().__init__(n_courts, n_sets, men, women)
        self.rounds: List[MatchRound] = []

    def restart(self):
        self.rounds = []
        super().restart()

    def add_round(self, new_round):
        self.rounds.append(new_round)
        super().add_round(new_round)

    def round_count(self):
        return len(self.rounds)

    def get_rounds(self):
        return self.rounds
