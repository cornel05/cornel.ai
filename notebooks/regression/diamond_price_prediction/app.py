import streamlit as st
import numpy as np
from pathlib import Path


ROOT = Path(__file__).parent
model = np.load(ROOT / "weight.npz")

x_mean = model['x_mean']
x_std = model['x_std']
theta = model['theta']
@st.cache_resource

def predict(carat, cut, color, clarity, depth, table, x, y, z, x_mean, x_std, theta):
    # Mapping for cut
    cut_mapping = {'Fair': 0, 'Good': 1, 'Very Good': 2, 'Premium': 3, 'Ideal': 4}
    # Mapping for color
    color_mapping = {'J': 0, 'I': 1, 'H': 2, 'G': 3, 'F': 4, 'E': 5, 'D': 6}
    # Mapping for clarity
    clarity_mapping = {'I1': 0, 'SI2': 1, 'SI1': 2, 'VS2': 3, 'VS1': 4, 'VVS2': 5, 'VVS1': 6, 'IF': 7}
    
    # .get() is python dict methods, to get value of a key if exists, else to default (0 here)
    cut = cut_mapping.get(cut, 0)
    color = color_mapping.get(color, 0)
    clarity = clarity_mapping.get(clarity, 0)
    
    # Create input array of shape (1,9)
    input = np.array([[carat, cut, color, clarity, depth, table, x, y, z]], dtype='float')
    
    # Normalize input
    input = (input - x_mean) / x_std
    input = np.hstack([np.ones((input.shape[0], 1)), input])
    prediction = input @ theta
    return prediction

st.snow()

# Add title for my app
st.title('💎DIAMOND PRICE PREDICTION 💎')

st.header('Vui lòng nhập các đặc trưng của viên kim cương bạn muốn mua:')
carat = st.number_input('Carat Weight:', min_value=0.1, max_value=10.0, value=1.0)
cut = st.selectbox('Cut Rating:', ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal'])
color = st.selectbox('Color Rating:', ['J', 'I', 'H', 'G', 'F', 'E', 'D'])
clarity = st.selectbox('Clarity Rating:', ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF'])
depth = st.number_input('Diamond Depth Percentage:', min_value=0.1, max_value=100.0, value=1.0)
table = st.number_input('Diamond Table Percentage:', min_value=0.1, max_value=100.0, value=1.0)
x = st.number_input('Diamond Length (X) in mm:', min_value=0.1, max_value=100.0, value=1.0)
y = st.number_input('Diamond Width (Y) in mm:', min_value=0.1, max_value=100.0, value=1.0)
z = st.number_input('Diamond Height (Z) in mm:', min_value=0.1, max_value=100.0, value=1.0)
if st.button('Predict Price'):
    out = predict(carat, cut, color, clarity, depth, table, x, y, z, x_mean, x_std, theta)
    st.success(f'Giá dự đoán của viên kim cương là: ${out[0,0]:.2f} USD')