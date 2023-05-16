import ethics_test as principle



# preference = ['a','b','c']
# happiness = [{'a':1,'b':2},{'a':3,'b':4}]
# contribution = [{'a':1,'b':2,'c':1},{'a':3,'b':4,'c':2},{'a':3,'b':4,'c':2}]
envy = [1,2,3,3]
luck = [5,6,7,5]
autonomy = [5,6,7,5]
harm = [1,2,3,4]
opportunity = [5,6,7,5]
# autonomy = [{'a':1,'b':2,'c':1,'d':4},{'a':1,'b':2,'c':1,'d':4},{'a':1,'b':2,'c':1,'d':4}]
# harm = [{'a':1,'b':2,'c':1,'d':4},{'a':1,'b':2,'c':1,'d':4},{'a':1,'b':2,'c':1,'d':4}]
# opportunity =[{'a':1,'b':2,'c':1,'d':4},{'a':1,'b':2,'c':1,'d':4},{'a':1,'b':2,'c':1,'d':4}]
users=4

# preference = ['a','b']
# # happiness = [{'a':1,'b':2},{'a':3,'b':4}]
# contribution = [{'a':1,'b':21},{'a':3,'b':4}]
# luck = [5,6]
# autonomy = [{'a':1,'b':21},{'a':3,'b':4}]
# harm = [{'a':1,'b':21},{'a':3,'b':4}]
# opportunity = [{'a':1,'b':21},{'a':3,'b':4}]
# users=2
contribution = [7,6,8,4]
happiness = [1,1,7,2]
resources = 'caonima'
resources_num = 13


cao = principle.Principle(None,happiness,contribution,envy,luck,autonomy,harm,opportunity,resources,resources_num,users)
# print(cao.happiness[0])
nb = cao.Users()
# print(cao.utilitarianism_allocate(nb))
# print(cao.prioritarianism_allocate(nb))
# print(cao.libertarian_allocating(nb))
# print(cao.desertbased_allocating(nb))
print(cao.nonmaleficence_allocate(nb))
# print(cao.Utilitarianism(nb),
# cao.Prioritarianism(nb),
# cao.DesertBased_Proportionalism(nb),
# cao.Libertarian_Proportionalism(nb),
# cao.Autonomy_Egalitarianism(nb),
# cao.NonMaleficence_Egalitarianism(nb), 
# cao.Equality_Opportunity(nb))
# print(fix)