import os

settings = {
    "template_path": "templates",
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "rDTzO1yDRNwtOpyU",
    "login_url": "/login",
    "xsrf_cookies": True,
    'redis': {
        "host": "127.0.0.1",
        "port": 11111
    },
    'mysql': {
        'database': 'schoolshop',
        'host': '127.0.0.1',
        'port': 11112,
        'user': 'root',
        'password': '199791'
    }
}
