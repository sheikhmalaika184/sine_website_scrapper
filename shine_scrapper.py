import requests 
from bs4 import BeautifulSoup
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
#can change these
keyword = 'wind'
location = 'india'
DRIVER_PATH = '/Users/malaikasheikh/python/chromedriver'
#do not change these
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

def make_request(url):
    driver.get(url)
    driver.implicitly_wait(5) # seconds
    soup = soup = BeautifulSoup(driver.page_source, 'lxml')
    return soup


def extract_links_form_all_pages():
    no_of_page = 1
    links = []
    while True:
        url = f'https://www.shine.com/job-search/{keyword}-jobs-jobs-{no_of_page}?q={keyword}%20jobs&loc={location}'
        soup = make_request(url)
        div_tag = soup.find('div' , class_='ParentClass')
        if(div_tag != None):
            a_tags = div_tag.find_all('div',itemprop="itemListElement")
            for a_tag in a_tags:
                meta_tag = a_tag.find('meta')
                link = meta_tag['content']
                links.append(link)
                
        else:
            break
        no_of_page = no_of_page+1
    print(len(links))    
    return links


def extract_information(jobs_urls):
    csvFile = open('shine.csv', 'w')
    try:
        writer = csv.writer(csvFile)
        #columns names
        writer.writerow(('Sr','Job Title', 'Company Name','Experience','Salary','Location','Education','Department','Industry IT','Key Skills','Job Url'))
        
        i = 1
        for job_url in jobs_urls:
            sr_no = str(i)
            url = job_url
            job_title = "Not Available"
            company_name = "Not Available"
            experience = "Not Available"
            location = "Not Available"
            salary = "Not Available"
            key_skills = "Not Available"
            department = "Not Available"
            industry = "Not Available"
            education = "Not Available"
        #job_url = 'https://www.shine.com/jobs/general-manager-operationsplant-head/nutan-enterprises/9974799'
            soup = make_request(job_url)
            div_tag = soup.find('div',class_='JobDetailWidget_jobDetail_blue__JDzC6 JobDetailWidget_jobCard__ZheXJ cls_jobCard white-box-border')
            job_title_tag = div_tag.find('h2',class_='font-size-24')
            company_name_tag = div_tag.find('div',class_='JobDetailWidget_jobCard_cName__qvsdW')
            experience_tag= div_tag.find('div',class_='JobDetailWidget_jobCard_location_item__sorvQ undefined')
            location_tag =  div_tag.find('div',class_='JobDetailWidget_jobCard_location_item__sorvQ')
            salary_tag = div_tag.find('span',class_='JobDetailWidget_jobCard_location_item__sorvQ')

            #other details
            other_details = soup.find('div',class_='jobDetail_OtherDetails__uwJHU')
            #key skills
            key_skills_tag = soup.find('ul',class_='keyskills_keySkills_items__ej9_3')


            if(job_title_tag!=None):
                job_title = job_title_tag.text.strip()
            if(company_name_tag!=None):
                company_name = company_name_tag.text.strip()
            if(experience_tag!=None):
                experience = experience_tag.text.strip()
            if(location_tag!=None):
                locations=location_tag.text.split('+')
                location = locations[0].strip()
            if(salary_tag != None):
                salary = salary_tag.text.strip()
            #other details
            if(other_details!=None):
                li_tags = other_details.find_all('li')
                for li_tag in li_tags:
                    if(li_tag.find('span').text.strip() == 'Department'):
                        department = li_tag.find('a').text
                    if(li_tag.find('span').text.strip() == 'Industry IT'):
                        industry = li_tag.find('a').text
                    if(li_tag.find('span').text.strip() == 'Education'):
                        education = li_tag.find('a').text
            #key skills
            if(key_skills_tag!=None):
                skills = key_skills_tag.find_all('li')
                key_skills = ""
                for skill in skills:
                    key_skills = key_skills+skill.text+","
                key_skills = key_skills[:-1]

            #print output
            print("Sr No: "+sr_no)
            print("Job Url: " + url)    
            print("Job Title: "+ job_title)
            print("Compnay Name: "+company_name)
            print("Experience: "+experience)
            print("Location: "+location)
            print("Salary: "+salary)
            print("Department: "+department)
            print("Industry IT: "+industry)
            print("Education: "+education)
            print("Skills: "+key_skills)
            print(" ")
            writer.writerow((sr_no,job_title,company_name,experience,salary,location,education,department,industry,key_skills,url))
            i=i+1
            
    except Exception as e:
        print(e)
        
    finally:
        csvFile.close()
        
        
def main():
    jobs_urls = extract_links_form_all_pages()
    extract_information(jobs_urls)
    driver.close()
    
    
if __name__ == '__main__':
    main()