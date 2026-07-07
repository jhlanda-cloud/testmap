import pandas as pd
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import st_folium

# ------------------------------------------------------------------
# 기본 설정
# ------------------------------------------------------------------
st.set_page_config(page_title="제주도 카페 지도", page_icon="☕", layout="wide")
st.title("☕ 제주도 카페 혼저 옵서예")

CSV_PATH = "제주상권.csv"

# 시군구별 색상 매핑 (folium 아이콘 색)
SIGUNGU_COLORS = {
    "제주시": "blue",
    "서귀포시": "red",
}
DEFAULT_COLOR = "gray"


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """CSV(cp949)를 읽어 '카페'만 추출하고 좌표가 유효한 행을 반환한다."""
    df = pd.read_csv(path, encoding="cp949")
    # 카페만 필터 (상권업종소분류명 == '카페')
    df = df[df["상권업종소분류명"] == "카페"].copy()
    # 위도/경도 숫자화 및 결측 제거
    df["위도"] = pd.to_numeric(df["위도"], errors="coerce")
    df["경도"] = pd.to_numeric(df["경도"], errors="coerce")
    df = df.dropna(subset=["위도", "경도"])
    # 주소: 도로명주소 우선, 없으면 지번주소
    df["주소"] = df["도로명주소"].fillna(df["지번주소"]).fillna("주소 정보 없음")
    return df


df = load_data(CSV_PATH)

# ------------------------------------------------------------------
# 사이드바 필터
# ------------------------------------------------------------------
st.sidebar.header("🔎 필터")

# 시군구 필터
sigungu_list = ["전체"] + sorted(df["시군구명"].dropna().unique().tolist())
sel_sigungu = st.sidebar.selectbox("시군구", sigungu_list)

# 상호명 검색
keyword = st.sidebar.text_input("카페명 검색 (일부 입력)")

# 필터 적용
filtered = df.copy()
if sel_sigungu != "전체":
    filtered = filtered[filtered["시군구명"] == sel_sigungu]
if keyword:
    filtered = filtered[filtered["상호명"].str.contains(keyword, case=False, na=False)]

# 성능을 위한 최대 마커 수 제한
max_markers = st.sidebar.slider("지도에 표시할 최대 개수", 100, 3000, 1500, step=100)
total = len(filtered)
if total > max_markers:
    filtered = filtered.sample(max_markers, random_state=42)

# ------------------------------------------------------------------
# 요약 정보
# ------------------------------------------------------------------
c1, c2, c3 = st.columns(3)
c1.metric("전체 카페 수", f"{len(df):,} 개")
c2.metric("필터 결과", f"{total:,} 개")
c3.metric("지도 표시 개수", f"{len(filtered):,} 개")
if total > max_markers:
    st.info(f"결과가 많아 무작위 {max_markers:,}개만 지도에 표시합니다. 필터를 좁혀보세요.")

# ------------------------------------------------------------------
# 지도 생성
# ------------------------------------------------------------------
지도 = folium.Map(location=[33.3694, 126.5298], zoom_start=11)
묶음 = MarkerCluster().add_to(지도)

for _, row in filtered.iterrows():
    sigungu = row["시군구명"]
    color = SIGUNGU_COLORS.get(sigungu, DEFAULT_COLOR)
    popup_html = (
        f"<b>{row['상호명']}</b><br>"
        f"지역: {sigungu}<br>"
        f"주소: {row['주소']}"
    )
    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=row["상호명"],
        icon=folium.Icon(color=color, icon="coffee", prefix="fa"),
    ).add_to(묶음)

# 시군구별 색상 범례 (지도 위 고정)
legend_items = "".join(
    f'<div style="margin:2px 0;">'
    f'<span style="display:inline-block;width:12px;height:12px;background:{c};'
    f'border-radius:50%;margin-right:6px;"></span>{sg}</div>'
    for sg, c in SIGUNGU_COLORS.items()
)
legend_html = f"""
<div style="position:fixed; bottom:30px; left:30px; z-index:9999;
     background:white; padding:10px 14px; border:1px solid #999; border-radius:6px;
     font-size:13px; box-shadow:2px 2px 6px rgba(0,0,0,0.2);">
  <b>☕ 카페 (시군구)</b>{legend_items}
</div>
"""
지도.get_root().html.add_child(folium.Element(legend_html))

st_folium(지도, width=None, height=600, returned_objects=[])

# ------------------------------------------------------------------
# 데이터 테이블
# ------------------------------------------------------------------
with st.expander("📋 표시된 카페 목록 보기"):
    st.dataframe(
        filtered[["상호명", "시군구명", "주소", "위도", "경도"]].reset_index(drop=True),
        use_container_width=True,
    )
