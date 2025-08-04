gold = 800
has_discount = True

if has_discount:
    item_price = 750
    print("You used a discount coupon!")
else:
    item_price = 1000
print("Item cost:", item_price)

if gold >= item_price:
    print("Purchase successful!")
    gold = gold - item_price
    print("Remaining gold:",gold)
else:
    print("You can't afford this item.")