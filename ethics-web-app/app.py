from flask import Flask, render_template, url_for, redirect, request
from ethics import ethics_test as principle
import string
from urllib.parse import urlencode

app = Flask(__name__)
app.config.from_object(principle)
# app.config['STATIC_FOLDER'] = '/static'
# app.config['STATIC_URL_PATH'] = '/static'
#
# #
# @app.context_processor
# def add_timestamp():
#     def timestamped_url_for(endpoint, **values):
#         if endpoint == 'static':
#             filename = values.get('filename', None)
#             if filename:
#
#                 values['v'] = int(os.stat(os.path.join(app.static_folder, filename)).st_mtime)
#         return url_for(endpoint, **values)
#     return dict(url_for=timestamped_url_for)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        # return render_template('homepage.html')
        return render_template('homepage.html')
    else:
        # return redirect(url_for('num_users'))
        action = request.form['action']
        if action == 'allocating':
            return redirect(url_for('allocating'))
        elif action == 'deciding':
            return redirect(url_for('deciding_prefer'))


# @app.route('/num_users', methods=['GET', 'POST'])
# def num_users():
#     if request.method == 'GET':
#         return render_template('num_users.html')
#     else:
#         if not request.form['user_num'].isdigit():
#             error = 'Please enter a valid number.'
#             return render_template('num_users.html', error=error)
#         else:
#             num = int(request.form['user_num'])
#             return redirect(url_for('scenario', number=num))


# @app.route('/choose_social_dilemma', methods=['GET', 'POST'])
# def scenario():
#     if request.method == 'GET':
#         return render_template('scenario.html')
#     else:
#         action = request.form['action']
#         if action == 'allocating':
#             return redirect(url_for('allocating'))
#         elif action == 'deciding':
#             return redirect(url_for('deciding_prefer'))


@app.route('/allocating', methods=['GET', 'POST'])
def allocating():
    if request.method == 'GET':
        return render_template('allocating.html')
    else:
        allocate_num = request.form.get('allocate_num', '')
        resource = request.form.get('resource', '')
        resource_num = request.form.get('resource_num', '')
        if not request.form['allocate_num'].isdigit() or not request.form['resource_num'].isdigit():
            error = 'Please enter a valid number.'
            return render_template('allocating.html', error=error, allocate_num=allocate_num, resource=resource,
                                   resource_num=resource_num)
        else:
            for char in request.form['resource']:
                if char in string.punctuation:
                    error_r = 'Please enter valid resource.'
                    return render_template('allocating.html', error_r=error_r,  allocate_num=allocate_num,
                                           resource=resource, resource_num=resource_num)
        num_user = int(request.form['allocate_num'])
        resource_num = int(request.form['resource_num'])
        resource = request.form['resource']
        return redirect(url_for('allocating_factors', resource=resource, resource_num=resource_num, num_user=num_user+1))


@app.route('/deciding/', methods=['GET', 'POST'])
def deciding_prefer():
    if request.method == 'GET':
        return render_template('preference.html')
    else:
        user_num = request.form.get('user_num', '')
        actions = request.form.get('preference', '')
        up_actions = actions.upper()
        up_actions = up_actions.split(',')
        if not request.form['user_num'].isdigit():
            error = 'Please enter a valid number.'
            return render_template('preference.html', error=error, user_num=user_num, actions=actions)
        else:
            num_user = int(request.form['user_num'])
            preference = request.form['preference']
            if '/' in preference:
                error_p = 'Please input valid options.'
                return render_template('preference.html', error_p=error_p, user_num=user_num, actions=actions)
            else:
                preference = preference.split(',')
                if len(preference) < 2:
                    error_n = 'Please input enough options.'
                    return render_template('preference.html', error_p=error_n, user_num=user_num, actions=actions)
                if len(up_actions) != len(set(up_actions)):
                    error_l = 'Some Options are the same. Please input enough options.'
                    return render_template('preference.html', error_p=error_l, user_num=user_num, actions=actions)
                # for num in range(1, num_user):
                #     preference.append(request.form[f'user{num}prefer'])

                preference = [x.strip() for x in preference]
                fix_prefer = principle.Principle(preference=preference).fix_prefer()
                preference = ', '.join(map(str, preference))
                fix_prefer = ','.join(map(str, fix_prefer))
                return redirect(url_for('deciding_factors', preference=preference,
                                        fix_prefer=fix_prefer, num_user=num_user+1))
                # return redirect(url_for('deciding_factors', preference=preference,
                #                         num_user=num_user+1))


