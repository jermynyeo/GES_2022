import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('./data/GES.csv')
df = df.drop('Unnamed: 0', 1)
df = df.drop(df[df['basic_monthly_mean'] == 'na'].index)
df["basic_monthly_mean"] = pd.to_numeric(df["basic_monthly_mean"])

# uni_mean_yoy_basic_income_df = df[['university','year','basic_monthly_mean']]
# try_uni_mean_yoy_basic_income_df = uni_mean_yoy_basic_income_df.groupby(['university', 'year']).mean().reset_index()

uni_mean_yoy_basic_income_df = df[['university', 'school', 'degree', 'year','basic_monthly_mean']]
try_school_uni_mean_yoy_basic_income_df = uni_mean_yoy_basic_income_df.groupby(['university', 'school', 'degree', 'year']).mean().sort_values(['basic_monthly_mean'],ascending=False).reset_index()
try_school_uni_mean_yoy_basic_income_df.school = try_school_uni_mean_yoy_basic_income_df.degree.apply(lambda x: x.lower())

# DEG_SEARCH_TERM = "computing"
# query_df = try_school_uni_mean_yoy_basic_income_df[try_school_uni_mean_yoy_basic_income_df.school.str.contains(f'{DEG_SEARCH_TERM}')]

st.title("GES 2013 to 2020")

search_text = st.text_input('Term to search:', '')

if search_text:
    query_df = try_school_uni_mean_yoy_basic_income_df[try_school_uni_mean_yoy_basic_income_df.school.str.contains(f'{search_text}')]

    fig1 = px.bar(query_df, x="year",
                 y="basic_monthly_mean",
                 color='degree',
                 barmode='group',
                 width=2000,
                 height=800,
                 title="Year-on-Year Change in Mean Basic Monthly According to Singapore Universities (2013 to 2020)",
                 labels={"degree": "Degree"}
                 )
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(query_df, x="year",
                 y="basic_monthly_mean",
                 color='university',
                 barmode='group',
                 width=2000,
                 height=800,
                 title="Year-on-Year Change in Mean Basic Monthly According to Singapore Universities (2013 to 2020)",
                 labels={"university": "University"}
                 )
    st.plotly_chart(fig2, use_container_width=True)