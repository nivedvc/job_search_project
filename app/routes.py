from flask import Blueprint, render_template, request
from .scraper import get_search_results
from .utils import get_jobs, get_latest_10_jobs

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home.html')

@main.route('/search', methods=['GET', 'POST'])
def search():
    keyword = None
    results = None
    data_summary = None
    search_flag = False
    no_websites_flag = False
    websites = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        websites = request.form.getlist('websites')
        results, data_summary = get_search_results(keyword, websites)
        if not websites:
            no_websites_flag = True
            print('No websites selected for search')
        else:
            search_flag = True
        print(f'length of result obtained is {len(results)}')
    total_results = sum(data_summary.values()) if data_summary else 0
    return render_template(
        'search_result.html',
        jobs=results,
        data_summary=data_summary,
        total_results=total_results,
        search_flag=search_flag,
        request=request,
        no_websites_flag=no_websites_flag,
        keyword=keyword,
    )

@main.route('/database', methods=['GET'])
def database():
    job_title = request.args.get('job_title', None)
    location = request.args.get('location', None)
    source = request.args.get('source', None)
    if job_title or location or source:
        jobs = get_jobs(input_keyword=job_title, source=source, location=location)
    else:
        jobs = get_latest_10_jobs()
    return render_template('database.html', jobs=jobs, request=request)