# @app.route('/deciding/<preference>/<fix_prefer>/<int:num_user>', methods=['GET', 'POST'])
@app.route('/decidingInput/', methods=['GET', 'POST'])
def deciding_factors():
    # preference = eval(preference)
    # preference = ', '.join(preference)
    #
    # fix_prefer = eval(fix_prefer)

    preference = request.args.get('preference')
    # preference = eval(preference)
    # preference = list(map(str, preference.split(',')))
    # preference = eval(preference)
    # preference = ', '.join(preference)

    fix_prefer = request.args.get('fix_prefer')
    fix_prefer = list(map(str, fix_prefer.split(',')))
    # print(fix_prefer)
    num_user = request.args.get('num_user')
    num_user = int(num_user)

    if request.method == 'GET':
        return render_template('deciding.html', preference=preference, fix_prefer=fix_prefer, num_user=num_user)
    else:
        # for value in request.form.values():
        #     if not value.isdigit():
        #         error = 'Please enter a valid number.'
                # valueID = request.form.get(value)
                # happiness = ','.join(map(str, happiness))
                # contribution = ','.join(map(str, contribution))
                # autonomy = ','.join(map(str, autonomy))
                # opportunity = ','.join(map(str, opportunity))
                # harm = ','.join(map(str, harm))
                # fix_prefer = ','.join(map(str, fix_prefer))
                # return render_template('deciding.html', preference=preference, fix_prefer=fix_prefer, num_user=num_user,
                #                        error=error)
        happiness = []
        # envy = []
        luck = []
        contribution = []
        # autonomy = []
        # harm = []
        # opportunity = []
        for num in range(1, num_user):
            tmp_happy = {}
            tmp_envy = {}
            tmp_contribute = {}
            # tmp_auto = {}
            # tmp_harm = {}
            # tmp_oppo = {}
            if not request.form.get(f'user{num}luck').isdigit():
                luck.append(0)
            else:
                luck.append(int(request.form[f'user{num}luck']))
            for prefer in fix_prefer:
                if not request.form.get(f'user{num}{prefer}happy').isdigit():
                    tmp_happy[prefer] = 0
                else:
                    tmp_happy[prefer] = int(request.form[f'user{num}{prefer}happy'])
                # tmp_envy[prefer] = int(request.form[f'user{num}{prefer}envy'])
                if not request.form.get(f'user{num}{prefer}contribute').isdigit():
                    tmp_contribute[prefer] = 0
                else:
                    tmp_contribute[prefer] = int(request.form[f'user{num}{prefer}contribute'])
                # tmp_auto[prefer] = int(request.form[f'user{num}{prefer}auto'])
                # tmp_harm[prefer] = int(request.form[f'user{num}{prefer}harm'])
                # tmp_oppo[prefer] = int(request.form[f'user{num}{prefer}oppo'])
            happiness.append(tmp_happy)
            # envy.append(tmp_envy)
            contribution.append(tmp_contribute)
            # autonomy.append(tmp_auto)
            # harm.append(tmp_harm)
            # opportunity.append(tmp_oppo)

        luck = ','.join(map(str, luck))
        happiness = ','.join(map(str, happiness))
        contribution = ','.join(map(str, contribution))
        # autonomy = ','.join(map(str, autonomy))
        # opportunity = ','.join(map(str, opportunity))
        # harm = ','.join(map(str, harm))
        fix_prefer = ','.join(map(str, fix_prefer))

        # return redirect(url_for('deciding_output', preference=preference, fix_prefer=fix_prefer, num_user=num_user-1, luck=luck,
        #                         happiness=happiness, contribution=contribution, autonomy=autonomy, harm=harm,
        #                         opportunity=opportunity))
        return redirect(url_for('deciding_output', preference=preference, fix_prefer=fix_prefer, num_user=num_user - 1, luck=luck,
                    happiness=happiness, contribution=contribution))


