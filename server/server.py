import streamlit as st
import numpy as np
import plotly.graph_objs as go

from mycache.array_db import load_array_from_db

MAX = 50.0
LENGTH = 15
NUM = 10


@st.cache_resource
def get_data() -> tuple[np.ndarray, np.ndarray]:
    # データベースからデータを取得
    mean = load_array_from_db("mean")
    eigenvecs = load_array_from_db("eigenvectors")
    eigenvecs = eigenvecs[:, :NUM]
    return mean, eigenvecs


def pca_contour_app(
    mean: np.ndarray, eigenvecs: np.ndarray, parameters_num: int
) -> None:
    st.title("PCA Contour Viewer")

    # レイアウトを2カラムに分割（左広め：右狭め）
    col1, col2 = st.columns([2, 1])

    # 右カラムにスライダー置く
    with col2:
        st.markdown("### パラメータ調整")
        params = []
        for i in range(parameters_num):
            param = st.slider(f"第 {i + 1} 主成分", -MAX, MAX, 0.0, step=0.1)
            params.append(param)
        params = np.array(params)

    # contours 計算
    contours = mean + eigenvecs @ params
    contours = contours.reshape(-1, 2)
    contours = contours[::10]

    with col1:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=contours[:, 0],
                y=contours[:, 1],
                mode="lines+markers",
                line=dict(shape="linear"),
                marker=dict(size=1, color="blue"),
            )
        )
        fig.update_layout(
            title="PCAによる輪郭再構成",
            xaxis=dict(scaleanchor="y", range=[-LENGTH, LENGTH]),
            yaxis=dict(scaleanchor="x", range=[-LENGTH, LENGTH]),
            margin=dict(l=0, r=0, t=30, b=0),
        )
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    mean, eigenvecs = get_data()

    pca_contour_app(mean, eigenvecs, NUM)
