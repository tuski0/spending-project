import os
import sys
import pandas as pd
import numpy as np



SPENDING_DATA_PATH = '../data/spending (1).csv'

def load_data():

    if os.path.exists(SPENDING_DATA_PATH) :
        df = pd.read_csv(SPENDING_DATA_PATH, encoding="utf-8-sig")
        rows , cols = df.shape
        print(f'데이터 로드 완료: {rows}행 x {cols}열')
    else :
        sys.exit(1)
        
    return df
        
    
    

def parse_date(df) :

    date_clean = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    
    failed_df = df.loc[date_clean.isna(), ['record_id', 'date']]
    failed_dic = dict(zip(failed_df['record_id'], failed_df['date']))
    
    df["date"] = date_clean
    
    print(f'날짜 변환 실패(NaT): {len(failed_df)}건', end="")
    for record_id, date in failed_dic.items():
        print(f' -> {record_id} ({date}는 존재하지 않는 날짜)')
        
    
    df["year"] = df["date"].dt.year.astype('Int64')
    df["month"] = df["date"].dt.month.astype('Int64')
    df["day"] = df["date"].dt.day.astype('Int64')
    
    return df
    
    
    
def standardize_category(df) :
    cleaned_list = []
    standardize_count = 0
    
    allowed_category = ['식비', '교통', '쇼핑', '의료', '문화', '기타']
    
    for val in df['category'] : 
        
        if not isinstance(val, str) :
           cleaned_list.append('기타')
           standardize_count += 1
           continue
        
        if val in allowed_category :
            cleaned_list.append(val)
        else :
            cleaned_list.append('기타')
            standardize_count += 1
            
    df['category'] = cleaned_list
    
    print(f'카테고리 표준화 : 변경 {standardize_count}건')
    
    return df
    
    
def add_amount_level(df) :
    
    amount_level = []
    
    for i in df['amount'] :
        if i < 10000 :
            amount_level.append('소액')
        elif 10000 <= i < 50000 :
            amount_level.append('중액')
        else :
            amount_level.append('고액')
    
    df['amount_level'] = amount_level
    
    print(f'amount_level 분포 -> 소액 {(df["amount_level"] == "소액").sum()} | 중액 {(df["amount_level"] == "중액").sum()} | 고액 {(df["amount_level"] == "고액").sum()}')
    
    return df
        
    
    
def clean_values(df) :
        
    before_na_count = df["memo"].isna().sum()
    df["memo"] = df["memo"].fillna("")
    print(df["date"].isna().sum())
    df = df.dropna(subset=["date"])
    print(df["date"].isna().sum())
    
    return df
    
    
    

if __name__ == '__main__' :
    
    
    # 기능 1
    df = load_data()
    
    # # 기능 2
    df = parse_date(df)
    
    # 기능 3
    df = standardize_category(df) 
    
    # 기능 4
    df = add_amount_level(df)
    
    # 기능 5
    df = clean_values(df)
    
    

