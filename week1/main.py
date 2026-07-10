import os
import sys
import pandas as pd

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
    
    else :
        sys.exit(1)
        
def explore_structure():
    for col_name, col_type in df.dtypes.items() :
        print(f' - {col_name} : {col_type}')
    print("====================================================================")
    print(df.head(5))
    print("====================================================================")
    
    
def show_distribution() :
    total_count = df["category"].count()
    
    # category 별 비율 구하기
    category = df['category'].unique()
    category_ratio = {}
 
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
        
        
        

load_data()
show_distribution()

# explore_structure()