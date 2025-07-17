import streamlit as st
import numpy as np
import tensorflow
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
from huggingface_hub import hf_hub_download
import json
from PIL import Image

st.title("🐚🥥 EffiB0 이미지 분류기")
st.write("이 이미지 분류기는 coconut,conch를 분류해주는 분류기입니다.")
st.image(
    ["coconut,png","conch.png"],
    caption=["코코넛","소라"],
    use_column_width=True
)

# 모델 및 클래스 불러오기
@st.cache_resource
def load_model_and_labels():
    model_path = hf_hub_download(repo_id="eu-001/conch_coconut_cnn", filename="EffiB0_test.h5")
    label_path = hf_hub_download(repo_id="eu-001/conch_coconut_cnn", filename="EffiB0_test.json")

    model = load_model(model_path)
    with open(label_path, 'r') as f:
        class_names = json.load(f)  # 리스트 또는 딕셔너리 확인 필요

    return model, class_names

model, class_names = load_model_and_labels()

# 사용자 이미지 업로드
uploaded_file = st.file_uploader("이미지를 업로드하세요 (jpg/png)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 이미지 로딩
    img = Image.open(uploaded_file).convert('RGB')
    st.image(img, caption='업로드된 이미지', use_column_width=True)

    # 전처리
    IMG_HEIGHT = 224
    IMG_WIDTH = 224
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    img_array = image.img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    # 예측
    predictions = model.predict(img_array)
    predicted_class = class_names[np.argmax(predictions)]

    st.markdown(f"### ✅ 예측 결과: **{predicted_class}**")
    st.markdown("### 🔢 클래스별 확률")
    for i, prob in enumerate(predictions[0]):
        st.write(f"{class_names[i]}: {prob:.4f}")
