import streamlit as st
import requests
import pandas as pd

access_key = "m9CxMc54nNM3WKgINkoQRuVkKIOwwgvSWmLhJDi1dp0"
url = "https://api.unsplash.com//search/photos"

word = st.text_input('what')

if st.button('get'):
  parameters = {'client_id':access_key, 'query':word}
  res = requests.get(url, params=parameters)
  st.image(res.json()['results'][0]['urls']['small'])
  
  

