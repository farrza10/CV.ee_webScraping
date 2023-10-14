mport pandas as pd
import requests
from bs4 import BeautifulSoup
import re

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_cv_ee(base_url, total_pages, limit=20):
    
    titles = {"title": [], "link": [], "date": [], "location": []}

    for page in range(total_pages):
        
        """
        limit: allows for the number of items appearing as a result of search
        offset: number of pages available for the search in the same page
        """
        
        offset = page * limit
        url = f"{base_url}?limit={limit}&offset={offset}&fuzzy=true&suitableForRefugees=false&isHourlySalary=false&isRemoteWork=false&isQuickApply=false"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            test = soup.find_all('li', class_='jsx-1871295890 jsx-78775730 vacancies-list__item false')
            published_date = soup.find_all('span', class_='jsx-3024910437')
            country = soup.find_all('div', class_='jsx-3024910437 vacancy-item__column vacancy-item__locations')

            for item in test:
                title = item.text.strip().split()[0]
                relative_link = item.find('a')['href']
                absolute_link = base_url + relative_link
                titles["title"].append(title)
                titles["link"].append(absolute_link)
                titles["date"].append([i for i in published_date if re.search("Expires", i.text.strip())])

            # for t in range(len(dff)):
            #     print(dff["date"][i][5])
    
            for con in country:
                titles["location"].append(con.text.strip().split(",")[0])
        else:
            print(f"Failed to retrieve page {page}. Status code:", response.status_code)

    df = pd.DataFrame(titles)
    return df

if __name__ == "__main__":
    base_url = "https://www.cv.ee/en/search/a"
    total_pages = 5
    dff = scrape_cv_ee(base_url, total_pages)

dff
