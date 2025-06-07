from flask import Flask, render_template, request
# from test import get_search_results
import requests
import re

app = Flask(__name__)  # create the app

@app.route('/')  # Tells which function to call when homepage is accessed
def home():
    return render_template('home.html')


@app.route('/page', methods=['GET', 'POST'])
def page():
    name = None
    if request.method == 'POST':
        name = request.form['name']
    return render_template('page.html', name=name)

@app.route('/wish/<name>')  # Tells which function to call when homepage is accessed
def wish(name):
    return render_template('wish.html', name=name)


@app.route('/search', methods=['GET', 'POST'])
def search():
    keyword = None
    results = None
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = get_search_results(keyword)
        print(f'lenght of result obtained is {len(results)}')
    return render_template('search_result.html', jobs=results)



def get_search_results(keyword):
    if not keyword:
        return
    headers = {
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
    params = {
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
    proxy = {
        'http': 'http://dsjwwsal:182nac4z6csf@198.23.239.134:6540',
        'https': 'http://dsjwwsal:182nac4z6csf@198.23.239.134:6540',
    }
    response = requests.get(
        'https://www.naukri.com/jobapi/v3/search',
        params=params,
        headers=headers,
        proxies=proxy
    )
    print(f'Rewuest send response obtained: status code: {response.status_code}')
    job_data = get_results(response)
    # print('jobdata: ', job_data)
    return job_data
    

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

def get_results(response):
    try:
        data = response.json()
    except Exception as error:
        print(f"Got none json response! | {response.status_code} | length: {len(response.text)}")
        return
    data = response.json()
    jobs = data.get('jobDetails')
    job_data = []
    for job in jobs:
        title = job.get('title')
        desc = remove_html_tags(job.get('jobDescription'))
        posted_on = job.get('footerPlaceholderLabel')
        company = job.get('companyName')
        det = get_exp_sal_loc(job.get('placeholders'))
        experience = det.get('experience')
        salary = det.get('salary')
        location = det.get('location')
        job_url = 'https://www.naukri.com' + job.get('jdURL')
        jdata = {
            'title': title,
            'company': company,
            'location': location,
            'description': desc,
            'posted_on': posted_on,
            'experience': experience,
            'salary': salary,
            'url': job_url,
        }
        job_data.append(jdata)
    return job_data



if __name__ == '__main__':
    app.run(debug=True)