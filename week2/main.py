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



    

if __name__ == '__main__' :
    # 기능 1
    load_data()
    
    
    

