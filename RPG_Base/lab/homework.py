def recurse(lst):
    return (lst[0]+3, lst[1]+4), (lst[0]+4, lst[1]+3)

l = set(((0,0)))
ordered_pairs = {(0,0)}

for i in range(5):
    new = []
    for l in ordered_pairs:
        
        for x in recurse(l):
            new.append(x)
    for h in new:
        ordered_pairs.add(h)

print(ordered_pairs)