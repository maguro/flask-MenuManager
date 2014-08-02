# coding=utf-8
#
# (C) Copyright 2014 Alan Cabrera
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
"""
    flaskext.MenuManager
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: © 2014 Alan Cabrera
    :email: `Alan Cabrera (adc@toolazydogs.com)`
    :license: ASL20, see LICENSE for more details.
"""


class MenuManager(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        pass
