import requests
from decouple import config
import json

def get_instagram_session():
    session = requests.Session()
    session.cookies.update({
        'sessionid': config('INSTAGRAM_SESSION_ID'),
        'csrftoken': config('INSTAGRAM_CSRF_TOKEN'),
    })
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    session.headers.update(headers)
    return session

def verify_instagram_session():
    session = get_instagram_session()
    try:
        response = session.get('https://www.instagram.com/accounts/login/')
        return response.status_code == 200
    except:
        return False 