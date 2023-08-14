import numpy as np
import pandas as pd
from collections import defaultdict


# from tabulate import tabulate

class Principle:

    # def __init__(self, preference=None, happiness=None, contribution=None, luck=None, autonomy=None,
    #              harm=None,
    #              opportunity=None, resources=None, resources_num=0, users=0):
    def __init__(self, preference=None, happiness=None, contribution=None, luck=None, resources=None, resources_num=0, users=0):
        self.preference = preference
        self.happiness = happiness
        self.contribution = contribution
        # self.envy = envy
        self.luck = luck
        # self.autonomy = autonomy
        # self.harm = harm
        # self.opportunity = opportunity
        self.users = users
        self.resources = resources
        self.resources_num = resources_num

    def Users(self):
        user = []
        for index in range(self.users):
            # user.append({'happiness': self.happiness[index], 'contribution': self.contribution[index],
            #             'luck': self.luck[index],
            #              'autonomy': self.autonomy[index], 'harm': self.harm[index],
            #              'opportunity': self.opportunity[index]})
            if self.luck == 0 or not self.luck:
                user.append({'happiness': self.happiness[index], 'contribution': self.contribution[index]})
            else:
                user.append({'happiness': self.happiness[index], 'contribution': self.contribution[index],
                             'luck': self.luck[index]})

        # for index,prefer in enumerate(self.preference):
        #     users[index]['preference'] = prefer
        #     users[index]['happiness'] = self.happiness[]

        # user = {'preference': self.preference, 'happiness': self.happiness, 'contribution': self.contribution,
        #  'luck': self.luck, 'autonomy':self.autonomy,'harm':self.harm,'opportunity':self.opportunity}
        return user

    # def num_prefer(self):
    #     num = self.users
    #     for pref in self.preference:
    #         if self.preference.count(pref) > 1:
    #             num = num - (self.preference.count(pref) - 1)
    def fix_prefer(self):
        prefer = []
        for pref in self.preference:
            if pref not in prefer:
                prefer.append(pref)
        return prefer

    def general_proportion_allocation(self, users, total):
        allocating = []
        if total == 0:
            return 'This Principle CAN NOT give the BEST output. Please look others.'
        else:
            for user in users:
                resource = round((user / total) * self.resources_num, 3)
                allocating.append(str(resource) + ' ' + self.resources)
            return allocating

    def Utilitarianism(self, users):
        total_happiness = {}
        for user in users:
            for key, value in user['happiness'].items():
                if key in total_happiness:
                    total_happiness[key] += value
                else:
                    total_happiness[key] = value
        tmp = []
        for val in total_happiness.values():
            tmp.append(val)

        if tmp.count(max(total_happiness.values())) > 1:
            return 'This Principle CAN NOT give the BEST output. Please try another.'
        else:
            return max(total_happiness, key=total_happiness.get), max(total_happiness.values())

    def utilitarianism_allocate(self, users):
        total_happiness = 0
        happiness = []
        for user in users:
            total_happiness += user['happiness']
            happiness.append(user['happiness'])
        return self.general_proportion_allocation(happiness, total_happiness)
        # for user in users:
        #     resource = round((user['happiness']/total_happiness)*self.resources_num,3)
        #     allocating.append(str(resource) + ' '+ self.resources)
        # return allocating

    def Prioritarianism(self, users):
        min_happiness = defaultdict(lambda: float('inf'))
        for user in users:
            for key, value in user['happiness'].items():
                min_happiness[key] = min(min_happiness[key], value)

        # print(min_happiness)
        tmp = []
        for val in min_happiness.values():
            tmp.append(val)

        if tmp.count(max(min_happiness.values())) > 1:
            return 'This Principle CAN NOT give the BEST output. Please try using Utilitarianism.'
        else:
            k = max(min_happiness, key=min_happiness.get)

            total_happiness = 0
            for user in users:
                for key, value in user['happiness'].items():
                    if key == k:
                        total_happiness += value
            return k, max(min_happiness.values()), total_happiness

    def EnvyFreeness(self, users):
        total_envy = {}
        for user in users:
            for key, value in user['envy'].items():
                if key in total_envy:
                    total_envy[key] += value
                else:
                    total_envy[key] = value
        mean_envy = {}
        tmp = []
        for key, val in total_envy.items():
            mean_envy[key] = round(val / self.users, 3)
            tmp.append(mean_envy[key])
        count = tmp.count(min(mean_envy.values()))
        if count > 1:
            return 'This Principle CAN NOT give the BEST output. Please try another.', min(mean_envy.values()), mean_envy, count
        else:
            return min(mean_envy, key=mean_envy.get), min(mean_envy.values()), mean_envy, count

    def envyfreeness_allocating(self, users):
        envy = {}
        total_envy = 0
        allocating = []
        for index, user in enumerate(users):
            envy[index] = user['envy']
            total_envy += user['envy']
        min_to_max = dict(sorted(envy.items(), key=lambda x: x[1]))
        max_to_min = sorted(list(envy.values()), reverse=True)
        # print(min_to_max)
        # print(max_to_min)
        # print(envy)
        envy_weight = {}
        for index, key in enumerate(min_to_max.keys()):
            envy_weight[key] = max_to_min[index]
        # print(envy_weight)
        for key, val in envy.items():
            tmp = envy_weight[key]
            for k, v in envy.items():
                if k == key:
                    continue
                if v == val:
                    if envy_weight[k] != tmp:
                        return 'This Principle CAN NOT give the BEST output. Please look others.'
        if total_envy == 0:
            return 'This Principle CAN NOT give the BEST output. Please look others.'
        else:
            for index, key in enumerate(min_to_max.keys()):
                envy[key] = round((max_to_min[index] / total_envy) * self.resources_num, 3)
            for value in envy.values():
                allocating.append(str(value) + ' ' + self.resources)
            return allocating

    # def prioritarianism_allocate(self, users):
    #     happiness = {}
    #     total_happiness = 0
    #     allocating = []
    #     for index, user in enumerate(users):
    #         happiness[index] = user['happiness']
    #         total_happiness += user['happiness']
    #     min_to_max = dict(sorted(happiness.items(), key=lambda x: x[1]))
    #     max_to_min = sorted(list(happiness.values()), reverse=True)
    #     # print(max_to_min)
    #     if len(max_to_min) != len(set(max_to_min)):
    #         return 'This Principle CAN NOT give the BEST output. Please look others.'
    #     else:
    #         for index, key in enumerate(min_to_max.keys()):
    #             happiness[key] = round((max_to_min[index] / total_happiness) * self.resources_num, 3)
    #         for value in happiness.values():
    #             allocating.append(str(value) + ' ' + self.resources)
    #         return allocating

    def DesertBased_Proportionalism(self, users):
        diff_user = {}
        for user in users:
            for key, value in user['contribution'].items():
                if key in diff_user.keys():
                    diff_user[key].append(value - user['luck'])
                else:
                    diff_user[key] = [value - user['luck']]

        # print(diff_user)
        maxvalue = {}
        tmp = []
        for key, val in diff_user.items():
            maxvalue[key] = max(val)
            tmp.append(max(val))
        # print(tmp)
        count = tmp.count(max(maxvalue.values()))
        if count > 1:
            return 'This Principle CAN NOT give the BEST output. Please try another.', max(maxvalue.values()), diff_user, count
        else:
            return max(maxvalue, key=maxvalue.get), max(maxvalue.values()), diff_user, count

    def desertbased_allocating(self, users):
        diff = []
        total_diff = 0
        allocating = []
        for user in users:
            diff.append(user['contribution'] - user['luck'])
            total_diff += user['contribution'] - user['luck']
        if any(i < 0 for i in diff):
            return 'This Principle CAN NOT give the BEST output. Please look others.'
        elif total_diff == 0:
            return 'This Principle CAN NOT give the BEST output. Please look others.'
        else:
            for value in diff:
                resource = round((value / total_diff) * self.resources_num, 3)
                allocating.append(str(resource) + ' ' + self.resources)
            return allocating

    def Libertarian_Proportionalism(self, users):
        max_contribution = {}
        for user in users:
            for key, value in user['contribution'].items():
                if key in max_contribution.keys():
                    max_contribution[key].append(value)
                else:
                    max_contribution[key] = [value]

        for key, value in max_contribution.items():
            max_contribution[key] = max(value)
        tmp = []
        for val in max_contribution.values():
            tmp.append(val)
        count = tmp.count(max(max_contribution.values()))
        if count > 1:
            return 'This Principle CAN NOT give the BEST output. Please try another.', max(max_contribution.values()), max_contribution, count
        else:
            return max(max_contribution, key=max_contribution.get), max(max_contribution.values()), max_contribution, count

    def libertarian_allocating(self, users):
        total_contribution = 0
        contribution = []
        for user in users:
            total_contribution += user['contribution']
            contribution.append(user['contribution'])
        return self.general_proportion_allocation(contribution, total_contribution)
        # for user in users:
        #     resource = round((user['contribution']/total_contribution)*self.resources_num,3)
        #     allocating.append(str(resource) + ' '+ self.resources)
        # return allocating

    def Egalitarianism(self, diction, principle):
        std = {}
        tmp = []
        sum_factor = {}
        for key, value in diction.items():
            std[key] = np.std(value)
            std[key] = round(std[key], 3)
            sum_factor[key] = sum(value)
            tmp.append(np.std(value))
        # print(std)
        count_std = tmp.count(min(tmp))
        if count_std > 1:
            new_distri = {}
            tmp2 = []
            if principle == 1:
                for key, value in diction.items():
                    if np.std(value) == min(tmp):
                        new_distri[key] = max(value)
                        tmp2.append(max(value))
                count = tmp2.count(max(new_distri.values()))
                if count > 1:
                    return 'This Principle CAN NOT give the BEST output. Please try another.', min(std.values()), max(new_distri.values()), std, sum_factor, count_std, count
                else:

                    return max(new_distri, key=new_distri.get), min(std.values()), max(new_distri.values()), std, sum_factor, count_std, count
            elif principle == 2:
                for key, value in diction.items():
                    if np.std(value) == min(tmp):
                        new_distri[key] = min(value)
                        tmp2.append(min(value))
                count = tmp2.count(min(new_distri.values()))
                if count > 1:
                    return 'This Principle CAN NOT give the BEST output. Please try another.', min(std.values()), min(new_distri.values()), std, sum_factor, count_std, count
                else:
                    return min(new_distri, key=new_distri.get), min(std.values()), min(new_distri.values()), std, sum_factor, count_std, count
        else:
            return min(std, key=std.get), min(std.values()), 'nonexistent', std, sum_factor, count_std

    def luck_egalitarianism(self, users):
        luck = {}
        total_luck = 0
        allocating = []
        for index, user in enumerate(users):
            luck[index] = user['luck']
            total_luck += user['luck']
        min_to_max = dict(sorted(luck.items(), key=lambda x: x[1]))
        max_to_min = sorted(list(luck.values()), reverse=True)
        # print(max_to_min)
        weight = {}
        for index, key in enumerate(min_to_max.keys()):
            weight[key] = max_to_min[index]
        # print(luck)
        # print(weight)
        for key, val in luck.items():
            tmp = weight[key]
            for k, v in luck.items():
                if k == key:
                    continue
                if v == val:
                    if weight[k] != tmp:
                        return 'This Principle CAN NOT give the BEST output. Please look others.'
        if total_luck == 0:
            return 'This Principle CAN NOT give the BEST output. Please look others.'
        else:
            for index, key in enumerate(min_to_max.keys()):
                luck[key] = round((max_to_min[index] / total_luck) * self.resources_num, 3)
            for value in luck.values():
                allocating.append(str(value) + ' ' + self.resources)
            return allocating

    def Autonomy_Egalitarianism(self, users):
        distri = {}
        for user in users:
            for key, value in user['autonomy'].items():
                if key in distri.keys():
                    distri[key].append(value)
                else:
                    distri[key] = [value]
        # print(distri)
        return self.Egalitarianism(distri, principle=1)

    def autonomy_allocate(self, users):
        total_autonomy = 0
        autonomy = []
        for user in users:
            total_autonomy += user['autonomy']
            autonomy.append(user['autonomy'])
        return self.general_proportion_allocation(autonomy, total_autonomy)

    def NonMaleficence_Egalitarianism(self, users):
        distri = {}
        for user in users:
            for key, value in user['harm'].items():
                if key in distri.keys():
                    distri[key].append(value)
                else:
                    distri[key] = [value]
        # print(distri)
        return self.Egalitarianism(distri, principle=2)

    def nonmaleficence_allocate(self, users):
        harm = {}
        total_harm = 0
        allocating = []
        for index, user in enumerate(users):
            harm[index] = user['harm']
            total_harm += user['harm']
        min_to_max = dict(sorted(harm.items(), key=lambda x: x[1]))
        max_to_min = sorted(list(harm.values()), reverse=True)
        # print(max_to_min)
        weight = {}
        for index, key in enumerate(min_to_max.keys()):
            weight[key] = max_to_min[index]
        # print(luck)
        # print(weight)
        for key, val in harm.items():
            tmp = weight[key]
            for k, v in harm.items():
                if k == key:
                    continue
                if v == val:
                    if weight[k] != tmp:
                        return 'This Principle CAN NOT give the BEST output. Please look others.'
        if total_harm == 0:
            return 'This Principle CAN NOT give the BEST output. Please look others.'
        else:
            for index, key in enumerate(min_to_max.keys()):
                harm[key] = round((max_to_min[index] / total_harm) * self.resources_num, 3)
            for value in harm.values():
                allocating.append(str(value) + ' ' + self.resources)
            return allocating

    def Equality_Opportunity(self, users):
        distri = {}
        for user in users:
            for key, value in user['opportunity'].items():
                if key in distri.keys():
                    distri[key].append(value)
                else:
                    distri[key] = [value]
        # print(distri)
        return self.Egalitarianism(distri, principle=1)

    def opportunity_allocate(self, users):
        total_opportunity = 0
        opportunity = []
        for user in users:
            total_opportunity += user['opportunity']
            opportunity.append(user['opportunity'])
        return self.general_proportion_allocation(opportunity, total_opportunity)

