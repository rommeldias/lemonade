#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import gettext

import eventlet
import os
from seed.socketio_events import StandSocketIO

locales_path = os.path.join(os.path.dirname(__file__), '..', 'i18n', 'locales')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str,
                        help="Config file", required=True)
    parser.add_argument("--lang", help="Minion messages language (i18n)",
                        required=False, default="en_US")
    args = parser.parse_args()

    eventlet.monkey_patch(all=True)

    from seed.factory import create_app, create_babel_i18n, \
        create_redis_store

    t = gettext.translation('messages', locales_path, [args.lang],
                            fallback=True)
    t.install(str=True)

    app = create_app(config_file=args.config)
    babel = create_babel_i18n(app)
    # socketio, socketio_app = create_socket_io_app(app)
    seed_socket_io = StandSocketIO(app)
    redis_store = create_redis_store(app)

    if app.debug:
        app.run(debug=True)
    else:
        port = int(app.config['SEED_CONFIG'].get('port', 5000))

        # noinspection PyUnresolvedReferences
        eventlet.wsgi.server(eventlet.listen(('', port)),
                             seed_socket_io.socket_app)
