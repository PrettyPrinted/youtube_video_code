import requests

def load_urls():
    urls = [
        'httpss://prettyprinted.com', 
        'https://prettyprinted.coms', 
        'prettyprinted.com', 
        'https://prettyprinted.com'
    ]

    exceptions = []

    for url in urls:
        try:
            r = requests.get(url)
        except Exception as e:
            e.add_note(url)
            exceptions.append(e)
    
    raise ExceptionGroup('Request Errors', exceptions)

try:
    load_urls()
except* requests.exceptions.InvalidSchema as eg:
    print('Invalid Schema', [e.__notes__[0] for e in eg.exceptions])
except* requests.exceptions.MissingSchema as eg:
    print('Missing Schema', [e.__notes__[0] for e in eg.exceptions])
except* requests.exceptions.ConnectionError as eg:
    print('Connection Error', [e.__notes__[0] for e in eg.exceptions])