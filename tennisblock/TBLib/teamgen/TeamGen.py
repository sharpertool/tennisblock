from .Meeting import Meeting


class TeamGen(object):
    def __init__(self, courts, num_seq, men, women):
        self.n_courts = courts
        self.meeting = Meeting(courts, num_seq, men, women)
        self.diff_max = 0.1
        self.MaxBadDiff = 1.0
        self.n_sequences = num_seq
        self.iterLimit = 1000

    def generate_set_sequences(self, b_allow_duplicates=False):
        self.meeting.restart()

        self.meeting.set_see_partner_once(not b_allow_duplicates)

        while self.meeting.round_count() < self.n_sequences:
            round = None
            diff_max = 0.1

            while diff_max <= 1.0 and round is None:
                max_quality = 1.0
                while max_quality < 2.5 and round is None:
                    round, min_found_diff, min_found_q = self.meeting.get_new_round(
                        diff_max, max_quality)

                    if round is None:
                        print(f"Lowest Diff was {min_found_diff:5.3}")
                        max_quality = min_found_q
                        print("min_quality increased to {min_quality:3.1}")

                    diff_max = min_found_diff

                if round is None:
                    diff_max += 0.1
                    print("DiffMax Increased to {diff_max:5.3")

            if round is None:
                self.meeting.print_check_stats()
                print("Failed to build the sequence.")
                return None
            else:
                round.display()
                d_max, d_avg, diff_list = round.diff_stats()
                diffs = ",".join(["%5.3f" % x for x in diff_list])
                print("Found a set sequence with DiffMax:%5.3f Max:%3.3f Avg:%5.3f List:%s" % (
                    self.diff_max, d_max, d_avg, diffs))
                self.meeting.add_round(round)

        return self.meeting.get_rounds()

    def display_sequences(self, seq):
        for s in seq:
            s.display()

    def show_all_diffs(self, seq):
        [s.show_diffs() for s in seq]
