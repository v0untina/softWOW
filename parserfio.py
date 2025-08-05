from bs4 import BeautifulSoup
import requests
def getfio():
    url = "https://generatefakename.com/ru/name/random/uk/ua"
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    allname = soup.select_one(".panel-body h3")
    array = [allname.text.split()]
    fio=list(array[0][0])
    name = list(array[0][1])
    return name,fio

