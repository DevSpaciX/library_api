import asyncio
from datetime import datetime, date
from django.utils.timezone import now
from celery import shared_task
from borrowing.models import Borrow
from borrowing.telegram_alert import send_message_to_channel


@shared_task
def send_overdue_book_returns():
    overdue_borrows = Borrow.objects.filter(expected_return__lt=now().date())
    if overdue_borrows:
        for barrow in overdue_borrows:
            date_format = "%Y-%m-%d"
            expected_return_date = datetime.strptime(
                str(barrow.expected_return), date_format
            )
            overdue_days = date.today() - expected_return_date.date()
            asyncio.run(
                send_message_to_channel(
                    text=f"{barrow.user.email} has an overdue book ({barrow.book.title}). The delay is {overdue_days.days} days."
                )
            )
    else:
        asyncio.run(send_message_to_channel(text=f"No borrowings overdue today!"))
