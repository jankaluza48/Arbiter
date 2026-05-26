import json
from lib import parties, voters

"""testovací soubor"""

with open('../txt/user_data/voters.txt', "w", encoding='utf-8') as file:
    json.dump(voters, file, ensure_ascii=False, indent=4)

print(voters)

