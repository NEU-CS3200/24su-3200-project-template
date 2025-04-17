from faker import Faker
from faker.providers import DynamicProvider
import random

cities_provider = DynamicProvider(
     provider_name="cities",
     elements=["Boston", "New York", "Chicago", "Miami", "San Francisco"],
)

colleges_provider = DynamicProvider(
     provider_name="colleges",
     elements=["Northeastern", "Fordham", "Northwestern", "UMiami", "UCBerkeley"],
)

states_provider = DynamicProvider(
     provider_name="states",
     elements=["Massachusetts", "New York", "Illinois", "Florida", "California"],
)

street_address_provider = DynamicProvider(
     provider_name="street_addresses",
     elements=["458 Huntington Ave", "14 Baker St", "199 High St", "15 Fruit St", "12 Summit Pl"],
)

zipcode_provider = DynamicProvider(
     provider_name="zipcodes",
     elements=["01950", "02110", "90210", "11111", "77777"],
)

store_name_provider = DynamicProvider(
     provider_name="stores",
     elements=["Wollastons", "Panera", "Aroma Joes", "Star Market", "Target"],
)

club_name_provider = DynamicProvider(
     provider_name="clubs",
     elements=["Society of Women in Tech", "Badminton Club", "Trivia Club", "Phi Delta Theta", "Film Club"],
)

colleges1 = ["Northeastern", "Fordham", "Northwestern", "UMiami", "UCBerkeley"]
colleges2 = ["Northeastern", "Fordham", "Northwestern", "UMiami", "UCBerkeley"]
price_ranges = ['$', '$$', '$$$']
hours = ['7:00am-12:00am', '10:00am-5:00pm', '12:00pm-9:00pm', '11:00am-11:00pm']
categories = ['convenience', 'grocery', 'food', 'clothing']
items = ['clothing', 'coffee', 'books', 'produce', 'furniature']
sDates = ['2025-04-14', '2025-03-20', '2025-03-30', '2025-02-18']
eDates = ['2025-04-15', '2025-05-05', '2025-06-01', '2025-05-10']
codes = ['BIGSALE', 'BUYBUYBUY', 'SALECODE', 'REDEEMCODE', 'SPRINGSALE']
birthdates = ['2000-04-15', '2001-05-05', '2002-06-01', '2003-05-10', '1999-09-12', '2005-11-11']
all_usernames = []
admin_users = []

fake = Faker()
fake.add_provider(cities_provider)
fake.add_provider(colleges_provider)
fake.add_provider(states_provider)
fake.add_provider(street_address_provider)
fake.add_provider(zipcode_provider)
fake.add_provider(store_name_provider)
fake.add_provider(club_name_provider)



location_rows = 5  
college_rows = 5
club_rows = 5
store_rows = 5
discount_rows = 10
user_rows = 10
saved_discount_rows = 10
admin_rows = 2

