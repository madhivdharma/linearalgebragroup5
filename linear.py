# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# --- Fungsi matriks transformasi 3x3 dalam koordinat homogen ---

def translation_matrix(tx, ty):
    # Matriks translasi
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])

def scaling_matrix(sx, sy):
    # Matriks penskalaan
    return np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])

def rotation_matrix(theta_deg):
    # Matriks rotasi dengan sudut theta (derajat), positif = CCW
    theta = np.radians(theta_deg)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    return np.array([
        [cos_t, -sin_t, 0],
        [sin_t, cos_t, 0],
        [0, 0, 1]
    ])

def shearing_matrix(shx, shy):
    # Matriks shear
    return np.array([
        [1, shx, 0],
        [shy, 1, 0],
        [0, 0, 1]
    ])

def reflection_matrix(kind):
    # Matriks refleksi terhadap x, y, y=x, atau origin
    if kind == "Sumbu X":
        return np.array([
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ])
    elif kind == "Sumbu Y":
        return np.array([
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
    elif kind == "Garis y = x":
        return np.array([
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])
    elif kind == "Titik Origin":
        return np.array([
            [-1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ])
    else:
        return np.identity(3)

# --- Definisi bentuk dasar (segitiga) dalam koordinat homogen ---
# Titik dalam bentuk (x, y, 1)
base_shape = np.array([
    [0, 0, 1],
    [1, 0, 1],
    [0.5, 1, 1],
    [0, 0, 1]  # Tutup poligon segitiga
]).T  # shape 3x4 (x, y, 1)

# --- Fungsi untuk memperlihatkan bentuk dengan matplotlib ---
def plot_shapes(original, transformed):
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].plot(original[0, :], original[1, :], "o-", color="#10B981")
    axes[0].set_title("Bentuk Asli", color="#10B981")
    axes[0].axis('equal')
    axes[0].grid(True, linestyle='--', alpha=0.5)

    axes[1].plot(transformed[0, :], transformed[1, :], "o-", color="orange")
    axes[1].set_title("Bentuk Hasil Transformasi", color="#10B981")
    axes[1].axis('equal')
    axes[1].grid(True, linestyle='--', alpha=0.5)

    for ax in axes:
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)

    plt.tight_layout()
    return fig

# --- Fungsi menggabungkan transformasi sesuai urutan ---
def compose_transformations(order, params):
    mat_dict = {
        "Translation": translation_matrix(params['tx'], params['ty']),
        "Scaling": scaling_matrix(params['sx'], params['sy']),
        "Rotation": rotation_matrix(params['theta']),
        "Shearing": shearing_matrix(params['shx'], params['shy']),
        "Reflection": reflection_matrix(params['reflection'])
    }
    # Kali matriks sesuai urutan
    composite = np.identity(3)
    for name in order:
        composite = mat_dict[name] @ composite
    return composite, mat_dict

# --- UI Streamlit ---

st.set_page_config(page_title="Demo Transformasi Matriks 2D (Koordinat Homogen)", layout="wide")

st.title("Demo Interaktif Transformasi Matriks 2D dengan Koordinat Homogen")
st.markdown(
    """
    Aplikasi ini membantu memahami bagaimana transformasi 2D seperti translasi, penskalaan, rotasi, shearing, dan refleksi dapat direpresentasikan sebagai matriks 3x3 dalam koordinat homogen.
    Dengan koordinat homogen, semua transformasi dapat digabungkan (komposit) hanya dengan perkalian matriks, sehingga memudahkan visualisasi dan analisis dalam grafik komputer dan aljabar linear.
    """
)

# Sidebar untuk input parameter transformasi
st.sidebar.header("Pengaturan Transformasi")

tx = st.sidebar.slider("Translasi: tx", -2.0, 2.0, 0.0, 0.1)
ty = st.sidebar.slider("Translasi: ty", -2.0, 2.0, 0.0, 0.1)

sx = st.sidebar.slider("Penskalaan: sx", 0.1, 3.0, 1.0, 0.1)
sy = st.sidebar.slider("Penskalaan: sy", 0.1, 3.0, 1.0, 0.1)

theta = st.sidebar.slider("Rotasi: θ (derajat)", -180, 180, 0, 1)

shx = st.sidebar.slider("Shearing: shx", -2.0, 2.0, 0.0, 0.1)
shy = st.sidebar.slider("Shearing: shy", -2.0, 2.0, 0.0, 0.1)

reflection_type = st.sidebar.selectbox("Refleksi terhadap:", ("Tidak Ada", "Sumbu X", "Sumbu Y", "Garis y = x", "Titik Origin"))

# Pilihan urutan komposisi transformasi
st.sidebar.markdown("---")
st.sidebar.subheader("Urutan Komposisi Transformasi")
default_order = ["Translation", "Rotation", "Scaling"]
order = st.sidebar.multiselect(
    "Pilih dan urutkan transformasi (drag & drop tidak didukung, pilih urut dari atas ke bawah)",
    options=["Translation", "Scaling", "Rotation", "Shearing", "Reflection"],
    default=default_order
)

# Jika Reflection "Tidak Ada", buang dari order
if "Reflection" in order and reflection_type == "Tidak Ada":
    st.sidebar.warning("Anda memilih Reflection dalam urutan, tapi tipe refleksi 'Tidak Ada'.")
elif "Reflection" not in order and reflection_type != "Tidak Ada":
    # Auto tambahkan reflection ke akhir jika dipilih tipe refleksi selain 'Tidak Ada'
    order.append("Reflection")

# Parameter dictionary
params = {
    'tx': tx,
    'ty': ty,
    'sx': sx,
    'sy': sy,
    'theta': theta,
    'shx': shx,
    'shy': shy,
    'reflection': reflection_type if reflection_type != "Tidak Ada" else None
}

# Matriks transformasi dan komposit
composite_matrix, matrices = compose_transformations(order, params)

# Transformasi bentuk dasar
transformed_shape = composite_matrix @ base_shape

# Visualisasi bentuk asli dan bentuk hasil transformasi
fig = plot_shapes(base_shape, transformed_shape)
st.pyplot(fig)

# Tampilkan matriks transformasi
st.subheader("Matriks Transformasi 3x3")
for name in order:
    st.markdown(f"**{name}**")
    st.write(matrices[name])

st.markdown("**Matriks Komposit (hasil perkalian semua transformasi sesuai urutan):**")
st.write(composite_matrix)

# Tabel koordinat
st.subheader("Tabel Koordinat Titik")
n_points = base_shape.shape[1]
data = []
for i in range(n_points):
    x, y = base_shape[0, i], base_shape[1, i]
    x_t, y_t = transformed_shape[0, i], transformed_shape[1, i]
# Matriks Komposit
st.markdown("**Matriks Komposit (hasil perkalian semua transformasi sesuai urutan):**")
st.write(composite_matrix)

# TABEL KOORDINAT - VERSI BENAR (HANYA INI)
st.subheader("Tabel Koordinat Titik")
n_points = base_shape.shape[1]
data = []
for i in range(n_points):
    x, y = base_shape[0, i], base_shape[1, i]
    x_t, y_t = transformed_shape[0, i], transformed_shape[1, i]
    data.append([x, y, x_t, y_t])

df = pd.DataFrame(data, columns=["x", "y", "x' (hasil)", "y' (hasil)"])
st.dataframe(df)  # ✅ HANYA df, tanpa parameter columns
