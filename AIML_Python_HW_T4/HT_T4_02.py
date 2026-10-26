import random

def get_numbers_ticket(min, max, quantity):
    if min < 1 or max > 1000 or min > max:
        return []
    if quantity < min or quantity > max - min + 1:
        return []

    lottery_numbers = set()
    while len(lottery_numbers) < quantity:
        lottery_numbers.add(random.randint(min, max))
    return sorted(lottery_numbers)

print("Ваші лотерейні числа:", get_numbers_ticket(1, 49, 6))