from os import link
import requests, time
import xml.etree.ElementTree as ET
# import datetime, calendar
# from dateutil.tz import gettz
# from requests.models import DecodeError    
# import json 
        

def scrap_pages(URL):
    
    scrap_res = []
        
    data = requests.get(URL)

    root = ET.fromstring(data.content)

    pods = root.findall('pod')

    scrap_res = {}
    microsource = []

    for pod in pods:
        subpods = pod.findall('subpod')

        for subpod in subpods:

            microsources = subpod.findall('plaintext')
            for final_text in microsources:
                microsource.append(final_text.text)
            
    scrap_res['food_item'] = microsource[0].split(' | ')[0]
    scrap_res['amount'] = microsource[0].split(' | ')[2]
    scrap_res['total_calorie'] = microsource[1].split('\n')[1].split(' | ')[0].split(' ')[2]
    scrap_res['fat_calories'] = microsource[1].split('\n')[1].split(' | ')[1].split(' ')[2]
    safe_res = '\n\n'.join([i for i in microsource])

    return scrap_res



        
if __name__ == '__main__':

    url = 'http://api.wolframalpha.com/v2/query?input=french%20fries%20nutrition%20facts&appid=VW4AAW-43H9PK84A4'
    scrap_res = scrap_pages(url)
    
    print('Completed insight creation for :', url, '\n', scrap_res)
    # print(database, scrap_res)