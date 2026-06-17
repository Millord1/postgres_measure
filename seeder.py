from faker import Faker
import random

class Seeder:
    
    def __seed(self, nb: int) -> list[tuple]:
        if not isinstance(nb, int):
            raise ValueError("nb must be a number")
        
        fake = Faker('fr_FR')
        Faker.seed(0)
        
        data = []
        
        for _ in range(nb):
            integer = fake.random_int(min=1, max=100000)
            text = fake.sentence(nb_words=5)
            date = fake.date_this_century()
            float = round(random.uniform(10.0, 999.9), 2)
            
            data.append((integer, text, date, float))
            
        return data

    def create_thousand(self):
        return self.__seed(1000)
    
    def create_hundred_thousand(self):
        return self.__seed(100000)
    
    def create_million(self):
        return self.__seed(1000000)