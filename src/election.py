import random
import lib

def get_election_result(name, data):
    parties = lib.parties
    voters = lib.voters
    parties_name_bank = lib.parties_name_bank
    prefc = lib.prefc

    my_party = {name : data}
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
        party_entry = {party_name : party_data}
        parties.update(party_entry)

        get_party_result(party_name, party_data)

def get_party_result(name, data):
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

def get_probability(number_one, number_two):
    if number_one > number_two:
        return round(number_two/number_one, 2)
    elif number_one == number_two:
        return round(number_two/number_one, 2)
    elif number_one < number_two:
        return round(number_one/number_two, 2)
    else:
        return False
    
def get_avarage(numbers):
    count_numbers = 0
    sum_numbers = 0
    for number in numbers:
        if isinstance(numbers[number], (int, float)):
            count_numbers += 1
            sum_numbers += numbers[number]
    return round(sum_numbers/count_numbers, 2)

def get_one_result(number):
    if number >= 0 and number <= 1:
        new = number*100
        maybe = random.randint(1, 200)
        if maybe <= new:
            return True
        else:
            return False
    else:
        return False

def get_opinion(number, values, max_rest_count):
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

    
def get_point(values):
    i = random.randint(1, 100)
    y = 0
    for value in values:
        if i <= (values[value]+y):
            return value
        else:
            y += values[value]