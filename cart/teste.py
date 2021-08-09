d = {'casa': {'cozinha': 'grande', 'sala': 'pequena'}}
comodo = 'banheiro'
d['casa'][comodo] = 'estreito'
for item in d.values():
    print(item)
