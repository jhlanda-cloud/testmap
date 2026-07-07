# ☕ 제주도 카페 지도 시각화

제주도 상권 데이터에서 **카페**만 추출해 지도 위에 위치·주소와 함께 시각화하는 Streamlit 앱입니다.

## 주요 기능

- 제주도 지도 위에 카페 위치 마커 표시 (클러스터링)
- **시군구별 색상 구분** (제주시 / 서귀포시) + 범례
- 마커 팝업: 상호명 · 지역 · 주소
- 사이드바 필터: 시군구 · 카페명 검색 · 표시 개수 조절
- 카페 목록 테이블

## 파일 구성

| 파일 | 설명 |
|------|------|
| `app.py` | Streamlit 앱 본체 |
| `제주상권.csv` | 원본 상권 데이터 (cp949 인코딩) |
| `requirements.txt` | 의존 패키지 |
| `runtime.txt` | Python 버전 (3.13) |
| `.streamlit/config.toml` | 테마 설정 |

## 로컬 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

브라우저에서 http://localhost:8501 접속.

## Streamlit Community Cloud 배포

1. **GitHub 저장소 준비** — 이 폴더 전체(`app.py`, `제주상권.csv`, `requirements.txt`, `runtime.txt`, `.streamlit/`)를 GitHub에 푸시합니다.

   ```bash
   git init
   git add .
   git commit -m "제주도 카페 지도 앱"
   git branch -M main
   git remote add origin https://github.com/<사용자명>/<저장소명>.git
   git push -u origin main
   ```

2. **배포** — https://share.streamlit.io 접속 → GitHub 로그인 → **New app** 클릭.
   - Repository: 위에서 만든 저장소
   - Branch: `main`
   - Main file path: `app.py`
   - (Advanced) Python version: **3.13**
   - **Deploy** 클릭

3. 몇 분 뒤 `https://<앱이름>.streamlit.app` 주소로 공개됩니다.

## 데이터 출처

소상공인시장진흥공단 상가(상권)정보 — 제주 지역.
`상권업종소분류명 == "카페"` 조건으로 순수 카페 2,912개만 사용 (독서실/스터디 카페 제외).
