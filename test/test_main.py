# © 2024 Fraunhofer-Gesellschaft e.V., München
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# still needs to be implemented

import main


class TestUrlIsPublic:

    def test_public(self):
        result = main._url_is_public('https://github.com/fraunhofer-isi')
        assert result

    def test_not_public(self):
        result = main._url_is_public('https://github.com/fraunhofer-enas')
        assert not result
