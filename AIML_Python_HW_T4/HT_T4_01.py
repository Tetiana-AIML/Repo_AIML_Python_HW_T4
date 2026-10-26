from datetime import datetime

def get_days_from_today(date):
    try:
        given_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        print("Неправильний формат дати")
        return None

    today = datetime.today().date()
    difference = today - given_date
    return difference.days

print(get_days_from_today("2026-09-21"))
print(get_days_from_today("2026-11-01"))
print(get_days_from_today("2026-10-25"))
print(get_days_from_today("25-10-2026"))