# @app.route('/deciding/<preference>/<int:num_user>/<luck>/<happiness>/<contribution>/<autonomy>/<harm>/<opportunity>', methods=['GET', 'POST'])
@app.route('/decidingOutput/', methods=['GET', 'POST'])
def deciding_output():
    preference = request.args.get('preference')

    fix_prefer = request.args.get('fix_prefer')
    preferenceList = list(map(str, fix_prefer.split(',')))

    luck = request.args.get('luck')
    luck = eval(luck)
    # print(luck)

    happiness = request.args.get('happiness')
    happiness = eval(happiness)


    contribution = request.args.get('contribution')
    contribution = eval(contribution)

    # autonomy = request.args.get('autonomy')
    # autonomy = eval(autonomy)
    #
    # harm = request.args.get('harm')
    # harm = eval(harm)
    #
    # opportunity = request.args.get('opportunity')
    # opportunity = eval(opportunity)

    num_user = request.args.get('num_user')
    num_user = int(num_user)


    # num_user = int(num_user)
    # print(num_user)
    output = principle.Principle(preferenceList, happiness, contribution, luck, None, 0, num_user)
    users = output.Users()

    utilitarianism = output.Utilitarianism(users)
    total_happiness = {}
    for value in happiness:
        for key, v in value.items():
            if key in total_happiness:
                total_happiness[key] += v
            else:
                total_happiness[key] = v
    tmpH = []
    for val in total_happiness.values():
        tmpH.append(val)
    max_happiness = max(total_happiness.values())
    count_happiness = tmpH.count(max(total_happiness.values()))
    # envyfreeness = output.EnvyFreeness(users)

    prioritarianism = output.Prioritarianism(users)
    low_happiness = {}
    for value in happiness:
        for key, v in value.items():
            if key in low_happiness:
                low_happiness[key].append(v)
            else:
                low_happiness[key] = [v]
    lowestPri = {}
    for key, value in low_happiness.items():
        lowestPri[key] = min(value)
    tmpPri = []
    for val in lowestPri.values():
        tmpPri.append(val)
    max_valuePri = max(lowestPri.values())
    countPri = tmpPri.count(max(lowestPri.values()))

    desertbased_proportionalism = output.DesertBased_Proportionalism(users)
    libertarian_proportionalism = output.Libertarian_Proportionalism(users)
    # autonomy_egalitarianism = output.Autonomy_Egalitarianism(users)
    # nonmaleficence_egalitarianism = output.NonMaleficence_Egalitarianism(users)
    # equality_opportunity = output.Equality_Opportunity(users)

    if request.method == 'GET':
        return render_template('deciding_output.html', preference=preference, preferenceList=preferenceList,
                               fix_prefer=fix_prefer, num_user=num_user,
                               luck=luck,
                               happiness=happiness,
                               contribution=contribution,
                               utilitarianism=utilitarianism, max_happiness=max_happiness,
                               count_happiness=count_happiness, total_happiness=total_happiness,
                               prioritarianism=prioritarianism, max_valuePri=max_valuePri, countPri=countPri,
                               lowestPri=lowestPri,
                               desertbased_proportionalism=desertbased_proportionalism,
                               libertarian_proportionalism=libertarian_proportionalism)
        # return render_template('deciding_output.html', preference=preference, preferenceList=preferenceList,
        #                        fix_prefer=fix_prefer, num_user=num_user,
        #                        luck=luck,
        #                        happiness=happiness,
        #                        contribution=contribution,
        #                        autonomy=autonomy,
        #                        harm=harm,
        #                        opportunity=opportunity,
        #                        utilitarianism=utilitarianism, max_happiness=max_happiness,
        #                        count_happiness=count_happiness, total_happiness=total_happiness,
        #                        prioritarianism=prioritarianism, max_valuePri=max_valuePri, countPri=countPri,
        #                        lowestPri=lowestPri,
        #                        desertbased_proportionalism=desertbased_proportionalism,
        #                        libertarian_proportionalism=libertarian_proportionalism,
        #                        autonomy_egalitarianism=autonomy_egalitarianism,
        #                        nonmaleficence_egalitarianism=nonmaleficence_egalitarianism,
        #                        equality_opportunity=equality_opportunity)
    else:

        return redirect(url_for('hello_world'))


