# © 2023 - 2024 Fraunhofer-Gesellschaft e.V., München
# © 2024 Fraunhofer-Gesellschaft e.V., M├╝nchen
#
# SPDX-License-Identifier: AGPL-3.0-or-later

class StringOrder:
    def __init__(self, obj):
        self.obj = obj

    def __eq__(self, other):
        return other.obj == self.obj

    def __lt__(self, other):
        if self.obj == '':
            return False
        if other.obj == '':
            return True

        return other.obj > self.obj
