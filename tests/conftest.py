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
import flask
import pytest


@pytest.fixture
def app():
    flask_app = flask.Flask(__name__)

    flask_app.config['DEBUG'] = True
    flask_app.config['TESTING'] = True
    flask_app.logger.disabled = True

    return flask_app
