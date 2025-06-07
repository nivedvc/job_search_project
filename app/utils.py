import pandas as pd
import random

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

def get_headers(website):
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
        return headers
    elif website.lower() == 'linkedin':
        headers = LINKEDIN_HEADERS.copy()
        headers['user-agent'] = f'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36'
        headers['sec-ch-ua'] = f'"Chromium";v="{chrome_version}", "Not(A:Brand";v="24", "Google Chrome";v="{chrome_version}"'
        return headers
    else:
        raise ValueError(f"Headers for website '{website}' are not defined.")

def get_headers_url(website):
    """
    Returns a tuple of (headers dictionary, base URL) for the given website name.
    Supported: 'naukri', 'linkedin'
    """
    if website.lower() == 'naukri':
        return NAUKRI_HEADERS, "https://www.naukri.com/jobapi/v3/search"
    elif website.lower() == 'linkedin':
        return LINKEDIN_HEADERS, "https://www.linkedin.com/jobs/search"
    else:
        raise ValueError(f"Headers/URL for website '{website}' are not defined.")

PROXIES = [
    {
        'http': 'http://dsjwwsal:182nac4z6csf@198.23.239.134:6540',
        'https': 'http://dsjwwsal:182nac4z6csf@198.23.239.134:6540',
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
        return {
            'keywords': keyword,
            'location': 'India',
            'geoId': '102713980',
            'trk': 'public_jobs_jobs-search-bar_search-submit',
            'original_referer': 'https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs&position=1&pageNum=0',
        }
    else:
        raise ValueError(f"Params for website '{website}' are not defined.")