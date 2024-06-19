import random
import datetime
import bson
from pymongo import MongoClient

families_count=10000
num_records=100000

# Fonction pour générer des coordonnées aléatoires en France
def generate_random_coords():
    latitude = random.uniform(41.0, 51.0)
    longitude = random.uniform(-5.0, 9.0)
    return {"lat": latitude, "lon": longitude}

# Générer une liste de familles avec des coordonnées
families = [
    {"familyId": i, "coords": generate_random_coords()} for i in range(1, families_count + 1)
]

# Connect to docker openfoodfacts service
mongo_client=MongoClient('off-db', 27017, username="admin", password="nimda")
db=mongo_client['off']

# Gather all of ean from products collection
products_collection=db['products']

# Sets query
query={
    '_id': {
        '$regex': '^[1-9][0-9]{12}$'
    },
    'product_name_fr': {
        '$exists': True,
        '$ne': ''
    }
}

projection={
    '_id': 1,
    'product_name_fr': 1
}
count=products_collection.count_documents(query)
print(f"Cursor returns {count} documents")

ean_codes_cursor=products_collection.find(query, projection)
ean_codes=[doc['_id'] for doc in ean_codes_cursor]

if not ean_codes:
    raise ValueError("'products' collection contains any ean codes")

def generate_random_date():
    start_date=datetime.datetime.now() - datetime.timedelta(days=365)
    end_date=datetime.datetime.now()
    random_date=start_date + (end_date - start_date) * random.random()
    return random_date.isoformat()

def generate_record(ean_code):
    family = random.choice(families)
    return {
        "family": family,
        "ean": ean_code,
        "dateTime": generate_random_date(),
        "quantity": random.randint(1, 10),
        "mouvementType": random.choice(["input", "output", "waste"])

    }

def generate_records(num_records): 
    return [
        generate_record(random.choice(ean_codes)) for _ in range(num_records)
    ]

# Records generation
records=generate_records(num_records)

# Data persistence
uptake_client=MongoClient('mongodb://127.0.0.1:27017/')
uptake_db=uptake_client['uptake']
uptake_collection=uptake_db['uptakes']

# Clear collection
uptake_collection.drop()

# Insert previous random data
uptake_collection.insert_many(records)

# Sets indexes
uptake_collection.create_index("familyId")
uptake_collection.create_index("ean")

# Store datas to bson, so will import them
with open('/data/dump/data.bson', 'wb') as file:
    for record in uptake_collection.find():
        file.write(bson.BSON.encode(record))

print(f"Process complete {num_records} documents was generated and exported")

# Close connexions
mongo_client.close()
uptake_client.close()
