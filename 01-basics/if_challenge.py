health = 49
has_shield = True

if health < 50 and not has_shield:
    print("Use healing!")
elif health < 50 and has_shield:
    print("Hold position!")
else:
    print("Keep attacking!")
