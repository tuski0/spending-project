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
        print(f'데이터 로드 완료 {rows}행 x {cols}열')
    else :
        sys.exit(1)
        
def explore_structure():
    load_data()
    for col_name, col_type in df.dtypes.items() :
        print(f' - {col_name} : {col_type}')
    print(df.head(5))
    


explore_structure()