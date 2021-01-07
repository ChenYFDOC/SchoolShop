from apps.users.urls import url_match as users_url
from apps.display.urls import url_match as display_url

url_match = [
    *users_url,
    *display_url,
]
