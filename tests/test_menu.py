#
# (C) Copyright 2014 Alan Cabrera
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import sys

import flask
from flask.ext import MenuManager as mgr


def test_menu(app):
    mgr.MenuManager(app)

    @app.route('/test')
    @app.route('/hello', endpoint='say_hello')
    @app.route('/goodbye', endpoint='say_goodbye')
    @mgr.register_menu(app, '#test', 'Test')
    @mgr.register_menu(app, '#test#hello', 'Hello', endpoint='say_hello')
    @mgr.register_menu(app, '#test#goodbye', 'Goodbye', endpoint='say_goodbye')
    def test_endpoint():
        return 'test'

    with app.test_client() as c:
        c.get('/test')

        test_menu_item = mgr.menu_context['test']
        assert 'hello' in test_menu_item
        assert 'goodbye' in test_menu_item

        hello_menu_item = mgr.menu_context['test']['hello']
        goodbye_menu_item = mgr.menu_context['test']['goodbye']

        c.get('/test')
        current_menu_item = mgr.menu_context.current_menu_item
        assert test_menu_item == current_menu_item
        assert current_menu_item.endpoint == 'test_endpoint'
        assert current_menu_item.endpoint == flask.request.endpoint
        assert current_menu_item.text == 'Test'
        assert current_menu_item.url == '/test'
        assert current_menu_item.selected

        assert test_menu_item.selected
        assert not hello_menu_item.selected
        assert not goodbye_menu_item.selected

        assert test_menu_item.branch_selected
        assert not hello_menu_item.branch_selected
        assert not goodbye_menu_item.branch_selected

        c.get('/hello')
        current_menu_item = mgr.menu_context.current_menu_item
        assert hello_menu_item == current_menu_item
        assert current_menu_item.endpoint == 'say_hello'
        assert current_menu_item.endpoint == flask.request.endpoint
        assert current_menu_item.text == 'Hello'
        assert current_menu_item.url == '/hello'
        assert current_menu_item.selected

        assert not test_menu_item.selected
        assert hello_menu_item.selected
        assert not goodbye_menu_item.selected

        assert test_menu_item.branch_selected
        assert hello_menu_item.branch_selected
        assert not goodbye_menu_item.branch_selected

        c.get('/goodbye')
        current_menu_item = mgr.menu_context.current_menu_item
        assert goodbye_menu_item == current_menu_item
        assert current_menu_item.endpoint == 'say_goodbye'
        assert current_menu_item.endpoint == flask.request.endpoint
        assert current_menu_item.text == 'Goodbye'
        assert current_menu_item.url == '/goodbye'
        assert current_menu_item.selected

        assert not test_menu_item.selected
        assert not hello_menu_item.selected
        assert goodbye_menu_item.selected

        assert test_menu_item.branch_selected
        assert not hello_menu_item.branch_selected
        assert goodbye_menu_item.branch_selected


def test_order(app):
    mgr.MenuManager(app)

    @app.route('/test')
    @app.route('/hello')
    @app.route('/goodbye')
    @mgr.register_menu(app, '#test', 'Test')
    @mgr.register_menu(app, '#test#hello', 'Hello', order=2)
    @mgr.register_menu(app, '#test#goodbye', 'Goodbye', order=1)
    def test_endpoint():
        return 'test'

    with app.test_client() as c:
        c.get('/test')
        current_menu_item = mgr.menu_context.current_menu_item

        assert current_menu_item.keys() == ['goodbye', 'hello']


def test_order_reverse(app):
    mgr.MenuManager(app)

    @app.route('/test')
    @app.route('/hello')
    @app.route('/goodbye')
    @mgr.register_menu(app, '#test', 'Test')
    @mgr.register_menu(app, '#test#hello', 'Hello', order=1)
    @mgr.register_menu(app, '#test#goodbye', 'Goodbye', order=2)
    def test_endpoint():
        return 'test'

    with app.test_client() as c:
        c.get('/test')
        current_menu_item = mgr.menu_context.current_menu_item

        assert current_menu_item.keys() == ['hello', 'goodbye']


def test_active(app):
    mgr.MenuManager(app)

    hello_active = True
    hello_active_fn = lambda: hello_active

    @app.route('/test')
    @app.route('/hello')
    @app.route('/goodbye')
    @mgr.register_menu(app, '#test', 'Test')
    @mgr.register_menu(app, '#test#hello', 'Hello', active_fn=hello_active_fn)
    @mgr.register_menu(app, '#test#goodbye', 'Goodbye')
    def test_endpoint():
        return 'test'

    with app.test_client() as c:
        c.get('/test')

        test_menu_item = mgr.menu_context['test']
        hello_menu_item = mgr.menu_context['test']['hello']
        goodbye_menu_item = mgr.menu_context['test']['goodbye']

        c.get('/test')
        assert test_menu_item.active
        assert hello_menu_item.active
        assert goodbye_menu_item.active

        c.get('/hello')
        assert test_menu_item.active
        assert hello_menu_item.active
        assert goodbye_menu_item.active

        c.get('/goodbye')
        hello_active = False
        assert test_menu_item.active
        assert not hello_menu_item.active
        assert goodbye_menu_item.active


