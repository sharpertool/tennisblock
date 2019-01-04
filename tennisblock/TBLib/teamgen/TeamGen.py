from .Meeting import Meeting


class TeamGen(object):
    def __init__(self, courts, num_seq, men, women):
        self.n_courts = courts
        self.meeting = Meeting(courts, num_seq, men, women)
        self.diff_max = 0.1
        self.MaxBadDiff = 1.0
        self.n_sequences = num_seq
        self.iterLimit = 1000

    def generate_set_sequences(self,
                               b_allow_duplicates: bool = False,
                               iterations: int = None,
                               max_tries: int = 20):
        self.meeting.restart()

        self.meeting.set_see_player_once(not b_allow_duplicates)
        if iterations is not None:
            self.meeting.set_max_iteration(iterations)

        while self.meeting.round_count() < self.n_sequences:
            group_round = None
            diff_max = 0.1
            max_quality = 1.0

            while diff_max <= 1.0 and max_quality < 2.5 and group_round is None:
                results = self.meeting.get_new_round(
                    diff_max, max_quality, max_tries)
                group_round, min_found_diff, min_found_q = results

                if group_round is None:
                    # Increase the quality then the diff
                    max_quality = max(max_quality+0.1, min_found_q)
                    if max_quality >= 2.5:
                        max_quality = 1.0
                        diff_max += 0.1
                    print(f"Criteria updated. Diff:{diff_max} Q:{max_quality}")

            if group_round is None:
                self.meeting.print_check_stats()
                print("Failed to build the sequence.")
                return None
            else:
                group_round.display()
                d_max, d_avg, diff_list = group_round.diff_stats()
                diffs = ",".join(["%5.3f" % x for x in diff_list])
                print("Found a set sequence with DiffMax:%5.3f Max:%3.3f Avg:%5.3f List:%s" % (
                    self.diff_max, d_max, d_avg, diffs))
                self.meeting.add_round(group_round)

        return self.meeting.get_rounds()

    def display_sequences(self, seq):
        for s in seq:
            s.display()

    def show_all_diffs(self, seq):
        [s.show_diffs() for s in seq]
