from requests import get
import pprint

response = get("https://dummyjson.com/users?limit=2&skip=10")

data = response.json()

pprint.pprint(data["users"][1])