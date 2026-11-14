import sys

def parse_log_line(line: str) -> dict:
    date, time, level, message = line.split(maxsplit=3)
    return {"date": date, "time": time, "level": level, "message": message}

def load_logs(file_path: str) -> list:
    logs = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    logs.append(parse_log_line(line))
    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдено.")
        return []
    except ValueError:
        print("Неправильний формат лог-файлу.")
        return []
    except OSError as error:
        print(f"Помилка читання файлу: {error}")
        return []
    return logs

def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(lambda log: log["level"] == level.upper(), logs))

def count_logs_by_level(logs: list) -> dict:
    counts = {}
    for log in logs:
        level = log["level"]
        counts[level] = counts.get(level, 0) + 1
    return counts

def display_log_counts(counts: dict):
    # вивід таблиці
    print(f"{'Рівень логування':<16} | Кількість")
    print(f"{'-' * 16}-|----------")
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    for level, count in sorted_counts:
        print(f"{level:<16} | {count}")

def main():
    if len(sys.argv) < 2:
        print("Вкажіть шлях до лог-файлу.")
        print(f"Приклад: python {sys.argv[0]} logfile.log error")
        return

    logs = load_logs(sys.argv[1])
    if not logs:
        return

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if len(sys.argv) > 2:
        level = sys.argv[2]
        filtered = filter_logs_by_level(logs, level)
        print(f"\nДеталі логів для рівня '{level.upper()}':")
        for log in filtered:
            print(f"{log['date']} {log['time']} - {log['message']}")


if __name__ == "__main__":
    main()