import random
import lib 
import json

"""modul pro výpočet výsledků voleb"""

def get_election_result(name: str, data: dict):
    """vytvoření a uložení kompletních výsledků voleb na základě vstupních hodnot"""
    parties = lib.parties

    voters = lib.voters
    parties_name_bank = lib.parties_name_bank
    prefc = lib.prefc

    my_party = {name : data}
    my_party = {name : {
        "data" : data,
        "seats" : 0
    }}
    parties.update(my_party)

    get_party_result(name, data)


    for a in range(1,7):
        party_data = {}
        for one_prefer in prefc:
            values = {}
            values.update(prefc[one_prefer]["point_class"]["values"])
            max_rest_count = prefc[one_prefer]["point_class"]["max_rest_count"]
            for party in parties:
                if one_prefer in parties[party]:
                    number = parties[party][one_prefer]
                    values = get_opinion(number, values, max_rest_count)
            points = get_point(values)
            one_prefer_points = {one_prefer : points}
            party_data.update(one_prefer_points)
        party_name = parties_name_bank[a]
        party_entry = {party_name : {
            "data" : party_data,
            "seats" : 0
        }}
        parties.update(party_entry)

        get_party_result(party_name, party_data)
    update_seats()
    
def update_seats():
    """výpočet a uložení počtu křesel pro jednotlivé strany"""
    parties = lib.parties
    voters = lib.voters

    parties_list = []
    voters_list = []
    seats_list = []

    for party in parties:
        count = 0
        for voter in voters:
            if voters[voter]["commitment"] == party:
                count += voters[voter]["quantity"]
        parties_list.append(party)
        voters_list.append(count)

    winner = parties_list[voters_list.index(max(voters_list))]

    winner_index = voters_list.index(max(voters_list))
    winner_party = parties_list[winner_index]
    winner_voters = voters_list[winner_index]
    parties_list.remove(winner_party)
    voters_list.remove(winner_voters) 

    parties[winner]["seats"] = 101    

    rest = sum([i for i in voters_list])
    one_seat = rest / 99

    for one_party in parties_list:
        index = parties_list.index(one_party)
        votes = voters_list[index]
        seats = round(votes / one_seat)
        seats_list.append(seats)

    # while True:
    #     if sum([i for i in seats_list]) > 99:
    #         top_party = voters_list.index(max(voters_list))
    #         voters_list[top_party] -= 1
    #     elif sum([i for i in seats_list]) < 99:
    #         top_party = voters_list.index(max(voters_list))
    #         voters_list[top_party] += 1
    #     else:
    #         break
    
    for party in parties_list:
        seats = seats_list[parties_list.index(party)]
        parties[party]["seats"] = seats

def change_game_variables(requirements: dict):
    """změna herních proměnných"""
    game_variables = lib.game_variables
    for one in requirements:
        for variable in game_variables:
            if one == variable:
                game_variables[variable] += requirements[one]

def get_party_result(name: str, data: dict):
    """výpočet a uložení výsledků pro jednu stranu"""
    voters = lib.voters
    for voter in voters:
        if voters[voter]["commitment"] == False:
            semi_party_data = {}
            for category in data:
                number_one = voters[voter]["opinion"][category]
                number_two = data[category]
                number_three = get_probability(number_one, number_two)
                semi_party_data.update({category : number_three})
            avarage = get_avarage(semi_party_data)
            if get_one_result(avarage) == True:
                voters[voter]["commitment"] = name
    return voters

def get_probability(number_one: float, number_two: float):
    """výpočet pravděpodobnosti"""
    if number_one > number_two:
        return round(number_two/number_one, 2)
    elif number_one == number_two:
        return round(number_two/number_one, 2)
    elif number_one < number_two:
        return round(number_one/number_two, 2)
    else:
        return False
    
def get_avarage(numbers: dict):
    """výpočet průměru pro jednu stranu"""
    count_numbers = 0
    sum_numbers = 0
    for number in numbers:
        if isinstance(numbers[number], (int, float)):
            count_numbers += 1
            sum_numbers += numbers[number]
    return round(sum_numbers/count_numbers, 2)

def get_one_result(number: float):
    """výpočet, zda se volič rozhodne pro stranu, na základě pravděpodobnosti"""
    if number >= 0 and number <= 1:
        new = number*100
        maybe = random.randint(1, 200)
        if maybe <= new:
            return True
        else:
            return False
    else:
        return False

def get_opinion(number: int, values: dict, max_rest_count: int):
    """výpočet a úprava hlasovacích preferencí pro jednu stranu"""
    rest = 0
    if number in values:
        old = values[number] 
        values[number] = values[number]/2
        rest = old - values[number]
            
    for value in values:
        if value != number:
            values[value] += rest/max_rest_count

    count = 0
    for value in values:
        new_value = round(values[value])
        values[value] = new_value
        count += values[value]

    if count < 100:
        x = 100 - count
        values[1] += x
    elif count > 100:
        x = count - 100
        values[1] -= x

    return values

    
def get_point(values: dict):
    """výpočet hlasovacích preferencí pro jednu stranu, na základě upravených preferencí"""
    i = random.randint(1, 100)
    y = 0
    for value in values:
        if i <= (values[value]+y):
            return value
        else:
            y += values[value]

def restart_game():
    lib.parties.clear()

    with open('../txt/user_data/voters.txt', encoding='utf-8') as voters_data:
        voters = json.load(voters_data)
    
    lib.voters.clear()
    lib.voters.update(voters)

def get_variables_election_result(data: dict):
    """změna herních proměnných na základě preferencí strany"""
    if data["energy"] + data["infrastructure"] + data["industry"] + data["startups"] >= 16:
        change_game_variables({"economy" : 1})
    if data["healthcare"] + data["education"] + data["pensions"] >= 12:
        change_game_variables({"social" : 1})
    if data["defense"] == 5:
        change_game_variables({"army" : 1})
    if data["alliance"] == 5:
        change_game_variables({"diplomacy_alliance" : 1})
    if data["enemy"] == 5:
        change_game_variables({"diplomacy_enemy" : 1, "diplomacy_alliance" : -1})
    if data["housing"] + data["culture"] + data["environment"] >= 12:
        change_game_variables({"social" : 1})
    if data["migration"] + data["minorities"] <= 3:
        change_game_variables({"radicalization" : 1})
    if data["human_tax"] == 10 and data["corporate_tax"] == 8:
        change_game_variables({"radicalization" : 1})
    if data["freedom"] == 1:
        change_game_variables({"radicalization" : 1, "crime" : 1})
    if data["corruption"] == 1:
        change_game_variables({"crime" : 1})
    if data["referendum"] + data["debts"] + data["digitalization"] >= 12:
        change_game_variables({"economy" : 1, "social" : 1})