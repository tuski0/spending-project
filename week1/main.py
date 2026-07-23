import os
import sys
import pandas as pd
import numpy as np

DATA_PATH ='../data/spending (1).csv' 

def load_data(path):
        
    if os.path.exists(path) :
        df = pd.read_csv(path, encoding="utf-8-sig")
        rows , cols = df.shape
        print(f'데이터 로드 완료: {rows}행 × {cols}열')
    else :
        sys.exit(1)

    return df
        
        
def explore_structure(df):
    rows, cols = df.shape
    print(f'전체 행 수: {rows}, 열 수: {cols}')
    print('===== 컬럼별 자료형 =====')
    for col_name, col_type in df.dtypes.items() :
        print(f' - {col_name} : {col_type}')
    print('===== 상위 5행 =====')
    print(df.head(5))
    
    
def show_distribution(df) :
    total_count = df["category"].count()
    
    # category 별 비율 구하기
    print("===== 카테고리별 비율 =====")
    category = df['category'].unique()
    category_ratio = {}

    for i in category:
        count = (df['category'] == i).sum()
        category_ratio[i] = count
            
    for key, value in category_ratio.items() :
        ratio = count / total_count * 100
        print(f'{key} : {count}건 {value:.2f}%')
    
    # payment 별 비율 구하기
    print("===== 결제 수단별 평균 금액 =====")
    payment = df['payment'].unique()
    payment_ratio = {}
    
    for i in payment:
        count = (df['payment'] == i).sum()
        payment_ratio[i] = (count / total_count) * 100
        
    for key, value in payment_ratio.items() :
        print(f'{key} : {value:.2f}%')
        
    
    # category 별 평균 금액 계산
    print("===== 카테고리별 평균 금액 =====")
    category_avg = {}
    
    for i in category:
        amount_total = df[df['category'] == i]['amount'].mean()
        category_avg[i] = amount_total
        
    for key, value in category_avg.items() :
        print(f'{key} : {value:.2f}원')
        
    print("\n")

    return {'category_ratio': category_ratio, 'payment_ratio': payment_ratio, 'category_avg': category_avg}
    
def check_missing(df) :
    missing_dic = {}
    Not_Missing_Dic = {}
    
    # 결측치 유무 확인 후 맞는 딕셔너리에 값 삽입
    for i in df.columns :
        if df[i].isnull().sum() > 0 :
            miss_ratio = (df[i].isnull().sum() / (len(df[i]) ) * 100)
            if miss_ratio < 5 :
                severity = '낮음'
            elif miss_ratio >= 5 and miss_ratio < 20 :
                severity = '주의'
            else :
                severity = '높음'
            missing_dic[i] = df[i].isnull().sum(), miss_ratio, severity
        else :
            Not_Missing_Dic[i] = df[i].isnull().sum()
    
    # 결측치가 있는 컬럼 출력
    print("===== 결측치 있는 컬럼 =====")
    for key, (value1, value2, value3) in missing_dic.items() :
        print(f'{key} : {value1}, {value2:.1f}%, {value3}')
    print("===== 결측치 없는 컬럼 =====")
    # 결측치가 없는 컬럼 출력
    for key, value in Not_Missing_Dic.items() :
        print(f'{key} : {value}')
    
    print('\n')

    return missing_dic
    

def numpy_amount_stats(df) :
    arr = np.array(df['amount'])
    clean_array = arr[~np.isnan(arr)]
    print("===== numpy 활용한 5가지 통계량 =====")
    
    np_dic = {
        'mean' : round(np.mean(clean_array), 0),
        'std' : round(np.std(clean_array, ddof=1), 0),
        'median' : round(np.median(clean_array), 0),
        'min' : np.min(clean_array),
        'max' : np.max(clean_array)
    }
    
    for key, value in np_dic.items() :
        print(f'{key} : {value}')
    print()
    
    print("===== 5만 원 초과 지출 =====")
    over_amount = [clean_array[clean_array > 50000]]
    # over_amount = []
    # for i in clean_array :
    #     if i > 50000 :
    #         over_amount.append(i)
    
    print(*over_amount)
    print("\n")
    
    pandas_amount = df['amount'].describe()
    
    pandas_dic = {
        'mean' : round(pandas_amount['mean'], 0),
        'std' : round(pandas_amount['std'], 0),
        'median' : pandas_amount['50%'],
        'min' : pandas_amount['min'],
        'max' : pandas_amount['max']
    }
    
    print("===== Numpy와 Pandas의 값 일치여부 =====")
    print('title    Numpy값    Pandas값    일치여부')
    for title in np_dic.keys() :
        np_val = np_dic[title]
        pd_val = pandas_dic[title]
    
        result = 'V' if np_val == pd_val else 'X'
        
        print(f'{title}    {np_val}    {pd_val}    {result}')
        

def main() :
    # 기능 1
    df = load_data(DATA_PATH)
    
    # 기능 2
    explore_structure(df)
    
    # 기능 3
    show_distribution(df)
    
    # 기능 4
    check_missing(df)
    
    # 기능 5
    numpy_amount_stats(df)
    

if __name__ == '__main__' :

    main()