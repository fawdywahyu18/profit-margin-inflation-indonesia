"""
Estimation for all the function in the "unveiling the supply side inflation in Indonesia: Profits or Wages?"
@author: fawdywahyu
"""

# Estimation for Inflation
# Estimasi Inflasi yang berasal dari profit taking behaviour dan kontribusi wages terhadap inflasi
# Inflasi diukur menggunakan perubahan value add perusahaan

import pandas as pd

# Creating the function to generate Real Variables and Nominal Variables

def analisis_dasar(tahun):
    
    # tahun: str
    # tahun = '2015'
    
    # Import Data
    ibs_dta = pd.read_stata(f'Data Industri Besar Sedang BPS/ibs_{tahun}.dta', 
                            convert_categoricals=True,
                            convert_missing=False, 
                            preserve_dtypes=True)

    # Import data deflator
    deflator = pd.read_excel('Deflator Indonesia.xlsx', sheet_name='Deflator Indonesia')
    deflator.set_index('Year', inplace=True)
    
    # Data Upah
    ibs_copy = ibs_dta.copy()
    ibs_copy.rename(columns=lambda x: x.lower(), inplace=True)
    dua_digit_tahun = tahun[-2:]
    
    ibs_copy['total upah'] = ibs_copy[(f'zndvcu{dua_digit_tahun}')] + ibs_copy[(f'zpdvcu{dua_digit_tahun}')]
    wage = ibs_copy['total upah']
    nominal_gva = ibs_copy[(f'vtlvcu{dua_digit_tahun}')]
    # inflasi_deflator = deflator.loc[tahun, 'Deflator Percentage'].values[0]
    deflator_pdb = deflator.loc[tahun, 'Deflator Index 2010_1'].values[0]
    
    if tahun=='2015':
        klasifikasi = ibs_copy['disic215']
    elif tahun=='2017':
        klasifikasi = ibs_copy['disic517']
    elif tahun=='2018':
        klasifikasi = ibs_copy['disic518']
    elif tahun=='2019':
        klasifikasi = ibs_copy['disic519']
        
    # pengali = 1 + inflasi_deflator/100
    real_gva = nominal_gva / deflator_pdb
    nominal_profit = nominal_gva - wage
    profit_deflator = nominal_profit / real_gva
    wage_deflator = wage / real_gva
    renum = ibs_copy['renum']
    
    result = {
        'Kode Klasifikasi': klasifikasi,
        'Renum': renum,
        'Nominal GVA': nominal_gva,
        'Real GVA': real_gva,
        'Nominal Profit': nominal_profit,
        'Profit Deflator': profit_deflator,
        'Nominal Wage': wage,
        'Wage Deflator': wage_deflator
        }
    result_df = pd.DataFrame(result)
    result_df['Deflator PDB'] = result_df['Profit Deflator'] + result_df['Wage Deflator']  
    return result_df

# Renum adalah kode unik perusahaan yang ada di IBS
# Wage Deflator bisa diinterpretasikan sebagai bagian peran wage terhadap kenaikan inflasi
# Profit Deflator bisa diinterpretasikan sebagai bagian peran profit terhadap kenaikan inflasi

# Analisis Tabel by Industri
def analisis_industri(df_input, metode_agg='mean'):
    
    # df_input : dataframe input dari hasil analisis_dasar
    # df_input = analisis_dasar_2015
    # metode_agg : str, merupakan string untuk metode agregasi
    
    df_olah = df_input.copy()
    df_grouped = df_olah.groupby('Kode Klasifikasi').agg({'Nominal GVA':metode_agg,
                                                          'Real GVA':metode_agg,
                                                          'Nominal Profit':metode_agg,
                                                          'Profit Deflator': metode_agg,
                                                          'Nominal Wage': metode_agg,
                                                          'Wage Deflator': metode_agg,
                                                          'Deflator PDB': metode_agg}).reset_index()

    df_grouped['Share Profit terhadap Deflator'] = df_grouped['Profit Deflator']/df_grouped['Deflator PDB']
    df_grouped['Share Wage terhadap Deflator'] = df_grouped['Wage Deflator']/df_grouped['Deflator PDB']
    
    return df_grouped


# Creating the function to generate Real Variables and Nominal Variables

