import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .consumers import ScheduleConsumer

logger = logging.getLogger(__name__)


class MixerSyncHandler:
    """
    Synchronous versions that can be called from Django code
    """

    @staticmethod
    def mixer_status():
        channel_layer = get_channel_layer()
        logger.debug("Sending comment updated message")
        async_to_sync(channel_layer.group_send)(
            'tennis_mixer_group',
            {
                "type": "mixer.event",
                "action": "mixerUpdate",
                "payload": {
                    'status': 'something here'
                }
            }
        )


class ScheduleSyncHandler:
    """
    Synchronous versions that can be called from Django code
    """

    @staticmethod
    def schedule_verify_update(schedule_date=None):
        channel_layer = get_channel_layer()
        logger.debug("Sending schedule verify update")
        group = ScheduleConsumer.calc_group_name(schedule_date)
        async_to_sync(channel_layer.group_send)(
            group,
            {
                "type": "schedule.event",
                "action": "scheduleVerifyChanged",
                "payload": {
                    'date': schedule_date,
                    'user': 'bobby dillon',
                    'user_id': 23,
                    'status': 'verified|rejected',
                    'message': 'I do not want to play this Friday',
                }
            }
        )
