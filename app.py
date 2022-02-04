from flask import Flask
from flask import render_template
from flask import Response
import cv2
app = Flask(__name__)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades +
     "haarcascade_frontalface_default.xml")

def rescale_frame(frame, percent = 75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

def generate(tamanho):
     print (tamanho)
     while True:
          ret, frame = cap.read()
          if tamanho == 25:
              frame = rescale_frame(frame, tamanho)
          elif tamanho == 50:
              frame = rescale_frame(frame, tamanho)
          elif tamanho == 80:
              frame = rescale_frame(frame, tamanho)
          elif tamanho == 125:
              frame = rescale_frame(frame, tamanho)
          else:
            frame = rescale_frame(frame, tamanho)
          
          if ret:
               gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
               faces = face_detector.detectMultiScale(gray, 1.3, 5)
               for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
               (flag, encodedImage) = cv2.imencode(".jpg", frame)
               if not flag:
                    continue
               yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                    bytearray(encodedImage) + b'\r\n')
@app.route("/")
def index():
     return render_template("index.html")
@app.route("/80")
def p80():
     return render_template("index80.html")
@app.route("/50")
def p50():
     return render_template("index50.html")
@app.route("/25")
def p25():
     return render_template("index25.html")
@app.route("/125")
def p125():
     return render_template("index125.html")


@app.route("/video_feed", methods=['GET', 'POST'])
def video_feed():
     return Response(generate(tamanho = 100),
          mimetype = "multipart/x-mixed-replace; boundary=frame")
@app.route("/video_feed80", methods=['GET', 'POST'])
def video_feed80():
     return Response(generate(tamanho = 80),
          mimetype = "multipart/x-mixed-replace; boundary=frame")
@app.route("/video_feed50", methods=['GET', 'POST'])
def video_feed50():
     return Response(generate(tamanho = 50),
          mimetype = "multipart/x-mixed-replace; boundary=frame")
@app.route("/video_feed25", methods=['GET', 'POST'])
def video_feed25():
     return Response(generate(tamanho = 25),
          mimetype = "multipart/x-mixed-replace; boundary=frame")
@app.route("/video_feed125", methods=['GET', 'POST'])
def video_feed125():
     return Response(generate(tamanho = 125),
          mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
     app.run(debug=False)
cap.release()