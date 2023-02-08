import streamlit as st
import json
import requests
import os
from PIL import Image

st.title("求职生成器")

st.sidebar.title("输入")

name = st.sidebar.text_input('求职者姓名')
title = st.sidebar.text_input('工作名称')
description = st.sidebar.text_area('工作描述')

length = st.sidebar.slider('Summary Length', min_value = 1, max_value = 10, value = 5, step = 1)
tone = st.sidebar.selectbox('Tone', ('Positive', 'Neutral', 'Negative'))

if st.sidebar.button('生成', key = 'generate'):
    inputs = {
        'prompt': 'Dear {0},\nI am applying for the position of {1}.\n{2}'.format(name, title, description),
        'length': length,
        'temperature': 0.5,
        'top_p': 0.9
    }

    headers = {
      'Content-Type': 'application/json',
    }
    response = requests.post('https://api.openai.com/v1/engines/davinci/completions',
                            data=json.dumps(inputs),
                            headers=headers,
                            auth=(os.environ['OPENAI_SECRET_KEY'], ''))

    # Use the positive, neutral, or negative tone
    if tone == '积极':
        response_json = response.json()
        complete_text = response_json['choices'][0]['text']
    elif tone == '中立':
        response_json = response.json()
        complete_text = response_json['choices'][1]['text']
    elif tone == '消极':
        response_json = response.json()
        complete_text = response_json['choices'][2]['text']


    st.write(complete_text)

# Save the generated job application
if st.button('保存'):
    img = Image.open('/path/to/file.png')
    img.save(complete_text)