from scraper.govt_job_scraper import get_job, get_admit,get_result
import json

def saving():
    with open('scraper/details/jobs_details.json','w') as f:
        json.dump({'data':get_job()}, f , indent=4)

    with open('scraper/details/admit_details.json','w') as f:
        json.dump({'data':get_admit()}, f , indent=4)
    
    with open('scraper/details/result_details.json','w') as f:
        json.dump({'data':get_result()}, f , indent=4)
# saving()
def details_jobs():
    data = get_job(True)
    with open('scraper/details/detiled_info.json','w') as f:
       json.dump({'data':data},f, indent=4) 
    