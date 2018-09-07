import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import datetime as dt
import matplotlib as inline

#2
df = pd.read_csv('My Uber Drives - 2016.csv')

'''
the csv file and placing it into a pandas data frame lets look at the columns and their associated data types.
Noticed from the below there are variables that contains null values.
'''
#3
print("---------------------------------------------------------------------------------")
df.info()
print("---------------------------------------------------------------------------------")

'''
Here is a snapshot of the first 5 rows of the data. This gives us an idea of the data elements within the variables. We can see there is a Category, Purpose, Miles and other.
We will be utlizing primarly the purpose and miles to draw conclusion on the purpose of trips and miles travelled.
'''

#4
print("---------------------------------------------------------------------------------")
print (df.head())
print("---------------------------------------------------------------------------------")

#5
print("---------------------------------------------------------------------------------")
print (df.tail())
print("---------------------------------------------------------------------------------")

#data cleaning
#6
df1 = df.drop(df.index[1155])

#7
df1['PICK_DATE'] = df['START_DATE*'].str.split(' ').str[0]

#8
df1['DROP_DATE'] = df['END_DATE*'].str.split(' ').str[0]

#9
test = [df1]
for dataset in test: 
    dataset['START_DATE*'] = pd.to_datetime(dataset['START_DATE*']).astype('datetime64[ns]')
    dataset['END_DATE*'] = pd.to_datetime(dataset['END_DATE*']).astype('datetime64[ns]')

#10
df1['CITY_PAIR'] = df1['START*']+'-'+ df1['STOP*']

#11
df1['TOTAL_TIME'] = df1['END_DATE*']-df1['START_DATE*']

#12
print("---------------------------------------------------------------------------------")
df1.info()
print("---------------------------------------------------------------------------------")
#13
print("---------------------------------------------------------------------------------")
print (df1.isnull().sum())
print("---------------------------------------------------------------------------------")

#14
df1['PURPOSE*'] = df1['PURPOSE*'].fillna('OTHER')

#15
print("---------------------------------------------------------------------------------")
print(df1.groupby('PURPOSE*', as_index=False).sum())
print("---------------------------------------------------------------------------------")

#16
print("---------------------------------------------------------------------------------")
print(df1.isnull().sum())
print("---------------------------------------------------------------------------------")

#17
print("---------------------------------------------------------------------------------")
data = [df1]

for dataset in data:
    dataset['CATEGORY*'][df1['PURPOSE*']=='Meal/Entertain'] = 'Meals'
print("---------------------------------------------------------------------------------")

#181111111111111111111111111
print("---------------------------------------------------------------------------------")
print(df1.describe())
print("---------------------------------------------------------------------------------")

#19
print("---------------------------------------------------------------------------------")
print(df1.describe(include=['O']))
print("---------------------------------------------------------------------------------")

#20
print("---------------------------------------------------------------------------------")
print(df1.head())
print("---------------------------------------------------------------------------------")

#21

df1['START'] = pd.to_datetime(df1['START_DATE*'], errors='coerce')

df1['weekday'] = df1['START'].dt.weekday_name


#Data Visualization
'''
The below boxplot shows by purpose and miles driven.
As you can see from the boxplot the outliers in this case there are several.
The one that catches my attention is the customer visit with a total miles driven of 300 miles.
This represet a trip picked up from city Latta to city Jacksonville with aproximate travel time of 5 hours and 30 minutes.
'''
#22 Figure 1 Box Plot
oth = ['OTHER']

g = sns.FacetGrid(data=df1[~df1['PURPOSE*'].isin(oth)], aspect=2, size=6)
g.map(sns.boxplot, 'PURPOSE*', 'MILES*', palette="Set1")
plt.show()

'''
The below Distriubtion plot shows the miles disributed by trips.
It shows that between 0-25 there are a total of 1100 trips.
'''
#23 Figure 2 Histogram
plt.figure(figsize=(18,8))
plt.hist(df1['MILES*'])
plt.xlabel('Miles')
plt.ylabel('Drives')
plt.show()



'''
This pie chart represents the percentage of trips made using the PURPOSE* variables.
I have exploded the piece of the pie chart with the highest percentage.
In this case are those trips that did not have a value assigned.
Hence earlier I used a fillna() function to this missing values and replace those values with NA.
'''
#24 Figure 3 PieChart
plt.figure(figsize=(10,10))
df1['PURPOSE*'].value_counts()[:11].plot(kind='pie',autopct='%1.1f%%',shadow=True,explode=[0.1,0,0,0,0,0,0,0,0,0,0])
plt.show()



#25 Figure 4 BarPlot
g = sns.FacetGrid(data=df1, aspect=2, size=8)
g.map(sns.countplot, 'PURPOSE*', palette="Set1")
plt.ylabel('Miles')
plt.show()


#26 Figure 5 Scatter plot
x = np.arange(0, 1155)
y = df1['MILES*']

plt.figure(figsize=(18,8))

plt.scatter(x, y, s=15)
plt.xticks([0, 400, 800, 1200])
plt.xlabel('Miles')
plt.ylabel('Drives')
plt.show()

#27 Figure 6 FacetGrid Plot
g = sns.FacetGrid(data=df1, aspect=2, size=8, hue='PURPOSE*')
g.map(plt.plot, 'START_DATE*')
plt.legend()
plt.xlabel('# of Trips')
plt.ylabel('Time')
plt.show()

#28 Figure 7 BarPlot
plt.figure(figsize=(18,8))
df1['CITY_PAIR'].value_counts()[:50].plot(kind='bar')
plt.ylabel('Miles')
plt.show()

#29 Figure 8 FacetGrid
g = sns.FacetGrid(data=df1, aspect=2, size=8, hue='CATEGORY*')
g.map(plt.plot, 'TOTAL_TIME')
plt.show()

'''
In conclusion, the data shows that there are trips that are outside of the normal average miles travel by an UBER drive.
For example out of the total 1150 observations in the data which equal to trips made,
what the data does not shows is how many drivers are in the total observation.
THerefore I could not draw a concrete conclusion per driver. THe data shows cities that are overseas.
'''
#30
totals = df1.groupby('CATEGORY*', as_index=False).agg({'MILES*': 'sum'})

#31
totals['PERCENTAGE'] = (totals['MILES*']/df1['MILES*'].sum())*100

#32
print("---------------------------------------------------------------------------------")
print(totals
      )
print("---------------------------------------------------------------------------------")

#33 Figure 9 PieChart
sizes = np.array(totals['PERCENTAGE'])
labels = np.array(totals['CATEGORY*'])


fig1, ax1 = plt.subplots(figsize=(9,9))
ax1.pie(sizes, explode=[0.2,0,0], labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('PERCENTAGE OF MILES BY CATEGORY')

plt.show()

#34 Figure 10 Bar plot
cat = df1.groupby('CATEGORY*', as_index=False).mean()

plt.figure(figsize=(18,8))

sns.barplot('CATEGORY*', 'MILES*', data=cat)
plt.title('AVERAGE MILES DRIVEN PER PURPOSE')
plt.show()

#35 Figure 11
plt.figure(figsize=(7,7))
df1['weekday'].value_counts().plot(kind='bar')
plt.ylabel('Times')
plt.xlabel('Days')
plt.show()