@app.route('/deciding/utilitarianism/<utilitarianism>/<preference>/<int:num_user>/<happiness>')
def utilitarianism_deciding(preference, num_user, utilitarianism, happiness):
    if utilitarianism != 'This Principle CAN NOT give the BEST output. Please try another.':
        utilitarianism = eval(utilitarianism)
    preference = eval(preference)
    happiness = eval(happiness)
    total_happiness = {}
    for value in happiness:
        for key, v in value.items():
            if key in total_happiness:
                total_happiness[key] += v
            else:
                total_happiness[key] = v
    tmp = []
    for val in total_happiness.values():
        tmp.append(val)
    max_value = max(total_happiness.values())
    count = tmp.count(max(total_happiness.values()))
    return render_template('utilitarianism_deciding.html', preference=preference, num_user=num_user,
                           utilitarianism=utilitarianism, happiness=happiness,
                           total_happiness=total_happiness, count=count, max_value=max_value)


@app.route('/deciding/prioritarianism/<prioritarianism>/<preference>/<int:num_user>/<happiness>')
def prioritarianism_deciding(preference, num_user, prioritarianism, happiness):
    if prioritarianism != 'This Principle CAN NOT give the BEST output. Please try using Utilitarianism.':
        prioritarianism = eval(prioritarianism)
    preference = eval(preference)
    happiness = eval(happiness)
    low_happiness = {}
    for value in happiness:
        for key, v in value.items():
            if key in low_happiness:
                low_happiness[key].append(v)
            else:
                low_happiness[key] = [v]
    lowest = {}
    for key, value in low_happiness.items():
        lowest[key] = min(value)
    tmp = []
    for val in lowest.values():
        tmp.append(val)
    max_value = max(lowest.values())
    count = tmp.count(max(lowest.values()))
    return render_template('prioritarianism_deciding.html', preference=preference, num_user=num_user,
                           prioritarianism=prioritarianism, happiness=happiness,
                           lowest=lowest, count=count, max_value=max_value)


@app.route('/deciding/envyfreeness/<envyfreeness>/<preference>/<int:num_user>/<envy>')
def envyfreeness_deciding(preference, num_user, envyfreeness, envy):
    envyfreeness = eval(envyfreeness)
    preference = eval(preference)
    envy = eval(envy)
    total_envy = {}
    for value in envy:
        for key, v in value.items():
            if key in total_envy:
                total_envy[key] += v
            else:
                total_envy[key] = v
    return render_template('envyfreeness_deciding.html', preference=preference, num_user=num_user,
                           envyfreeness=envyfreeness, envy=envy,
                           total_envy=total_envy)


@app.route('/deciding/desertbased_proportionalism/<desertbased_proportionalism>/<preference>/<int:num_user>/<luck>/'
           '<contribution>')
def desertbased_deciding(preference, num_user, desertbased_proportionalism, luck, contribution):
    desertbased_proportionalism = eval(desertbased_proportionalism)
    preference = eval(preference)
    luck = eval(luck)
    contribution = eval(contribution)
    return render_template('desertbased_deciding.html', preference=preference, num_user=num_user,
                           desertbased_proportionalism=desertbased_proportionalism, luck=luck, contribution=contribution)


@app.route('/deciding/egalitarianism/<egalitarianism>/<preference>/<int:num_user>/<factor>/<typ>/')
def egalitarianism_deciding(preference, num_user, egalitarianism, factor, typ):
    egalitarianism = eval(egalitarianism)
    preference = eval(preference)
    factor = eval(factor)
    return render_template('egalitarianism_deciding.html', preference=preference, num_user=num_user,
                           egalitarianism=egalitarianism, factor=factor, typ=typ)


@app.route('/deciding/libertarian_proportionalism/<libertarian_proportionalism>/<preference>/<int:num_user>/<contribution>')
def libertarian_deciding(preference, num_user, libertarian_proportionalism, contribution):
    libertarian_proportionalism = eval(libertarian_proportionalism)
    preference = eval(preference)
    contribution = eval(contribution)
    return render_template('libertarian_deciding.html', preference=preference, num_user=num_user,
                           libertarian_proportionalism=libertarian_proportionalism, contribution=contribution)


