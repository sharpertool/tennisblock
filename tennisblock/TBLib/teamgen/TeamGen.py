import logging
from .Meeting import Meeting
from .round import MatchRound
from tennis_channels.sync_handlers import MixerSyncHandler

logger = logging.getLogger(__name__)


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

        self.meeting.see_player_once = not b_allow_duplicates
        if iterations is not None:
            self.meeting.max_iterations = iterations

        while self.meeting.round_count() < self.n_sequences:
            group_round = None
            min_quality = 98

            while min_quality >= 50 and group_round is None:
                results = self.meeting.get_new_round(
                    quality_min=min_quality, max_tries=max_tries)

                group_round, min_found_diff, min_q, max_q = results
                status_msg = f"Quality Stats: min:{min_q} max:{max_q}"
                MixerSyncHandler.mixer_status(status_msg)
                logger.info(status_msg)

                if group_round is None:
                    # Increase the quality then the diff
                    min_quality = min_quality - 2
                    logger.debug(f"Criteria updated. Q:{min_quality}")

            if group_round is None:
                self.meeting.print_check_stats()
                logger.info("Failed to build the sequence.")
                return None
            else:
                if isinstance(group_round, list):
                    matches = []
                    for round in group_round:
                        matches.extend(round.matches)
                    round = MatchRound(matches=matches)

                    status_msg = f"Generated {self.meeting.round_count()} sequence(s)"
                    MixerSyncHandler.mixer_status(status_msg)
                    logger.info(status_msg)

                    d_max, d_avg, diff_list = round.diff_stats()
                    diffs = ",".join(["%5.3f" % x for x in diff_list])
                    logger.info("Found a set sequence with DiffMax:%5.3f Max:%3.3f Avg:%5.3f List:%s" % (
                        self.diff_max, d_max, d_avg, diffs))
                    self.meeting.add_round(round)

                else:
                    group_round.display()

                    status_msg = f"Generated {self.meeting.round_count()} sequence(s)"
                    MixerSyncHandler.mixer_status(status_msg)
                    logger.info(status_msg)

                    d_max, d_avg, diff_list = group_round.diff_stats()
                    diffs = ",".join(["%5.3f" % x for x in diff_list])
                    logger.info("Found a set sequence with DiffMax:%5.3f Max:%3.3f Avg:%5.3f List:%s" % (
                        self.diff_max, d_max, d_avg, diffs))
                    self.meeting.add_round(group_round)

        MixerSyncHandler.mixer_status("Able to generate the sequences")
        return self.meeting.get_rounds()

    def display_sequences(self, seq):
        for s in seq:
            s.display()

    def show_all_diffs(self, seq):
        [s.show_diffs() for s in seq]
