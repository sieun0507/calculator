import pandas as pd
import requests
from datetime import datetime
import time

# 사용자 설정
NOTION_TOKEN = "노션 API 입력(따옴표 포함)"
DATABASE_ID = "노션 데이터베이스 ID입력(따옴표 포함)"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# 엑셀 파일 경로 (한글 경로도 가능)
excel_path = r"거래내역 엑셀 파일 절대 경로 입력"
 # 엑셀에서 거래내역의 머리글(헤더) 시작 행 (기본: 11 → 실제로는 12번째 줄)
df = pd.read_excel(excel_path, header=11)
df = df[df["입금금액"].notna() | df["출금금액"].notna()]
df = df.fillna("")

def get_unique_id(row):
    return f"{row['거래일시']}_{row['입금금액']}_{row['출금금액']}_{row['거래내용']}"

def is_duplicate(unique_id):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {
        "filter": {
            "property": "고유값",
            "rich_text": {
                "equals": unique_id
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return len(result["results"]) > 0
    else:
        print(f"❗ 중복 확인 실패: {response.status_code}, {response.text}")
        return False

for _, row in df.iterrows():
    try:
        # 날짜 변환
        date_raw = str(row["거래일시"]).strip()
        date_obj = datetime.strptime(date_raw, "%Y/%m/%d %H:%M:%S")
        iso_date = date_obj.isoformat()
    except Exception as e:
        print(f"날짜 변환 실패: {row['거래일시']} → {e}")
        continue

    # 금액, 구분
    if row["입금금액"]:
        amount = float(row["입금금액"])
        category = "입금"
    elif row["출금금액"]:
        amount = -float(row["출금금액"])
        category = "출금"
    else:
        amount = 0
        category = "기타"

    # 설명: 거래기록사항 우선
    description = (
        str(row["거래기록사항"]).strip()
        if "거래기록사항" in row and pd.notna(row["거래기록사항"]) and str(row["거래기록사항"]).strip()
        else str(row["거래내용"]).strip()
    )

    # 고유 ID 생성
    unique_id = get_unique_id(row)
    if is_duplicate(unique_id):
        print(f"🔁 이미 존재하는 거래입니다: {unique_id}")
        continue

    # Notion 데이터 전송
    notion_data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "날짜": {"date": {"start": iso_date}},
            "금액": {"number": amount},
            "잔액": {"number": float(row["거래후잔액"]) if row["거래후잔액"] else 0},
            "거래내용": {
                "title": [{
                    "text": {"content": description}
                }]
            },
            "계좌": {"select": {"name": "농협"}},
            "구분": {"select": {"name": category}},
            "고유값": {"rich_text": [{"text": {"content": unique_id}}]}
        }
    }

    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=notion_data)
    if response.status_code == 200:
        print(f"✅ 등록 완료: {description}")
    else:
        print(f"❌ 등록 실패: {response.status_code} - {response.text}")
    
    time.sleep(0.3)  # Notion API 과도 요청 방지

