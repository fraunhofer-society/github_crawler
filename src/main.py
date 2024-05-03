# © 2024 Fraunhofer-Gesellschaft e.V., München
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime
import json
import shutil
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import github
from reverser import Reverser
from string_order import StringOrder


def main(arguments):
    if len(arguments) != 3:
        print("Usage: python main.py github_user github_access_token")
        # return

    # file_name = arguments[0]

    github_user = arguments[1]
    github_access_token = arguments[2]

    target_folder = './public'

    institutes_url = 'https://www.fraunhofer.de/en/institutes/institutes-and-research-establishments-in-germany.html'

    github_session = github.session(github_user, github_access_token)

    institutes = _crawl_institute_data(institutes_url, github_session)

    json_file_path = target_folder + '/institutes.json'
    _save_json_file(json_file_path, institutes)

    institutes = _read_jon_file(json_file_path)

    institutes = _sort_institutes(institutes)

    _copy_stylesheet(target_folder)

    _save_html_file(
        target_folder + '/index.html',
        institutes,
        is_including_numbers=True,
    )


def _copy_stylesheet(target_folder):
    file_name = 'stylesheet.css'
    source_file_path = './src/' + file_name
    target_file_path = target_folder + '/' + file_name
    shutil.copyfile(source_file_path, target_file_path)


def _crawl_institute_data(institutes_url, github_session):
    html = _parse_html(institutes_url)
    institutes = _read_institute_data(html)
    # limit = 3
    # institutes = institutes[0:limit]
    institutes = _github_accounts(institutes, github_session)
    return institutes


def _fix_umlauts(full_html):
    full_html = full_html.replace('ä', '&auml;').replace('ö', '&ouml;').replace('ü', '&uuml;')
    return full_html


def _save_html_file(file_path, institutes, is_including_numbers=True):
    date = _date()
    full_html = (
        '<html>\n'
        + '<head>\n'
        + '  <link rel="stylesheet" href="stylesheet.css">\n'
        + '<head>\n'
        + '<body>\n'
        + '  <p>Overview Fraunhofer GitHub pages as of '
        + date
        + '  </p>\n'
        + '  <table>\n'
        + _html_header_row(is_including_numbers)
    )

    for institute in institutes:
        html_row = _html_row(institute, is_including_numbers)
        full_html += html_row

    full_html += '''</table>
        <p><a href="https://www.fraunhofer.de/en/publishing-notes.html">PUBLISHING NOTES</a></p>
      </body>
    </html>
    '''

    full_html = _fix_umlauts(full_html)

    with open(file_path, 'w', encoding='utf8') as file:
        file.write(full_html)


def _date():
    current_date = datetime.datetime.now()
    current_month = current_date.strftime("%B")
    current_year = current_date.strftime("%Y")
    current_month_and_year = f"{current_month} {current_year}"
    return current_month_and_year


def _html_empty_detail_columns(is_including_numbers):
    if is_including_numbers:
        return '''
         <td></td>
         <td></td>
         <td></td>
         <td></td>
         <td></td>
        '''

    return '''
         <td></td>        
         <td></td>
         <td></td>
        '''


def _html_header_row(include_numbers):
    if include_numbers:
        return '''
        <hr>
          <th>Institute</th>
          <th>Id</th>
          <th>Location</th>
          <th>GitHub</th>
          <th>Number of repos</th>
          <th>Activity</th>
          <th>Languages</th>
          <th>Licenses</th>
         </hr>
        '''

    return '''
        <hr>
          <th>Institute</th>
          <th>Id</th>
          <th>Location</th>
          <th>GitHub</th>   
          <th>Languages</th>
          <th>Licenses</th>
         </hr>
        '''


def _html_row(institute, is_including_numbers):
    html_row = '<tr>'
    link = institute['link']
    html_row += '<td>' + link + '</td>'
    institute_id = institute['id']
    html_row += '<td>' + institute_id.upper() + '</td>'
    location = institute['location']
    html_row += '<td>' + location + '</td>'
    account = institute['github_account']
    url = account['url']
    if url is None:
        html_row += _html_empty_detail_columns(is_including_numbers)
    else:
        html_row += '<td><a href="' + url + '"/>' + url + '</td>'

        if is_including_numbers:
            number_of_repositories = account['number_of_repositories']
            html_row += '<td>' + str(number_of_repositories) + '</td>'

            activity = account['activity']
            html_row += '<td>' + str(activity) + '</td>'

        languages = account['languages']
        html_row += _html_languages(languages, is_including_numbers)

        licenses = account['licenses']
        html_row += _html_licenses(licenses, is_including_numbers)

    html_row += '\n'

    return html_row


