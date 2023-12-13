import requests as re
from bs4 import BeautifulSoup as bs
# extact the first json data
def link_extract(file):
  
  data = file
  details = data['data']

  links =[]
  id = []
  for i in details:
    for itr,j in enumerate(i['col6']):
      links.append(j)
      id.append(i['col_id'][itr])
  only = lambda x: x if 'govtjobguru.in' in x else None
  output =[]
  for itr,i in enumerate(links):
    if only(i) :
      output.append([only(i),id[itr]])
  return output

def info_extract(url,id=None):
  html = re.get(url)
  soup = bs(html.content,'html.parser')
  main_data = {}
  # first (overview 1v1 format),div class = fl-col fl-node-5b90b581a83a2
  first = soup.find(class_ = "fl-col fl-node-5b90b581a83a2")
  collector1 = []
  table_rows = first.find('table').find_all('tr')
  for i in table_rows:
    data = {}
    data['heading'] = i.find_all('td')[0].text.replace('  ','').replace('\n','')
    data['info'] = i.find_all('td')[1].text.replace('  ','').replace('\n','')
    collector1.append(data)

  #secound (basic info 1v1 format)
  second= soup.find(class_ = "fl-col fl-node-5b90b12d58f8b")
  collector2 =[]
  table_rows = second.find('table').find_all('tr')[:-1]
  for i in table_rows:
    data = {}
    data['heading'] = i.find_all('td')[0].text.replace('  ','').replace('\n','')
    data['info'] = i.find_all('td')[1].text.replace('  ','').replace('\n','')
    collector2.append(data)

  # third discription (paragraph collecting whole p tag) 
  third = soup.find(class_ = "fl-col fl-node-5d1cda614829d")
  collector3 = str(third.find('p'))

  #forth contain paragraph and table like 1v1 for dates
  forth = soup.find(class_ = "fl-col fl-node-5b900d4b94ee5")
  try:
    paragraph = forth.find(class_ = "fl-html").find('p').text.replace('  ','').replace('\n','')
  except:
    paragraph = ''
  table_rows = forth.find(class_ = 'fl-html').find('table').find_all('tr')
  
  collector4 = []
  for i in table_rows:
    data = {}
    data['heading'] = i.find_all('td')[0].text.replace('  ','').replace('\n','')
    data['info'] = i.find_all('td')[1].text.replace('  ','').replace('\n','')
    collector4.append(data)
  collector4 = [paragraph,collector4]

  # fifth (payment) contain paragraph and table data in a 1v1 format 
  fifth = soup.find(class_ = "fl-col fl-node-5b900e1e0e9a2 fl-col-small")
  try:
    paragraph = fifth.find(class_ = "fl-html").find('p').text.replace('  ','').replace('\n','')
  except:
    paragraph = ''
  table_rows = fifth.find(class_ = 'fl-html').find('table').find_all('tr')
  
  collector5 = []
  for i in table_rows:
    data = {}
    data['heading'] = i.find_all('td')[0].text.replace('  ','').replace('\n','')
    data['info'] = i.find_all('td')[1].text.replace('  ','').replace('\n','')
    collector5.append(data)
  collector5 = [paragraph,collector5]
  

  
  # sixth more requirments for eligibility 4 columns format with paragraph
  sixth = soup.find(class_ = "fl-col fl-node-5b900eba7937f")
  paragraph = sixth.find(class_ = "fl-html").find('p').text.replace('  ','').replace('\n','')
  table = sixth.find('table')
  collector6 = []
  data = {}
  data['heading']= [i.text for i in table.find('thead').find_all('td')]
  data['info'] = [[j.text for j in i.find_all('td')] for i in table.find('tbody').find_all('tr')]
  collector6.append(data)

  collector6 = [paragraph,collector6]
  
  # seventh is contain the all important links in a 1v1 format
  seventh = soup.find(class_ = "fl-col fl-node-5b90a08d6ef23")
  paragraph = seventh.find(class_ = "fl-html").find('p').text.replace('  ','').replace('\n','')
  table = seventh.find('table').find_all('tr')
  collector7 = []
  for i in table[:-1]:
    data ={}
    data['heading'] = i.find_all('td')[0].text.replace('  ','')
    try:
      info = i.find_all('td')[1].find('a').get('href')
    except:
      info = i.find_all('td')[1].text.replace('  ','')
    data['info']= info
    collector7.append(data)
  collector7 =[paragraph,collector7]
  ''' extract the pages div wise '''

  output = {}
  
  output['overview'] =collector1
  output['basic'] =collector2
  output['discription'] =collector3
  output['dates'] =collector4
  output['payment'] =collector5
  output['eligibility'] =collector6
  output['links'] =collector7
  return {'id':id,'data':output}


def job_details(file):
  try:
    link = link_extract(file)
    info = []
    for itr,i in enumerate(link):
      
      # time.sleep(5)
      print('fetching data')
      try: 
        if '.' not in i[0].split('/')[-1]:
          print(itr,'\n','link :',i[0],'\n', 'id :',i[1],'\n')
          info.append(info_extract(i[0],i[1]))
          print('done \n')
        else:
          print(f'{itr} :its not an webpage ! --> {i[0]}\n')
      except:
        print('err')
    print('sending data .........')
    return info 
  except:
    return
  