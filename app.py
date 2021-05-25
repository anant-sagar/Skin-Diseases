import os
import streamlit as st
from streamlit.proto.Selectbox_pb2 import Selectbox
from db import Image
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


st.title("Skin Diseases Prediction")
st.image("images/s.png")

st.success("""we propose an image processing based approach to diagnose skin diseases. This method takes 
the digital image of disease effect skin area then use image analysis to identify the type of disease. Our
proposed approach is simple, fast and does not require expensive equipment's other than a camera and a computer.""")



def opendb():
    engine = create_engine('sqlite:///db.sqlite3') # connect
    Session =  sessionmaker(bind=engine)
    return Session()

def save_file(file,path):
    try:
        db = opendb()
        ext = file.type.split('/')[1] # second piece
        img = Image(filename=file.name,extension=ext,filepath=path)
        db.add(img)
        db.commit()
        db.close()
        return True
    except Exception as e:
        st.write("database error:",e)
        return False

if st.checkbox("About"):
    st.markdown("""Skin diseases are more common than other diseases. Skin diseases may be caused by fungal infection, bacteria,
allergy, or viruses, etc. A skin disease may change texture or color of the skin. In general, skin diseases are chronic,
infectious and sometimes may develop into skin cancer. Therefore, skin diseases must be diagnosed early to reduce their development and spread. The diagnosis and treatment of a skin disease takes longer time and causes financial
and physical cost to the patient""")

    st.markdown("""In general, most of the common people do not know the type and stage of a skin disease. Some of the skin
diseases show symptoms several months later, causing the disease to develop and grow further. This is due to the
lack of medical knowledge in the public. Sometimes, a dermatologist (skin specialist doctor) may also find it
difficult to diagnose the skin disease and may require expensive laboratory tests to correctly identify the type and
stage of the skin disease. The advancement of lasers and photonics based medical technology has made it possible to
diagnose the skin diseases much more quickly and accurately. But the cost of such diagnosis is still limited and very
expensive. Therefore, we propose an image processing-based approach to diagnose the skin diseases. This method
takes the digital image of disease effect skin area then use image analysis to identify the type of disease. Our
proposed approach is simple, fast and does not require expensive equipment's other than a camera and a computer.""")


if st.checkbox('Upload Images'):
    file = st.file_uploader("select a image",type=['jpg','png'])
    if file is not None:
        if file and st.button('Upload'):
            file_details = {"FileName":file.name,"FileType":file.type,"FileSize":file.size}
            st.write(file_details)
            path = os.path.join('uploads',file.name)
            with open(path,'wb') as f:
                f.write(file.getbuffer())
                status = save_file(file,path)
                if status:
                    st.sidebar.success("file uploaded")
                    st.sidebar.image(path,use_column_width=True)
                else:
                    st.sidebar.error('upload failed')
        

if st.checkbox('Predict/view'):
    db = opendb()
    results = db.query(Image).all()
    db.close()
    img = st.sidebar.radio('select image',results)
    if img and os.path.exists(img.filepath):
        st.sidebar.info("selected img")
        st.sidebar.image(img.filepath, use_column_width=True)
        if st.sidebar.button("predict"):
            st.title(f"{img.filename} predicting.....")
        

if st.checkbox('Delete Record'):
    db = opendb()
    results = db.query(Image).all()
    db.close()
    img = st.sidebar.radio('select image to remove',results)
    if img:
        st.error("img to be deleted")
        if os.path.exists(img.filepath):
            st.image(img.filepath, use_column_width=True)
        if st.sidebar.button("delete"): 
            try:
                db = opendb()
                db.query(Image).filter(Image.id == img.id).delete()
                if os.path.exists(img.filepath):
                    os.unlink(img.filepath)
                db.commit()
                db.close()
                st.info("image deleted")
            except Exception as e:
                st.error("image not deleted")
                st.error(e)