with open("faker.sql", "w") as f:
    print("✅ Writing to:", f.name)
    f.write("USE campusPerks_db;\n")

    # --- Locations ---
    f.write("INSERT INTO location (locationId, streetAddress, city, state, country, zipcode)\nVALUES\n")
    for i in range(location_rows):
        strAdd = fake.street_addresses().replace("'", "''")
        city = fake.cities().replace("'", "''")
        state = fake.states().replace("'", "''")
        zipcode = fake.zipcodes().replace("'", "''")
        line = f"({i+1}, '{strAdd}', '{city}', '{state}', 'USA', '{zipcode}')"
        f.write(line + (",\n" if i < location_rows - 1 else ";\n"))

    # --- Colleges ---
    f.write("INSERT INTO college (collegeName, locationId, noOfStores, noOfUsers, domain)\nVALUES\n")
    for i in range(college_rows):
        cn = random.choice(colleges1)
        colleges1.remove(cn)
        lId = random.randint(1, location_rows)
        domain = "@" + cn.replace("''", "") + ".edu"
        line = f"('{cn}', {lId}, 0, 0, '{domain}')"
        f.write(line + (",\n" if i < college_rows - 1 else ";\n"))

    # --- Stores ---
    f.write("INSERT INTO store (storeId, name, locationId, priceRange, noOfDiscounts, hoursOfOperations, category, phoneNo, website, starRating, delivery, ageRestricted, totalSales, noOfOrders, college, clubId)\nVALUES\n")
    for i in range(store_rows):
        name = fake.stores().replace("'", "''")
        lId = random.randint(1, location_rows)
        pr = random.choice(price_ranges)
        ho = random.choice(hours)
        cat = random.choice(categories)
        phone = fake.phone_number().replace("'", "''")
        web = fake.domain_name()
        rate = random.randint(1, 5)
        de = random.randint(0, 1)
        ar = random.randint(0, 1)
        ts = random.randint(0, 20000)
        no = random.randint(0, 500)
        col = fake.colleges().replace("'", "''")
        line = f"({i+1}, '{name}', {lId}, '{pr}', 0, '{ho}', '{cat}', '{phone}', '{web}', {rate}, {de}, {ar}, {ts}, {no}, '{col}', NULL)"
        f.write(line + (",\n" if i < store_rows - 1 else ";\n"))

    # --- Clubs ---
    f.write("INSERT INTO club (clubId, name, college, storeId, numberOfUsers)\nVALUES\n")
    for i in range(club_rows):
        name = fake.clubs().replace("'", "''")
        college = random.choice(colleges2)
        colleges2.remove(college)
        line = f"({i+1}, '{name}', '{college}', NULL, 0)"
        f.write(line + (",\n" if i < club_rows - 1 else ";\n"))

    # --- Discounts ---
    used_discounts = set()
    f.write("INSERT INTO discount (discountId, storeId, code, percentOff, item, startDate, endDate, ageRestricted, minPurchase, bdayDiscount)\nVALUES\n")
    for i in range(discount_rows):
        while True:
            stId = random.randint(1, store_rows)
            code = random.choice(codes)
            if (stId, code) not in used_discounts:
                used_discounts.add((stId, code))
                break
        pOff = random.randint(1, 99)
        item = random.choice(items)
        sDate = random.choice(sDates)
        eDate = random.choice(eDates)
        ageR = random.randint(0, 1)
        minP = random.randint(0, 100)
        bday = random.randint(0, 1)
        line = f"({i+1}, {stId}, '{code}', {pOff}, '{item}', '{sDate}', '{eDate}', {ageR}, {minP}, {bday})"
        f.write(line + (",\n" if i < discount_rows - 1 else ";\n"))

    # --- Users ---
    f.write("INSERT INTO user (username, firstName, lastName, password, college, email, phoneNo, birthdate, age, discountsUsed, clubId)\nVALUES\n")
    for i in range(user_rows):
        firstName = fake.first_name().replace("'", "''")
        lastName = fake.last_name().replace("'", "''")
        username = firstName + lastName + str(random.randint(0, 200))
        all_usernames.append(username)
        password = fake.password(length=8, special_chars=True, digits=True, upper_case=True, lower_case=True)
        cg = fake.colleges().replace("'", "''")
        em = username + "@" + cg + ".edu"
        phn = fake.phone_number().replace("'", "''")
        birth = random.choice(birthdates)
        age = random.randint(18, 30)
        discountsUsed = random.randint(0, 5)
        clubId = random.randint(1, club_rows)
        line = f"('{username}', '{firstName}', '{lastName}', '{password}', '{cg}', '{em}', '{phn}', '{birth}', {age}, {discountsUsed}, {clubId})"
        f.write(line + (",\n" if i < user_rows - 1 else ";\n"))

    # --- Discount Used ---
    f.write("INSERT INTO discount_used (username, discountId)\nVALUES\n")
    used_pairs = set()
    i = 0
    while i < saved_discount_rows:
        user = random.choice(all_usernames)
        disc = random.randint(1, discount_rows)
        pair = (user, disc)
        if pair in used_pairs:
            continue  # Skip duplicates
        used_pairs.add(pair)
        line = f"('{user}', {disc})"
        f.write(line + (",\n" if i < saved_discount_rows - 1 else ";\n"))
        i += 1


    # --- Admin ---
    f.write("INSERT INTO admin (username, firstName, lastName, password, email, phoneNo, supportUser, supportClub, supportStore)\nVALUES\n")
    for i in range(admin_rows):
        fn = fake.first_name().replace("'", "''")
        ln = fake.last_name().replace("'", "''")
        usern = fn + ln + str(random.randint(0, 200))
        admin_users.append(usern)
        pw = fake.password(length=8, special_chars=True, digits=True, upper_case=True, lower_case=True)
        eml = usern + "@gmail.com"
        phnn = fake.phone_number().replace("'", "''")
        sUser = random.choice(all_usernames)
        sClub = random.randint(1, club_rows)
        sStore = random.randint(1, store_rows)
        line = f"('{usern}', '{fn}', '{ln}', '{pw}', '{eml}', '{phnn}', '{sUser}', {sClub}, {sStore})"
        f.write(line + (",\n" if i < admin_rows - 1 else ";\n"))