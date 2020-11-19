import streamlit as st
import cv2
from PIL import Image
import numpy as np
import os

def detect_bugs(image):
    #Gray scale and blur the image
    img = np.array(image.convert('RGB'))
    imgGray = np.array(image.convert('L'))
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    height, width, channels = img.shape

    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 300
    #params.maxArea = 3000

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.01

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)

    #detector = cv2.SimpleBlobDetector_create()
    keypoints = detector.detect(imgBlur)
    imgKeyPoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Crop out keypoints
    os.mkdir("images")
    for keypoint in keypoints:
        filename = 1
        x = int(keypoint.pt[0])
        y = int(keypoint.pt[1])
        size = int(keypoint.size)
        crop = img[max(1,y-2*size): min(height-1,y+2*size), max(1,x-2*size): min(width-1,x+2*size)]
        st.image(crop, use_column_width = False)
        cv2.imwrite("images/" + str(filename) + ".jpg", crop)
    # Display found keypoints
    return imgKeyPoints


def about():
    info = '''
    <style>
    a {
        text-decoration: none;
        color: green !important;
    }

    a:hover {
        text-decoration: underline !important;
    }

    </style>

    <h3>Brought to you by <a href="https://grotech.berkeley.edu/static/index.html" target="_blank">Grotech @ Berkeley</a></h3>

    <p>Greenhouse laboratories, such as UC Berkeley's Oxford Greenhouse,
    employ yellow sticky traps to monitor and control plant pests. These traps
    capture hundreds of insects which are laborious to classify and count with the
     human eye. Our objective is to design an automated plant pest counter mobile app.
     The user takes a picture of the trap and an algorithm automatically classifies
     and counts the various pests present. </p>

     <img src="uploads/detected.jpg" height="600px">
    '''
    st.markdown(info, unsafe_allow_html=True)


def main():
    background_img = '''
    <style>
        body {
           background-image: url("https://lh3.googleusercontent.com/proxy/Ij_YGpsrh8AMukCLezadkJOFFx4Wup_weXfe23DkgHHiIsAnGHcoF9x_oZ42KDbWq-OyS5sEyYfopFUyq8XWm2JPgZ5B6sdeI4o3OxpN4STGS6JXEUvYyN2utKiAXrh10_ag");
           background-size: cover;
           color: green;
        }

        h1 {
            color: #454a52;
        }

        #logo {
            position: absolute;
            bottom: 0px;
            right: 0px;
            top: 40px;
            z-index: -1;
        }
    </style>
    <h1>PEST COUNTER APP</h1>
    <a href="https://grotech.berkeley.edu/static/index.html" target="_blank"><img id="logo" src="https://media-exp1.licdn.com/dms/image/C560BAQGxmyCSFNIIfQ/company-logo_200_200/0?e=2159024400&v=beta&t=yT4qrSL0jiHL-szBQ1zG3IVTHHNaiom9qWTNEvz8-bI" height="70px"></a>
    '''
    st.markdown(background_img, unsafe_allow_html=True)

    activities = ["Home", "About"]
    choice = st.sidebar.selectbox("Pick something fun", activities)

    if choice == "Home":
        st.write("**We count bugs :seedling: **")
        st.write("Upload an image of a sticky fly trap and our algorithm will detect the insects and display segmented images of each grid!")
        image_file = st.file_uploader("Upload image", type=['jpeg', 'png', 'jpg', 'webp'])
        if image_file is not None:
    	    image = Image.open(image_file)
    	    if st.button("Process"):
    		    detect_bugs(image=image)
    			#st.image(result_img, use_column_width = True)
    			#st.success("Found {} faces\n".format(len(result_faces)))

    elif choice == "About":
    	about()


if __name__ == "__main__":
    main()