@app.route('/allocatingFactor', methods=['GET', 'POST'])
def allocating_factors():
    # resource = eval(resource)
    num_user = request.args.get('num_user')
    num_user = int(num_user)

    resource_num = request.args.get('resource_num')
    resource_num = int(resource_num)

    resource = request.args.get('resource')

    if request.method == 'GET':
        return render_template('allocating_factors.html', resource=resource, resource_num=resource_num,
                               num_user=num_user)
    else:
        # for value in request.form.values():
        #     if not value.isdigit():
                # error = 'Please enter a valid number.'
                # return render_template('allocating_factors.html', resource=resource, resource_num=resource_num,
                #                        num_user=num_user, error=error)
        happiness = []
        # luck = []
        contribution = []
        # envy = []
        # autonomy = []
        # harm = []
        # opportunity = []
        for num in range(1, num_user):
            if not request.form.get(f'user{num}happy').isdigit():
                happiness.append(0)
            else:
                happiness.append(int(request.form.get(f'user{num}happy')))
            if not request.form.get(f'user{num}contribute').isdigit():
                contribution.append(0)
            else:
                contribution.append(int(request.form[f'user{num}contribute']))
            # envy.append(int(request.form[f'user{num}envy']))
            # luck.append(int(request.form[f'user{num}luck']))
            # autonomy.append(int(request.form[f'user{num}auto']))
            # harm.append(int(request.form[f'user{num}harm']))
            # opportunity.append(int(request.form[f'user{num}oppo']))
        # return redirect(url_for('allocating_output', resource=resource, resource_num=resource_num, num_user=num_user - 1,
        #                         luck=luck, happiness=happiness, envy=envy, contribution=contribution, autonomy=autonomy,
        #                         harm=harm, opportunity=opportunity))
        happiness = ','.join(map(str, happiness))
        contribution = ','.join(map(str, contribution))
        return redirect(url_for('allocating_output', resource=resource, resource_num=resource_num,
                                num_user=num_user - 1, happiness=happiness, contribution=contribution))


@app.route('/allocatingOutput', methods=['GET', 'POST'])
def allocating_output():
    happiness = request.args.get('happiness')
    happiness = eval(happiness)
    total_happiness = int(sum(happiness))
    # happiness = list(map(int, happiness.split(',')))


    contribution = request.args.get('contribution')
    # contribution = list(map(int, contribution.split(',')))
    contribution = eval(contribution)
    total_contribution = int(sum(contribution))

    num_user = request.args.get('num_user')
    num_user = int(num_user)

    resource_num = request.args.get('resource_num')
    resource_num = int(resource_num)

    resource = request.args.get('resource')

    output = principle.Principle(None, happiness, contribution, 0, resource, resource_num, num_user)

    users = output.Users()
    utilitarianism = output.utilitarianism_allocate(users)
    # envyfreeness = output.envyfreeness_allocating(users)
    # desertbased_proportionalism = output.desertbased_allocating(users)
    libertarian_proportionalism = output.libertarian_allocating(users)
    # luck_egalitarianism = output.luck_egalitarianism(users)
    # autonomy_egalitarianism = output.autonomy_allocate(users)
    # nonmaleficence_egalitarianism = output.nonmaleficence_allocate(users)
    # equality_opportunity = output.opportunity_allocate(users)
    if request.method == 'GET':
        return render_template('allocating_output.html', resource=resource, resource_num=resource_num,
                               happiness=happiness, contribution=contribution,
                               utilitarianism=utilitarianism, total_happiness=total_happiness,
                               libertarian_proportionalism=libertarian_proportionalism,
                               total_contribution=total_contribution, num_user=num_user)
        # return render_template('allocating_output.html', resource=resource, resource_num=resource_num, luck=luck,
        #                        happiness=happiness, envy=envy, contribution=contribution, autonomy=autonomy, harm=harm,
        #                        opportunity=opportunity, utilitarianism=utilitarianism,
        #                        envyfreeness=envyfreeness,
        #                        desertbased_proportionalism=desertbased_proportionalism,
        #                        libertarian_proportionalism=libertarian_proportionalism,
        #                        luck_egalitarianism=luck_egalitarianism,
        #                        autonomy_egalitarianism=autonomy_egalitarianism,
        #                        nonmaleficence_egalitarianism=nonmaleficence_egalitarianism,
        #                        equality_opportunity=equality_opportunity, num_user=num_user)
    else:
        return redirect(url_for('hello_world'))


