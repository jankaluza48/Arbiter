point_class = {
    "1-5" : {
        "values" : {
            1 : 20,
            2 : 20,
            3 : 20,
            4 : 20,
            5 : 20
        },
        "max_rest_count" : 4
    },
    "1-4" : {
        "values" : {
            1 : 25,
            2 : 25,
            3 : 25,
            4 : 25
        },
        "max_rest_count" : 3
    }
}

prefc = {
    "education" : {
        "point_class" : point_class["1-5"] 
    },
    "healthcare" : {
        "point_class" : point_class["1-5"] 
    },
    "pensions" : {
        "point_class" : point_class["1-5"] 
    },
    "energy" : {
        "point_class" : point_class["1-5"] 
    },
    "infrastructure" : {
        "point_class" : point_class["1-5"] 
    },
    "defense" : {
        "point_class" : point_class["1-5"] 
    }, 
    "agroculture" : {
        "point_class" : point_class["1-4"] 
    },
    "industry" : {
        "point_class" : point_class["1-4"] 
    },
    "startups" : {
        "point_class" : point_class["1-4"] 
    },
    "housing" : {
        "point_class" : point_class["1-4"] 
    },
    "environment" : {
        "point_class" : point_class["1-4"] 
    },
    "culture" : {
        "point_class" : point_class["1-4"] 
    }, 
    "alliance" : {
        "point_class" : point_class["1-4"] 
    },
    "small_alliance" : {
        "point_class" : point_class["1-5"] 
    },
    "enemy" : {
        "point_class" : point_class["1-5"] 
    },
    "migration" : {
        "point_class" : point_class["1-5"] 
    },
    "minorities" : {
        "point_class" : point_class["1-5"] 
    },
    "human_tax" : {
        "point_class" : point_class["1-5"] 
    },
    "corporate_tax" : {
        "point_class" : point_class["1-5"] 
    },
    "freedom" : {
        "point_class" : point_class["1-5"] 
    },
    "religion" : {
        "point_class" : point_class["1-5"] 
    },
    "corruption" : {
        "point_class" : point_class["1-5"] 
    },
    "digitization" : {
        "point_class" : point_class["1-5"] 
    },
    "debts" : {
        "point_class" : point_class["1-5"] 
    },
    "referendum" : {
        "point_class" : point_class["1-5"] 
    }
}

age_groups = {
    "m" : {
        "years" : "18-39"
    },
    "s" : {
        "quantity" : "40-65"
    },
    "d" : {
        "quantity" : "66-85"
    }
}

