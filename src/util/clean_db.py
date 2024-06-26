import requests
response = requests.delete("http://localhost:8000/delete-all")
print(response.status_code)