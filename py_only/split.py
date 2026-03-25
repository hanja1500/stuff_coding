import pandas as pd

# 엑셀 파일 불러오기
df = pd.read_excel("student.xlsx")

# 괄호 앞부분만 잘라서 이름만 추출
df['이름'] = df['이름'].apply(lambda x: str(x).split('(')[0].strip())

# 이름만 포함된 새로운 DataFrame
name_df = df[['이름']]

# 새 엑셀 파일로 저장
name_df.to_excel("class36_names_only.xlsx", index=False)
