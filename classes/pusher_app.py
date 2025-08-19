import pusher

import config

pusher_client = pusher.Pusher(
    app_id=config.PUSHER_APP_ID,
    key=config.PUSHER_KEY,
    secret=config.PUSHER_SECRET,
    cluster=config.PUSHER_CLUSTER,
    ssl=True,
    timeout=15,
)


def push_message(message: dict[str, str]):
    pusher_client.trigger('my-channel', 'my-event', message)
