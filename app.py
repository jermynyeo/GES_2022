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
    query_df = try_school_uni_mean_yoy_basic_income_df[try_school_uni_mean_yoy_basic_income_df.school.str.contains(f'{search_text.lower()}')]
    if (query_df.shape[0] == 0): 
        "No Records."
    else: 
        # groupby degree and year
        query_deg_df = query_df.groupby(["degree", "year"]).mean().reset_index()
        # df for animated chart
        query_deg_df['key']=query_deg_df.groupby(['year','degree']).cumcount()
        query_deg_df_frame = pd.pivot_table(query_deg_df,index='year',columns=['key','degree'],values='basic_monthly_mean')
        query_deg_df_frame = query_deg_df_frame.stack(level=[0,1],dropna=False).to_frame('basic_monthly_mean').reset_index()
        query_deg_df_frame = query_deg_df_frame[query_deg_df_frame.key.eq(0) | query_deg_df_frame['basic_monthly_mean'].notna()]
        query_deg_df_frame = query_deg_df_frame.fillna(0)
        
        # groupby uni and year
        query_uni_df = query_df.groupby(["university", "year"]).mean().reset_index()
        # df for animated chart
        query_uni_df['key']=query_uni_df.groupby(['year','university']).cumcount()
        query_uni_df_frame = pd.pivot_table(query_uni_df,index='year',columns=['key','university'],values='basic_monthly_mean')
        query_uni_df_frame = query_uni_df_frame.stack(level=[0,1],dropna=False).to_frame('basic_monthly_mean').reset_index()
        query_uni_df_frame = query_uni_df_frame[query_uni_df_frame.key.eq(0) | query_uni_df_frame['basic_monthly_mean'].notna()]
        query_uni_df_frame = query_uni_df_frame.fillna(0)

        fig1 = px.bar(query_deg_df_frame, x="degree",
                    y="basic_monthly_mean",
                    color='degree',
                    barmode='group',
                    width=2000,
                    height=800,
                    title="Year-on-Year Change in Mean Basic Monthly According to Singapore Universities (2013 to 2020)",
                    labels={"degree": "Degree"},
                    animation_frame="year",
                    animation_group="degree"
                    )

        fig1.update_layout(
            legend=dict(
                x=0,
                y=1,
                traceorder="reversed",
                title_font_family="Times New Roman",
                font=dict(
                    family="Courier",
                    size=12,
                    color="black"
                ),
                bgcolor="rgba(0,0,0,0)",
                bordercolor="Black",
                borderwidth=2
            )
        )


        fig1.update_traces(
            cliponaxis=True
        )
                
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.bar(query_uni_df_frame, x="university", 
                    y="basic_monthly_mean",
                    color='university', 
                    barmode='group', 
                    width = 2000,
                    height=800, 
                    title="Year-on-Year Change in Mean Basic Monthly According to Singapore Universities (2013 to 2020)",
                    labels={"university": "University"},
                    animation_frame="year",
                    animation_group="university",
                    range_y=[0,  query_uni_df.basic_monthly_mean.max() + 1500]
                    )

        fig2.update_layout(
            legend=dict(
                x=0,
                y=1,
                traceorder="reversed",
                title_font_family="Times New Roman",
                font=dict(
                    family="Courier",
                    size=12,
                    color="black"
                ),
                bgcolor="rgba(0,0,0,0)",
                bordercolor="Black",
                borderwidth=2
            ),
            transition = {'duration': 2000}
        )

                    
        st.plotly_chart(fig2, use_container_width=True)

    
        # update to employment rate? 
        # fig3 = 

        # fig3.update_layout(
        #     legend=dict(
        #         x=0,
        #         y=1,
        #         traceorder="reversed",
        #         title_font_family="Times New Roman",
        #         font=dict(
        #             family="Courier",
        #             size=12,
        #             color="black"
                # ),
                # bgcolor="rgba(0,0,0,0)",
        #         bordercolor="Black",
        #         borderwidth=2
        #     )
        # )
        
        # st.plotly_chart(fig3, use_container_width=True)

