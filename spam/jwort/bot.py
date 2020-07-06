#im literally gonna copy and paste this into every python project i do
def save_import(module, **kwargs):

    attribute = kwargs.get("attribute", None)
    name = kwargs.get("name", None)


    if not attribute:
        print("[*] Loading " + module + " library",end="")
    else:
        print("[*] Loading " + attribute + " from " + module + " library",end="")
    
    if name:
        print(" as " + name, end="")
    print("... ", end="")

    try:
        
        if not attribute:
            import_string = "import " + module
        else:
            import_string = "from " + module + " import " + attribute
        if name:
            import_string += " as " + name
        
        exec(import_string, globals())
        print("Done")
    except ModuleNotFoundError:
        print("Failed")
        print("[!] " + module + " library not found.")
        print("[*] Installing " + module + " library...\n")
        version = sys_version[:sys_version.find(".", sys_version.find(".") + 1)]
        system("py -" + version + " -m pip install " + module)
        print("")
        try:
            exec(import_string, globals())
        except ModuleNotFoundError:
            print("[!] Could not load " + module + " library. Try to install it manually.")
            exit()





import string

from sys import version as sys_version
from os import system
from time import sleep
from random import randint

###replace these with save_imports (might add more in the future). These are here so vs code works.

#import requests

save_import("requests")

default_word = "Schabernack"

def get_word():
    print("[*] Enter word to submit (or press enter to use \"Hurensohn\"):")

    word = input("[*] word >> ")
    if word == "":
        return default_word

    for c in word:
        if c not in string.ascii_letters and c not in string.digits:
            print("[!] The word you entered contains characters that aren't letters or numbers.")
            print("[!] Do you want to change it (y/n)?")
            while True:
                response = input("[!] (y/n) >> ")

                if response.lower() == "y":
                    word = get_word()
                    break
                elif response.lower() == "n":
                    break
                else:
                    print("[!] Not a valid answer.")
            break
    return word

print("")

word = get_word()


print("[*] Commencing spam...\n\n")

while True:
    #create session
    session = requests.Session()
    
    print("[*] Faking survey visit...")

    #extract survey_data
    try:
        page = session.get("https://www.surveymonkey.com/r/7JZRVLJ?embedded=1")
    except requests.RequestException:
        print("[!] Can't connect to host. Do you have an existing internet connection?")
        exit()

    print("[*] Extracting \"survey_data\" parameter...")
    survey_data_offset = page.text.find("survey_data\" value=\"") + 20

    if survey_data_offset == 19:
        print("[!] Failed to extract survey data. Please report this bug.")
        print("[!] Writing http response to debug file...")
        with open("debug_log.txt","w") as f:
            f.write(page.request.method+"\n")
            f.write('request headers:\n\n\n')
            f.write(str(page.request.headers) + "\n\n\n\n")

            f.write(str(page.status_code)+"\n")
            f.write('response headers:\n\n\n')
            f.write(str(page.headers) + "\n\n")
            f.write('\n\nresponse content:\n\n\n')
            f.write(str(page.content.decode()))
        exit()

    #python probably has a built in thing but i dont give a shit
    survey_data = ""
    #shit code
    for i in range(survey_data_offset,len(page.text)):
        if page.text[i] == "\"":
            break
        survey_data += page.text[i]

    print("[*] Debug info: Status code: " + str(page.status_code) + ", \"survey_data\" parameter length: " + str(len(survey_data)))

    wait = randint(0,5000) / 1000
    print("[*] Waiting " + str(wait) + "s...")
    sleep(wait)
    
    post_data = {

        "463803414": (None, "3067519628"),
        "463803684": (None, word),
        "483089934[]": (None,"3189794655"),
        "survey_data": (None,survey_data),
        'response_quality_data': (None,'{"question_info":{"qid_463803414":{"number":1,"type":"dropdown","option_count":5,"has_other":false,"other_selected":null,"relative_position":[[2,0]],"dimensions":[5,1],"input_method":null,"is_hybrid":false},"qid_463803684":{"number":2,"type":"open_ended","option_count":null,"has_other":false,"other_selected":null,"relative_position":null,"dimensions":null,"input_method":"text_typed","is_hybrid":true},"qid_483089934":{"number":3,"type":"multiple_choice_vertical","option_count":1,"has_other":false,"other_selected":null,"relative_position":[[0,0]],"dimensions":[1,1],"input_method":null,"is_hybrid":false}},"start_time":1593393913312,"end_time":1593393973805,"time_spent":60493,"previous_clicked":false,"has_backtracked":false,"bi_voice":{}}')

    }
    #sneak 100 (shouldve used webdriver dammit)
    headers_2 = {

        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        #Chrome User agent but no chrome for boundaries (shhhhh dont tell em) 'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryxwtjXVOdBvKFA4h4'
        'origin': 'https://www.surveymonkey.com',
        'referer': 'https://www.surveymonkey.com/r/7JZRVLJ?embedded=1',
        'sec-fetch-dest': 'iframe',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36 Edg/83.0.478.54'

    }

    print("[*] Submitting survey with word \""+ word + "\"...")
    try:
        response = session.post("https://www.surveymonkey.com/r/7JZRVLJ?embedded=1", headers=headers_2, files=post_data)
    except requests.RequestException:
        print("[!] Can't connect to host. Do you have an existing internet connection?")
        exit()

    
    print("[*] Debug info: Status code: " + str(response.status_code))

    if response.status_code != 200:
        print("[!] Failed to submit survey. Please report this bug.")
        print("[!] Writing http response to debug file...")
        with open("debug_log.txt","w") as f:
            f.write(response.request.method+"\n")
            f.write('request headers:\n\n\n')
            f.write(str(response.request.headers)+"\n\n")
            f.write('\n\nrequest content:\n\n\n')
            f.write(str(response.request.body.decode())+"\n\n\n\n")

            f.write(str(response.status_code)+"\n")
            f.write('response headers:\n\n\n')
            f.write(str(response.headers)+"\n\n")
            f.write('\n\nresponse content:\n\n\n')
            f.write(str(response.content.decode()))
        exit()
    print("")
