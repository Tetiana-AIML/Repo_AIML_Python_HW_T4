def get_cats_info(path):
    cats = []
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                id, name, age = line.split(",")
                cats.append({"id": id, "name": name, "age": age})
    except FileNotFoundError:
        print(f"Файл '{path}' відсутній.")
        return []
    except ValueError:
        print(f"Файл '{path}' пошкоджений.")
        return []

    return cats

cats_info = get_cats_info("AIML_Python_HW_T6/cats_file.txt")
print(cats_info)