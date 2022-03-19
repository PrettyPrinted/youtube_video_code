import copy

class Distance:
    def __init__(self, length, unit):
        if unit == 'm':
            self._meters = length
        elif unit == 'ft':
            self._meters = length * 0.3048

    @property
    def meters(self):
        return self._meters

    @meters.setter
    def meters(self, length):
        self._meters = length

    @property
    def feet(self):
        return self._meters * 3.28084

    @feet.setter
    def feet(self, length):
        self._meters = length * 0.3048

    def __add__(self, other):
        if isinstance(other, Distance):
            return Distance(self._meters + other._meters, 'm')

    def __str__(self):
        return f'<{self._meters} meters>'

#ten_meters = Distance(10, 'm')
#print(ten_meters.feet)
#ten_meters.feet = 20
#print(ten_meters.feet)

#five_meters = Distance(5, 'm')
#ten_meters = Distance(12, 'm')

#fifteen_meters = five_meters + ten_meters
#print(fifteen_meters.meters)
#print(fifteen_meters)

ten_meters = Distance(10, 'm')
copy_of_ten_meters = copy.deepcopy(ten_meters)
print(ten_meters)
print(copy_of_ten_meters)
copy_of_ten_meters.meters = 20
print(ten_meters)
print(copy_of_ten_meters)