def test_hidden(app):
    mgr.MenuManager(app)

    hello_hidden = False
    hello_hidden_fn = lambda: hello_hidden

    @app.route('/test')
    @app.route('/hello')
    @app.route('/goodbye')
    @mgr.register_menu(app, '#test', 'Test')
    @mgr.register_menu(app, '#test#hello', 'Hello', hidden_fn=hello_hidden_fn)
    @mgr.register_menu(app, '#test#goodbye', 'Goodbye')
    def test_endpoint():
        return 'test'

    with app.test_client() as c:
        c.get('/test')

        test_menu_item = mgr.menu_context['test']
        hello_menu_item = mgr.menu_context['test']['hello']
        goodbye_menu_item = mgr.menu_context['test']['goodbye']

        c.get('/test')
        assert not test_menu_item.hidden
        assert not hello_menu_item.hidden
        assert not goodbye_menu_item.hidden

        c.get('/hello')
        assert not test_menu_item.hidden
        assert not hello_menu_item.hidden
        assert not goodbye_menu_item.hidden

        c.get('/goodbye')
        hello_hidden = True
        assert not test_menu_item.hidden
        assert hello_menu_item.hidden
        assert not goodbye_menu_item.hidden


def test_values(app):
    mgr.MenuManager(app)

    @app.route('/test/<int:value>')
    @mgr.register_menu(app, '#test#1', 'Test',
                       endpoint_fn=lambda: {'value': 121, 'a': 1})
    @mgr.register_menu(app, '#test#2', 'Test',
                       endpoint_fn=lambda: {'value': 122, 'b': 2})
    @mgr.register_menu(app, '#test#3', 'Test',
                       endpoint_fn=lambda: {'value': 123, 'c': 3})
    def test_endpoint(value):
        return 'test'

    with app.test_client() as c:
        c.get('/test/122')
        assert mgr.menu_context['test']['1'].url == '/test/121?a=1'
        assert mgr.menu_context['test']['2'].url == '/test/122?b=2'
        assert mgr.menu_context['test']['3'].url == '/test/123?c=3'


def test_generated(app):
    mgr.MenuManager(app)

    def projects_generated_fn():
        return [
            mgr.MenuEntry('#zookeeper', 'Zookeeper',
                          order=3, values={'value': 123}),
            mgr.MenuEntry('#geronimo', 'Geronimo',
                          order=2, values={'value': 122}),
            mgr.MenuEntry('#accumulo', 'Accumulo',
                          order=1, values={'value': 121}),
            mgr.MenuEntry('#activemq', 'ActiveMQ',
                          order=0, values={'value': 120}),
        ]

    @app.route('/test/<int:value>')
    @mgr.register_menu(app, '#test', 'Test',
                       generated_fn=projects_generated_fn)
    @mgr.register_menu(app, '#test#hello', 'Hello',
                       order=-sys.maxint, endpoint_fn=lambda: {'value': 119})
    @mgr.register_menu(app, '#test#goodbye', 'Goodbye',
                       order=sys.maxint, endpoint_fn=lambda: {'value': 130})
    def test_endpoint(value):
        return 'test'

    with app.test_client() as c:
        c.get('/test/124')
        current_menu_item = mgr.menu_context.current_menu_item

        assert current_menu_item.keys() == ['hello', 'activemq', 'accumulo',
                                            'geronimo', 'zookeeper', 'goodbye']

        assert current_menu_item.keys() == ['hello', 'activemq', 'accumulo',
                                            'geronimo', 'zookeeper', 'goodbye']

        assert [mi.text for mi in current_menu_item.values()] == [
            'Hello',
            'ActiveMQ', 'Accumulo',
            'Geronimo', 'Zookeeper',
            'Goodbye']

        assert all(mi.active for mi in current_menu_item.values())
        assert not any(mi.hidden for mi in current_menu_item.values())

        test_menu_item = mgr.menu_context['test']
        assert test_menu_item.branch_selected
        assert test_menu_item.selected


def test_blueprint(app):
    mgr.MenuManager(app)
    blueprint = flask.Blueprint('foo', 'foo', url_prefix="/foo")

    @app.route('/test')
    @mgr.register_menu(app, '#', 'Test')
    def test():
        return 'test'

    @blueprint.route('/bar')
    @mgr.register_menu(blueprint, '#bar', 'Foo Bar')
    def bar():
        return 'bar'

    app.register_blueprint(blueprint)

    with app.test_client() as c:
        c.get('/test')
        current_menu_item = mgr.menu_context.current_menu_item
        assert current_menu_item.text == 'Test'
        assert current_menu_item.url == '/test'

    with app.test_client() as c:
        c.get('/foo/bar')
        current_menu_item = mgr.menu_context.current_menu_item
        assert current_menu_item.text == 'Foo Bar'
        assert current_menu_item.url == '/foo/bar'
