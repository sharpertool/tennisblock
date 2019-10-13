import logging
import typing as t
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .consumers import ScheduleConsumer

logger = logging.getLogger(__name__)


class MixerSyncHandler:
    """
    Synchronous versions that can be called from Django code
    """

    @staticmethod
    def mixer_status(msg: str):
        channel_layer = get_channel_layer()
        logger.info(f"Sending mixer status: {msg}")
        async_to_sync(channel_layer.group_send)(
            'tennis_mixer_group',
            {
                "type": "mixer.event",
                "action": "mixerUpdate",
                "payload": {
                    'status_msg': msg
                }
            }
        )


class ScheduleSyncHandler:
    """
    Synchronous versions that can be called from Django code
    """

    @staticmethod
    def schedule_verify_update(schedule_date: str = "",
                               status: bool = True,
                               player: t.Dict = None,
                               msg: str = ""):
        channel_layer = get_channel_layer()
        logger.info("Sending schedule verify update")
        group = ScheduleConsumer.calc_group_name(schedule_date)
        async_to_sync(channel_layer.group_send)(
            group,
            {
                "type": "schedule.event",
                "action": "scheduleVerifyChanged",
                "payload": {
                    'date': schedule_date,
                    'name': player.get('name'),
                    'user_id': player.get('user_id'),
                    'status': 'verified' if status else 'rejected',
                    'message': msg,
                }
            }
        )
