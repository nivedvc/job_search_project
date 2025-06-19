import pandas as pd
import random
import sqlite3
import re
from datetime import datetime, timedelta


def export_to_csv(jobs, filename="jobs.csv"):
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)

NAUKRI_HEADERS = {
    'authority': 'www.naukri.com',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'appid': '109',
    'cache-control': 'no-cache',
    'clientid': 'd3skt0p',
    'content-type': 'application/json',
    'gid': 'LOCATION,INDUSTRY,EDUCATION,FAREA_ROLE',
    'nkparam': 'XCpN/RFeuRFgmHVpqDYNQxLCgoLmadnB2LdAbGI7KcS1bIxGglhig5R/bApXZZSGzINZuP6p0zNMedNaMnFxlA==',
    'pragma': 'no-cache',
    'referer': 'https://www.naukri.com/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'systemid': 'Naukri',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

LINKEDIN_HEADERS = {
    'authority': 'www.linkedin.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://www.linkedin.com/jobs/search',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

INFOPARK_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://infopark.in/companies/job-search',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

def get_headers_url(website):
    """
    Returns the headers dictionary for the given website name.
    Randomizes Chrome version in user-agent and sec-ch-ua between 110 and 136.
    Supported: 'naukri', 'linkedin'
    """
    chrome_version = str(random.randint(110, 136))
    if website.lower() == 'naukri':
        headers = NAUKRI_HEADERS.copy()
        headers['user-agent'] = f'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36'
        headers['sec-ch-ua'] = f'"Chromium";v="{chrome_version}", "Not(A:Brand";v="24", "Google Chrome";v="{chrome_version}"'
        return headers, "https://www.naukri.com/jobapi/v3/search"
    elif website.lower() == 'linkedin':
        headers = LINKEDIN_HEADERS.copy()
        headers['user-agent'] = f'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36'
        headers['sec-ch-ua'] = f'"Chromium";v="{chrome_version}", "Not(A:Brand";v="24", "Google Chrome";v="{chrome_version}"'
        return headers, "https://www.linkedin.com/jobs/search"
    elif website.lower() == 'infopark':
        headers = INFOPARK_HEADERS.copy()
        headers['user-agent'] = f'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36'
        headers['sec-ch-ua'] = f'"Not A(Brand";v="8", "Chromium";v="{chrome_version}", "Google Chrome";v="{chrome_version}"'
        return headers, 'https://infopark.in/companies/job-search'
    else:
        raise ValueError(f"Headers/URL for website '{website}' are not defined.")

PROXIES = [
    {
        'http': 'http://dsjwwsal:182nac4z6csf@198.23.239.134:6540',
        'https': 'http://dsjwwsal:182nac4z6csf@198.23.239.134:6540',
    },
    {
        'http': 'http://dsjwwsal:182nac4z6csf@107.172.163.27:6543',
        'https': 'http://dsjwwsal:182nac4z6csf@107.172.163.27:6543',
    },
    {
        'http': 'http://dsjwwsal:182nac4z6csf@23.94.138.75:6349',
        'https': 'http://dsjwwsal:182nac4z6csf@23.94.138.75:6349',
    },
    {
        'http': 'http://dsjwwsal:182nac4z6csf@216.10.27.159:6837',
        'https': 'http://dsjwwsal:182nac4z6csf@216.10.27.159:6837',
    },
]

def get_proxy():
    """
    Returns a random proxy from the list of available proxies.
    """
    if not PROXIES:
        return None
    return random.choice(PROXIES)

def get_params(website, keyword=None):
    """
    Returns the params dictionary for the given website name.
    Supported: 'naukri', 'linkedin'
    """
    if website.lower() == 'naukri':
        if not keyword:
            raise ValueError("Keyword is required for Naukri params.")
        return {
            'noOfResults': '20',
            'urlType': 'search_by_keyword',
            'searchType': 'adv',
            'keyword': keyword,
            'pageNo': '1',
            'k': keyword,
            'seoKey': 'jobs',
            'src': 'jobsearchDesk',
            'latLong': '',
        }
    elif website.lower() == 'linkedin':
        if not keyword:
            raise ValueError("Keyword is required for Infopark params.")
        return {
            'keywords': keyword,
            'location': 'India',
            'geoId': '102713980',
            'trk': 'public_jobs_jobs-search-bar_search-submit',
            'original_referer': 'https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs&position=1&pageNum=0',
        }
    elif website.lower() == 'infopark':
        if not keyword:
            raise ValueError("Keyword is required for Infopark params.")
        return {
            'search': keyword,
        }
    else:
        raise ValueError(f"Params for website '{website}' are not defined.")
    

def create_table():
    conn = sqlite3.connect('jobs.db')  # Creates the .db file
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        description TEXT,
        posted_on TEXT,
        experience TEXT,
        salary TEXT,
        source TEXT,
        url TEXT,
        input_keyword TEXT
    )
    ''')
    conn.commit()
    conn.close()


def insert_jobs(job_list, input_keyword):
    create_table()
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    for job in job_list:
        posted_date = convert_posted_text(job['posted_on'])
        cursor.execute('''
            INSERT INTO jobs (title, company, location, description, posted_on, experience, salary, source, url, input_keyword)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            job['title'], job['company'], job['location'],
            job['description'], posted_date,
            job['experience'], job['salary'], job['site'], job['url'],
            input_keyword
        ))
    conn.commit()
    conn.close()
    print(f"Inserted {len(job_list)} jobs into the database with keyword {input_keyword}")


def convert_posted_text(posted_text):
    """
    Converts relative posted text like '1 week ago', '2 days ago', '3 hours ago', etc.
    into an actual date string in the format DD-MM-YYYY.
    If the text is not recognized, returns today's date.
    """
    posted_text = posted_text.lower().strip()
    now = datetime.now()

    patterns = [
        (r'(\d+)\s*week', 7),
        (r'(\d+)\s*day', 1),
        (r'(\d+)\s*hour', 0),
        (r'(\d+)\s*minute', 0),
        (r'(\d+)\s*month', 30),
    ]

    for pattern, days_per_unit in patterns:
        match = re.search(pattern, posted_text)
        if match:
            value = int(match.group(1))
            if 'hour' in pattern or 'minute' in pattern:
                date = now  # Less than a day ago, so today
            else:
                date = now - timedelta(days=value * days_per_unit)
            return date.strftime("%d-%m-%Y")

    # Handle 'today' or 'just now'
    if 'today' in posted_text or 'just now' in posted_text:
        return now.strftime("%d-%m-%Y")

    # Handle 'yesterday'
    if 'yesterday' in posted_text:
        date = now - timedelta(days=1)
        return date.strftime("%d-%m-%Y")

    # If not matched, return today's date
    return now.strftime("%d-%m-%Y")