def _html_languages(languages, is_including_numbers):
    html = '<td>'
    for language, count in languages.items():
        if language is not None and language != 'null':
            if is_including_numbers:
                html += language + ': ' + str(count) + '<br>'
            else:
                html += language + '<br>'
    html += '</td>'
    return html


def _html_licenses(licenses, is_including_numbers):
    html = '<td>'
    for license_name, count in licenses.items():
        if license_name is not None and license_name != 'other':
            if is_including_numbers:
                html += license_name + ': ' + str(count) + '<br>'
            else:
                html += license_name + '<br>'
    html += '</td>'
    return html


def _github_accounts(institutes, github_session):
    for institute in institutes:
        institute_id = institute['id']
        print('Searching for ' + institute_id + ' ...')
        urls = _find_github_urls(institute_id)

        all_repositories = github.repository_map(urls, github_session)
        main_url = _main_url(urls, all_repositories)
        repositories = _main_repositories(main_url, all_repositories)
        main_languages = github.languages(repositories)
        main_licenses = github.licenses(repositories)
        main_activity = github.activity(main_url, github_session) if main_url else 0

        account = {
            'url': main_url,
            'repositories': repositories,
            'number_of_repositories': len(repositories),
            'languages': main_languages,
            'licenses': main_licenses,
            'activity': main_activity,
            'all_urls': urls,
            'all_repositories': all_repositories,
        }
        institute['github_account'] = account

    return institutes


def _find_github_urls(institute_id):
    # Assumes that usernames follow the pattern
    # fraunhofer{institute_id} or fraunhofer-{institute_id}
    # "Username may only contain alphanumeric characters or single hyphens,
    # and cannot begin or end with a hyphen."
    url_prefix = 'https://github.com/fraunhofer'
    separators = ['-', '']
    urls = []
    for separator in separators:
        url = url_prefix + separator + institute_id
        if _url_exists(url):
            urls.append(url)
    return urls


def _main_repositories(main_url, repositories):
    if main_url and main_url in repositories:
        return repositories[main_url]

    return []


def _main_url(urls, repositories):
    main_url = ''
    max_number_of_repositories = 0
    for url in urls:
        if not _url_is_public(url):
            continue

        if main_url == '':
            main_url = url
        repositories_for_url = repositories[url]
        number_of_repositories = len(repositories_for_url)
        if number_of_repositories > max_number_of_repositories:
            max_number_of_repositories = number_of_repositories
            main_url = url

    return main_url


def _url_is_public(url):
    try:
        response = requests.head(url, timeout=10000)
        return response.status_code == requests.codes.ok  # pylint: disable=no-member
    except requests.exceptions.RequestException:
        return False


def _parse_html(url):
    html = requests.get(url, timeout=10000).text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def _read_institute_data(html):
    ids = []
    institutes = []
    id_divs = html.find_all('div', {'class': 'table-cell-id'})
    for id_div in id_divs:
        institute_id = id_div.text.strip().lower()
        if institute_id in ids:
            continue

        if institute_id != 'abbr.':
            ids.append(institute_id)
            institute = {
                'id': institute_id,
                'link': _read_institute_link(id_div),
                'location': _read_institute_location(id_div),
            }
            institutes.append(institute)

    return institutes


def _read_institute_link(id_div):
    link_div = id_div.previous_sibling.previous_sibling
    link_tag = list(link_div.children)[1]
    return str(link_tag)


def _read_institute_location(id_div):
    location_div = id_div.next_sibling.next_sibling
    location = list(location_div.children)[0].strip()
    return location


def _read_jon_file(file_path):
    with open(file_path, "r", encoding='utf8') as file:
        json_data = json.load(file)
        return json_data


def _save_json_file(file_path, json_data):
    directory_path = Path(file_path).parent
    directory_path.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf8') as file:
        json.dump(json_data, file)


def _sort_institutes(institutes):
    sorted_institutes = sorted(
        institutes,
        key=lambda x: (
            Reverser(x['github_account']['number_of_repositories']),
            Reverser(x['github_account']['activity']),
            StringOrder(x['github_account']['url']),
            x['id'],
        ),
    )
    return sorted_institutes


def _url_exists(url):
    text = requests.get(url, timeout=10000).text
    if text == 'Not Found':
        return False

    return True


if __name__ == '__main__':
    main(sys.argv)
