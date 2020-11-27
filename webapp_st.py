import streamlit as st
import streamlit.components.v1 as components
import cv2
from PIL import Image
import numpy as np
import os
import base64

from streamlit.hashing import _CodeHasher
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server

def display_state_values(state):
    st.write("Accuracy: ", state.numBugs / state.totalImgs)

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

    state = _get_state()
    state.numBugs = 0
    state.totalImgs = len(keypoints)
    display_state_values(state)

    # Crop out keypoints
    if not os.path.exists('immages'):
        os.mkdir("immages")
    filename = 0
    for keypoint in keypoints:
        filename += 1
        x = int(keypoint.pt[0])
        y = int(keypoint.pt[1])
        size = int(keypoint.size)
        crop = img[max(1,y-2*size): min(height-1,y+2*size), max(1,x-2*size): min(width-1,x+2*size)]
        key = keypoint
        col1, col2, = st.beta_columns(2)
        with col1:
            st.image(crop, use_column_width = False)
        with col2:
            state.numBugs += st.button("Click if bug!", keypoint)
        cv2.imwrite("immages/" + str(filename) + ".jpg", crop)

    zipdir("immages")
    return imgKeyPoints

#helper function to display local images
def showImage(filepath):
    img = cv2.imread(filepath)
    st.image(img, width = 300)

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def zipdir(path):
    # ziph is zipfile handle
    # zipf = zipfile.ZipFile('tomato.zip','w')
    #
    # for root, dirs, files in os.walk(path):
    #     for file in files:
    #         zipf.write(os.path.join(root, file))
    #
    # zipf.close()

    # href = f'<a href="data:file/zip;base64,{b64}" download=\'croppedbugs.zip\'>\
    #     Click to download\
    #     </a>'
    href = '''
    <style>

    </style>
    <a href="#">Click here to download </a>
    '''

    # with open('tomato.zip', "rb") as f:
    #     bytes = f.read()
    #     b64 = base64.b64encode(bytes).decode()
    #     href = f'<a href="data:file/zip;base64,{b64}" download=\'croppedbugs.zip\'>\
    #         Click to download\
    #         </a>'
    st.markdown(href, unsafe_allow_html=True)


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

    '''
    st.markdown(info, unsafe_allow_html=True) #can't detect relative path to image
    col1, col2, = st.beta_columns(2)
    with col1:
        st.header("Before")
        showImage("uploads/flypaper1.jpg")
    with col2:
        st.header("After")
        showImage("uploads/detected.jpg")

    pic1 = get_base64_of_bin_file("uploads/detected.jpg")
    pic2 = get_base64_of_bin_file("uploads/flypaper1.jpg")
    pic3 = get_base64_of_bin_file("uploads/IMG_0041.jpg")
    # components.html(
    # """
    # <head>
    #   <meta name="viewport" content="width=device-width, initial-scale=1">
    #   <style>
    #     * {box-sizing: border-box}
    #     body {font-family: Verdana, sans-serif; margin:0}
    #     .mySlides {display: none}
    #     img {vertical-align: middle;}
    #
    #     /* Slideshow container */
    #     .slideshow-container {
    #       max-width: 600px;
    #       position: relative;
    #       margin: auto;
    #     }
    #
    #     /* Next & previous buttons */
    #     .prev, .next {
    #       cursor: pointer;
    #       position: absolute;
    #       top: 50%;
    #       width: auto;
    #       padding: 16px;
    #       margin-top: -22px;
    #       color: white;
    #       font-weight: bold;
    #       font-size: 18px;
    #       transition: 0.6s ease;
    #       border-radius: 0 3px 3px 0;
    #       user-select: none;
    #     }
    #
    #     /* Position the "next button" to the right */
    #     .next {
    #       right: 0;
    #       border-radius: 3px 0 0 3px;
    #     }
    #
    #     /* On hover, add a black background color with a little bit see-through */
    #     .prev:hover, .next:hover {
    #       background-color: rgba(0,0,0,0.8);
    #     }
    #
    #     /* Caption text */
    #     .text {
    #       color: #f2f2f2;
    #       font-size: 15px;
    #       padding: 8px 12px;
    #       position: absolute;
    #       bottom: 8px;
    #       width: 100%;
    #       text-align: center;
    #     }
    #
    #     /* Number text (1/3 etc) */
    #     .numbertext {
    #       color: #f2f2f2;
    #       font-size: 12px;
    #       padding: 8px 12px;
    #       position: absolute;
    #       top: 0;
    #     }
    #
    #     /* The dots/bullets/indicators */
    #     .dot {
    #       cursor: pointer;
    #       height: 15px;
    #       width: 15px;
    #       margin: 0 2px;
    #       background-color: #bbb;
    #       border-radius: 50%;
    #       display: inline-block;
    #       transition: background-color 0.6s ease;
    #     }
    #
    #     .active, .dot:hover {
    #       background-color: #717171;
    #     }
    #
    #     /* Fading animation */
    #     .fade {
    #       -webkit-animation-name: fade;
    #       -webkit-animation-duration: 1.5s;
    #       animation-name: fade;
    #       animation-duration: 1.5s;
    #     }
    #
    #     @-webkit-keyframes fade {
    #       from {opacity: .4}
    #       to {opacity: 1}
    #     }
    #
    #     @keyframes fade {
    #       from {opacity: .4}
    #       to {opacity: 1}
    #     }
    #
    #     /* On smaller screens, decrease text size */
    #     @media only screen and (max-width: 300px) {
    #       .prev, .next,.text {font-size: 11px}
    #     }
    #   </style>
    # </head>
    # <body>
    #
    #   <div class="slideshow-container">
    #
    #     <div class="mySlides fade">
    #       <div class="numbertext">1 / 3</div>
    #       <img src="data:image/jpeg;base64, %s" style="width:100%">
    #       <div class="text">Caption Text</div>
    #     </div>
    #
    #     <div class="mySlides fade">
    #       <div class="numbertext">2 / 3</div>
    #       <img src="#" style="width:100%">
    #       <div class="text">Caption Two</div>
    #     </div>
    #
    #     <div class="mySlides fade">
    #       <div class="numbertext">3 / 3</div>
    #       <img src="#" style="width:100%">
    #       <div class="text">Caption Three</div>
    #     </div>
    #
    #     <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
    #     <a class="next" onclick="plusSlides(1)">&#10095;</a>
    #
    #   </div>
    #   <br>
    #
    #   <div style="text-align:center">
    #     <span class="dot" onclick="currentSlide(1)"></span>
    #     <span class="dot" onclick="currentSlide(2)"></span>
    #     <span class="dot" onclick="currentSlide(3)"></span>
    #   </div>
    #
    #   <script>
    #     var slideIndex = 1;
    #     showSlides(slideIndex);
    #
    #     function plusSlides(n) {
    #       showSlides(slideIndex += n);
    #     }
    #
    #     function currentSlide(n) {
    #       showSlides(slideIndex = n);
    #     }
    #
    #     function showSlides(n) {
    #       var i;
    #       var slides = document.getElementsByClassName("mySlides");
    #       var dots = document.getElementsByClassName("dot");
    #       if (n > slides.length) {slideIndex = 1}
    #       if (n < 1) {slideIndex = slides.length}
    #       for (i = 0; i < slides.length; i++) {
    #         slides[i].style.display = "none";
    #       }
    #       for (i = 0; i < dots.length; i++) {
    #         dots[i].className = dots[i].className.replace(" active", "");
    #       }
    #       slides[slideIndex-1].style.display = "block";
    #       dots[slideIndex-1].className += " active";
    #     }
    #   </script>
    #
    # </body>
    #
    # """ % pic1
    # )
    # components.html(slideshow)

def main():
    state = _get_state()
    background_img = '''
    <style>
        body {
           background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSKqvjjmTFakcu3tyUj2UGchw40gH72VmGLjQ&usqp=CAU");
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

    elif choice == "About":
    	about()

class _SessionState:

    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()

    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False

        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    return session_info.session


def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_state

if __name__ == "__main__":
    main()
