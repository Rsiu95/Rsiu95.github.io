import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px
import seaborn as sns
import scipy.stats as stats

df_monthly = pd.read_csv('C:/Users/RSiu9/OneDrive/Documents/GitHub/RoySiu.github.io/Udemy 100 Days of Code/Day 80/monthly_deaths.csv')
df_yearly = pd.read_csv('C:/Users/RSiu9/OneDrive/Documents/GitHub/RoySiu.github.io/Udemy 100 Days of Code/Day 80/annual_deaths_by_clinic.csv')

# check shape of dfs
print(f"Shape of yearly df: {df_yearly.shape}")
print(f"Shape of monthly df: {df_monthly.shape}")

# get column names
print("Monthly DF Column Names\n", df_monthly.info())
print("Yearly DF Column Names\n", df_yearly.info())

# check for NaNs
print(f"NaNs in Monthly DF: {df_monthly.isna().values.any()}")
print(f"NaNs in Yearly DF: {df_yearly.isna().values.any()}")

# check for duplicates
print(f"Duplicates in Monthly DF: {df_monthly.duplicated().values.any()}")
print(f"Duplicates in Yearly DF: {df_yearly.duplicated().values.any()}")

# check averages
print("Monthly DF Info\n", df_monthly.describe())
print("Yearly DF Info\n", df_yearly.describe())

# percentage of women dying in child birth
print("By year\n", df_yearly['deaths']/df_yearly['births'] * 100)
print(f"Chances of dying in the 1840s in Vienna: {df_yearly['deaths'].sum() / df_yearly['births'].sum() * 100:.3}%")

# convert date to datetime format
df_monthly.date = pd.to_datetime(df_monthly.date)

# use mdates to apply locators
years = mdates.YearLocator()
months = mdates. MonthLocator()
years_format = mdates.DateFormatter('%Y') 

# plotting
# plt.figure(figsize=(14,8), dpi=200)
# plt.title('Total Number of Monthly Births and Deaths', fontsize=18)
 
# ax1 = plt.gca()
# ax2 = ax1.twinx()

# ax1.set_xlim([df_monthly.date.min(), df_monthly.date.max()])
# ax1.xaxis.set_major_locator(years)
# ax1.xaxis.set_major_formatter(years_format)
# ax1.xaxis.set_minor_locator(months)
 
# ax1.grid(color='grey', linestyle='--')
 
# ax1.plot(df_monthly['date'], 
#          df_monthly['births'], 
#          color='skyblue', 
#          linewidth=3)
 
# ax2.plot(df_monthly['date'], 
#          df_monthly['deaths'], 
#          color='crimson', 
#          linewidth=2, 
#          linestyle='--')
 
# plt.show()

df_monthly['pct_deaths'] = (df_monthly['deaths'] / df_monthly['births']* 100).round(2)

date = '1846-06-01'
df_before_1846 = df_monthly.query('date < @date')
df_after_1846 = df_monthly.query('date >= @date')
print(df_after_1846)
print(f"Average death rate before 1846: {(df_before_1846.pct_deaths.sum()/len(df_before_1846)).round(3)} %")
print(f"Average death rate after 1846: {(df_after_1846.pct_deaths.sum()/len(df_after_1846)).round(3)} %")

# set the date to the index
monthly_deaths_1846 = df_before_1846.set_index('date')

# create a rolling average of 6
moving_average = monthly_deaths_1846.rolling(window=6).mean()
print(moving_average)
# plotting
plt.figure(figsize=(14,8), dpi=200)
plt.title('Total Number of Monthly Births and Deaths', fontsize=18)
 
ax1 = plt.gca()

ax1.set_xlim([df_monthly.date.min(), df_monthly.date.max()])
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_format)
ax1.xaxis.set_minor_locator(months)
 
ax1.grid(color='grey', linestyle='--')
 
ax1.plot(df_before_1846['date'], 
                df_before_1846['pct_deaths'], 
                color='skyblue', 
                linewidth=3,
                label = 'Before Handwashing')

ax1.plot(moving_average.index, 
         moving_average['pct_deaths'], 
         color='black', 
         linewidth=3,
         linestyle = '--',
         label = "Moving Average")
 
ax1.plot(df_after_1846['date'], 
                df_after_1846['pct_deaths'], 
                color='crimson', 
                linewidth=2, 
                linestyle='--',
                label = 'After Handwashing')

plt.legend(fontsize=18)
 
plt.show()

print(df_before_1846.describe())
print(df_after_1846.describe())

# create a column using np.where
df_monthly['before_handwash'] = np.where(df_monthly.date < date, "Yes", "No")
print(df_monthly)

# Create box plot of before handwashing
box = px.box(df_monthly, 
             x='before_handwash', 
             y='pct_deaths',
             color='before_handwash',
             title='How Have the Stats Changed with Handwashing?')
 
box.update_layout(xaxis_title='Washing Hands?',
                  yaxis_title='Percentage of Monthly Deaths',)
 
box.show()

hist = px.histogram(
    df_monthly,
    x = 'pct_deaths',
    nbins = 30,
    opacity = 0.6,
    barmode = 'overlay',
    marginal = 'box',
    color = 'before_handwash',
    histnorm = 'percent',
)
hist.update_layout(xaxis_title='Proportion of Monthly Deaths',
                   yaxis_title='Count',)

hist.show()

# Use Kernel Density Estimate (KDE) to produce a smoother distribution

sns.kdeplot(df_before_1846.pct_deaths, fill = True, clip=(0,40), label = 'Before Handwashing')
sns.kdeplot(df_after_1846.pct_deaths, fill = True, clip=(0,40), label = 'After Handwashing')
plt.title('Est. Distribution of Monthly Death Rate Before and After Handwashing')
plt.xlim(0, 40)
plt.legend(fontsize=12)
plt.show()

# T-Test to show statistical significance
t_stat, p_value = stats.ttest_ind(a=df_before_1846.pct_deaths, 
                                  b=df_after_1846.pct_deaths)
print(f'p-palue is {p_value:.10f}')
print(f't-statstic is {t_stat:.4}')
