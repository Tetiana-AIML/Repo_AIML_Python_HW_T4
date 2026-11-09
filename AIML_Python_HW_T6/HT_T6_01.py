def total_salary(path):
    total = 0
    count = 0

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue  # пропускаємо порожні рядки

                name, salary = line.split(",")
                total += int(salary)
                count += 1
    except FileNotFoundError:
        print(f"Файл '{path}' відсутній.")
        return 0, 0
    except ValueError:
        print(f"Файл '{path}' пошкоджений.")
        return 0, 0

    if count == 0:
        return 0, 0

    average = total // count
    return total, average

total, average = total_salary("AIML_Python_HW_T6/salary_file.txt")
print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")