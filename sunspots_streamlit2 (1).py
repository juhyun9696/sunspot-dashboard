# -*- coding: utf-8 -*-
"""sunspots_streamlit2

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wRCI7Q4JHe7Ewlz8w5lByaprqmd-N5iP
"""

# sunspot_app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# -------------------------------
# 1. 데이터 불러오기 (파일 경로 고정)
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("sunspots.csv")
    df['YEAR_INT'] = df['YEAR'].astype(int)
    df['DATE'] = pd.to_datetime(df['YEAR_INT'].astype(str), format='%Y')
    df.set_index('DATE', inplace=True)
    return df

# -------------------------------
# 2. 시각화 함수
# -------------------------------
def plot_advanced_sunspot_visualizations(df, sunactivity_col='SUNACTIVITY'):
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle("Sunspots Data Advanced Visualization", fontsize=18)

    # (a) 시계열
    axs[0, 0].plot(df.index, df[sunactivity_col], color='blue', alpha=0.7)
    axs[0, 0].set_title("Sunspot Activity Over Time")
    axs[0, 0].set_xlabel("Year")
    axs[0, 0].set_ylabel("Sunspot Count")
    axs[0, 0].grid(True)

    # (b) 분포
    data = df[sunactivity_col].dropna().values
    if len(data) > 0:
        xs = np.linspace(data.min(), data.max(), 200)
        density = gaussian_kde(data)
        axs[0, 1].hist(data, bins=30, density=True, alpha=0.6, color='gray', label='Histogram')
        axs[0, 1].plot(xs, density(xs), color='red', linewidth=2, label='Density')

    axs[0, 1].set_title("Distribution of Sunspot Activity")
    axs[0, 1].set_xlabel("Sunspot Count")
    axs[0, 1].set_ylabel("Density")
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # (c) 상자 그림: 1900~2000
    try:
        df_20th = df.loc["1900":"2000"]
        if not df_20th.empty:
            axs[1, 0].boxplot(df_20th[sunactivity_col].dropna(), vert=False)
    except:
        pass
    axs[1, 0].set_title("Boxplot of Sunspot Activity (1900-2000)")
    axs[1, 0].set_xlabel("Sunspot Count")

    # (d) 산점도 + 회귀선
    years = df['YEAR'].values
    sun_activity = df[sunactivity_col].values
    mask = ~np.isnan(sun_activity)
    years_clean = years[mask]
    sun_activity_clean = sun_activity[mask]

    if len(years_clean) > 1:
        axs[1, 1].scatter(years_clean, sun_activity_clean, s=10, alpha=0.5, label='Data Points')
        coef = np.polyfit(years_clean, sun_activity_clean, 1)
        trend = np.poly1d(coef)
        axs[1, 1].plot(years_clean, trend(years_clean), color='red', linewidth=2, label='Trend Line')

    axs[1, 1].set_title("Trend of Sunspot Activity")
    axs[1, 1].set_xlabel("Year")
    axs[1, 1].set_ylabel("Sunspot Count")
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig

# -------------------------------
# 3. Streamlit 앱 실행
# -------------------------------
st.title('🌞 태양흑점 데이터 분석 대시보드 🌞')
st.markdown("이 대시보드는 태양흑점 데이터를 다양한 시각화 방법으로 보여줍니다.")

try:
    # 데이터 로드
    df = load_data()

    # 필터링된 데이터 - 전체 데이터 사용
    filtered_df = df

    # 시각화
    if not filtered_df.empty:
        st.subheader('태양흑점 데이터 종합 시각화')
        fig = plot_advanced_sunspot_visualizations(filtered_df)
        st.pyplot(fig)
    else:
        st.warning("데이터가 없습니다.")

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
    st.info("데이터 파일의 구조를 확인해주세요. 'data/sunspots.csv' 파일이 존재하고 'YEAR'와 'SUNACTIVITY' 컬럼이 있어야 합니다.")

