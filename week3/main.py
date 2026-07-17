import os
import sys
import sqlite3
import pandas as pd

DATA_PATH = '../data/'
def load_data():
    path = DATA_PATH+'spending_clean.csv'
    if os.path.exists(path) :
        df = pd.read_csv(path, encoding="utf-8-sig")
        rows , cols = df.shape
        print(f'데이터 로드 완료: {rows}행 x {cols}열')
    else :
        sys.exit(1)
        
    return df

def init_db() :
    os.makedirs("../data", exist_ok=True)
    conn = sqlite3.connect("../data/spending.db")
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS spendings")
    
    create_table_query = """
    CREATE TABLE spendings( -- 테이블(Table) : 데이터를 행과 열로 저장하는 구조
        record_id TEXT PRIMARY KEY, -- 기본키(Primary Key) : 각 행을 고유하게 구분하는 컬럼 (중복·NULL 불가)
        date TEXT NOT NULL, -- NOT NULL : 해당 컬럼에 빈 값을 허용하지 않음
        category TEXT NOT NULL,
        item TEXT NOT NULL,
        amount INTEGER NOT NULL,
        payment TEXT NOT NULL,
        memo TEXT,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        day INTEGER NOT NULL,
        amount_level TEXT NOT NULL
    );
    """
    
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

    print("테이블 생성 완료")
    
def save_to_db() :
    db_path = DATA_PATH+"spending.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    df.to_sql("spendings", conn, if_exists="append", index=False)
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM spendings")
    
    result = cursor.fetchone()
    
    total_count = result[0]
    
    print(f"{total_count}행 저장 완료 (DB 내 행 수 : {total_count})")

    conn.close()
    
    
    
    
    
    
    
if __name__ == '__main__' :
    
    # 
    df = load_data()
    
    # 기능 1 -> Table 생성하기
    init_db()
    
    # 기능 2 -> csv 값을 가지고 Table에 대입하기
    save_to_db()

    