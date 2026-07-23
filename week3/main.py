import os
import sys
import sqlite3
import pandas as pd

DATA_PATH = '../data/'
CSV_PATH = DATA_PATH + 'spending_clean.csv'
DB_PATH = DATA_PATH+'spendings.db'

def load_clean_data(path):
    
    if os.path.exists(path) :
        df = pd.read_csv(path, encoding="utf-8-sig")
        rows , cols = df.shape
        print(f'데이터 로드 완료: {rows}행 x {cols}열')
    else :
        sys.exit(1)
        
    return df

def init_db(conn, path) :
    os.makedirs(path, exist_ok=True)
    
    conn.execute("DROP TABLE IF EXISTS spendings")
    
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
    
    conn.execute(create_table_query)
    conn.commit()

    print("테이블 생성 완료")
    
def save_to_db(conn, df) :

    df.to_sql("spendings", conn, if_exists="append", index=False)
    conn.commit()
    
    result = conn.execute("SELECT COUNT(*) FROM spendings").fetchone()
    
    total_count = result[0]
    
    print(f"{total_count}행 저장 완료 (DB 내 행 수 : {total_count})")

    

def verify_with_python(conn) :
        
    query = """
    SELECT
        category,
        COUNT(*) AS 건수,
        SUM(amount) AS 총지출액,
        CAST(AVG(amount) AS INT) AS 평균지출액,
        MAX(amount) AS 최대지출액
    FROM spendings
    GROUP BY category
    ORDER BY 총지출액 DESC;
    """
    
    print('=== 카테고리별 집계 ===')
    df_summary = pd.read_sql(query, conn)
    print(df_summary.to_string(index=False))
    
    query = """
    SELECT
        month,
        count(*) AS 건수,
        SUM(amount) AS 총지출액
    FROM spendings
    GROUP BY month;
    """
    
    print("=== 월별 총 지출 ===")
    df_summary = pd.read_sql(query, conn)
    print(df_summary.to_string(index=False))
    
    
    df_raw = pd.read_sql("SELECT * FROM spendings", conn)
    py_result = df_raw.groupby('category')['amount'].sum()
    
    
    query = """
    SELECT category, SUM(amount) AS amount
    FROM spendings
    GROUP BY category
    ORDER BY category;
    """
    sql_result = pd.read_sql(query, conn)
    sql_result = sql_result.set_index('category')['amount']
    
    is_equal = py_result.equals(sql_result)
    
    print('=== Python vs SQL 검증 ===')
    print(f'전체 카테고리 일치 : {is_equal}')

    
def main() :
    # CSV 연결
    df = load_clean_data(CSV_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    
    # 기능 1 -> Table 생성하기
    init_db(conn, DATA_PATH)
    
    # 기능 2 -> csv 값을 가지고 Table에 대입하기
    save_to_db(conn, df)
    
    # 기능 3, 4, 5, 6 구현
    verify_with_python(conn)
    
    conn.close()
    
    
    
if __name__ == '__main__' :
    
    main()