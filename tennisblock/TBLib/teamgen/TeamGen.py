from .Meeting import Meeting


class TeamGen(object):
    def __init__(self, courts, num_seq, men, women):
        self.n_courts = courts
        self.meeting = Meeting(courts, num_seq, men, women)
        self.diffMax = 0.1
        self.MaxBadDiff = 1.0
        self.n_sequences = num_seq
        self.iterLimit = 1000

    def generate_set_sequences(self, b_allow_duplicates):
        self.meeting.restart_meeting()
        diff_max = 0.1

        self.meeting.set_see_partner_once(b_allow_duplicates)

        while self.meeting.SetCount() < self.n_sequences:
            set = None

            while diff_max <= 2.8 and set is None:
                set = self.meeting.get_new_set(diff_max)

                if set is None:
                    diff_max = self.meeting.diff_history_min()
                    print("DiffMax Increased to %5.3f" % diff_max)

            if set is None:
                self.meeting.print_check_stats()
                print("Failed to build the sequence.")
                return None
            else:
                set.display()
                d_max, d_avg, diff_list = set.diff_stats()
                diffs = ",".join(["%5.3f" % x for x in diff_list])
                print("Found a set sequence with DiffMax:%5.3f Max:%3.3f Avg:%5.3f List:%s" % (
                    self.diffMax, d_max, d_avg, diffs))
                self.meeting.add_set(set)

        return self.meeting.sets

    def display_sequences(self, seq):
        for s in seq:
            s.display()

    def show_all_diffs(self, seq):
        [s.show_diffs() for s in seq]
