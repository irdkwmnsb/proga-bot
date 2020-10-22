from telegram import Bot
from telegram.ext import messagequeue as mq, Updater


class MQBot(Bot):
    def __init__(self, *args, is_queued_def=True, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mq.MessageQueue()

    def stop(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        return super(MQBot, self).send_message(*args, **kwargs)

    @mq.queuedmessage
    def send_photo(self, *args, **kwargs):
        return super(MQBot, self).send_photo(*args, **kwargs)

    @mq.queuedmessage
    def send_document(self, *args, **kwargs):
        return super(MQBot, self).send_document(*args, **kwargs)

    @mq.queuedmessage
    def send_video(self, *args, **kwargs):
        return super(MQBot, self).send_video(*args, **kwargs)

    @mq.queuedmessage
    def send_voice(self, *args, **kwargs):
        return super(MQBot, self).send_voice(*args, **kwargs)

    @mq.queuedmessage
    def send_location(self, *args, **kwargs):
        return super(MQBot, self).send_location(*args, **kwargs)

    @mq.queuedmessage
    def send_poll(self, *args, **kwargs):
        return super(MQBot, self).send_poll(*args, **kwargs)

    @mq.queuedmessage
    def send_contact(self, *args, **kwargs):
        return super(MQBot, self).send_contact(*args, **kwargs)

    @mq.queuedmessage
    def send_audio(self, *args, **kwargs):
        return super(MQBot, self).send_audio(*args, **kwargs)

    @mq.queuedmessage
    def send_sticker(self, *args, **kwargs):
        return super(MQBot, self).send_sticker(*args, **kwargs)

    @mq.queuedmessage
    def send_media_group(self, *args, **kwargs):
        return super(MQBot, self).send_media_group(*args, **kwargs)

    @mq.queuedmessage
    def send_animation(self, *args, **kwargs):
        return super(MQBot, self).send_animation(*args, **kwargs)


class QueuedUpdater(Updater):
    def __init__(self, bot: MQBot, *args, **kwargs):
        super(QueuedUpdater, self).__init__(bot=bot, *args, **kwargs)

    def signal_handler(self, signum, frame):
        super().signal_handler(signum, frame)
