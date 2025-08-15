from datetime import datetime
from database.tables import QuestionsTable, AnswersTable


def on_start():
    current_date = datetime.now()
    print(f'Bot started at {current_date.strftime('%Y/%m/%d %H:%M')}')


def on_shutdown():
    current_date = datetime.now()
    print(f'Bot is down at {current_date.strftime('%Y/%m/%d %H:%M')}')


def build_text_message(question: tuple[QuestionsTable, list[AnswersTable]]):
    question, answers = question
    message = f'{question.question}\n' + '\n'.join([f'\t- {answer.answer}' for answer in answers])
    return message
