<!--
© 2023 - 2024 Fraunhofer-Gesellschaft e.V., München
© 2024 Fraunhofer-Gesellschaft e.V., M├╝nchen

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# github_crawler

Uses GitHub API to crawl data about GitHub pages of Fraunhofer institutes:

https://fraunhofer-society.github.io/github_crawler/

In order to generate *public/index.html* locally, run following command:

python src/main.py {github_user} {github_access_token}

where the {} variables need to replaced with actual values.

## Licenses

This project is free and open source:

* It is licensed under the GNU Affero General Public License v3 or later (AGPLv3+) - see LICENSE.md.
* It uses third-party open source modules, see pyproject.toml and THIRDPARTY.md.

## Badges

Click on some badge to navigate to the corresponding **quality assurance** workflow:


### Formatting & linting

[![lint](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/fhg-isi/2bb9509d2a0c1605acdc671fd313de59/raw/github_crawler_lint.json)](https://github.com/fraunhofer-society/github_crawler/actions/workflows/lint.yml) Checks code formatting with [Pylint](https://pylint.readthedocs.io/)

### Test coverage

[![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/fhg-isi/2bb9509d2a0c1605acdc671fd313de59/raw/coverage.json)](https://github.com/fraunhofer-isi/micat/actions/workflows/coverage.yml) Determines test coverage with [pytest-cov](https://github.com/pytest-dev/pytest-cov)


### License compliance

[![license_check](https://github.com/fraunhofer-society/github_crawler/actions/workflows/license_check.yml/badge.svg)](https://github.com/fraunhofer-society/github_crawler/actions/workflows/license_check.yml) Checks license compatibility with [LicenseCheck](https://github.com/FHPythonUtils/LicenseCheck)

[![reuse_annotate](https://github.com/fraunhofer-society/github_crawler/actions/workflows/reuse_annotate.yml/badge.svg)](https://github.com/fraunhofer-society/github_crawler/actions/workflows/reuse_annotate.yml) Creates copyright & license annotations with [reuse](https://git.fsfe.org/reuse/tool)

[![reuse compliance](https://api.reuse.software/badge/github.com/fraunhofer-society/github_crawler)](https://api.reuse.software/badge/github.com/fraunhofer-society/github_crawler) Checks for REUSE compliance with [reuse](https://git.fsfe.org/reuse/tool)

### Dependency updates & security checks

[![renovate](https://github.com/fraunhofer-society/github_crawler/actions/workflows/renovate.yml/badge.svg)](https://github.com/fraunhofer-society/github_crawler/actions/workflows/renovate.yml) Updates dependencies with [renovate](https://github.com/renovatebot/renovate)

[![CodeQL](https://github.com/fraunhofer-society/github_crawler/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/fraunhofer-society/github_crawler/actions/workflows/github-code-scanning/codeql) Discovers vulnerabilities with [CodeQL](https://codeql.github.com/)

