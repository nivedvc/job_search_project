import requests
import random
import string
from .utils import get_proxy, get_headers_url, get_params, insert_jobs
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
        verify = True
        if site == 'linkedin':
            # Generate a random string for 'bcookie'
            bcookie_value = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            cookies = {'bcookie': bcookie_value}
        if site == 'infopark':
            verify = False
        response = requests.get(
            url,
            params=params,
            headers=headers,
            proxies=proxy,
            cookies=cookies,
            verify=verify
        )
        job_data = get_results(response, site)
        data_summary[site] = len(job_data)
        print(f'Request sent to {site} | status code: {response.status_code} | jobs found: {len(job_data)}')
        if job_data:
            data.extend(job_data)
    insert_jobs(data, keyword)
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
    elif site.lower() == 'infopark':
        return parse_infopark(response)
    
def parse_infopark(response):
    parser = fromstring(response.text)
    jobs = parser.xpath('//table[@class="table"]/tbody//tr')
    job_data = []
    for job in jobs:
        title = job.xpath('./td[@class="head"]/text()')
        title = title[0].strip() if title else ''
        if 'no jobs' in title.lower():
            print('No jobs found on Infopark')
            return []
        company = job.xpath('./td[@class="date"]/text()')
        company = company[0].strip() if company else ''
        last_date = job.xpath('./td[3]/text()')
        last_date = last_date[0].strip() if last_date else ''
        url_list = job.xpath('./td[@class="btn-sec"]/a/@href')
        url = url_list[0].strip() if url_list else ''
        if url:
            print(f'sending details request to {url}')
            headers, main_url = get_headers_url('infopark')
            details_response = requests.get(
                url,
                headers=headers,
                proxies=get_proxy(),
                verify=False  # Infopark uses self-signed SSL certificates
            )
            details_parser = fromstring(details_response.text)
            details1_xpath = '//div[@class="deatil-box"]/text()'
            details2_xpath = '//div[@class="deatil-box"]/div[@class="contact"]//text()'
            details1 = get_single_string(details_parser.xpath(details1_xpath))
            details2 = get_single_string(details_parser.xpath(details2_xpath))
            details = details1 + '\n' + details2 + '\nLast date to apply: ' + last_date
            details = remove_html_tags(details)
        jdata = {
            'title': title,
            'company': company,
            'location': '',  # Infopark search page doesn't provide location,
            'posted_on': '',
            'url': url,
            'site': 'infopark',
            'description': details,  # Infopark search page doesn't provide description
            'experience': '',   # Not available directly
            'salary': '',       # Not available directly
        }
        job_data.append(jdata)
    return job_data


def get_single_string(lst):
    """
    Joins a list of strings into a single string, removing any leading or trailing whitespace.
    """
    return ' '.join([s.strip() for s in lst if s and s.strip()])

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