@app.route('/allocating/utilitarianism/<utilitarianism>/<int:num_user>/<resource>/<int:resource_num>/<happiness>')
def utilitarianism_allocating(resource, resource_num, num_user, utilitarianism, happiness):
    if utilitarianism != 'This Principle CAN NOT give the BEST output. Please look others.':
        utilitarianism = eval(utilitarianism)
    happiness = eval(happiness)
    total_happiness = int(sum(happiness))
    return render_template('utilitarianism_allocating.html', resource=resource, resource_num=resource_num,
                           num_user=num_user, utilitarianism=utilitarianism, happiness=happiness,
                           total_happiness=total_happiness)


@app.route('/allocating/envyfreeness/<resource>/<int:resource_num>/<int:num_user>/<envyfreeness>/<envy>')
def envyfreeness_allocating(resource, resource_num, num_user, envyfreeness, envy):
    if envyfreeness != 'This Principle CAN NOT give the BEST output. Please look others.':
        envyfreeness = eval(envyfreeness)
    envy = eval(envy)
    total_envy = int(sum(envy))
    user_index = {}
    for index in range(0, num_user):
        user_index[index] = envy[index]
    min_to_max = dict(sorted(user_index.items(), key=lambda x: x[1]))
    max_to_min = sorted(list(user_index.values()), reverse=True)
    weight = {}
    for index, key in enumerate(min_to_max.keys()):
        weight[key] = max_to_min[index]
    return render_template('envyfreeness_allocating.html', resource=resource, resource_num=resource_num,
                           num_user=num_user, envyfreeness=envyfreeness, envy=envy,
                           total_envy=total_envy, weight=weight)


@app.route('/allocating/desertbased/<desertbased_proportionalism>/<int:num_user>/<resource>/<int:resource_num>/'
           '<contribution>/''<luck>')
def desertbased_allocating(resource, resource_num, num_user, desertbased_proportionalism, contribution, luck):
    if desertbased_proportionalism != 'This Principle CAN NOT give the BEST output. Please look others.':
        desertbased_proportionalism = eval(desertbased_proportionalism)
    contribution = eval(contribution)
    luck = eval(luck)
    total_difference = int(sum(contribution) - sum(luck))
    return render_template('desertbased_allocating.html', resource=resource, resource_num=resource_num,
                           num_user=num_user, desertbased_proportionalism=desertbased_proportionalism, luck=luck,
                           contribution=contribution, total_difference=total_difference)


@app.route('/allocating/autonomy/<resource>/<int:resource_num>/<int:num_user>/'
           '<autonomy_egalitarianism>/<autonomy>')
def autonomyegalitarianism_allocating(resource, resource_num, num_user, autonomy_egalitarianism, autonomy):
    if autonomy_egalitarianism != 'This Principle CAN NOT give the BEST output. Please look others.':
        autonomy_egalitarianism = eval(autonomy_egalitarianism)
    autonomy = eval(autonomy)
    total_autonomy = int(sum(autonomy))
    return render_template('autonomyegalitarianism_allocating.html', resource=resource, resource_num=resource_num,
                           num_user=num_user, autonomy_egalitarianism=autonomy_egalitarianism,
                           autonomy=autonomy, total_autonomy=total_autonomy)


@app.route('/allocating/luckegalitarianism/<resource>/<int:resource_num>/<int:num_user>/<luck_egalitarianism>/<luck>')
def luckegalitarianism_allocating(resource, resource_num, num_user, luck_egalitarianism, luck):
    if luck_egalitarianism != 'This Principle CAN NOT give the BEST output. Please look others.':
        luck_egalitarianism = eval(luck_egalitarianism)
    luck = eval(luck)
    total_luck = int(sum(luck))
    user_index = {}
    for index in range(0, num_user):
        user_index[index] = luck[index]
    min_to_max = dict(sorted(user_index.items(), key=lambda x: x[1]))
    max_to_min = sorted(list(user_index.values()), reverse=True)
    weight = {}
    for index, key in enumerate(min_to_max.keys()):
        weight[key] = max_to_min[index]
    return render_template('luckegalitarianism_allocating.html', resource=resource, resource_num=resource_num,
                           num_user=num_user, luck_egalitarianism=luck_egalitarianism, luck=luck,
                           total_luck=total_luck, weight=weight)


