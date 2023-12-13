import requests as re
from bs4 import BeautifulSoup as bs
import json
# supporting librarys
from scraper.details_info import job_details
from scraper.basic_data import page1, page2
from scraper.result_details import result
from scraper.admit_details import admit


def get_main_link():
  url = 'https://govtjobguru.in/'

  html = re.get(url)
  soup = bs(html.content,'html.parser')

  data = soup.find_all(class_ = ['fl-button-wrap', 'fl-button-width-auto' ,'fl-button-center', 'fl-button-has-icon'])

  links = [[i.get('href') for i in i.find_all('a')] for i in data]
  
  return [i[0] for i in links]


def get_job():
  data,title = page1(get_main_link()[0])
  basic = {'page_title':title,'data':data} 
  # return both data for id sync
  return basic,job_details(basic)

# get full details for admits
def get_admit():
  data, title = page2(get_main_link()[1])
  
  id = data['col_id']
  links = data['col2']
  output =[]
  for itr,i in enumerate(links[1:]):
    filter = lambda x : x if '/jobs' not in x else False
    print(itr , '\t',filter(i),'\n')
    
    try:
      
      if filter(i):
        info = admit(i,id[itr+1])
        output.append(info)
    except:
      print('error')

  return output

# get full details for results
def get_result():
  data, title = page2(get_main_link()[2])
  id = data['col_id']
  links = data['col2']
  output =[]
  for itr,i in enumerate(links[1:]):
    filter = lambda x : x if '/jobs' not in x else False
    print(itr , '\t',filter(i),'\n')
    
    if filter(i):
      info = result(i,id[itr+1])
      output.append(info)
      
  return output

