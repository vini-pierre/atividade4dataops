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
  "project_id": "e-cycling-382122",
  "private_key_id": "5f3814d9dd7ea3ed40c1d6e992989056cf851e66",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC4+yxwnTZojHnF\n8ydxf/Deuu3VIv+woL1yKIEWvZGEvg9xRRxRjbEhclRYXB9Zj8ta1zyEhrCJU0tt\nSitRdDgpbpmlyi3yhcsdDiDs8uN7ZBeTZVRUmBTh8YSultsb9U13bcuNu8/CkkDi\nWOoY7vh9hv9MPnt0/0pIVefduiZYju3QEZXUZRC+9wNf60XvkDjyRZdLiIEXmuh6\nJPdR66sXQDKCPEW2kWpSg2U8pmLS4rpAe3AoTK8sAPTUgpBQwBnfzD5fZA5lktFq\nx41apSW4n7RyENzGApreaw6NVqlBXj1ITo2ZVh0QX++omwqVMYWX0kZ3G2dDDKKy\nE2R8PXctAgMBAAECggEAASUQIBf0+tN9uxoiC8YwgdcIeu8cbnsm2P1DrpXt6oij\nlKj1FSh06MGp9cxc0aN9wm+Tu2KQVp/k7Fr5vCdljpTAOiyvY/FshvRBWL4NvC6B\nJS4gG2WVNtXADgrhyxaVoWV/ouj/OZNz99f4MOnPsLUvFh7KiaLn0ofyPKbMLx7x\nSLnwmoouq7OFGJSrgMJ4+Sm0ldf74rMVybCtRK82zEaoZnvwT2Y/HNXzQXpv3P/X\ny5TonioyVmn9rbRckuhqPAiOnJyFkv3TlR7zKHZZQAArP2KvxCtdPA0fnjU6nsvh\nhG9aQuupMQqmBrPCgSyjk/pPgzjErUQNfAwx1y724QKBgQDvItNUpUVLMqnRWWti\nQSdRDxdlggZPeVpjlkvp7v7rAQdpyVieV6olQSzk/s6C/QTUkN/igjy1Awypucdt\niPaPbkbEUMyu26Mezq6fcBxQqjrLWCw+ZYLKaTWykUn2oCIsN7G2VBhAyQBDrapI\ngwFN1be0kqc4waDKqBMYfICnoQKBgQDGBq2b7jGuKY7PLkEjbFxYaqsQ4baLBq4J\n2D7pE00Ek8BTcRZ9PFzSPpYJGNl/70y/fnTfSeuuqbhTFNCGme2IsAkX5+Y1FTqa\n0MgDfBJ0lE9mCtawdO46VzYYFI1bxcpOnexnloD1c4AHs8BJ+ebyGIq3o16FsYKD\njdv4BcB0DQKBgQChr2NBzQjgAh5NnO79HN5PcSu5h0NrArr5sIodXmlfTW/Mt8VC\nMjWpQLrxDdNlP1u/uUCW7sXLAYfTTfgn+D301nPkklkCNSDCWK46wNt0MtTT3gb0\nHUBkSOR0msVuifDxAqsWgx9u1jhmigojQuhjzweJgMqtlkV4IFHg8XUvYQKBgAzB\nD1t0qvR5rr3/T6i1aPk03ZG3x+cKZhkyOVMPsC00SvXU2cr1IVFVQJqTZCbORdYr\nkeFzxF86hSmstIWG0nq0Q9GrWPNgS6b+/XLkAdhKWRbMaelxjoppZY2FfVlE0vPf\nTgOZ+PJWHw/f7umU0+AR3pVXS1Y3CZ3pfBpsXGndAoGBAOs5c9yatw4dyCMlHJRs\nPVAEzL2MTWk7K2a+6rLTxSmvtfsq+p8ZIXpiK3u1n9XLOZwFRqpK/TxQWPKOCFGz\nOsuUzr0V0NvbF7rjHmWB/SB95icRty6mK+o2OXvI8BvYvcJqq6pQOiRLrGh7iYr5\n6yZv3j9+K/uOTZ7IL7Xn0RNW\n-----END PRIVATE KEY-----\n",
  "client_email": "975177100251-compute@developer.gserviceaccount.com",
  "client_id": "117044790078051334110",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/975177100251-compute%40developer.gserviceaccount.com"
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('artists_names') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

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