def analisis_dasar_csv(tahun):
    
    # tahun: str
    # tahun = '2014'
    
    # Import Data
    # Read the .csv file using pandas
    ibs_csv = pd.read_csv(f'Data Industri Besar Sedang BPS/ibs_{tahun}.csv',
                          low_memory=False)

    # Import data deflator
    deflator = pd.read_excel('Deflator Indonesia.xlsx', sheet_name='Deflator Indonesia')
    deflator.set_index('Year', inplace=True)

    # Data Upah
    ibs_copy = ibs_csv.copy()
    ibs_copy.rename(columns=lambda x: x.lower(), inplace=True)
    dua_digit_tahun = tahun[-2:]
    
    ibs_copy['total upah'] = ibs_copy[(f'zndvcu{dua_digit_tahun}')] + ibs_copy[(f'zpdvcu{dua_digit_tahun}')]
    wage = ibs_copy['total upah']
    nominal_gva = ibs_copy[(f'vtlvcu{dua_digit_tahun}')]
    # inflasi_deflator = deflator.loc[tahun, 'Deflator Percentage'].values[0]
    deflator_pdb = deflator.loc[tahun, 'Deflator Index 2010_1'].values[0]
    
    # Exctract the first two digits of integers in a column pandas
    ibs_copy[(f'disic5{dua_digit_tahun}_str')] = ibs_copy[(f'disic5{dua_digit_tahun}')].astype(str)
    ibs_copy[f'disic2{dua_digit_tahun}_str'] = ibs_copy[(f'disic5{dua_digit_tahun}_str')].str[:2]
    ibs_copy[f'disic2{dua_digit_tahun}'] = ibs_copy[(f'disic2{dua_digit_tahun}_str')].astype(int)
    klasifikasi = ibs_copy[(f'disic2{dua_digit_tahun}')]
        
    # pengali = 1 + inflasi_deflator/100
    real_gva = nominal_gva / deflator_pdb
    nominal_profit = nominal_gva - wage
    profit_deflator = nominal_profit / real_gva
    wage_deflator = wage / real_gva
    renum = ibs_copy['psid']
    
    result = {
        'Kode Klasifikasi': klasifikasi,
        'Renum': renum,
        'Nominal GVA': nominal_gva,
        'Real GVA': real_gva,
        'Nominal Profit': nominal_profit,
        'Profit Deflator': profit_deflator,
        'Nominal Wage': wage,
        'Wage Deflator': wage_deflator
        }
    result_df = pd.DataFrame(result)
    result_df['Deflator PDB'] = result_df['Profit Deflator'] + result_df['Wage Deflator']  
    return result_df

def analisis_dasar_csv_07(tahun):
    
    # tahun: str
    # tahun = '2009'
    
    # Import Data
    # Read the .csv file using pandas
    ibs_csv = pd.read_csv(f'Data Industri Besar Sedang BPS/ibs_{tahun}.csv',
                          low_memory=False)

    # Import data deflator
    deflator = pd.read_excel('Deflator Indonesia.xlsx', sheet_name='Deflator Indonesia')
    deflator.set_index('Year', inplace=True)
    
    # Data Upah
    ibs_copy = ibs_csv.copy()
    ibs_copy.rename(columns=lambda x: x.lower(), inplace=True)
    dua_digit_tahun = tahun[-2:]
    
    ibs_copy['total upah'] = ibs_copy[(f'zpzvcu{dua_digit_tahun}')] + ibs_copy[(f'znzvcu{dua_digit_tahun}')]
    wage = ibs_copy['total upah']
    nominal_gva = ibs_copy[(f'vtlvcu{dua_digit_tahun}')]
    # inflasi_deflator = deflator.loc[tahun, 'Deflator Percentage'].values[0]
    deflator_pdb = deflator.loc[tahun, 'Deflator Index 2010_1'].values[0]
    
    # Exctract the first two digits of integers in a column pandas
    ibs_copy[(f'disic5{dua_digit_tahun}_str')] = ibs_copy[(f'disic5{dua_digit_tahun}')].astype(str)
    ibs_copy[f'disic2{dua_digit_tahun}_str'] = ibs_copy[(f'disic5{dua_digit_tahun}_str')].str[:2]
    ibs_copy[f'disic2{dua_digit_tahun}'] = ibs_copy[(f'disic2{dua_digit_tahun}_str')].astype(int)
    klasifikasi = ibs_copy[(f'disic2{dua_digit_tahun}')]
        
    # pengali = 1 + inflasi_deflator/100
    real_gva = nominal_gva / deflator_pdb
    nominal_profit = nominal_gva - wage
    profit_deflator = nominal_profit / real_gva
    wage_deflator = wage / real_gva
    renum = ibs_copy['psid']
    
    result = {
        'Kode Klasifikasi': klasifikasi,
        'Renum': renum,
        'Nominal GVA': nominal_gva,
        'Real GVA': real_gva,
        'Nominal Profit': nominal_profit,
        'Profit Deflator': profit_deflator,
        'Nominal Wage': wage,
        'Wage Deflator': wage_deflator
        }
    result_df = pd.DataFrame(result)
    result_df['Deflator PDB'] = result_df['Profit Deflator'] + result_df['Wage Deflator']  
    return result_df

# Herfindahl-Hirrschman Index (HHI) estimation
# Author: Fawdy

# Equation: HHI = sum(s_i^2)
# s_i = market share of firm i
# Market shares are estimated based on the domestic industry revenue values (excluding the revenues from abroad), assuming that the industry activities are dominated by sales
# theres is no sales data for each firm

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

