import os
import sys
import sqlite3
import pandas as pd

DATA_DIR = '../data/'
CSV_PATH = DATA_DIR + 'spending (1).csv'
DB_PATH = DATA_DIR + 'spendings.db'

def load_data():
   
    if os.path.exists(CSV_PATH) :
        df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
        rows , cols = df.shape
        print(f'[1] 데이터 로드 완료 : ({rows}, {cols})')
    else :
        sys.exit(1)
        
    return df
        
def parse_date(df) :

    date_clean = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    
    df["date"] = date_clean
    
    df["year"] = df["date"].dt.year.astype('Int64')
    df["month"] = df["date"].dt.month.astype('Int64')
    df["day"] = df["date"].dt.day.astype('Int64')
    
    return df
       
def standardize_category(df) :
    cleaned_list = []
    
    allowed_category = ['식비', '교통', '쇼핑', '의료', '문화', '기타']
    
    for val in df['category'] : 
        
        if not isinstance(val, str) :
           cleaned_list.append('기타')
           continue
        
        if val in allowed_category :
            cleaned_list.append(val)
        else :
            cleaned_list.append('기타')
            
    df['category'] = cleaned_list
    
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
    
    return df
        
       
def clean_values(df) :
    # memo 결측치 -> 빈칸 변경
    df["memo"] = df["memo"].fillna("")

    # date 결측치 행 제거
    df = df.dropna(subset=["date"])  
    df = df.reset_index(drop=True)
    
    rows, cols = df.shape
    print(f'[2] 데이터 정리 완료 : ({rows}, {cols})')

    return df

def init_db(conn) :
    os.makedirs("../data", exist_ok=True)
    
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
    
def save_to_db(conn) :

    
    df.to_sql("spendings", conn, if_exists="append", index=False)
    conn.commit()
    
    result = conn.execute("SELECT COUNT(*) FROM spendings").fetchone()
    
    total_count = result[0]
    
    print(f"[3] DB 저장 완료 (DB 행 내 수: {total_count})")
    
    
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
    
    print('\n')
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
    
    print('\n')
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
    
    print('\n')
    print('=== Python vs SQL 검증 ===')
    print(f'전체 카테고리 일치 : {is_equal}')

def payment_analyze(conn) :
    query = '''
    SELECT month, payment, SUM(amount) AS 'total_amount'
    FROM spendings
    GROUP BY month, payment
    ORDER BY month, payment;
    '''
    df_payment = pd.read_sql_query(query, conn)
    print('카드 vs 현금 월별 지출 비교')
    print(df_payment.to_string(index=False))
    
    query = '''
    SELECT 
        CASE strftime('%w', date)
            WHEN '0' THEN '일요일'
            WHEN '1' THEN '월요일'
            WHEN '2' THEN '화요일'
            WHEN '3' THEN '수요일'
            WHEN '4' THEN '목요일'
            WHEN '5' THEN '금요일'
            WHEN '6' THEN '토요일'
        END AS '요일',
        SUM(amount) AS '총지출',
        CAST(AVG(amount) AS INTEGER) AS '평균지출'
    FROM spendings
    GROUP BY strftime('%w', date)
    ORDER BY strftime('%w', date);
    '''
    
    df_day = pd.read_sql_query(query, conn)
    print(df_day.to_string(index=False))


if __name__ == '__main__':
    
    conn = sqlite3.connect(DB_PATH)
    
    # 과제 1
    df = load_data()
    
    # 과제 2
    df = parse_date(df)
    df = standardize_category(df)
    df = add_amount_level(df)
    df = clean_values(df)
    
    # 과제 3
    init_db(conn)
    save_to_db(conn)
    verify_with_python(conn)
    
    # 과제 4
    payment_analyze(conn)
    
    
    
    
    
    
    