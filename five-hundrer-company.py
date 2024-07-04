import requests
from bs4 import BeautifulSoup
import time
import random

def get_list_companies():
    url_500_wiki = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    
    response = requests.get(url=url_500_wiki)
    if response.status_code != 200:
        print ("Maybe URL wrong")
        return []
    
    soup = BeautifulSoup(response.text, features='html.parser')
    
    companies = []
    table_sp_500 = soup.find("table").find_all("tr")

    for tr in table_sp_500:
        try: 
            company = tr.find("td").text
            cut_point = company.find("\n")
            companies.append(company[:cut_point])
        except:
            continue
    return companies

def get_companies_information(companies):
    print("begin get information")
    list_company_info = {}
    
    # List of user agents to rotate
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
    ]
    
    for company in companies:
        company_info = {}
        url = f"https://finance.yahoo.com/quote/{company}/"
        print(f"Trying: {url}")
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, features='html.parser')
                lis = soup.find_all("li", class_="svelte-tx3nkj")
                
                for li in lis:
                    spans = li.find_all("span")
                    if len(spans) >= 2:
                        name, val = spans[0].text, spans[1].text
                        company_info[name] = val
                
                list_company_info[company] = company_info
            else:
                print(f"Failed to retrieve data for {company}")
                list_company_info[company] = {"error": f"HTTP {response.status_code}"}
        
        except requests.RequestException as e:
            print(f"Error retrieving data for {company}: {e}")
            list_company_info[company] = {"error": str(e)}
        
        # Random delay between requests
        time.sleep(random.uniform(1, 3))
    
    return list_company_info

def main():
    five_hundred_companies = get_list_companies()
    
    if five_hundred_companies.__len__() == 0:
        print("ERROR, check the get_list_companies function")
        
    list_info = get_companies_information(five_hundred_companies)
    print(list_info.items())
    
    
if __name__ == "__main__":
    main()