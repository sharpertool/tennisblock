from .MeetingStats import MeetingStats


class Meeting(object):
    def __init__(self, n_courts, nSets, men, women):
        self.n_courts = n_courts
        self.nSets = nSets
        self.men = men
        self.women = women
        self.sets = []

        self.ms = MeetingStats(n_courts, nSets, men, women)

    def restart_meeting(self):
        self.ms.restart()
        self.sets = []

    def set_see_partner_once(self, b_allow_duplicates):
        """
        Set value on meeting stats object.
        :param b_allow_duplicates:
        :return:
        """
        self.ms.set_see_partner_once(b_allow_duplicates)

    def add_set(self, blockset):
        self.sets.append(blockset)
        self.ms.add_set(blockset)

    def display(self):
        for index, blockset in enumerate(self.ms.get_sets()):
            print("Set {index+1}")
            blockset.display()

    def SetCount(self):
        return len(self.sets)

    def Check(self, set, diffMax):
        return self.ms.Check(set, diffMax)

    def get_new_set(self, diffMax):
        self.ms.set_curr_set_count(len(self.sets))
        return self.ms.get_new_set(diffMax)

    def print_check_stats(self):
        self.ms.print_check_stats()

    def diff_history_min(self):
        return self.ms.diff_history_min()
