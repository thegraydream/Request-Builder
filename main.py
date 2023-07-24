import time
import os

try:import pyperclip
except:
    os.system('pip install pyperclip')
    import pyperclip


method_list = ["get", "post", "patch", "head", "put", "delete", "trace", "options", "connect"]

class color:
    red = "\033[0;31m"
    green = "\033[0;32m"
    cyan = "\033[0;36m"
    reset = "\033[0m"

def clear():os.system('cls')

def verify_method(rq_method):
    global method_list

    if rq_method in method_list:return True
    return False


def choice(text):
    while True:
        try:
            response = input(f"{text} (y/n) > ").lower()
            if response == "y":return True
            elif response == "n": return False
            else:print('Please answer with "y" or "n"!')
        except:print('Please answer with "y" or "n"!')

def choice_list(lists):
    while True:
        try:
            print('')
            c = -1
            for data in lists:
                c += 1
                print(f'{color.reset}[{color.cyan}{c}{color.reset}] {data}')

            response = int(input(f'{color.green}Please enter the number corresponding to your choice{color.reset} > '))

            if response < 0 or response > c:
                print(f'{color.red}Please enter a number between 0 and {c}!{color.reset}')
            else:
                c = -1
                for data in lists:
                    c += 1
                    if response == c:return data

        except:print(f'{color.red}Your choice must be a number!{color.reset}')


        

def transform_to_json(data):
    try:
        lines = data.split("\n")
        lines = [line for line in lines if line.strip() != '']

        result = {}

        for i in range(0, len(lines), 2):
            key = lines[i].strip().replace(':', '')
            value = lines[i+1].strip()

            result[key] = value

        return result
    except:return

def data_converter(types: str):
    paste = pyperclip.paste()

    print(f'Please make a "ctrl + c" of "{types}".')
    while True:
        if paste != pyperclip.paste():
            paste = pyperclip.paste()
            break
    
    while True:
        try:
            if transform_to_json(paste):
                if choice(f"\n{color.cyan}{pyperclip.paste()}\n{color.green}We've copied your copy, is this it?{color.reset}") == True:
                    data = transform_to_json(pyperclip.paste())
                    if data:
                        return data
                    else:print(f'{color.red}An error occurred while converting {types.lower()} to json, please try again.{color.reset}')
                else:print(f'Please copy the "{types}".')
            else:
                print(f'{color.red}The copy seems to be incomplete, please try again. Please copy the "{types}".{color.reset}')

            while True:
                if paste != pyperclip.paste():
                    paste = pyperclip.paste()
                    break
        except:print(f'{color.red}An error has occurred while obtaining {types} data.{color.reset}')

def main():
    # General
    while True:
        try:
            General = data_converter('General')

            Request_URL = General['Request URL']
            Request_Method = str(General['Request Method']).lower()

            break
        except:
            print(f'{color.red}An error occurred while obtaining the request url or request method.{color.reset}')
            if choice(f'{color.green}Do you want to enter them manually?{color.reset}') == True:
                while True:
                    Request_URL = input('Enter the request url > ')
                    if "http" in Request_URL:break
                    print(f'{color.red}Please enter a correct url!{color.reset}')


                Request_Method = choice_list(method_list)
                break

    # Request Headers
    clear()
    if choice(f'{color.green}are there any headers in your requests?{color.reset}') == True:
        Request_Headers = data_converter('Request Headers')
    else:Request_Headers = None


    # Payload
    clear()
    if choice(f'{color.green}are there any payloads in your requests?{color.reset}') == True:
        paste = pyperclip.paste()

        print(f'Please make a "ctrl + c" of "payload" in view source.')
        while True:
            if paste != pyperclip.paste():
                paste = pyperclip.paste()
                break

        while True:
            try:
                if choice(f"\n{color.cyan}{pyperclip.paste()}\n{color.green}We've copied your copy, is this it?{color.reset}") == True:
                    Request_Payload = pyperclip.paste()
                    break
                while True:
                    if paste != pyperclip.paste():
                        paste = pyperclip.paste()
                        break
            except:print(f'{color.red}An error has occurred while obtaining payload data.{color.reset}')
    else:Request_Payload = None

    clear()

    try:
        request = f"""import requests

{f"payload = '''{Request_Payload}'''" if not Request_Payload == None else ""}

{f'headers = {Request_Headers}' if not Request_Headers == None else ""}

response = requests.{Request_Method}('{Request_URL}'{f',headers=headers' if not Request_Headers == None else ""}{f',json=payload' if not Request_Payload == None else ""})
print(response.text)
print(response.status_code)"""

        output_folder = int(time.time())
        os.makedirs(f'export/{output_folder}')
        open(f'export/{output_folder}/main.py', 'w').write(request)
        print(f'{color.green}Your file has been created! Path: "{f"export/{output_folder}/main.py"}".{color.reset}')
        if choice(f'{color.green}Would you like to rebuild a request?{color.reset}') == True:main()
        else:exit()
    except:
        print(f'{color.red}An error has occurred while creating your file.{color.reset}')

print(f"{color.cyan}Request builder by TheGrayDream\nDiscord support: https://dsc.gg/thegraydreamgithub\n\nThe texts used are those used in Chrome's Network mode.\n{color.reset}")
main()