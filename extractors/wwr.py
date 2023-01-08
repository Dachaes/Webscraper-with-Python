from requests import get
from bs4 import BeautifulSoup


# weworkremotely
def extract_wwr_jobs(keyword):
    results = []
    url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}"
    response = get(url, headers={"User-Agent": "Dachae"})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("section", class_="jobs")
        for job_section in jobs:
            job_section = soup.find_all("li", class_="feature")
            for job in job_section:
                job = job.find_all("a")
                job = job[1]
                link = job["href"]
                link = f"https://weworkremotely.com{link}"
                position = job.find("span", class_="title")
                company, kind, location = job.find_all("span", class_="company")

                job_data = {
                    'position': position.string.replace(",", " "),
                    'company': company.string.replace(",", " "),
                    'location': location.string.replace(",", " "),
                    'link': link
                }
                results.append(job_data)

    else:
        print("Can't get jobs!")

    return results
