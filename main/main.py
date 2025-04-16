import threading, requests, json, os
from colorama import Fore, init

init(autoreset=True)

lck = threading.Lock()
f_n = 'available.json'

if os.path.exists(f_n):
    os.remove(f_n)

with open(f_n, 'w') as f:
    json.dump([], f)

def chk_nm(u):
    r = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{u}')
    data = r.json()
    return 'errorMessage' in data

def add_to_file(u):
    with lck:
        with open(f_n, 'r') as f:
            d = json.load(f)
        d.append({'username': u, 'link': f'https://namemc.com/search?q={u}'})
        with open(f_n, 'w') as f:
            json.dump(d, f, indent=2)

def rq():
    while True:
        try:
            w = requests.get('https://random-word-api.herokuapp.com/word').json()[0]
            if chk_nm(w):
                print(f'{Fore.GREEN}AVAILABLE >> {w}\n')
                add_to_file(w)
            else:
                print(f'{Fore.RED}TAKEN >> {w}\n')
        except Exception as e:
            print(f'{Fore.YELLOW}ERROR >> RATE LIMITED\n')

for _ in range(10):
    threading.Thread(target=rq).start()
