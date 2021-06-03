
import streamlit as st
import logging
import os
import re
import requests
from functools import wraps
from collections import Counter
from html import unescape
import streamlit.components.v1 as components
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)
kw_list = ['chelsea manchester']
exec_times_counter = []
exec_times_dico = []

st.title("App.py web page")
st.title("Digital Traces TP3")
df = pytrends.get_historical_interest(kw_list, year_start=2021, month_start=1, day_start=1, hour_start=0, year_end=2021, month_end=3, day_end=30, hour_end=0, cat=0, geo='', gprop='', sleep=0)
st.text(df)
st.text("Research of 'chelsea vs manchester' on google on 90 days")
st.line_chart(df)

def timer(fn):
    from time import perf_counter
    def inner(*args, **kwargs):
        start_time = perf_counter()
        to_execute = fn(*args, **kwargs)
        end_time = perf_counter()
        execution_time = end_time - start_time
        if(fn.__name__ == "counting_words_counter"):
            exec_times_counter.append(execution_time)
        if(fn.__name__ == "counting_words_dictionnary"):
            exec_times_dico.append(execution_time)
        print("{0} took {1:.8f}s to execute".format(fn.__name__, execution_time))
        return to_execute
    
    return inner
    
@timer
def counting_words_dictionnary(filename):
    file = open(filename)
    str = file.read().replace("\n", " ")
    counts = dict()
    words = str.split()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

def readFile(filename):
    with open(filename, "r") as data:
        text = data.read()
    return re.findall('[a-z]+', text)

@timer
def counting_words_counter(filename):
    res = readFile(filename)
    return Counter(res)
        

st.markdown("*Number of appearance for each words in shakespeare artwork file (using dictionnary):*")
st.text(counting_words_dictionnary("sa.txt"))
st.markdown("*Number of appearance for each words in shakespeare artwork file (using counter):*")
st.text(counting_words_counter("sa.txt"))

for i in range(100):
    counting_words_dictionnary("sa.txt")
    counting_words_counter("sa.txt")

st.markdown("**Chart showing execution times for 100 occurences of the function counting words with dictionnary**")
st.line_chart(exec_times_dico)
st.markdown("**Chart showing execution times for 100 occurences of the function counting words with counter**")
st.line_chart(exec_times_counter)


code = """<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-197402995-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'UA-197402995-1');
</script>"""

a=os.path.dirname(st.__file__) + '/static/index.html'
with open(a, 'r') as f:
    data=f.read()
    if len(re.findall('UA-', data)) == 0:
        with open(a, 'w') as f:
            newdata=re.sub('<head>','<head>' + code, data)
            f.write(newdata)

title=st.text_input('Movie title',value='Life of Olive')
st.write('The current movie title is',title)
logging.warning('Watch out man')
logging.info('I told you so')
req=request.get("https://www.google.com/")
st.markdown(req.cookies_cookies)
components.html(unescape(req.text))


