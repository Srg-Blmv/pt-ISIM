import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

cookies = ""

def auth():
    global cookies
    url = f"https://{isim_ip}/httpapi/login"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "login": isim_login,
        "password": isim_pass,
        "domain":""
    }
    
    response_auth = requests.post(url, json=payload, headers=headers, verify=False)
    if response_auth.status_code == 200:
        print("auth ok")
        cookies = response_auth.cookies
    else:
        print("auth fail")
        exit()


def delete_tech_sig(id):
    url_del_tech_id = f"https://{isim_ip}/api/techsignal/{id}"
    headers = {"Content-Type": "application/json, text/plain, */*"}
    response = requests.delete(url_del_tech_id, headers=headers, verify=False, cookies=cookies) 
    return response.status_code
    
def get_tech_table(): 
    auth()
    url_tech_tables  = f"https://{isim_ip}/api/techsignal/table"
    payload = {"page":{"limit":1000,"offset":0,"sortFields":[{"field":"createTime","direction":1}]},"filters":{}}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url_tech_tables, json=payload, headers=headers, verify=False, cookies=cookies)   
    
    data = response.json()

    for item in data["data"]:
        if delete:
            status_code = delete_tech_sig(item.get('id',''))
            if status_code == 200:
                print(f"DELETE: {item.get('id','')}:  {item.get('name','')}")
            else:
                print(f"Error: {status_code}   {item.get('id','')}:  {item.get('name','')}")
      
        else:
            print(f"{item.get('id','')}:  {item.get('name','')} {item.get('ownersMacs','')}")


isim_ip = "192.168.212.4"
isim_login =  "Administrator"
isim_pass = "P@ssw0rd"
delete = 1


get_tech_table()
