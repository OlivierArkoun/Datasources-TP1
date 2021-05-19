import streamlit as st
st.title("Hello world")
import os

import re

code = """<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-5RCBDK28T7"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-5RCBDK28T7');
</script>"""

a=os.path.dirname(st.__file__) + '/static/index.html'
with open(a, 'r') as f:
    data=f.read()
    if len(re.findall('G-', data)) == 0:
        with open(a, 'w') as f:
            newdata=re.sub('<head>','<head>' + code, data)
            f.write(newdata)
