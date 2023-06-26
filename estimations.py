# -*- coding: utf-8 -*-
"""
The script is to estimate the share of profit margin to the GVA inflation

@author: Fawdy
"""

# Estimasi Inflasi yang berasal dari profit taking behaviour dan kontribusi wages terhadap inflasi
# Inflasi diukur menggunakan perubahan value add perusahaan

import pandas as pd

# Dasar Perhitungan (Teori yang mendasari)
# Since nominal profits and
# compensation of employees sum to the nominal value of GVA (Isabella)
# Artinya, nominal profit adalah nilai tambah dikurangi dengan kompensasi ke labor.
# PROOOF!!!! kalau profit adalah GVA - upah (buktinya ada di kertas HVS/gdrive)
# Profit dengan metode ini kalau menggunakan data BPS adalah profit yang bersih, bahkan setelah pajak dan pembayaran bunga
# tapi belum consider depresiasi dan amortisasi



# Bagaimana cara estimasi Real Gross Value Add (Real GVA)?
# Real GVA = Nominal GVA / (1 + Inflation Rate)^periods dimana periods = 1
# Krn di data BPS tidak didefnisikan real GVA dan asumsi harga yang digunakan dalam estimasi nominal GVA,
# inflasi diestimasi berdasarkan deflator PDB, dimana diasumsikan bahwa
# Nominal PDB dari sisi pengeluaran sama dengan pendapatan dan nilai tambah
# Sehingga, PDB deflator merepresentasikan deflator GVA.


deflator = pd.read_excel('Deflator Indonesia.xlsx', sheet_name='Deflator Indonesia')
deflator.set_index('Year', inplace=True)

# Creating the function to generate Real Variables and Nominal Variables

def analisis_dasar(tahun):
    
    # tahun: str
    # tahun = '2015'
    
    # Import Data
    ibs_dta = pd.read_stata(f'Data Industri Besar Sedang BPS/ibs_{tahun}.dta', 
                            convert_categoricals=True,
                            convert_missing=False, 
                            preserve_dtypes=True)
    
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

# Running the function
analisis_dasar_2015 = analisis_dasar('2015')
analisis_dasar_2017 = analisis_dasar('2017')
analisis_dasar_2018 = analisis_dasar('2018')
analisis_dasar_2019 = analisis_dasar('2019')

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

industri_2015 = analisis_industri(analisis_dasar_2015, 'median')
industri_2017 = analisis_industri(analisis_dasar_2017, 'median')
industri_2018 = analisis_industri(analisis_dasar_2018, 'median')
industri_2019 = analisis_industri(analisis_dasar_2019, 'median')

industri_2015.to_excel('industri 2015 median.xlsx', index=False)
industri_2017.to_excel('industri 2017 median.xlsx', index=False)
industri_2018.to_excel('industri 2018 median.xlsx', index=False)
industri_2019.to_excel('industri 2019 median.xlsx', index=False)

# Creating the function to generate Real Variables and Nominal Variables

def analisis_dasar_csv(tahun):
    
    # tahun: str
    # tahun = '2014'
    
    # Import Data
    # Read the .csv file using pandas
    ibs_csv = pd.read_csv(f'Data Industri Besar Sedang BPS/ibs_{tahun}.csv',
                          low_memory=False)
    
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


# Running the function (trial dari 2010 sampai 2014)
analisis_dasar_2014 = analisis_dasar_csv('2014')
analisis_dasar_2013 = analisis_dasar_csv('2013')
analisis_dasar_2012 = analisis_dasar_csv('2012')
analisis_dasar_2011 = analisis_dasar_csv('2011')
analisis_dasar_2010 = analisis_dasar_csv('2010')
analisis_dasar_2009 = analisis_dasar_csv_07('2009')
analisis_dasar_2008 = analisis_dasar_csv_07('2008')
analisis_dasar_2007 = analisis_dasar_csv_07('2007')

# Group the result
industri_2014 = analisis_industri(analisis_dasar_2014, 'median')
industri_2013 = analisis_industri(analisis_dasar_2013, 'median')
industri_2012 = analisis_industri(analisis_dasar_2012, 'median')
industri_2011 = analisis_industri(analisis_dasar_2011, 'median')
industri_2010 = analisis_industri(analisis_dasar_2010, 'median')
industri_2009 = analisis_industri(analisis_dasar_2009, 'mean')
industri_2008 = analisis_industri(analisis_dasar_2008, 'mean')
industri_2007 = analisis_industri(analisis_dasar_2007, 'mean')

industri_2014.to_excel('industri 2014 median.xlsx', index=False)
industri_2013.to_excel('industri 2013 median.xlsx', index=False)
industri_2012.to_excel('industri 2012 median.xlsx', index=False)
industri_2011.to_excel('industri 2011 median.xlsx', index=False)
industri_2010.to_excel('industri 2010 median.xlsx', index=False)
industri_2009.to_excel('industri 2009 mean.xlsx', index=False)
industri_2008.to_excel('industri 2008 mean.xlsx', index=False)
industri_2007.to_excel('industri 2007 mean.xlsx', index=False)

