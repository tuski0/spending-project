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
        print("====================================================================")
        print(f'데이터 로드 완료 {rows}행 x {cols}열')
        print("====================================================================")
        print('\n')
    else :
        sys.exit(1)
        
def explore_structure():
    
    for col_name, col_type in df.dtypes.items() :
        print(f' - {col_name} : {col_type}')
    print("====================================================================")
    print(df.head(5))
    print("====================================================================")
    print("\n")
    
    
def show_distribution() :
    total_count = df["category"].count()
    
    # category 별 비율 구하기
    category = df['category'].unique()
    category_ratio = {}
    
    print("====================================================================")
 
    for i in category:
        count = (df['category'] == i).sum()
        category_ratio[i] = (count / total_count) * 100
            
    for key, value in category_ratio.items() :
        print(f'{key} : {value:.2f}%')
        
        
    print("====================================================================")
    
    # payment 별 비율 구하기
    payment = df['payment'].unique()
    payment_ratio = {}
    
    for i in payment:
        count = (df['payment'] == i).sum()
        payment_ratio[i] = (count / total_count) * 100
        
    for key, value in payment_ratio.items() :
        print(f'{key} : {value:.2f}%')
        
    print("====================================================================")
    
    # category 별 평균 금액 계산
    
    category_avg = {}
    
    for i in category:
        amount_total = df[df['category'] == i]['amount'].mean()
        category_avg[i] = amount_total
        
    for key, value in category_avg.items() :
        print(f'{key} : {value:.2f}원')
        
    print("====================================================================")
    print("\n")
    
    
def check_missing() :
    missing_dic = {}
    Not_Missing_Dic = {}
    
    # 결측치 유무 확인 후 맞는 딕셔너리에 값 삽입
    for i in df.columns :
        if df[i].isnull().sum() > 0 :
            miss_ratio = (df[i].isnull().sum() / (len(df[i]) ) * 100)
            if miss_ratio <= 5 :
                severity = '낮음'
            elif miss_ratio >= 5 and miss_ratio <= 20 :
                severity = '주의'
            else :
                severity = '위험'
            missing_dic[i] = df[i].isnull().sum(), miss_ratio, severity
        else :
            Not_Missing_Dic[i] = df[i].isnull().sum()
    
    # 결측치가 있는 컬럼 출력
    print("====================================================================")
    for key, (value1, value2, value3) in missing_dic.items() :
        print(f'{key} : {value1}, {value2:.1f}%, {value3}')
    print("====================================================================")
    # 결측치가 없는 컬럼 출력
    for key, value in Not_Missing_Dic.items() :
        print(f'{key} : {value}')
    print("====================================================================")
    

def numpy_amount_stats() :
    print(np.array(df['amount']))
            
            
        
        
        

load_data()
explore_structure()
show_distribution()
check_missing()
numpy_amount_stats()
