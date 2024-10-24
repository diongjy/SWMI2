import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta
import xarray as xr
#from datetime import datetime

#get the timestamp and prepare to get the file
ct = datetime.datetime.now().date()
print(ct)

def subtract_days_from_date(date, days):
    """ Subtract days from a date and return the date
     Args:
        date(string): Date string in YYYY-MM-DD format
        days (int) : Number of days to subtract from date

    Returns:
        date (date): Date in YYYYY-MM-DD with X days subtracted
    """
    subtracted_date= pd.to_datetime(date) - timedelta(days=days)
    subtracted_date= subtracted_date.strftime("%Y%m%d")

    return subtracted_date

forecast_date = subtract_days_from_date(ct,1)
print('forecast_init_date:',forecast_date)

ds=xr.open_dataset('./home/diong/Desktop/SWMI2/gefs/u850_'+str(forecast_date)+'_gfs_gefs_00z')
ds_daily=ds.resample(time='D').mean()

ds_daily=ds.resample(time='D').mean()

lat_bnd=[5,10]
lon_bnd=[100,115]
u850=ds_daily.u850
swmi=u850.sel(lat=slice(*lat_bnd),lon=slice(*lon_bnd)).mean(dim=['lat','lon'])
df=swmi.to_dataframe()
df=df.reset_index()
df = df.rename(columns={'time': 'Date', 'u850': 'SWMI2'})
#print(df)
df.to_csv('./home/diong/Desktop/SWMI2/test/swmi_'+str(forecast_date)+'.csv',index=False, header=False)

from datetime import datetime
date_object = datetime.strptime(forecast_date, "%Y%m%d")
#date_object1= datetime.strptime(forecast_date, "%d/%m/%Y")
fdate = date_object.strftime("%-d/%-m/%Y")
print(fdate)

df1=pd.read_csv('./home/diong/Desktop/SWMI2/test/swmi1.csv', header=None, parse_dates=True)
header=['Date','SWMI2']
df1.columns=header
df2=pd.read_csv('./home/diong/Desktop/SWMI2/test/swmi_'+str(forecast_date)+'.csv', header=None, parse_dates=True)
df2.columns=header
df2['Date'] = pd.to_datetime(df2['Date'], format='%Y-%m-%d')
#df2['Date'] = df2['Date'].dt.strftime("%#d/%#m/%Y")
df2['Date']= df2['Date'].dt.strftime('%-d/%-m/%Y')
#df2['Date']=df2['Date'].dt.strftime('%d/%m/%Y').str.lstrip('0').replace('/0','/')
#print(df1)
#print(df2)
#merge two df
merged_df = pd.merge(df1, df2, on='Date', suffixes=('_old', '_new'), how='outer')
# Identify conflicting columns (in this case, 'Value')
conflicting_columns = ['SWMI2']

# Update values in the first DataFrame with the latest values from the second DataFrame
for column in conflicting_columns:
    merged_df[column] = merged_df[column + '_new'].combine_first(merged_df[column + '_old'])

# Drop the redundant columns
merged_df.drop(columns=[col + '_old' for col in conflicting_columns] + [col + '_new' for col in conflicting_columns], inplace=True)

# Drop rows with NaN values (if any)
merged_df.dropna(subset=['Date'], inplace=True)
#print(merged_df)

merged_df['5day']=merged_df.SWMI2.rolling(5).mean()
merged_df['5day']=merged_df['5day'].shift(-4)
merged_df['polarity']=np.sign(merged_df['SWMI2'])
merged_df['15day']=merged_df['polarity'].rolling(20).sum()
merged_df['15day']=merged_df['15day'].shift(-19)
merged_df['20day']=merged_df['SWMI2'].rolling(20).mean()
merged_df['20day']=merged_df['20day'].shift(-19)
df_new=merged_df[['Date','SWMI2','5day','15day','20day']].copy()
#print(df_new)

df_new['5day'] = df_new['5day'].fillna(0)
df_new['15day'] = df_new['15day'].fillna(0)
df_new['20day'] = df_new['20day'].fillna(0)

#On the onset day, zonal wind must be westerly and mean over the next 5 days must be westerly.
##In the 20 days window, the wind must be positive for at least 15 days.
#The mean of the zonal wind for 20 days window must exceed +1 m/s
#We first scan for the first westerly wind.

for index, row in df_new.iterrows():
    #print(df_new)
    if row['SWMI2'] > 0.0 :
        if row['5day']>0.0 & row['15day']>=15.0 & row['20day']>1.0:
            print(row['Date'])
            odate=row['Date']
            print('Onset falls on :',odate)
        #print(i)
            break    
    else:
        print('No onset')
        odate='Not all criteria fullfiled'
        break

fdate2=fdate
print(fdate2)

#On the onset day, zonal wind must be westerly and mean over the next 5 days must be westerly.
#In the 20 days window, the wind must be positive for at least 15 days.
#The mean of the zonal wind for 20 days window must exceed +1 m/s
#We first scan for the first westerly wind.

idx=df_new.index[df_new.SWMI2.gt(0.0)]
print(idx)

for i in idx:
    if [(df_new['5day'].gt(0.0)) & (df_new['15day'].ge(15.0) )& (df_new['20day'].gt(1.0))]:
        print(i)
        odate1=df_new.Date[i]
        print('Onset falls on :',odate1)
        #print(i)
        break
        
    else:
        print('No onset')

#plot
x=df_new['Date'].iloc[-30:]
print(x)
y=df_new['SWMI2'].iloc[-30:]
print(y)
plt.figure(figsize=(12,8))
ax=plt.subplot(111)
plt.plot(x,y,marker='4',label='SWMI2')
plt.xticks(fontsize=8,rotation=90)
plt.ylabel('850hPa U-component (m/s)')
plt.xlabel('Date')
plt.title('GEFS SWMI2 Initialized 00z ' +str(fdate2) + '\n Updated: ' +str(ct))
#plt.title('Updated: ' +str(ct))
maxy=max(df_new['SWMI2'].apply(np.ceil))+0.3
miny=min(df_new['SWMI2'].apply(np.floor))
avey=(maxy+miny)
#print(maxy)
text_date=df_new['Date'].iloc[80]
#print(text_date)
plt.text(str(text_date), maxy,'(Onset Date :'+str(odate1)+')',fontsize=10)
plt.text(str(text_date), maxy+0.25,'(Possible Onset Date :'+str(odate1)+')',fontsize=10)
#plt.text(str(odate), maxy,'(Onset Date :'+str(odate)+')',fontsize=10)
ax.axvline(x=fdate2, color="gray", linestyle="--", label="analysis/forecast split")
ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.savefig('./home/diong/Desktop/SWMI2/test/GEFS_SWMI2.png', bbox_inches='tight')
df_new1=df_new.iloc[:,[0,1]]
df_new1.to_csv('./home/diong/Desktop/SWMI2/test/swmi.csv',index=False, header=False)
