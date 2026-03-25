import pandas as pd

# 엑셀 파일 불러오기
df = pd.read_excel("data.xlsx")

# '성'과 '이름' 열을 합쳐서 새로운 '전체이름' 열 만들기
df["Name"] = df["Last Name"].astype(str) + " " + df["First Name"].astype(str)

# 필요하다면 기존 열 삭제
# df = df.drop(columns=["성", "이름"])

# 결과를 새 파일로 저장
df.to_excel("merged_names.xlsx", index=False)
