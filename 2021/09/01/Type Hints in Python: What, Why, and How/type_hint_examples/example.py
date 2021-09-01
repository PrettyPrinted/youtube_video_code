'''
def calculate_total_per_person(meal_price, number_of_people, tip=0.2):
    price_after_tip = meal_price * tip + meal_price
    per_person_price = price_after_tip / number_of_people
    return per_person_price
'''

def calculate_total_per_person(meal_price: float, number_of_people: int, tip: float = 0.2) -> float:
    price_after_tip: float = meal_price * tip + meal_price
    per_person_price: float = price_after_tip / number_of_people
    return per_person_price

#print('Total per person: ', calculate_total_per_person(100.0, 5))
#print('Total per person: ', calculate_total_per_person("One hundred", "Five"))

value: float
price: float = float(input('What is the meal price? '))
num_people: int = int(input('How many people? '))
tip: str = input('What is the tip? (Leave blank of 20%)')

if tip == '':
    value = calculate_total_per_person(price, num_people)
else:
    value = calculate_total_per_person(price, num_people, tip)

print('Total per person: ', value)