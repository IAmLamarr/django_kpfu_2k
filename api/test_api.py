from pprint import pprint
import requests

resp = requests.get(
    url="http://127.0.0.1:8000/items/",
    timeout=1
)

pprint(resp.json())