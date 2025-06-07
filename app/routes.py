from flask import Blueprint, render_template, request
from .scraper import get_search_results

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