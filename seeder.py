# ---
# title: "Seeder, create fake data"
# author: Millord
# format: html
# ---
# %%
#| eval: false

from faker import Faker
import random
# %%
#| eval: false

class Seeder:
    
    def __init__(self):
        self.fake = Faker('fr_FR')
        Faker.seed(0)
    
    def __seed(self, nb: int) -> list[tuple]:
        if not isinstance(nb, int):
            raise ValueError("nb must be a number")
        
        data = []
        
        for _ in range(nb):
            integer = self.fake.random_int(min=1, max=100000)
            text = self.fake.sentence(nb_words=5)
            date = self.fake.date_this_century()
            float = round(random.uniform(10.0, 999.9), 2)
            
            data.append((integer, text, date, float))
            
        return data

    def create_thousand(self):
        return self.__seed(1000)
    
    def create_hundred_thousand(self):
        return self.create_thousand() * 100
    
    def create_million(self):
        return self.create_thousand() * 1000
    
    # For the Science
    
    def __seed_on_stream(self, nb: int):
        if not isinstance(nb, int):
            raise ValueError("nb must be a number")
        
        for _ in range(nb):
            yield (
                self.fake.random_int(min=1, max=100000), 
                self.fake.sentence(nb_words=5), 
                self.fake.date_this_century(), 
                round(random.uniform(10.0, 999.9), 2)
            )
    
    def create_million_on_stream(self):
        return self.__seed_on_stream(1000000)