from itertools import count
import streamlit as st
import pandas as pd
# from core import analysis_by_country, get_dataframe, get_totals, get_new, populate_diary_evolution, populate_metrics, add_date_picker
from utils import format_date
import datetime
import pandas as pd
import plotly.express as px

df = pd.read_excel('DF_Merged.xlsx')

years = df.year.sort_values().unique()
current_year = datetime.datetime.today().year

st.set_page_config(
    page_title='Evolução populacional',
    page_icon='📈',
    layout='wide'
)
hide_menu_style = '''<style>
        #MainMenu {visibility: hidden;}
        </style>'''

st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title(f'Evolução populacional')

st.header('Consolidado Mundial')

selected_year = st.select_slider('Selecione o ano:', options=years, value=current_year)

head_population, head_motality, head_life_expectancy = st.columns(3)

st.markdown("""---""")

population_cur_year = df[df.year == selected_year].midyear_population.sum()

infant_mortality = df[df.year == selected_year].infant_mortality.sum()

life_expectancy = df[df.year == selected_year].life_expectancy.mean()

head_population.metric(f"População total ou prevista {selected_year}:", f'{int(population_cur_year):,d}'.replace(',','.'), '')

head_motality.metric(f"Mortalidade total ou prevista {selected_year}:", f'{int(infant_mortality):,d}'.replace(',','.'), '')

head_life_expectancy.metric(f"Expectativa de vida média ou prevista {selected_year}:", f'{int(life_expectancy):,d}'.replace(',','.'), '')


st.markdown("""---""")
st.header('Evolução anual')

countries = ['Todos']

countries.extend(df.country_name.unique())

country = st.selectbox('Selecione um ou mais países',  options=countries)

st.header('Evolução de mortes por dia')

df_pop = df.groupby(['country_name', 'year'], as_index=False)['midyear_population'].sum()

df_pop.rename({'country_name':'País', 'midyear_population':'População'}, axis=1, inplace=True)

if country != 'Todos':
    df_pop.set_index('year', inplace=True)
    df_pop = df_pop[df_pop['País'] == country]
else:
    df_pop = df_pop.groupby(['year']).agg({'População':'sum'})


fig = px.line(
        x=df_pop.index,
        y=df_pop['População'],
        title="Evolução anual da população", 
        labels={'x': 'Ano', 'y':'População'}
    )


st.plotly_chart(fig, use_container_width=True)

### SIDEBAR
# st.sidebar.title(f'Evolução populacional')

# st.sidebar.markdown('----')
st.markdown('Dados extraídos de [Google Cloud](https://console.cloud.google.com/marketplace/details/united-states-census-bureau/international-census-data?project=avid-catalyst-342122)')

