
from flask import Flask, render_template, url_for, request, redirect
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

#https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask

UPLOAD_FOLDER = "static/images"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    filePath = "static/images/"
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filePath += filename
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('uploadFile.html')

#FIX: add a close button idk how
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('uploadFile.html', files=files)
    #return send_from_directory(app.config['UPLOAD_FOLDER'],
                               #filename)
                               
@app.route('/static/images/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def detect_bugs():
    # start with colored image
    pathImage = filePath
    widthImg = 600
    heightImg = 800

    #Gray scale and blur the image
    img = cv2.imread(pathImage)
    imgGray = cv2.imread(pathImage, cv2.IMREAD_GRAYSCALE)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    height, width, channels = img.shape

    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 400
    #params.maxArea = 3000

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.00001

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.000001


    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)

    #detector = cv2.SimpleBlobDetector_create()
    keypoints = detector.detect(imgBlur)
    imgKeyPoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


    # Crop out keypoints
    # str = ""
    # for keypoint in keypoints:
    # str += "1"
    # x = int(keypoint.pt[0])
    # y = int(keypoint.pt[1])
    # size = int(keypoint.size)
    # cv2.imshow(str, img[max(1,y-2*size): min(height-1,y+2*size), max(1,x-2*size): min(width-1,x+2*size)])

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)
#
# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)
#
#     def __repr__(self):
#         return '<Task %r>' % self.id
#
# #comment
# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         task_content = request.form['content']
#         new_task = Todo(content=task_content)
#
#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue adding your task'
#
#     else:
#         tasks = Todo.query.order_by(Todo.date_created).all()
#         return render_template('index.html', tasks=tasks)
#
#
# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)
#
#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was a problem deleting that task'
#
# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task = Todo.query.get_or_404(id)
#
#     if request.method == 'POST':
#         task.content = request.form['content']
#
#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue updating your task'
#
#     else:
#         return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
