import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set_theme(style='dark')


#Create Monthly Rentals DataFrame

def create_monthly_rentals_df(df):
    monthly_rentals_df = df.groupby(by=['yr','mnth']).agg({
    "cnt":"sum"
    })
    monthly_rentals_df = monthly_rentals_df.reset_index()
    monthly_rentals_df.rename(columns={
    'yr' : 'year',
    'mnth' : 'month',
    'cnt' : 'total'
    }, inplace = True)

    return monthly_rentals_df

#Create Holidays DataFrame

def create_holidays_df(df):
    holidays_df = df.loc[df['yr']==1]
    holidays = ['2012-01-01', '2012-10-31', '2012-12-25']
    holidays = pd.to_datetime(holidays)
    holidays_df = holidays_df[df['dteday'].isin(holidays)]
    holidays_map = {
    pd.Timestamp('2012-01-01'): 'Tahun Baru',
    pd.Timestamp('2012-10-31'): 'Halloween',
    pd.Timestamp('2012-12-25'): 'Natal'
} 
    holidays_df['dteday'] = holidays_df['dteday'].apply(lambda x: holidays_map.get(pd.Timestamp(x), x))

    return holidays_df

#Create Time Of Day DataFrame

def create_time_of_day_df(df_hour):
    df_hour['time_of_day'] = ''
    df_hour.loc[(df_hour['hr'] >= 4) & (df_hour['hr'] < 11), 'time_of_day'] = 'Pagi'
    df_hour.loc[(df_hour['hr'] >= 11) & (df_hour['hr'] < 17), 'time_of_day'] = 'Siang-Sore'
    df_hour.loc[(df_hour['hr'] >= 17) | (df_hour['hr'] < 4), 'time_of_day'] = 'Malam'
    time_of_day_df = df_hour.copy()
    return time_of_day_df

#Load berkas data
df = pd.read_csv("bike_day.csv")
df_hour = pd.read_csv("bike_hour.csv")

#Mengurutkan df berdasarkan date
datetime_columns = ["dteday"]
df.sort_values(by="dteday", inplace=True)
df.reset_index(inplace=True)
 
for column in datetime_columns:
    df[column] = pd.to_datetime(df[column])


monthly_rentals_df = create_monthly_rentals_df(df)
holidays_df = create_holidays_df(df)
time_of_day_df = create_time_of_day_df(df_hour)

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")


st.header('Dicoding Bike Rentals \U0001F6B2')
tab1, tab2, tab3 = st.tabs(["Rentals per Month", "Rentals on Holidays", "Time of Day"])

with tab1:
    st.subheader("Rentals per Month")

    plt.figure(figsize=(10, 6))
    monthly_rentals_df = monthly_rentals_df.reset_index()
    months_map = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun',
        7: 'Jul', 8: 'Agu', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'
    }

    years_map = {
        0: '2011', 1: '2012'}

    monthly_rentals_df['month'] = monthly_rentals_df['month'].map(months_map)
    monthly_rentals_df['year'] = monthly_rentals_df['year'].map(years_map)

    plt.plot(monthly_rentals_df['month'] + ' ' + monthly_rentals_df['year'].astype(str), monthly_rentals_df['total'], marker='o', linestyle='-')
    plt.title('Monthly Bike Rents 2011-2012')
    plt.xlabel('Bulan')
    plt.xticks(rotation=45)
    plt.ylabel('Jumlah Sewa Sepeda')
    plt.grid(True)

    st.pyplot(plt)

with tab2:
    st.subheader("Bike Rentals on Holidays")

    fig, ax = plt.subplots()

    ax.pie(holidays_df['cnt'], labels = holidays_df['dteday'], autopct='%1.1f%%', startangle=140)
    ax.set_title('')
    ax.axis('equal')

    st.pyplot(fig)

with tab3:
    st.subheader("Time of Days")

    fig, ax = plt.subplots()
    sns.countplot(data=time_of_day_df, x='time_of_day', ax=ax)
    plt.title('')
    plt.xlabel('Time')
    plt.ylabel('Frequency')

    st.pyplot(fig)