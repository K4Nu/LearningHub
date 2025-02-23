import requests
import random
"""
fullHDURL bedzie dopiero jak mi zatwierdza api
"""
key="45952489-ff408b638bb31e70bc4675a3a"
url = f"https://pixabay.com/api/?key={key}&q=nature&image_type=photo"
response=requests.get(url)
response=response.json()
#print(response["hits"][random.randint(0,20)]["largeImageURL"])

