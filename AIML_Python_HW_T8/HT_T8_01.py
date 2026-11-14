
# створення функції з кеш
def caching_fibonacci():
    cache = {} # кеш (номер числа, значення)

# внутрішня функція, повертає n-е число використовуючи кеш
    def fibonacci(n):

# можливі випадки
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache: #якщо значення є в кеші, беремо з кеша
            return cache[n]

# інакше обчислюємо рекурсивно та зберігаємо в кеш
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


# отримання функції fibonacci
fib = caching_fibonacci()

# використання функції fibonacci (перевірка), вивід результатів
print(fib(10))  # виведе 55
print(fib(15))  # виведе 610