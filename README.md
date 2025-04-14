# 🧾 노션과 연동된 가계부 자동화 시스템

> **엑셀로 저장된 금융거래내역**을 기반으로  
> **노션 가계부에 자동으로 입력**하는 파이썬 프로그램입니다.

---

## 📌 주요 기능

- **엑셀 파일(.xlsx)**에서 거래 데이터를 읽어옴
- **날짜, 거래 내용, 금액, 입출금 구분**을 자동으로 처리
- **입금 시 +금액**, **출금 시 -금액**으로 변환
- 거래 내역 중 **중복 항목은 등록되지 않도록 방지**
- 노션 API를 이용해 **자동으로 데이터베이스에 입력**

---

## 🗂️ 사용 방법

# 💰 Notion 가계부 자동 등록기

농협 Excel 금융거래내역을 Notion 데이터베이스에 자동으로 등록하는 파이썬 스크립트입니다.  
입출금 내역을 자동으로 인식하고, 날짜/금액/계좌/구분 등의 정보를 정리해 Notion에 깔끔하게 저장해줍니다.

---

## 📌 주요 기능

- 엑셀에서 거래내역 자동 파싱 (입출금 구분 포함)
- Notion 데이터베이스와 연동하여 자동 등록
- 중복 거래 방지를 위한 **고유값** 체크
- 거래기록이 없으면 **거래 내용**으로 대체

---

## 🛠️ 사용 방법

### 1. 노션 API 연동 준비

1. [Notion Developers](https://www.notion.so/my-integrations)에서 **새로운 통합 (Integration)** 생성
2. 생성된 통합에서 **Internal Integration Token** 복사
3. 가계부 데이터베이스 페이지에서 해당 통합에 대한 **공유 권한 부여**
4. 데이터베이스 링크(URL)에서 **Database ID** 추출  
 예 : 'https://www.notion.so/yourworkspace/자동-가계부-1234567890abcdef1234567890abcdef' 중 '1234567890abcdef1234567890abcdef' 
---

### 2. 엑셀 파일 설정

- `EXCEL_FILE_PATH`: 불러올 **엑셀 파일의 전체 경로** 입력 (한글 경로도 가능)
- `EXCEL_HEADER_ROW`: **거래내역이 시작되는 행 번호 - 1** 설정  
  예: 거래내역이 12번째 줄부터 시작되면 → `EXCEL_HEADER_ROW = 11`

---

## 🐍 파이썬 코드 주요 설정

### pip 설치
```python
pip install pandas requests openpyxl
```

### 🔧 직접 입력해야 하는 부분

```python
NOTION_API_KEY = "your_notion_api_key"
DATABASE_ID = "your_notion_database_id"
EXCEL_FILE_PATH = r"C:\경로\거래내역.xlsx"
df = pd.read_excel(excel_path, header=11)

