# Herfindahl-Hirrschman Index (HHI) estimation
# Author: Fawdy

# Equation: HHI = sum(s_i^2)
# s_i = market share of firm i
# Market shares are estimated based on production values minus exports values
# theres is no sales data for each firm

import pandas as pd
import numpy as np

def hhi_estimation_csv(year):
    
    # year = '2008'
    
    # Import data
    ibs_csv = pd.read_csv(f'Data Industri Besar Sedang BPS/ibs_{year}.csv', low_memory=False)
    
    # Lower all the column names
    ibs_copy = ibs_csv.copy()
    ibs_copy.rename(columns=lambda x: x.lower(), inplace=True)
    dua_digit_tahun = year[-2:]

    # Exctract the first two digits of integers in a column pandas about classification code
    ibs_copy[(f'disic5{dua_digit_tahun}_str')] = ibs_copy[(f'disic5{dua_digit_tahun}')].astype(str)
    ibs_copy[f'disic2{dua_digit_tahun}_str'] = ibs_copy[(f'disic5{dua_digit_tahun}_str')].str[:2]
    ibs_copy[f'disic2{dua_digit_tahun}'] = ibs_copy[(f'disic2{dua_digit_tahun}_str')].astype(int)
    klasifikasi = ibs_copy[(f'disic2{dua_digit_tahun}')]

    # Filter data based on classification code and do iteration
    hhi_result = []
    index_df = []
    for i in klasifikasi.unique():
        ibs_filter = ibs_copy[ibs_copy[f'disic2{dua_digit_tahun}']==i]
        export = ibs_filter[f'prprex{dua_digit_tahun}'].fillna(0)
        dalam_negeri = 1 - export/100
        nilai_makloon = ibs_filter[f'yisvcu{dua_digit_tahun}']
        np_dn = nilai_makloon * dalam_negeri # Nilai produksi dalam negeri
        total_makloon = np_dn.sum()
        s_i_sq = np.square(np_dn/total_makloon) # market shares squared
        hhi = s_i_sq.sum() * 100
        hhi_result.append(hhi)
        index_df.append(i)
    hhi_df = pd.DataFrame({'Kode Klasifikasi':index_df,
                           f'HH Index {year} (Percentage)': hhi_result})
    hhi_result = hhi_df.set_index('Kode Klasifikasi')
    return hhi_result

def hhi_estimation_dta(tahun):
    
    # tahun = '2017'
    
    ibs_dta = pd.read_stata(f'Data Industri Besar Sedang BPS/ibs_{tahun}.dta', 
                            convert_categoricals=True,
                            convert_missing=False, 
                            preserve_dtypes=True)
    
    # Lower all the column names
    ibs_copy = ibs_dta.copy()
    ibs_copy.rename(columns=lambda x: x.lower(), inplace=True)
    dua_digit_tahun = tahun[-2:]
    
    # Classification code
    if tahun=='2015':
        ibs_copy['klasifikasi'] = ibs_copy['disic215']
    elif tahun=='2017':
        ibs_copy['klasifikasi'] = ibs_copy['disic517']
    elif tahun=='2018':
        ibs_copy['klasifikasi'] = ibs_copy['disic518']
    elif tahun=='2019':
        ibs_copy['klasifikasi'] = ibs_copy['disic519']
    ibs_copy['klasifikasi'] = ibs_copy['klasifikasi'].astype('int64') 
    
    # Filter data based on classification code and do iteration
    hhi_result = []
    index_df = []
    for i in ibs_copy['klasifikasi'].unique():
        ibs_filter = ibs_copy[ibs_copy['klasifikasi']==i]
        
        if int(tahun) < 2017:
            export = ibs_filter[f'prprex{dua_digit_tahun}'].fillna(0)
            dalam_negeri = 1 - export/100
            nilai_makloon = ibs_filter[f'yisvcu{dua_digit_tahun}']
            np_dn = nilai_makloon * dalam_negeri # Nilai makloon dalam negeri
        else:
            np_dn = ibs_filter[f'yisvdo{dua_digit_tahun}'] # Nilai makloon dalam negeri
        
        total_makloon = np_dn.sum()
        s_i_sq = np.square(np_dn/total_makloon) # market shares squared
        hhi = s_i_sq.sum() * 100
        hhi_result.append(hhi)
        index_df.append(i)
    hhi_df = pd.DataFrame({'Kode Klasifikasi':index_df,
                           f'HH Index {tahun} (Percentage)': hhi_result})
    hhi_result = hhi_df.set_index('Kode Klasifikasi')
    
    return hhi_result
    
# Result for Herfindahl-Hirrschman Index (HHI)
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
