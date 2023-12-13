import requests as re
from bs4 import BeautifulSoup as bs
import uuid


''' scrape page 1 '''

def page1(url):
  html_data = re.get(url)  
  html = bs(html_data.content,'html.parser')
  main_container= html.find(class_='entry-content')
  table = main_container.find_all('table')
  
  '''  extracting the titles  ''' 
  heading = [str(i.text).replace('  ','').replace('\n','') for i in main_container.find_all('h2')]
  
  ''' extracting the table data ''' 
  collection = []
  
  for itr,i in enumerate(table):
    data ={}
    data['id']=itr
    data['title'] = heading[itr]
    col1 = [i.text.replace('  ','').replace('\n','') for i in i.find_all(class_ = 'column-1')[1:]]
    data['col_id'] = [str(uuid.uuid4()) for i in col1]
    data['col1'] =col1
    data['col2'] = [i.text.replace('  ','').replace('\n','') for i in i.find_all(class_ = 'column-2')[1:]]
    data['col3'] = [i.text.replace('  ','').replace('\n','') for i in i.find_all(class_ = 'column-3')[1:]]
    data['col4'] = [i.text.replace('  ','').replace('\n','') for i in i.find_all(class_ = 'column-4')[1:]]
    data['col5'] = [i.text.replace('  ','').replace('\n','') for i in i.find_all(class_ = 'column-5')[1:]]
    ''' col6 only contain links '''
    data['col6'] = [data.find('a').get('href') for data in i.find_all(class_ = 'column-6')[1:]]
    # data['col6'].insert(0,'None')
    collection.append(data)
  
  return collection, html.find('title').text


''' PGAE2 FUNCTION IS USED FOR EXTRACT DATA FOR ADMIT AND RESULTS '''

'page2 scrape'

def page2(url):
  file = re.get(url)
  html = bs(file.content,'html.parser')
  main_div = html.find(class_ = 'entry-content')
  ''' table_find is use to prevent the table to return none '''
  
  table_find = lambda x : main_div.find(id='tablepress-321') if x is None else x
  
  table = table_find(main_div.find(id = 'tablepress-320'))
  
  title = main_div.find('p').text.replace('  ','').replace('\n','')
  
  col1 = table.find_all(class_ = 'column-1')
  col1_name =  [i.text.replace('  ','').replace('\n','') for i in col1]
  col1_link = [i.find('a').get('href') for i in col1[1:]]
  col1_link.insert(0,'None')
  print(title) 

  data = {}
  data['id'] = 0
  data['title'] = title
  data['col_id'] = [str(uuid.uuid4()) for i in col1_name]
  
  data['col1'] = col1_name
  data['col2'] = col1_link
  return data, html.find('title').text
