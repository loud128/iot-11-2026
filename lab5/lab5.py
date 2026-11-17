from datetime import datetime, timedelta
from enum import Enum
from math import ceil


class Brand(Enum):
    BMW = "BMW"
    AUDI = "Audi"
    TOYOTA = "Toyota"
    FORD = "Ford"
    VOLKSWAGEN = "Volkswagen"


class Car:
    def __init__(self, brand: Brand, age: int, max_speed: int, horse_power: int,
                 number: str):
        if not isinstance(brand, Brand):
            raise ValueError("Марка повинна бути значенням Brand")
        if age < 0 or max_speed <= 0 or horse_power <= 0:
            raise ValueError("Некоректні характеристики автомобіля")
        self.__brand = brand
        self.__age = age
        self.__max_speed = max_speed
        self.__horse_power = horse_power
        self.__number = number
        self.__arrival_time = None

    def get_brand(self):
        return self.__brand

    def get_age(self):
        return self.__age

    def get_max_speed(self):
        return self.__max_speed

    def get_horse_power(self):
        return self.__horse_power

    def get_number(self):
        return self.__number

    def get_arrival_time(self):
        return self.__arrival_time

    def set_arrival_time(self, arrival_time):
        self.__arrival_time = arrival_time

    def __str__(self):
        return (f"{self.__brand.value} | номер: {self.__number} | "
                f"вік: {self.__age} р. | швидкість: {self.__max_speed} км/год | "
                f"потужність: {self.__horse_power} к. с.")

    def __del__(self):
        pass


class Parking:
    def __init__(self, max_places: int, price_per_hour: float):
        if max_places <= 0 or price_per_hour < 0:
            raise ValueError("Некоректна кількість місць або тариф")
        self.__max_places = max_places
        self.__price_per_hour = price_per_hour
        self.__cars = []

    def get_max_places(self):
        return self.__max_places

    def get_price_per_hour(self):
        return self.__price_per_hour

    def get_free_places(self):
        return self.__max_places - len(self.__cars)

    def set_price_per_hour(self, price):
        if price < 0:
            raise ValueError("Тариф не може бути від'ємним")
        self.__price_per_hour = price

    def parkCar(self, car: Car, arrival_time=None):
        if len(self.__cars) >= self.__max_places:
            print("Паркінг переповнений! Вільних місць немає.")
            return False
        if any(parked.get_number() == car.get_number() for parked in self.__cars):
            print(f"Автомобіль {car.get_number()} вже на паркінгу.")
            return False
        if arrival_time is None:
            arrival_time = datetime.now()
        if arrival_time > datetime.now():
            print("Час прибуття не може бути в майбутньому.")
            return False
        car.set_arrival_time(arrival_time)
        self.__cars.append(car)
        print(f"Автомобіль {car.get_number()} припарковано.")
        return True

    def duration(self, car: Car, current_time=None):
        if current_time is None:
            current_time = datetime.now()
        arrival_time = car.get_arrival_time()
        if arrival_time is None:
            raise ValueError("Автомобіль ще не був припаркований")
        seconds = (current_time - arrival_time).total_seconds()
        if seconds < 0:
            raise ValueError("Час завершення передує часу прибуття")
        return seconds / 3600

    def calculate_price(self, car: Car, current_time=None):
        hours = self.duration(car, current_time)
        # Будь-яка неповна година рахується як повна.
        return ceil(hours) * self.__price_per_hour

    def sort_by_duration(self, current_time=None):
        return sorted(self.__cars,
                      key=lambda car: self.duration(car, current_time),
                      reverse=True)

    def show_cars(self, current_time=None):
        if current_time is None:
            current_time = datetime.now()
        print("\nАвтомобілі за тривалістю стоянки (від найдовшої):")
        if not self.__cars:
            print("Паркінг порожній.")
            return
        for car in self.sort_by_duration(current_time):
            print(f"{car} | {self.duration(car, current_time):.2f} год | "
                  f"вартість: {self.calculate_price(car, current_time):.2f} грн")

    def leaveParking(self, number: str, departure_time=None):
        if departure_time is None:
            departure_time = datetime.now()
        for car in self.__cars:
            if car.get_number() == number:
                try:
                    price = self.calculate_price(car, departure_time)
                except ValueError as error:
                    print(error)
                    return False
                self.__cars.remove(car)
                car.set_arrival_time(None)
                print(f"Автомобіль {number} виїхав. До сплати: {price:.2f} грн")
                return True
        print(f"Автомобіля {number} немає на паркінгу.")
        return False

    def __del__(self):
        pass


def main():
    parking = Parking(max_places=3, price_per_hour=40)
    now = datetime.now()

    car1 = Car(Brand.BMW, 5, 250, 190, "BC1234AA")
    car2 = Car(Brand.TOYOTA, 3, 200, 150, "BC5678BB")
    car3 = Car(Brand.AUDI, 7, 240, 210, "BC9012CC")
    car4 = Car(Brand.FORD, 2, 190, 125, "BC3456DD")

    parking.parkCar(car1, now - timedelta(hours=2, minutes=20))
    parking.parkCar(car2, now - timedelta(hours=1, minutes=10))
    parking.parkCar(car3, now - timedelta(hours=3, minutes=5))
    parking.parkCar(car4)  # Четверта машина не поміститься.

    print(f"Вільних місць: {parking.get_free_places()}")
    parking.show_cars(now)

    print("\nВиїзд автомобіля:")
    parking.leaveParking("BC1234AA", now)
    print(f"Вільних місць: {parking.get_free_places()}")

    print("\nПриїзд нового автомобіля:")
    parking.parkCar(car4)
    parking.show_cars()


if __name__ == "__main__":
    main()
