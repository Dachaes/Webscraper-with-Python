from requests import get
from bs4 import BeautifulSoup


# remoteok
def extract_remoteok_jobs(keyword):
    url = f"https://remoteok.com/remote-{keyword}-jobs"
    response = get(url, headers={"User-Agent": "Dachae"})
    results = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("tr", class_="job")

        for job in jobs:
            company = job.find("h3", itemprop="name")
            company = company.string.strip()
            position = job.find("h2", itemprop="title")
            position = position.string.strip()
            location = job.find("div", class_="location")
            location = location.string.strip()
            anchor = job.find("a", itemprop="url")
            link = anchor["href"]
            link = f"https://remoteok.com{link}"

            job_data = {
                'position': position.replace(",", " "),
                'company': company.replace(",", " "),
                'location': location.replace(",", " "),
                'link': link
            }
            results.append(job_data)

    else:
        print("Can't get jobs!")

    return results
