from faker import Faker
import random



fake = Faker()
random_date = fake.date_time_between(start_date="-180d",end_date="-91d")
print(type(random_date))
print(random.randrange(6000000,20000000))