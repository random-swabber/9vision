import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import json
from datetime import datetime
from PIL import Image
from os import listdir
from os import path


st.set_page_config(page_title="9vision", page_icon='👁',menu_items={"About":'*bandev2022*'})

# Selecting user
users = [dir for dir in listdir('./data/') if path.isdir('./data/' + dir)]

with st.sidebar:
    user = st.selectbox('Select or type user name',(users))


# loading data
df = pd.read_csv(f'./data/{user}/{user}_posts.csv')
df_sections = df.groupby('section').count()[['link']].rename(columns={'link':'count'})

with open(f'./data/{user}/{user}_meta.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
scrap_date = datetime.strptime(data['scrap_date'], '%d-%m-%Y')
nb_posts = df.shape[0]

df_comments = pd.read_csv(f'./data/{user}/{user}_reactions.csv')
df_comments_sections = df_comments.groupby('section').count()[['link']].rename(columns={'link':'count'})
nb_comments = df_comments.shape[0]
activity_ratio = round(nb_posts / (nb_posts + nb_comments),2)

# MAIN TITLE
st.markdown('<H1 style="color:gold;text-align:center;" >[ 9 \\/ | 5 | 0 |\\| ]</H1><br><br><br>', unsafe_allow_html=True)



# META USER
st.markdown(f'<h2>{data["alias"]}</h2>', unsafe_allow_html=True)

user_col1, user_col2, user_col3, user_col4 = st.columns([1.5,2,2,1])
with user_col1:
    st.markdown(f'<img src="{data["avatar_link"]}">', unsafe_allow_html=True)

with user_col2:
    st.markdown(f'<br>@{user}<br>{data["nb_days"]} days<br>\
    last update {datetime.strftime(scrap_date, "%d %b %y")}',
    unsafe_allow_html=True)

with user_col3:
    st.markdown(f'<br>{nb_posts} posts<br>\
    {nb_comments} comments<br>\
    Activity ratio <meter id="disk_c" value="{int(activity_ratio * 100)}" min="0" low="34" high="60" optimum = "100" max="100"></meter><br>',
    unsafe_allow_html=True)
    


# FAVORIT SECTIONS
st.markdown('<br><h2>Favorit posting sections</h2>', unsafe_allow_html=True)
st.write('Scroll on chart to zoom | Click and drag to pan | Hover column for details.')
st.bar_chart(df_sections)


# REACTIONS of COMMUNITY
st.markdown('<h2>9gaggers reactions</h2>', unsafe_allow_html=True)

# selection by category
sections_list = ['- All -'] + list(df_sections.index) 
selected_section = st.selectbox('Select a category',(sections_list))

# filter dataframe according to selection
if selected_section == '- All -':
    df_base = df
else:
    df_base = df[df['section'] == selected_section]
    
# compute all metrics and store into df_reactions dataframe
df_reactions = pd.DataFrame()
metrics=['min', 'mean', 'max', 'sum']
for metric in metrics:
    df_reactions[metric] = df_base[['nb_up','nb_down','nb_comments']].apply(metric)

# load nice icons
speech_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chat-left-fill" viewBox="0 0 16 16"><path d="M2 0a2 2 0 0 0-2 2v12.793a.5.5 0 0 0 .854.353l2.853-2.853A1 1 0 0 1 4.414 12H14a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/></svg>'
metric_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-speedometer2" viewBox="0 0 16 16"><path d="M8 4a.5.5 0 0 1 .5.5V6a.5.5 0 0 1-1 0V4.5A.5.5 0 0 1 8 4zM3.732 5.732a.5.5 0 0 1 .707 0l.915.914a.5.5 0 1 1-.708.708l-.914-.915a.5.5 0 0 1 0-.707zM2 10a.5.5 0 0 1 .5-.5h1.586a.5.5 0 0 1 0 1H2.5A.5.5 0 0 1 2 10zm9.5 0a.5.5 0 0 1 .5-.5h1.5a.5.5 0 0 1 0 1H12a.5.5 0 0 1-.5-.5zm.754-4.246a.389.389 0 0 0-.527-.02L7.547 9.31a.91.91 0 1 0 1.302 1.258l3.434-4.297a.389.389 0 0 0-.029-.518z"/><path fill-rule="evenodd" d="M0 10a8 8 0 1 1 15.547 2.661c-.442 1.253-1.845 1.602-2.932 1.25C11.309 13.488 9.475 13 8 13c-1.474 0-3.31.488-4.615.911-1.087.352-2.49.003-2.932-1.25A7.988 7.988 0 0 1 0 10zm8-7a7 7 0 0 0-6.603 9.329c.203.575.923.876 1.68.63C4.397 12.533 6.358 12 8 12s3.604.532 4.923.96c.757.245 1.477-.056 1.68-.631A7 7 0 0 0 8 3z"/></svg>'

# display metrics on 4 columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<h3>Metrics '+metric_icon+'</h3>', unsafe_allow_html=True)
    st.markdown('Min<br>Average<br>Max<br>Total', unsafe_allow_html=True)
    
with col2:
    st.markdown('<h3>Upvotes &#x1F845</h3>', unsafe_allow_html=True)
    st.markdown('<br>'.join(df_reactions.iloc[0].astype('int64').astype('str').to_list()), unsafe_allow_html=True)

with col3:
    st.markdown('<h3>Downvotes 🡇</h3>', unsafe_allow_html=True)
    st.markdown('<br>'.join(df_reactions.iloc[1].astype('int64').astype('str').to_list()), unsafe_allow_html=True)
    
with col4:
    st.markdown('<h3>Comments '+speech_icon+'</h3>', unsafe_allow_html=True)
    st.markdown('<br>'.join(df_reactions.iloc[2].astype('int64').astype('str').to_list()), unsafe_allow_html=True)



# TITLES WORD CLOUD
st.markdown('<br><h2>Post titles word cloud</h2>', unsafe_allow_html=True)
word_cloud = Image.open(f'./data/{user}/{user}_wcloud.png')
st.image(word_cloud)



# REACTIONS to COMMUNITY
st.markdown('<br><hr><br><h2>Community posts commented</h2>', unsafe_allow_html=True)
st.bar_chart(df_comments_sections)
