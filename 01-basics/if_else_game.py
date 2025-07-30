health = 35
has_potion = True

print("Current health:", health)

if health < 50 and has_potion:
    print("Your health is low! Using a potion...")
    health = health + 50
    has_potion = False
elif health < 50 and not has_potion:
    print("Low health, but no potions left! Be careful.")
else:
    print("You're healthy. Keep going!")

print("Updated health:", health)
print("Has potion left?", has_potion)

#more logic
gold = 1000

if gold >= 1000:
    print("You can afford a legendary sword!")
else:
    print("You need to farm more gold.")
