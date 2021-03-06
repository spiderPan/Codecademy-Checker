import csv
import json
from requests_html import HTMLSession
import time


def login(user_name, password):
    login_session = HTMLSession()
    login_url = 'https://www.codecademy.com/login'

    login_page = login_session.get(login_url)
    authenticity_token = login_page.html.find('input[name=authenticity_token]', first=True).attrs['value']
    login_data = {'user[login]': user_name,
                  'user[password]': password,
                  'authenticity_token': authenticity_token}
    login_session.post(login_url, data=login_data)

    if not is_session_logged_in(login_session):
        error_message = 'Login failed for {0}===>{1}\n'.format(user_name, password)

        debug_content(error_message, './error_users.txt')
        return False

    return login_session


def is_session_logged_in(login_session):
    login_cookies = login_session.cookies.get_dict()
    # print(login_cookies)

    return 'remember_user_token' in login_cookies


def get_check_course_list():
    return [
        {
            'name': 'learn-sql',
            'url': 'https://www.codecademy.com/learn/learn-sql',
            'courses': [
                'Manipulation',
                'Queries',
                'Aggregate Functions',
            ]
        }
    ]


def get_course_data(login_session, course_item):
    course_url = course_item['url']
    r_sql = login_session.get(course_url, cookies=login_session.cookies)
    react_props = r_sql.html.find('.react-root', first=True).attrs['data-react-props']
    react_props_json = json.loads(react_props)
    # course_name = course_item['name']
    # debug_content(react_props_json, course_name + '.json', type='json')
    return react_props_json


def debug_content(content, file, type='txt'):
    with open('./' + file, 'a+', encoding='utf8') as f:
        if (type == 'json'):
            json.dump(content, f, indent=4)
        else:
            f.write(content)


def is_subcourse_finished(sub_course, course_data):
    course_id = get_subcourse_id(sub_course, course_data['contentItems']['byUuid'])
    assert course_id != 0

    return course_data['contentItemProgresses']['byId'][course_id]['completed']


def get_subcourse_id(sub_course_name, course_content_items):
    for course_id, course_item in course_content_items.items():
        if course_item['title'] == sub_course_name:
            return course_id
    return 0


def get_user_list():
    user_list = []
    with open('./users.csv') as user_csv_file:
        user_rows = csv.reader(user_csv_file, delimiter=',')
        for line, row in enumerate(user_rows):
            try:
                row = list(map(str.strip, row))
                if len(row) != 5:
                    raise ValueError(line, 'Not Enough Fields', row)

                user_dict = {
                    'ID': row[0],
                    'user_name': row[3],
                    'password': row[4],
                }
                user_list.append(user_dict)
                # print(user_dict)
            except ValueError as err:
                error_message = 'Line {0} {1}===>{2}\n'.format(err.args[0], err.args[1], ','.join(err.args[2]))

                debug_content(error_message, './error_users.txt')
                pass
    return user_list


def run():
    user_list = get_user_list()
    for user in user_list:
        user_progress = {
            'completed': 0,
            'total': 0
        }
        print('Checking User:' + user['ID'] + '===')
        login_session = login(user['user_name'], user['password'])
        if login_session is False:
            continue

        checking_courses = get_check_course_list()

        for course_item in checking_courses:
            sub_course_list = course_item['courses']
            course_data = get_course_data(login_session, course_item)
            for sub_course in sub_course_list:
                user_progress['total'] += 1
                if is_subcourse_finished(sub_course, course_data['reduxData']['entities']):
                    user_progress['completed'] += 1
                    print('Passed ' + sub_course)
                else:
                    print('Failed ' + sub_course)
        user_score = str(user_progress['completed'] / user_progress['total'] * 100.0)

        print('User Score:' + user_score)
        debug_content('{0},{1}\n'.format(user['ID'], user_score), './completion_report.txt')


run()
