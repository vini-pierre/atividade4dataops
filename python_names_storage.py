from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "focal-pathway-382223",
  "private_key_id": "9b6c691176b0b2eeee6007d789c2b7bd82ab07c4",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDHvy3rAwcdHm9j\nZvbSAK39viXxe2OI4pJiqP2NjGmix2xsh6mcT4sfZ+EC60A+W/ZtNkgIXgC7j8M8\nkXtaOJGIK6u/Do57bius01UF1YzFjrmbb9YpvJXjl9GihCtBEyF+8VgB2fWqtCqr\nTc2XDVmYpgk66u1gVmA+zBFip+6oZdYpoWq3JM3/g2kFEfnDhVjbkOwe/flUalOn\nwPzUk5jo2pcJvUdqChJ5zMbHNALoC0FQDrQS4Drp1253BgABrpZCn4BoR5BasWpC\nj3H4nMpDjo9PSGs+jE89muPhNIkobPRXXG6Rjq8WD1FCsSfKkLB4xFlTUY3C+jNL\nk7symrW7AgMBAAECggEAHygYcvx1axrYuBIS9N3LRfWXeIvNEkh5Ge+PITmiLpRZ\nurIMiEe2BS+QXwKv8iopDY72fGuhRKBfjT6KFaAWPz3Em9ga7HDaWiparD7LpvMk\ny3SN3NPAM5B2UBm6n3tq8aCWoC9NzRMuRqsrouCftZpMfUawwSKn/5OYMKHOLbDy\nNExlH5ScoT4SFyotM9Vo63alhMXgnpiKDxHpbddP058JqUiwZ6w9kb9wB3QEQ6xm\nP+6LmtrwwVaGi+GETbq32wOVG/CojiGU6ZM1s46AZou4YdfsJ7XMa+4gbfJIe+on\ngNaASk0Bz0suI8V4klEZh7HpJS7RyyePtW43ogP+gQKBgQDrt2b/Xf5yzeEJRLHm\nBS+CPX9OmvoH0U8W3bNOID0IMKdtHFfO00Wmhlc7OE5fSsf+LobIAWexEIlAeRXM\nWSx1iZ0TjMntuYjBkTkcVU8WX6aT4SDN6+FHhSYSd3H8tY2tQT1zLecBWxVjuR3W\nEnYbcMwG1Z/nU5Xw+EuebUMqgQKBgQDY72byh6X+fTVauXglhgx+ge57Dw49Gr/D\nx5zNU1D6AEn4f0/d7ZZGNjkcJUC6Eqv7CXhOmgP8jOfB7A5frWQf2lfOOSTlb7vC\nXsSg7CKq76+QAfMf98bDAogd9GEIoYk1J+0kw9MMzD5Ysl4On06jL3n8PcK0cnzx\nMwp7AEbqOwKBgQCUxgkIHLdAlpj2VJlD6Pn3ZgE4B7DPxlf4wq0tHkPnK25A+6ag\nL9DCLgBYrE0q7/QShiMjkV907k7ylnofpBjfhp/RewboODYMljBJpb5pDK4CoBEo\nZzyk+3DwLtuO+LgXJho23D31KRvy+R/PwY8x+puLpMFsK+FzWgPAVo4SAQKBgFvQ\nDtkMsiNgKKmqH4B6GGWeZils+NDBtnGM1P9NiNMWNjhW4Z2CxXwXzNntplRaPLF1\nk5ZottE3bYr0dizmPJ8CkPD13HjCbkvYQg39grqn0Lz5JkXcXyH/u046NKsret+l\nc0eBHZyoAKcXbplvsR99o3ovRW2LmveWa5QdTOYrAoGACyP9fjWFRKoru6gHQ1Mp\nvhi7fQtKWv0YPwMi5Kv1LsaeicpffM8zg8/DkN1KFYoxJS/f8vg99/Ozc1Sf/RHE\nUzTGQKyNEcqraBCD546z25l0mptqfV/0SeM8AxqJKnzQDxwQM7Zj6U+laLQ8qPIz\nUphfE7viGbPxDeLHxMNp5Cs=\n-----END PRIVATE KEY-----\n",
  "client_email": "560613061323-compute@developer.gserviceaccount.com",
  "client_id": "116938114835156968651",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/560613061323-compute%40developer.gserviceaccount.com"
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('artists_names') ### Nome do seu bucket
  blob = bucket.blob('storage.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
