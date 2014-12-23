"""
Script that connects with a database 'Snootboots' and populates randomized
boot accessories.  The number of items generated/inserted can be set using the
NUM_OF_ITEMS constant near top of file.  Does not reset database on execution.

***DATABASE CONNECTION PARAMETERS ARE PLACEHOLDERS***

"""

import MySQLdb
import random

__author__ = 'jessebostic'

# Holds all of the possible string values for creating random items
# Integers are dynamically created with random module upon insertion
db_values = {"name_adjectives": ["Ugly", "Cheap", "Elegant", "Unique", "Used", "Gorgeous", "Plain", "Barbed", "Smooth",
                                 "Brilliant", "Awesome", "Basic", "Aquatic", "Cool", "Sexy", "Gawdy", "Gorgeous",
                                 "New",  "Antique", "Steampunk", "Coveted", "Rugged", "Durable", "Quality", "Stylish",
                                 "Enviable", "Common", "Worn"],
             "shapes": ["Sphere", "Triangle", "Tight Fit", "Square", "Loose Fit", "Cone", "Mask-ish", "Square", "Misc"],
             "types": ["Butterfly", "Button", "Snap", "Screw On", "Latch", "Catch", "Decorative"],
             "materials": ["Wool", "Polyester", "Plastic", "Bronze", "Sterling Silver", "Glass", "Pewter", "Wood",
                           "Lead", "Diamond", "Plutonium", "Agate", "Cement", "Silk", "Leather", "Paper", "Cotton"],
             "colors": ["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Translucent", "Rainbow", "Chameleon"],
             "boot_mfgs": ["Boot The World", "NoseStyl", "Shnoot", "Bootcetera"],
             "tie_mfgs": ["ThredLite", "RevoSnootion", "OGG", "Spinweel"],
             "clasp_mfgs": ["YKK", "Claspsmith and Sons", "Lockitup", "Stevenson & Kline"],
             "mfgs_cities": [("Tacoma", "WA"), ("San Francisco", "CA"), ("New York", "NY"), ("Salt Lake City", "UT"),
                             ("Miami", "FL"), ("Dallas", "TX"), ("Tucson", "AZ"), ("St. Paul", "MN"), ("Kiska", "AK"),
                             ("Portland", "OR"), ("Seattle", "WA"), ("Boise", "ID"), ("Olympia", "WA")]}

# How many items of each type to generate.
NUM_OF_ITEMS = 15

# UPDATE WITH DESIRED SERVER, USER, AND PASSWORD
db = MySQLdb.connect(host="12.34.567.890", port=3306, user="YourUSER", passwd="YourPSSWD", db="Snootboots")
cur = db.cursor()

#INSERT MFGS
for name in db_values["boot_mfgs"]:
    loc = random.choice(db_values["mfgs_cities"])
    cur.execute('INSERT INTO MFGS (Name, ProductType, City, State) '
                'VALUES ("{}", "{}", "{}", "{}")'.format(name, "Boots", loc[0], loc[1]))

for name in db_values["tie_mfgs"]:
    loc = random.choice(db_values["mfgs_cities"])
    cur.execute('INSERT INTO MFGS (Name, ProductType, City, State) '
                'VALUES ("{}", "{}", "{}", "{}")'.format(name, "Ties", loc[0], loc[1]))

for name in db_values["clasp_mfgs"]:
    loc = random.choice(db_values["mfgs_cities"])
    cur.execute('INSERT INTO MFGS (Name, ProductType, City, State) '
                'VALUES ("{}", "{}", "{}", "{}")'.format(name, "Clasps", loc[0], loc[1]))

#INSERT BOOTS
cur.execute('SELECT ID FROM MFGS WHERE ProductType = "Boots"')
mfg_ids = cur.fetchall()
for x in range(NUM_OF_ITEMS):
    name = random.choice(db_values["name_adjectives"]) + ' ' + random.choice(db_values["name_adjectives"]) + ' ' + "Boot"
    shape =  random.choice(db_values["shapes"])
    material = random.choice(db_values["materials"])
    color = random.choice(db_values["colors"])
    mfg = random.choice(mfg_ids)[0]
    price = random.randint(1, 100) + random.random() + random.random() * 0.1
    cur.execute('INSERT INTO BOOTS (Name, Shape, Material, Color, Mfg, Price) '
                'VALUES ("{}", "{}", "{}", "{}", {}, {})'.format(name, shape, material, color, mfg, price))

#INSERT TIES
cur.execute('SELECT ID FROM MFGS WHERE ProductType = "Ties"')
mfg_ids = cur.fetchall()
for x in range(NUM_OF_ITEMS):
    name = random.choice(db_values["name_adjectives"]) + ' ' + random.choice(db_values["name_adjectives"]) + ' ' + "Tie"
    length =  random.randint(8, 25)
    material = random.choice(db_values["materials"])
    color = random.choice(db_values["colors"])
    mfg = random.choice(mfg_ids)[0]
    price = random.randint(1, 100) + random.random() + random.random() * 0.1
    cur.execute('INSERT INTO TIES (Name, Length, Material, Color, Mfg, Price) '
                'VALUES ("{}", "{}", "{}", "{}", {}, {})'.format(name, length, material, color, mfg, price))

#INSERT CLASPS
cur.execute('SELECT ID FROM MFGS WHERE ProductType = "Clasps"')
mfg_ids = cur.fetchall()
for x in range(NUM_OF_ITEMS):
    name = random.choice(db_values["name_adjectives"]) + ' ' + random.choice(db_values["name_adjectives"]) + ' ' + "Clasp"
    type =  random.choice(db_values["types"])
    material = random.choice(db_values["materials"])
    color = random.choice(db_values["colors"])
    mfg = random.choice(mfg_ids)[0]
    price = random.randint(1, 100) + random.random() + random.random() * 0.1
    cur.execute('INSERT INTO CLASPS (Name, Type, Material, Color, Mfg, Price) '
                'VALUES ("{}", "{}", "{}", "{}", {}, {})'.format(name, type, material, color, mfg, price))

cur.close()
db.close()
