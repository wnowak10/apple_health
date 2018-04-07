import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set_style("darkgrid")

# read
health = pd.read_csv('health_data.csv')

# need to change the hour delta depending on the timezone I'm in when I export
# wrote this script in San Fran, which is UTC -7
health.endDate = pd.to_datetime(health.endDate)
health.endDate = health.endDate - pd.Timedelta(hours=4)

health.startDate = pd.to_datetime(health.startDate)
health.startDate = health.startDate - pd.Timedelta(hours=4)

health['segment_raw_time'] = health.endDate - health.startDate
health['segment_time_hours'] = health['segment_raw_time'].dt.seconds / 3600.
health['speed_mph'] = health.milage / health.segment_time_hours
health['activity'] = np.where(health['speed_mph'] >10, 'Cycling', np.where(health['speed_mph'] > 5, 'Running', 'Walking'))

print(health.tail())
print(health.speed_mph.max())
print(health.activity.value_counts())

walking = health.loc[health['activity'] == 'Walking',]
print(walking.head())

# Problem with this is that all times interpreted the same, so most of the times should
# be in UTC - 4 = United States EST

# group by days
days = walking.groupby(walking.startDate.dt.date)['startDate','milage'].sum().reset_index()
# plt.plot(days.startDate, days.milage)

# https://stackoverflow.com/questions/11352047/finding-moving-average-from-data-points-in-python
def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

# # MA plot
plt.plot(days.startDate, movingaverage(days.milage, 200))
hm = '2017-06-24'
plt.axvline(x=hm)
plt.text(hm,2.5,'Honeymoon Begins',rotation=10, color='red')

nyc = '2017-08-15'
plt.axvline(x=nyc)
plt.text(nyc,3.5,'Move to NYC',rotation=10, color='red')

germany = '2016-06-4'
plt.axvline(x=germany)
plt.text(germany,3.5,'Choate trip to Europe',rotation=10, color='red')

sb2017 = '2017-02-04'
plt.axvline(x=sb2017)
sb2017_end = '2017-03-20'
plt.axvline(x=sb2017_end)
plt.text(sb2017,7.5,'Spring Break',rotation=10, color='red')


unclear = '2017-04-15'
also_unclear = '2016-10-15'

plt.axvline(x=unclear)
plt.text(unclear,7.5,'Unclear?',rotation=10, color='red')
plt.axvline(x= also_unclear)
plt.text(also_unclear,7.5,'Also Unclear?',rotation=10, color='red')

plt.xticks(rotation=20)
plt.show()


# group by weeks
# year = health.startDate.dt.year
# months = health.startDate.dt.month
# months = health.groupby([year, months], as_index = False)['startDate','milage'].sum().reset_index()
# # weeks.columns = weeks.columns.droplevel(0)
# print(months)
# plt.plot(months.index, months.milage)
# plt.show()
