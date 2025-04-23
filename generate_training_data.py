import random 
from tqdm import tqdm

DATA_DIR = "data/training_data"
TEMPLATE_DIR = "data/training_templates"

categories = set()
with open(f"{DATA_DIR}/categories.txt", "r") as f:
    for line in f:
        categories.add(line.strip())
categories = list(categories)

cities = set()
with open(f"{DATA_DIR}/city.txt", "r") as f:
    for line in f:
        cities.add(line.strip())
cities = list(cities)

restaurants = set()
with open(f"{DATA_DIR}/restaurant.txt", "r") as f:
    for line in f:
        restaurants.add(line.strip())
restaurants = list(restaurants)

restaurant_templates = []
with open(f"{TEMPLATE_DIR}/restaurant_templates.txt", "r") as f:
    for line in f:
        restaurant_templates.append(line.strip())


tip_templates = []
with open(f"{TEMPLATE_DIR}/tip_templates.txt", "r") as f:
    for line in f:
        tip_templates.append(line.strip())

review_templates = []
with open(f"{TEMPLATE_DIR}/review_templates.txt", "r") as f:
    for line in f:
        review_templates.append(line.strip())

tip_examples = []
for _ in tqdm(range(20000)):
    template = random.choice(tip_templates)
    restaurant = random.choice(restaurants)
    tip_query = template.replace("{restaurant}", restaurant)
    tip_examples.append(f"Query:\n{tip_query}\nResponse:\n<|start_fn|> GET TIPS {restaurant} <|end_fn|>\n")

review_examples = []
for _ in tqdm(range(20000)):
    template = random.choice(review_templates)
    restaurant = random.choice(restaurants)
    number = random.randint(1, 5)
    review_query = template.replace("{restaurant}", restaurant).replace("{number}", str(number))
    review_examples.append(f"Query:\n{review_query}\nResponse:\n<|start_fn|> GET REVIEWS {restaurant} <|end_fn|>\n")

restaurant_examples = []
for _ in tqdm(range(20000)):
    template = random.choice(restaurant_templates)
    city = random.choice(cities)
    category = random.choice(categories)
    number = random.randint(1, 5)
    restaurant_query = template.replace("{city}", city).replace("{category}", category).replace("{number}", str(number))
    restaurant_examples.append(f"Query:\n{restaurant_query}\nResponse:\n<|start_fn|> GET RESTAURANTS {city}, {category} <|end_fn|>\n")

examples = restaurant_examples + review_examples + tip_examples
random.shuffle(examples)

for i in tqdm(range(len(examples))):
    with open(f"tmp/{i}.txt", "w") as f:
        f.write(examples[i])