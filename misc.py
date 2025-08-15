from datetime import datetime


def on_start():
    current_date = datetime.now()
    print(f'Bot started at {current_date.strftime('%Y/%m/%d %H:%M')}')


def on_shutdown():
    current_date = datetime.now()
    print(f'Bot is down at {current_date.strftime('%Y/%m/%d %H:%M')}')