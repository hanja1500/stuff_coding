import pandas as pd
import numpy as np

# 1. 파일 읽기 (데이터가 공백으로 구분되어 있다고 가정)
# 만약 구분자가 쉼표라면 sep=',' 를 추가하세요.
file_path = 'data.txt'
with open(file_path, 'r', encoding='utf-8') as f:
    raw_data = f.read().split()

# 2. 리스트를 3열 형태의 넘파이 배열로 재구성
# 504개 데이터를 (168, 3) 형태로 변환합니다.
# 1열: 3n-2, 2열: 3n-1, 3열: 3n 구조가 자동으로 형성됩니다.
data_array = np.array(raw_data).reshape(-1, 3)

# 3. 데이터프레임 생성
df = pd.DataFrame(data_array, columns=['Column1', 'Column2', 'Column3'])

# 결과 확인
print("데이터 변환 완료 (상위 5행):")
print(df.head())

# 4. CSV 파일로 저장 (DB 임포트용)
df.to_csv('processed_data.csv', index=False)

# 5. (선택사항) SQLite DB 파일로 직접 저장하고 싶을 경우
# import sqlite3
# conn = sqlite3.connect('my_database.db')
# df.to_sql('my_table', conn, if_exists='replace', index=False)
# conn.close()