opinions = {
    1 : {
        "education" : 4,
        "healthcare" : 5,
        "pensions" : 3,
        "energy" : 4,
        "infrastructure" : 4,
        "defense" : 5,
        "agroculture" : 1,
        "industry" : 1,
        "startups" : 3,
        "housing" : 2,
        "environment" : 4,
        "culture" : 3,
        "alliance" : 5, 
        "small_alliance" : 3,
        "enemy" : 1,
        "migration" : 4,
        "minorities" : 5,
        "human_tax" : 4,
        "corporate_tax" : 4, 
        "freedom" : 5, 
        "religion" : 2,
        "corruption" : 5,
        "digitization" : 5,
        "debts" : 3,
        "referendum" : 4
    }, 
    2 : {
        "education" : 4,
        "healthcare" : 4,
        "pensions" : 2,
        "energy" : 3,
        "infrastructure" : 3,
        "defense" : 3,
        "agroculture" : 2,
        "industry" : 2,
        "startups" : 4,
        "housing" : 2,
        "environment" : 2,
        "culture" : 1,
        "alliance" : 4, 
        "small_alliance" : 4,
        "enemy" : 1,
        "migration" : 2,
        "minorities" : 3,
        "human_tax" : 3,
        "corporate_tax" : 4, 
        "freedom" : 5, 
        "religion" : 2,
        "corruption" : 4,
        "digitization" : 4,
        "debts" : 3,
        "referendum" : 1
    },
    3 : {
        "education" : 4,
        "healthcare" : 3,
        "pensions" : 2,
        "energy" : 5,
        "infrastructure" : 4,
        "defense" : 1,
        "agroculture" : 1,
        "industry" : 1,
        "startups" : 4,
        "housing" : 3,
        "environment" : 4,
        "culture" : 1,
        "alliance" : 5, 
        "small_alliance" : 1,
        "enemy" : 1,
        "migration" : 1,
        "minorities" : 2,
        "human_tax" : 3,
        "corporate_tax" : 3, 
        "freedom" : 5, 
        "religion" : 1,
        "corruption" : 3,
        "digitization" : 5,
        "debts" : 2,
        "referendum" : 5
    },
    4 : {
        "education" : 4,
        "healthcare" : 5,
        "pensions" : 3,
        "energy" : 2,
        "infrastructure" : 4,
        "defense" : 4,
        "agroculture" : 2,
        "industry" : 3,
        "startups" : 3,
        "housing" : 2,
        "environment" : 2,
        "culture" : 1,
        "alliance" : 5, 
        "small_alliance" : 4,
        "enemy" : 2,
        "migration" : 2,
        "minorities" : 1,
        "human_tax" : 2,
        "corporate_tax" : 5, 
        "freedom" : 5, 
        "religion" : 2,
        "corruption" : 2,
        "digitization" : 5,
        "debts" : 3,
        "referendum" : 3
    },
    5 : {
        "education" : 4,
        "healthcare" : 4,
        "pensions" : 1,
        "energy" : 3,
        "infrastructure" : 4,
        "defense" : 5,
        "agroculture" : 1,
        "industry" : 2,
        "startups" : 2,
        "housing" : 3,
        "environment" : 3,
        "culture" : 2,
        "alliance" : 5, 
        "small_alliance" : 1,
        "enemy" : 1,
        "migration" : 2,
        "minorities" : 3,
        "human_tax" : 4,
        "corporate_tax" : 5, 
        "freedom" : 5, 
        "religion" : 3,
        "corruption" : 4,
        "digitization" : 5,
        "debts" : 4,
        "referendum" : 5
    },
    6 : {
        "education" : 5,
        "healthcare" : 5,
        "pensions" : 4,
        "energy" : 5,
        "infrastructure" : 4,
        "defense" : 5,
        "agroculture" : 4,
        "industry" : 4,
        "startups" : 3,
        "housing" : 3,
        "environment" : 3,
        "culture" : 3,
        "alliance" : 5, 
        "small_alliance" : 2,
        "enemy" : 1,
        "migration" : 3,
        "minorities" : 3,
        "human_tax" : 3,
        "corporate_tax" : 4, 
        "freedom" : 5, 
        "religion" : 3,
        "corruption" : 5,
        "digitization" : 5,
        "debts" : 4,
        "referendum" : 3
    },
    7 : {
        "education" : 3,
        "healthcare" : 4,
        "pensions" : 2,
        "energy" : 1,
        "infrastructure" : 2,
        "defense" : 5,
        "agroculture" : 3,
        "industry" : 1,
        "startups" : 2,
        "housing" : 4,
        "environment" : 2,
        "culture" : 4,
        "alliance" : 5, 
        "small_alliance" : 5,
        "enemy" : 5,
        "migration" : 1,
        "minorities" : 1,
        "human_tax" : 2,
        "corporate_tax" : 2, 
        "freedom" : 3, 
        "religion" : 4,
        "corruption" : 2,
        "digitization" : 1,
        "debts" : 5,
        "referendum" : 5
    },
    8 : {
        "education" : 1,
        "healthcare" : 1,
        "pensions" : 1,
        "energy" : 5,
        "infrastructure" : 3,
        "defense" : 2,
        "agroculture" : 4,
        "industry" : 4,
        "startups" : 2,
        "housing" : 3,
        "environment" : 1,
        "culture" : 1,
        "alliance" : 3, 
        "small_alliance" : 5,
        "enemy" : 1,
        "migration" : 1,
        "minorities" : 5,
        "human_tax" : 5,
        "corporate_tax" : 1, 
        "freedom" : 1, 
        "religion" : 1,
        "corruption" : 1,
        "digitization" : 3,
        "debts" : 5,
        "referendum" : 1
    },
    9 : {
        "education" : 4,
        "healthcare" : 4,
        "pensions" : 4,
        "energy" : 4,
        "infrastructure" : 4,
        "defense" : 2,
        "agroculture" : 4,
        "industry" : 2,
        "startups" : 2,
        "housing" : 3,
        "environment" : 1,
        "culture" : 3,
        "alliance" : 1, 
        "small_alliance" : 5,
        "enemy" : 3,
        "migration" : 1,
        "minorities" : 2,
        "human_tax" : 1,
        "corporate_tax" : 5, 
        "freedom" : 3, 
        "religion" : 3,
        "corruption" : 4,
        "digitization" : 2,
        "debts" : 5,
        "referendum" : 4
    },
    10 : {
        "education" : 2,
        "healthcare" : 5,
        "pensions" : 5,
        "energy" : 5,
        "infrastructure" : 5,
        "defense" : 5,
        "agroculture" : 3,
        "industry" : 3,
        "startups" : 1,
        "housing" : 4,
        "environment" : 1,
        "culture" : 2,
        "alliance" : 1, 
        "small_alliance" : 3,
        "enemy" : 5,
        "migration" : 1,
        "minorities" : 1,
        "human_tax" : 2,
        "corporate_tax" : 5, 
        "freedom" : 1, 
        "religion" : 2,
        "corruption" : 1,
        "digitization" : 2,
        "debts" : 4,
        "referendum" : 5
    },
}
voters = {
    "m1" : {
        "opinion" : opinions[1],
        "age_group" : age_groups["m"],
        "compassion" : 8, 
        "memory" : 10,
        "quantity" : 300000,
        "commitment" : False
    },
    "m2" : {
        "opinion" : opinions[2],
        "age_group" : age_groups["m"],
        "compassion" : 7, 
        "memory" : 10,
        "quantity" : 300000,
        "commitment" : False
    },
    "m3" : {
        "opinion" : opinions[3],
        "age_group" : age_groups["m"],
        "compassion" : 9, 
        "memory" : 9,
        "quantity" : 800000,
        "commitment" : False
    },
    "m4" : {
        "opinion" : opinions[4],
        "age_group" : age_groups["m"],
        "compassion" : 7, 
        "memory" : 7,
        "quantity" : 200000,
        "commitment" : False
    },
    "m5" : {
        "opinion" : opinions[5],
        "age_group" : age_groups["m"],
        "compassion" : 8, 
        "memory" : 7,
        "quantity" : 300000,
        "commitment" : False
    },
    "m6" : {
        "opinion" : opinions[6],
        "age_group" : age_groups["m"],
        "compassion" : 6, 
        "memory" : 6,
        "quantity" : 400000,
        "commitment" : False
    },
    "m7" : {
        "opinion" : opinions[7],
        "age_group" : age_groups["m"],
        "compassion" : 8, 
        "memory" : 5,
        "quantity" : 100000,
        "commitment" : False
    },
    "m8" : {
        "opinion" : opinions[8],
        "age_group" : age_groups["m"],
        "compassion" : 3, 
        "memory" : 4,
        "quantity" : 300000,
        "commitment" : False
    },
    "m9" : {
        "opinion" : opinions[9],
        "age_group" : age_groups["m"],
        "compassion" : 4, 
        "memory" : 4,
        "quantity" : 100000,
        "commitment" : False
    },
    "m10" : {
        "opinion" : opinions[10],
        "age_group" : age_groups["m"],
        "compassion" : 1, 
        "memory" : 3,
        "quantity" : 200000,
        "commitment" : False
    },
    "s1" : {
        "opinion" : opinions[1],
        "age_group" : age_groups["s"],
        "compassion" : 9, 
        "memory" : 9,
        "quantity" : 200000,
        "commitment" : False
    },
    "s2" : {
        "opinion" : opinions[2],
        "age_group" : age_groups["s"],
        "compassion" : 8, 
        "memory" : 10,
        "quantity" : 400000,
        "commitment" : False
    },
    "s3" : {
        "opinion" : opinions[3],
        "age_group" : age_groups["s"],
        "compassion" : 9, 
        "memory" : 9,
        "quantity" : 500000,
        "commitment" : False
    },
    "s4" : {
        "opinion" : opinions[4],
        "age_group" : age_groups["s"],
        "compassion" : 6, 
        "memory" : 8,
        "quantity" : 600000,
        "commitment" : False
    },
    "s5" : {
        "opinion" : opinions[5],
        "age_group" : age_groups["s"],
        "compassion" : 7, 
        "memory" : 7,
        "quantity" : 800000,
        "commitment" : False
    },
    "s6" : {
        "opinion" : opinions[6],
        "age_group" : age_groups["s"],
        "compassion" : 7, 
        "memory" : 6,
        "quantity" : 600000,
        "commitment" : False
    },
    "s7" : {
        "opinion" : opinions[7],
        "age_group" : age_groups["s"],
        "compassion" : 6, 
        "memory" : 5,
        "quantity" : 300000,
        "commitment" : False
    },
    "s8" : {
        "opinion" : opinions[8],
        "age_group" : age_groups["s"],
        "compassion" : 4, 
        "memory" : 5,
        "quantity" : 200000,
        "commitment" : False
    },
    "s9" : {
        "opinion" : opinions[9],
        "age_group" : age_groups["s"],
        "compassion" : 5, 
        "memory" : 3,
        "quantity" : 300000,
        "commitment" : False
    },
    "s10" : {
        "opinion" : opinions[10],
        "age_group" : age_groups["s"],
        "compassion" : 2, 
        "memory" : 2,
        "quantity" : 100000,
        "commitment" : False
    },
    "d1" : {
        "opinion" : opinions[1],
        "age_group" : age_groups["d"],
        "compassion" : 10, 
        "memory" : 8,
        "quantity" : 300000,
        "commitment" : False
    },
    "d2" : {
        "opinion" : opinions[2],
        "age_group" : age_groups["d"],
        "compassion" : 8, 
        "memory" : 9,
        "quantity" : 500000,
        "commitment" : False
    },
    "d3" : {
        "opinion" : opinions[3],
        "age_group" : age_groups["d"],
        "compassion" : 10, 
        "memory" : 8,
        "quantity" : 300000,
        "commitment" : False
    },
    "d4" : {
        "opinion" : opinions[4],
        "age_group" : age_groups["d"],
        "compassion" : 7, 
        "memory" : 6,
        "quantity" : 300000,
        "commitment" : False
    },
    "d5" : {
        "opinion" : opinions[5],
        "age_group" : age_groups["d"],
        "compassion" : 7, 
        "memory" : 5,
        "quantity" : 400000,
        "commitment" : False
    },
    "d6" : {
        "opinion" : opinions[6],
        "age_group" : age_groups["d"],
        "compassion" : 8, 
        "memory" : 4,
        "quantity" : 200000,
        "commitment" : False
    },
    "d7" : {
        "opinion" : opinions[7],
        "age_group" : age_groups["d"],
        "compassion" : 4, 
        "memory" : 3,
        "quantity" : 200000,
        "commitment" : False
    },
    "d8" : {
        "opinion" : opinions[8],
        "age_group" : age_groups["d"],
        "compassion" : 4, 
        "memory" : 6,
        "quantity" : 100000,
        "commitment" : False
    },
    "d9" : {
        "opinion" : opinions[9],
        "age_group" : age_groups["d"],
        "compassion" : 4, 
        "memory" : 2,
        "quantity" : 300000,
        "commitment" : False
    },
    "d10" : {
        "opinion" : opinions[10],
        "age_group" : age_groups["d"],
        "compassion" : 1, 
        "memory" : 1,
        "quantity" : 400000,
        "commitment" : False
    },
}
parties = {
    "xxx" : {
        "opinion" : {}
    }
}

data = {
    "education" : 4,
    "healthcare" : 5,
    "pensions" : 3,
    "energy" : 4,
    "infrastructure" : 4,
    "defense" : 5,
    "agroculture" : 1,
    "industry" : 1,
    "startups" : 3,
    "housing" : 2,
    "environment" : 4,
    "culture" : 3,
    "alliance" : 5, 
    "small_alliance" : 3,
    "enemy" : 1,
    "migration" : 4,
    "minorities" : 5,
    "human_tax" : 4,
    "corporate_tax" : 4, 
    "freedom" : 5, 
    "religion" : 2,
    "corruption" : 5,
    "digitization" : 5,
    "debts" : 3,
    "referendum" : 4
}

parties_name_bank = {
    1 : "BLOK",
    2 : "ProBudoucnost",
    3 : "Strana lidu",
    4 : "Občanská dohoda",
    5 : "Strana sociálně aktivních",
    6 : "Náš svět!"
}