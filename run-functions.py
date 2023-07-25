"""
How to run the functions in estimations-all.py
@author: fawdywahyu
"""

from estimations-all import *

# Running the funtion to estimate the inflation
# Running the function
analisis_dasar_2015 = analisis_dasar('2015')
analisis_dasar_2017 = analisis_dasar('2017')
analisis_dasar_2018 = analisis_dasar('2018')
analisis_dasar_2019 = analisis_dasar('2019')

industri_2015 = analisis_industri(analisis_dasar_2015)
industri_2017 = analisis_industri(analisis_dasar_2017)
industri_2018 = analisis_industri(analisis_dasar_2018)
industri_2019 = analisis_industri(analisis_dasar_2019)

industri_2015.to_excel('industri 2015.xlsx', index=False)
industri_2017.to_excel('industri 2017.xlsx', index=False)
industri_2018.to_excel('industri 2018.xlsx', index=False)
industri_2019.to_excel('industri 2019.xlsx', index=False)

# Running the function (from 2010 to 2014)
analisis_dasar_2014 = analisis_dasar_csv('2014')
analisis_dasar_2013 = analisis_dasar_csv('2013')
analisis_dasar_2012 = analisis_dasar_csv('2012')
analisis_dasar_2011 = analisis_dasar_csv('2011')
analisis_dasar_2010 = analisis_dasar_csv('2010')
analisis_dasar_2009 = analisis_dasar_csv_07('2009')
analisis_dasar_2008 = analisis_dasar_csv_07('2008')
analisis_dasar_2007 = analisis_dasar_csv_07('2007')

# Group the result
industri_2014 = analisis_industri(analisis_dasar_2014)
industri_2013 = analisis_industri(analisis_dasar_2013)
industri_2012 = analisis_industri(analisis_dasar_2012)
industri_2011 = analisis_industri(analisis_dasar_2011)
industri_2010 = analisis_industri(analisis_dasar_2010)
industri_2009 = analisis_industri(analisis_dasar_2009)
industri_2008 = analisis_industri(analisis_dasar_2008)
industri_2007 = analisis_industri(analisis_dasar_2007)

industri_2014.to_excel('industri 2014.xlsx', index=False)
industri_2013.to_excel('industri 2013.xlsx', index=False)
industri_2012.to_excel('industri 2012.xlsx', index=False)
industri_2011.to_excel('industri 2011.xlsx', index=False)
industri_2010.to_excel('industri 2010.xlsx', index=False)
industri_2009.to_excel('industri 2009.xlsx', index=False)
industri_2008.to_excel('industri 2008.xlsx', index=False)
industri_2007.to_excel('industri 2007.xlsx', index=False)

# Running the function to estimate the HHI
# 2007 doesn't have export percentage, so we skip 2007

year_list1 = ['2008', '2009']
year_list2 = ['2010', '2011', '2012', '2013', '2014',
              '2015', '2017', '2018', '2019']

df_list1 = []
for y in year_list1:
    result_hhi = hhi_estimation_csv(y)
    df_list1.append(result_hhi)
df1 = pd.DataFrame()
for d in df_list1:
    df1 = pd.concat([df1, d], axis=1)

df_list2 = []
for y in year_list2:
    if int(y)<2015:
        result_hhi2 = hhi_estimation_csv(y)
    else:
        result_hhi2 = hhi_estimation_dta(y)
    df_list2.append(result_hhi2)
df2 = pd.concat(df_list2, axis=1)

df1.to_excel('Herfindahl-Hirrschman Index/Herfindahl-Hirrschman Index 2008-2009.xlsx')
df2.to_excel('Herfindahl-Hirrschman Index/Herfindahl-Hirrschman Index 2010-2019.xlsx')

