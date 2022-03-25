import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    today_date = datetime.date.today()
    return {
        'year': today_date.year,
    }
