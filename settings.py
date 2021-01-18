import os

settings = {
    "template_path": "templates",
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "media_path": os.path.join(os.path.dirname(__file__), "media"),
    "cookie_secret": "rDTzO1yDRNwtOpyU",
    "login_url": "/login/?",
    # "xsrf_cookies": True,
    'redis': {
        "host": "192.168.2.168",
        "port": 6379
    },
    'mysql': {
        'database': 'schoolshop',
        'host': '192.168.2.168',
        'port': 3306,
        'user': 'root',
        'password': '199791'
    },
    'es': {
        'host': '192.168.2.168'
    }
}