@app.route('/allocating/libertarian/<resource>/<int:resource_num>/<int:num_user>/'
           '<libertarian_proportionalism>/<contribution>')
def libertarian_allocating(resource, resource_num, num_user, libertarian_proportionalism, contribution):
    if libertarian_proportionalism != 'This Principle CAN NOT give the BEST output. Please look others.':
        libertarian_proportionalism = eval(libertarian_proportionalism)
    contribution = eval(contribution)
    total_contribution = int(sum(contribution))
    return render_template('libertarian_allocating.html', resource=resource, resource_num=resource_num,
                           num_user=num_user, libertarian_proportionalism=libertarian_proportionalism,
                           contribution=contribution, total_contribution=total_contribution)


@app.route('/allocating/NonMaleficence/<resource>/<int:resource_num>/<int:num_user>/'
           '<nonmaleficence_egalitarianism>/<harm>')
def nonmaleficence_allocating(resource, resource_num, num_user, nonmaleficence_egalitarianism, harm):
    if nonmaleficence_egalitarianism != 'This Principle CAN NOT give the BEST output. Please look others.':
        nonmaleficence_egalitarianism = eval(nonmaleficence_egalitarianism)
    harm = eval(harm)
    total_harm = int(sum(harm))
    user_index = {}
    for index in range(0, num_user):
        user_index[index] = harm[index]
    min_to_max = dict(sorted(user_index.items(), key=lambda x: x[1]))
    max_to_min = sorted(list(user_index.values()), reverse=True)
    weight = {}
    for index, key in enumerate(min_to_max.keys()):
        weight[key] = max_to_min[index]
    return render_template('nonmaleficence_allocating.html', resource=resource, resource_num=resource_num,
                           num_user=num_user, nonmaleficence_egalitarianism=nonmaleficence_egalitarianism, harm=harm,
                           total_harm=total_harm, weight=weight)


@app.route('/allocating/equalityopportunity/<resource>/<int:resource_num>/<int:num_user>/'
           '<equality_opportunity>/<opportunity>')
def equalityopportunity_allocating(resource, resource_num, num_user, equality_opportunity, opportunity):
    if equality_opportunity != 'This Principle CAN NOT give the BEST output. Please look others.':
        equality_opportunity = eval(equality_opportunity)
    opportunity = eval(opportunity)
    total_opportunity = int(sum(opportunity))
    return render_template('equalityopportunity_allocating.html', resource=resource, resource_num=resource_num,
                           num_user=num_user, equality_opportunity=equality_opportunity,
                           opportunity=opportunity, total_opportunity=total_opportunity)


@app.route('/deciding/happiness')
def deciding_happiness():
    return render_template('deciding_happiness.html')


@app.route('/deciding/envy')
def deciding_envy():
    return render_template('deciding_envy.html')


@app.route('/deciding/contribution')
def deciding_contribution():
    return render_template('deciding_contribution.html')


@app.route('/deciding/luck')
def deciding_luck():
    return render_template('deciding_luck.html')


@app.route('/deciding/autonomy')
def deciding_autonomy():
    return render_template('deciding_autonomy.html')


@app.route('/deciding/harm')
def deciding_harm():
    return render_template('deciding_harm.html')


@app.route('/deciding/opportunity')
def deciding_opportunity():
    return render_template('deciding_opportunity.html')


@app.route('/allocating/happiness')
def allocating_happiness():
    return render_template('allocating_happiness.html')


@app.route('/allocating/envy')
def allocating_envy():
    return render_template('allocating_envy.html')


@app.route('/allocating/contribution')
def allocating_contribution():
    return render_template('allocating_contribution.html')


@app.route('/allocating/luck')
def allocating_luck():
    return render_template('allocating_luck.html')


@app.route('/allocating/autonomy')
def allocating_autonomy():
    return render_template('allocating_autonomy.html')


@app.route('/allocating/harm')
def allocating_harm():
    return render_template('allocating_harm.html')


@app.route('/allocating/opportunity')
def allocating_opportunity():
    return render_template('allocating_opportunity.html')


if __name__ == '__main__':
    app.run()