# users = []
# preference = []
# factors = []
# other_fac = []
# principle_decide = pd.read_csv('principle.csv')
# width = pd.util.terminal.get_terminal_size() # find the width of the user's terminal window
# pd.set_option('display.width', width[0]) # set that as the max width in Pandas
# print('What kind of Social Dilemma Scenario do you want to solve?')
# print('1.Deciding the Best Action 2.Allocating Resources')
# scenario = input('Please input the Number: ')
# num_user = int(input('How many people are involved in?(should be >2): '))
# if scenario == '1':
#     print('Please Choose a preferred Ethics Principle to solve')
#     print(tabulate(principle_decide, headers='keys'))
#     principle = input('Please input the Index: ')
#     if principle == '0':
#         for user in range(1,num_user+1):
#             specific_user = {'preference': None, 'happiness': None }
#             utili_prefer = input('For User' + user + ', Please input Preference: ')
#             utili_fac = input('And input Utility/Happiness value for this Preference(MAX 10): ')
#             specific_user['preference'] = utili_prefer
#             specific_user['happiness'] = {utili_prefer: utili_fac}
#             preference.append(utili_prefer)
#             factors.append(utili_fac)
#             fac = []
#             for u in range (1,num_user+1):
#                 if u == user:
#                     continue
#                 else:
#                     others = input('What`s your Utility/Happiness value for others` Preference? For User'+ u +': ')
#                     fac.append(others)
#             other_fac.append(fac)


# user1 = {'preference': 'pizza', 'happiness': {'pizza':3,'burger':4} , 'contribution':{'pizza': 6,'burger': 3}, 'luck': 4}
# user2 = {'preference': 'burger', 'happiness': {'pizza':5,'burger':6}, 'contribution':{'pizza': 4,'burger': 7}, 'luck': 7}


# Utilitarianism(users)
# Prioritarianism(users)
# Libertarian_Proportionalism(users)
# DesertBased_Proportionalism(users)


