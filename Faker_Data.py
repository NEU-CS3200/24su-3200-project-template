from faker import Faker
import random

# Seed for reproducibility
Faker.seed(1234)
random.seed(1234)

# Initialize Faker
fake = Faker()

# Print header
print(f"{'name':<25} {'date of birth':<15} {'discount %':<12} {'university name'}")

# Generate and print 10 rows
for _ in range(10):
    name = fake.name()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=30).strftime('%Y-%m-%d')
    discount = f"{random.choice(range(5, 55, 5))}%"  # Picks from 5% to 50% in steps of 5%
    university = fake.company() + " University"
    
    print(f"{name:<25} {dob:<15} {discount:<12} {university}")
