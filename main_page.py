from pathlib import Path
import streamlit as st
from PIL import Image
import base64


# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
resume_file = current_dir / "assets" / "CV_Camille_Bordes.pdf"
profile_pic = current_dir / "assets" / "profile-pic.png"
current_assets = current_dir / 'assets'


# --- GENERAL SETTINGS ---
PAGE_TITLE = "Portfolio | Camille Bordes"
PAGE_ICON = "🧑‍💻"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

st.sidebar.markdown("# 📚 My Portfolio")


# --- LOAD CSS, PDF & PROFIL PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
with open(resume_file, 'rb') as pdf_file:
    PDF_byte = pdf_file.read()
profile_pic = Image.open(profile_pic)


# --- PROFILE SECTION ---
NAME = "Camille Bordes"
DESCRIPTION = """
Hey I'm Camille, currently in my 2nd year of engineering studies (M1) at EFREI Paris. 
I'm studying in the Data & AI major and will soon be joining the startup Ormex as an artificial intelligence intern.
On this site, you can access my CV, contact details and all my projects. Don't hesitate to contact me !
"""
EMAIL = "camille.bordes@efrei.net"

col1, col2 = st.columns(2, gap="small")
with col1:
    st.image(profile_pic, width=230)

with col2:
    st.title(NAME)
    st.write(DESCRIPTION)
    st.download_button(
        label="📑 Download Resume",
        data=PDF_byte,
        file_name=resume_file.name,
        mime="application/octet-stream",
    )
    st.write('📧', EMAIL)


# --- CONTACTS ---
SOCIAL_MEDIA = {
    "GitHub": "https://github.com/camm22",
    "LinkedIn": "https://www.linkedin.com/public-profile/settings?trk=d_flagship3_profile_self_view_public_profile",
    "LeetCode": "https://leetcode.com/u/Camm2/",
    "Kaggle": "https://www.kaggle.com/camillebordes"
}

st.write("### 📲 Add me !")
st.write('---')
cols = st.columns(len(SOCIAL_MEDIA))

for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    with cols[index]:
        if st.button(platform):
            js = f"window.open('{link}')"
            st.components.v1.html(f"<script>{js}</script>")


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
      img_to_bytes(img_path)
    )
    return img_html

# --- PROJECTS ---
PROJECTS = [
    {
        "title": "Machine Learning Project",
        "description": """
                    Preparation, cleaning, analysis of the dataset pima indians diabetes.
                    Testing of numerous machine learning alogorithms: Linear Regression, KNN, MLP, Decision Tree, Random Forest to detect the presence or absence of diabetes.
                    """,
        "image": current_assets / "Machine-Learning.png",  
        "link": "https://github.com/camm22/Machine-Learning-Project_on_pima_indians_diabetes_dataset"
    },
    {
        "title": "FastPatent",
        "description": """
                    NLP AI: fine-tuning the DEBERTA model via PyTorch. For patent classification (group and subgroup). 
                    NLP training for the professional certification “Développer une solution d'intelligence artificielle (Machine et Deep Learning)” (RNCP n° 36129)
                    """,
        "image": current_assets / "NLP.png",  
        "link": "https://github.com/camm22/FastPatent"
    },
    {
        "title": "Mini Project Data Science",
        "description": """
                    Preparation, cleaning, analysis and prediction on a large dataset of land value requests using Pandas, NumPy, Matplotlib and Scikit-learn. 
                    Standardization with PCA, implementation of linear regression, and clustering with K-means. 
                    """,
        "image": current_assets / "DVF.jpg",  
        "link": "https://github.com/camm22/Mini-Project-Data-Science"
    },
    {
        "title": "NeuroVision",
        "description": """
                    Detection of brain tumors on an MRI image. 
                    Binary uni-modalbinary uni-modal
                    """,
        "image": current_assets / "NeuroVision.png",  
        "link": "https://github.com/camm22/NeuroVision?tab=readme-ov-file"
    },
    {
        "title": "Automates Project",
        "description": """
                    Implementation of numerous algorithms.
                    """,
        "image": current_assets / "Automate.png",  
        "link": "https://github.com/camm22/Finite-Automata-and-Rational-Expressions-Project"
    },
    {
        "title": "Graph Theory Project",
        "description": """
                    Implementation of numerous algorithms. 
                    Visualization with matplotlib and networkx.
                    """,
        "image": current_assets / "graphe.png",  
        "link": "https://github.com/camm22/Projet_Graphes"
    },
    {
        "title": "Social Event Management",
        "description": """
                    Web application: Vue.js, Node.js and phpMyAdmin.
                    Development of a web application to manage any event proposed by events proposed by different users.
                    """,
        "image": current_assets / "share.jpeg",  
        "link": "https://github.com/camm22/Social-Event-Management"
    },
    {
        "title": "C-language sentence generator",
        "description": """
                    Randomly generates orthographically and grammatically correct French sentences from a huge dictionary of words.
                    """,
        "image": current_assets / "arbre.png",  
        "link": "https://github.com/camm22/Exquisite-Cadaver-Game"
    },
    {
        "title": "Takuzu Game",
        "description": """
                    The takuzu game in C language. 4x4 and 8x8 grid.
                    """,
        "image": current_assets / "takuzu.png",  
        "link": "https://github.com/camm22/Takuzu-Game"
    },
    {
        "title": "Urban Fighter",
        "description": """
                    Development of a 2D “Street Fighter” style game in python with pygames. 
                    Implementation of physics and trajectory curves.
                    """,
        "image": current_assets / "urban.png",  
        "link": "https://github.com/camm22/Urban-Fighter"
    },
]

st.write("####")
st.write("### 📁My Projects")
st.write('---')
cols = st.columns(2)

for index, project in enumerate(PROJECTS):
    with cols[index % 2]:
        st.markdown(f"""
        <div class="card">
            {img_to_html(project['image'])}
            <p class="titre">{project['title']}</p>
            <p>{project['description']}</p>
            <a href="{project['link']}" target="_blank">
                <button>See project</button>
            </a>
        </div>
        """, unsafe_allow_html=True)
