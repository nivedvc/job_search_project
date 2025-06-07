import requests
import random
import string
from .utils import get_proxy, get_headers_url, get_params
import re
from lxml.html import fromstring

def get_search_results(keyword, websites):
    if not keyword:
        return
    data = []
    data_summary = {}
    for site in websites:
        headers, url = get_headers_url(site)
        params = get_params(site, keyword)
        proxy = get_proxy()
        cookies = None
        if site == 'linkedin':
            # Generate a random string for 'bcookie'
            bcookie_value = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            cookies = {'bcookie': bcookie_value}
        response = requests.get(
            url,
            params=params,
            headers=headers,
            proxies=proxy,
            cookies=cookies
        )
        job_data = get_results(response, site)
        data_summary[site] = len(job_data)
        print(f'Request sent to {site} | status code: {response.status_code} | jobs found: {len(job_data)}')
        if job_data:
            data.extend(job_data)
    return data, data_summary
    

def get_exp_sal_loc(details):
    req_data = {
        'experience': None,
        'salary': None,
        'location': None
    }
    for item in details:
        name = item.get('type')
        if name in req_data:
            req_data[name] = item.get('label')
    return req_data

def remove_html_tags(text):
    if text:
        clean = re.sub(r'<[^>]+>', '', text)
        return clean
    return text

def get_results(response, site):
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} from {site}.")
        return []
    if site.lower() == 'naukri':
        return parse_naukri(response)
    elif site.lower() == 'linkedin':
        return parse_linkedin(response)

def parse_naukri(response):
    try:
        data = response.json()
    except Exception as error:
        print(f"Got non-JSON response! | {response.status_code} | length: {len(response.text)}")
        return []
    jobs = data.get('jobDetails', [])
    job_data = []
    for job in jobs:
        title = job.get('title')
        desc = remove_html_tags(job.get('jobDescription'))
        posted_on = job.get('footerPlaceholderLabel')
        company = job.get('companyName')
        det = get_exp_sal_loc(job.get('placeholders', []))
        experience = det.get('experience')
        salary = det.get('salary')
        location = det.get('location')
        job_url = 'https://www.naukri.com' + job.get('jdURL', '')
        jdata = {
            'title': title,
            'company': company,
            'location': location,
            'description': desc,
            'posted_on': posted_on,
            'experience': experience,
            'salary': salary,
            'site': 'naukri',
            'url': job_url,
        }
        job_data.append(jdata)
    return job_data

def parse_linkedin(response):
    parser = fromstring(response.text)
    jobs = parser.xpath('//ul[@class="jobs-search__results-list"]/li')
    job_data = []
    for job in jobs:
        # Extract and clean all text, then join non-empty strings
        def clean_list(lst):
            return " ".join([s.strip() for s in lst if s and s.strip()])

        title = clean_list(job.xpath('.//h3[@class="base-search-card__title"]/text()'))
        company = clean_list(job.xpath('.//h4[@class="base-search-card__subtitle"]//text()'))
        location = clean_list(job.xpath('.//span[@class="job-search-card__location"]//text()'))
        posted = clean_list(job.xpath('.//time[@class="job-search-card__listdate"]/text()'))
        url_list = job.xpath('./div/a/@href')
        url = url_list[0].strip() if url_list else ''

        jdata = {
            'title': title,
            'company': company,
            'location': location,
            'posted_on': posted,
            'url': url,
            'site': 'linkedin',
            # LinkedIn search page doesn't provide these fields directly
            'description': '',  # LinkedIn search page doesn't provide description
            'experience': '',   # Not available directly
            'salary': '',       # Not available directly
        }
        job_data.append(jdata)
    return job_data