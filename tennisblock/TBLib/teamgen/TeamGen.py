import logging
from .Meeting import Meeting
from .round import MatchRound
from .meeting_history import MeetingHistory
from .random_builder import RandomMeetingBuilder
from tennis_channels.sync_handlers import MixerSyncHandler

logger = logging.getLogger(__name__)


class TeamGen(object):
    def __init__(self, courts, num_seq, men, women):
        self.n_courts = courts
        self.history = MeetingHistory(
            group1=men,
            group2=women
        )
        self.builder = RandomMeetingBuilder(
            courts, num_seq, men, women,
            history=self.history
        )
        self.meeting = Meeting(courts, num_seq, men, women,
                               history=self.history,
                               builder=self.builder)
        self.diff_max = 0.1
        self.MaxBadDiff = 1.0
        self.n_sequences = num_seq
        self.iterLimit = 1000

    def generate_rounds(self,
                        b_allow_duplicates: bool = False,
                        iterations: int = None,
                        max_tries: int = 20,
                        special_requests=None):
        self.meeting.restart()

        self.meeting.see_player_once = not b_allow_duplicates
        if iterations is not None:
            self.meeting.max_iterations = iterations

        while self.meeting.round_count < self.n_sequences:

            round = self.generate_round(self.meeting, max_tries=max_tries)

            if round is None:
                self.meeting.print_check_stats()
                logger.info("Failed to build the sequence.")
                return None
            else:
                round.display()

                status_msg = f"Generated {self.meeting.round_count} sequence(s)"
                MixerSyncHandler.mixer_status(status_msg)
                logger.info(status_msg)

                d_max, d_avg, diff_list = round.diff_stats()
                diffs = ",".join(["%5.3f" % x for x in diff_list])
                logger.info("Found a set sequence with DiffMax:%5.3f Max:%3.3f Avg:%5.3f List:%s" % (
                    self.diff_max, d_max, d_avg, diffs))
                self.meeting.add_round(round)

        MixerSyncHandler.mixer_status("Able to generate the sequences")
        return self.meeting.get_rounds()

    @staticmethod
    def generate_round(meeting, max_tries: int = 20):
        """
        Generate a new round in the meeting

        It won't matter how many rounds exists, we can just generate a new round given
        the current meeting statistics.

        ToDo: Isolate the statistics from the meeting, so we can generate them using other methods
        :param meeting:
        :param max_tries:
        :return:
        """
        min_quality = 98
        round = None

        while min_quality >= 50 and not round:
            results = meeting.get_new_round(
                diff_max=0.6,
                quality_min=min_quality,
                max_tries=max_tries)

            round, stats = results
            min_found_diff = stats.min_diff
            min_q = stats.min_q
            max_q = stats.max_q
            status_msg = f"Quality Stats: min:{min_q} max:{max_q}"
            MixerSyncHandler.mixer_status(status_msg)
            logger.info(status_msg)

            if not round:
                # Increase the quality then the diff
                min_quality = min_quality - 2
                logger.debug(f"Criteria updated. Q:{min_quality}")

        return round

    @staticmethod
    def display_sequences(seq):
        for s in seq:
            s.display()

    @staticmethod
    def show_all_diffs(seq):
        [s.show_diffs() for s in seq]
