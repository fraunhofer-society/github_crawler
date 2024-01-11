<!--
© 2023 - 2024 Fraunhofer-Gesellschaft e.V., München

SPDX-License-Identifier: AGPL-3.0-or-later
-->

Uses GitHub API to crawl data about GitHub pages of Fraunhofer institutes:

https://fraunhofer-society.github.io/github_crawler/

In order to generate *public/index.html* locally, run following command:

python src/main.py {github_user} {github_access_token}

where the {} variables need to replaced with actual values.

This project is free and open source:

* It is licensed under the GNU Affero General Public License v3 or later (AGPLv3+) - see LICENSE.md.
*  It uses third-party open source modules, see pyproject.toml and THIRDPARTY.md.

