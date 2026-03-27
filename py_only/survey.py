import pandas as pd
import random

# 1. 파일 경로 설정 (실제 파일명으로 변경해주세요)
survey_file = '2026-1 인공지능윤리와 안전 주제 설문(응답).xlsx'  # 설문 응답 엑셀 파일
attendance_file = '2026-1 인공지능윤리와안전.xlsx'  # 출석부(전체 명단) 엑셀 파일
output_file = 'survey_result_full.xlsx'  # 최종 저장될 파일

# 2. 기준 열 이름 및 순위 열 설정
# 두 엑셀 파일에 공통으로 들어있는 식별자 열(예: '이름', '학번', '사번' 등)을 적어주세요.
key_column = ['이름', '학번', '학과']
rank_columns = ['1순위 희망', '2순위 희망', '3순위 희망']

# 💡 새로 추가된 설정: 지우고 싶은 2, 3순위의 특정 단어와 적용할 열
word_to_remove = '인적관리 (교육 및 노동환경)' # 실제 지우고 싶은 단어로 변경해주세요 (예: '없음', 'X' 등)
target_columns_to_clear = ['2순위 희망', '3순위 희망']

# 💡 배정 알고리즘 설정
MAX_CAPACITY = 50  # 주제당 최대 인원 (50명으로 수정)
REQUIRED_TOPICS = 2  # 1인당 배정받아야 할 주제 개수

try:
    df_survey = pd.read_excel(survey_file)
    df_att = pd.read_excel(attendance_file)
    print("📌 [파일 불러오기 성공]")
except FileNotFoundError as e:
    print(f"❌ 파일을 찾을 수 없습니다: {e.filename}")
    exit()

# ==========================================
# 2. 데이터 전처리 (특정 단어 제거 및 빈칸 당기기)
# ==========================================
# 2, 3순위의 특정 단어를 '-'로 변경
for col in target_columns_to_clear:
    if col in df_survey.columns:
        df_survey[col] = df_survey[col].replace(word_to_remove, '-')


# 빈칸 당기기 함수
def shift_ranks(row, cols, empty_marks=['-', ' ', '']):
    choices = [row[col] for col in cols if col in row]
    valid_choices = [c for c in choices if pd.notna(c) and str(c).strip() not in empty_marks]
    shifted_choices = valid_choices + ['-'] * (len(cols) - len(valid_choices))
    for col, val in zip(cols, shifted_choices):
        row[col] = val
    return row


df_survey_clean = df_survey.apply(lambda row: shift_ranks(row, rank_columns), axis=1)

# 명단 병합 및 미응답자 빈칸 처리
df_merged = pd.merge(df_att, df_survey_clean, on=key_column, how='left')
for col in rank_columns:
    if col in df_merged.columns:
        df_merged[col] = df_merged[col].fillna('-')
df_merged = df_merged.fillna('')

# ==========================================
# 3. 선착순 주제 배정 알고리즘
# ==========================================

# 데이터에 존재하는 모든 유효한 주제 목록 추출 ('-' 등 제외)
all_topics = set()
for col in rank_columns:
    all_topics.update(df_merged[col].unique())
all_topics = {str(t).strip() for t in all_topics if str(t).strip() not in ['-', '', 'nan', 'NaN']}
all_topics = list(all_topics)

# 각 주제별 현재 배정된 인원수 추적
topic_counts = {t: 0 for t in all_topics}

# 각 학생별 배정된 주제를 담을 리스트
assignments = {idx: [] for idx in df_merged.index}

# 💡 [핵심] 엑셀 1번 행부터 순서대로 내려가며 즉시 2개를 꽉 채움 (진정한 선착순)
for idx in df_merged.index:
    student_name = df_merged.loc[idx, key_column]

    # 이 학생의 1, 2, 3순위 희망 목록 가져오기
    choices = [
        str(df_merged.loc[idx, '1순위 희망']).strip(),
        str(df_merged.loc[idx, '2순위 희망']).strip(),
        str(df_merged.loc[idx, '3순위 희망']).strip()
    ]

    # [1단계] 본인이 적어낸 1, 2, 3순위를 검토하여 자리가 있으면 즉시 배정
    for choice in choices:
        # 이미 2개를 다 받았으면 더 이상 보지 않음
        if len(assignments[idx]) >= REQUIRED_TOPICS:
            break

        # 유효한 주제이고, 본인이 아직 배정받지 않았고, 정원(50명)이 남아있다면 배정!
        if choice in all_topics and choice not in assignments[idx]:
            if topic_counts[choice] < MAX_CAPACITY:
                assignments[idx].append(choice)
                topic_counts[choice] += 1

    # [2단계] 설문을 안 냈거나(전부 '-'), 희망한 주제가 50명이 다 차서 튕긴 경우
    # 남은 자리가 있는 주제 중에서 랜덤으로 강제 배정하여 2개를 무조건 채움
    while len(assignments[idx]) < REQUIRED_TOPICS:
        # 정원 미달이고, 이 학생이 아직 받지 않은 주제 찾기
        available_topics = [t for t in all_topics if topic_counts[t] < MAX_CAPACITY and t not in assignments[idx]]

        if not available_topics:
            print("\n🚨 [치명적 경고] 전체 주제의 총 정원(Capacity)이 부족하여 배정을 완료할 수 없습니다!")
            break

        # 남은 것 중 하나 랜덤 배정
        random_choice = random.choice(available_topics)
        assignments[idx].append(random_choice)
        topic_counts[random_choice] += 1

# ==========================================
# 4. 결과를 데이터프레임에 추가 및 저장
# ==========================================
df_merged['최종_배정1'] = [assignments[idx][0] if len(assignments[idx]) > 0 else '-' for idx in df_merged.index]
df_merged['최종_배정2'] = [assignments[idx][1] if len(assignments[idx]) > 1 else '-' for idx in df_merged.index]

print("\n✨ [최종 주제 배정 완료] 상위 15명 결과 미리보기:")
print(df_merged[['이름', '학번', '학과', '1순위 희망', '2순위 희망', '3순위 희망', '최종_배정1', '최종_배정2']].head(15))

print("\n📊 [각 주제별 최종 배정 인원 현황 (Max: 50명)]")
# 이름순 정렬해서 예쁘게 출력
for topic in sorted(topic_counts.keys()):
    count = topic_counts[topic]
    status = "꽉 참 🛑" if count == MAX_CAPACITY else "여유 🟢"
    print(f" - {topic:15s} : {count:2d}명 / {MAX_CAPACITY}명 [{status}]")
print("-" * 40)

# 엑셀 파일로 저장
df_merged.to_excel(output_file, index=False)
print(f"✅ 선착순 배정이 완료되었습니다. '{output_file}' 파일을 확인해주세요.")