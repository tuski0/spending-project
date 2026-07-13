import os
import sys
import pandas as pd
import numpy as np

df = None

def load_data():
    global df
    path = '../data/spending (1).csv'

    if os.path.exists(path) :
        df = pd.read_csv(path, encoding="utf-8-sig")
        rows , cols = df.shape
        print(f'데이터 로드 완료: {rows}행 x {cols}열')
    else :
        sys.exit(1)
        
    print

def parse_date() :

    date_clean = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    
    failed_df = df.loc[date_clean.isna(), ['record_id', 'date']]
    failed_dic = dict(zip(failed_df['record_id'], failed_df['date']))
    
    df["date"] = date_clean
    
    for record_id, date in failed_dic.items():
        print(f'날짜 변환 실패(NaT): {len(failed_df)}건 -> {record_id} ({date}는 존재하지 않는 날짜)')
        
    
    df["year"] = df["date"].dt.year.astype('Int64')
    df["month"] = df["date"].dt.month.astype('Int64')
    df["day"] = df["date"].dt.day.astype('Int64')
    
    
    
    

    

if __name__ == '__main__' :
    # 기능 1
    load_data()
    parse_date()
    
    

