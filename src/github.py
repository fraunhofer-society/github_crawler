# © 2024 Fraunhofer-Gesellschaft e.V., München
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import requests

from reverser import Reverser


def activity(url, github_session):
    # example api url: https://api.github.com/orgs/fraunhofer-isi/events
    api_url = url.replace('github.com', 'api.github.com/orgs') + '/events?per_page=1000'
    json_data = github_session.get(api_url).json()
    if 'message' in json_data:
        error_message = 'API rate limit exceeded'
        message = json_data['message']
        if error_message in message:
            raise SystemError(error_message)

        return 0
    number_of_events = len(json_data)
    return number_of_events


def languages(repos):
    language_entries = {}
    for repository in repos:
        language = repository['language']
        if language not in language_entries:
            language_entries[language] = 0
        language_entries[language] = language_entries[language] + 1

    language_entries = _sort_dictionary_by_values(language_entries)
    return language_entries


def licenses(repos):
    license_entries = {}
    for repository in repos:
        software_license = repository['license']
        if software_license is not None:
            license_id = software_license['key']
            if license_id not in license_entries:
                license_entries[license_id] = 0
            license_entries[license_id] = license_entries[license_id] + 1
    license_entries = _sort_dictionary_by_values(license_entries)
    return license_entries


def repository_map(urls, github_session):
    repos = {}
    for url in urls:
        repositories_for_url = repositories(url, github_session)
        repos[url] = repositories_for_url
    return repos


def repositories(url, github_session):
    # example api url: https://api.github.com/orgs/fraunhofer-isi/repos
    api_url = url.replace('github.com', 'api.github.com/orgs') + '/repos?per_page=1000'
    json_data = github_session.get(api_url).json()
    if 'message' in json_data:
        message = json_data['message']
        error_message = 'API rate limit exceeded'
        if error_message in message:
            raise SystemError(error_message)

        api_url = url.replace('github.com', 'api.github.com/users') + '/repos?per_page=1000'
        json_data = github_session.get(api_url).json()
        if 'message' in json_data:
            message = json_data['message']
            error_message = 'API rate limit exceeded'
            if error_message in message:
                raise SystemError(error_message)

            return []

    if len(json_data) == 1:
        first_entry = json_data[0]
        if 'message' in first_entry:
            return []
    return json_data


def session(user, token):
    github_session = requests.Session()
    if token != '':
        github_session.auth = (user, token)
    return github_session


def _sort_dictionary_by_values(dictionary):
    sorted_dictionary = dict(sorted(dictionary.items(), key=lambda item: Reverser(item[1])))
    return sorted_dictionary
