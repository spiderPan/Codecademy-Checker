import requests
from requests_html import HTMLSession
import json

URL = 'https://www.codecademy.com/login'
PROFILE_URL = 'https://www.codecademy.com/profiles/me'
SQL_URL = 'https://www.codecademy.com/learn/learn-sql'


def login():
    login_session = HTMLSession()
    user_name = 'ajaxSolver08921'
    password = 'codecademy987'

    login_page = login_session.get(URL)
    authenticity_token = login_page.html.find('input[name=authenticity_token]', first=True).attrs['value']
    login_data = {'user[login]': user_name, 'user[password]': password, 'authenticity_token': authenticity_token}
    login_session.post(URL, data=login_data)

    return login_session


def check_course_completion():
    login_session = login()
    checking_courses = {
        'learn-the-command-line': 'https://www.codecademy.com/learn/learn-the-command-line',
        'learn-sql': 'https://www.codecademy.com/learn/learn-sql',
    }
    for name, url in checking_courses.items():
        r_sql = login_session.get(url, cookies=login_session.cookies)
        react_props = r_sql.html.find('.react-root', first=True).attrs['data-react-props']
        react_props_json = json.loads(react_props)
        debug_content(react_props_json, name+'.json', type='json')

    print(json.dumps(react_props_json, indent=4))


def debug_content(content, file, type='txt'):
    with open('./' + file, 'w+', encoding='utf8') as f:
        if (type == 'json'):
            json.dump(content, f, indent=4)
        else:
            f.write(content)


check_course_completion()
