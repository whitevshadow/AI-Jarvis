import datetime
import socket

from Features.Web_Scraping.Thoughts import thought_day
from Body.Speaker import Speak

global name


def isConnect():
    try:
        s = socket.create_connection(
            ("www.google.com", 80))
        if s is not None:
            s.close()
        return True
    except OSError:
        pass
    return False


def wishMe(user):
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        Speak(f"Good Morning {user} !")

    elif 12 <= hour < 18:
        Speak(f"Good Afternoon {user} !")

    else:
        Speak(f"Good Evening  {user} !")


def face_detection():
    global name, id
    import cv2

    recognizer = cv2.face.LBPHFaceRecognizer_create()  # Local Binary Patterns Histograms
    recognizer.read('Brain\\trainer\\trainer.yml')  # load trained model
    cascadePath = "Brain\\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)  # initializing haar cascade for object detection approach

    font = cv2.FONT_HERSHEY_SIMPLEX  # denotes the font type

    id = 2  # number of persons you want to Recognize

    names = ['','Anish','Ansh']  # names, leave first empty bcz counter starts from 0

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cv2.CAP_DSHOW to remove warning
    cam.set(3, 640)  # set video FrameWidht
    cam.set(4, 480)  # set video FrameHeight

    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    # flag = True

    while True:

        ret, img = cam.read()  # read the frames using the above created object

        converted_image = cv2.cvtColor(img,
                                       cv2.COLOR_BGR2GRAY)  # The function converts an input image from one color space to another

        faces = faceCascade.detectMultiScale(
            converted_image,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # used to draw a rectangle on any image

            id, accuracy = recognizer.predict(converted_image[y:y + h, x:x + w])  # to predict on every single image

            # Check if accuracy is less them 100 ==> "0" is perfect match
            if (accuracy <= 70):
                detected_name = names[id - 1]
                name = detected_name
                accuracy = "  {0}%".format(round(100 - accuracy))

            else:
                detected_name = "unknown"
                name = detected_name
                accuracy = "  {0}%".format(round(100 - accuracy))

            cv2.putText(img, str(detected_name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(accuracy), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break

    # Do a bit of cleanup
    cam.release()
    cv2.destroyAllWindows()

    if name == "unknown":
        user_name = "My Friend"
        wishMe(user_name)
        Speak("You Don't have access to the Program")
        exit()
    elif name != "unknown":
        wishMe(name)


def Check_Net():
    Net = isConnect()
    if True is Net:
        print("J.A.R.V.I.S is Online")

    else:
        print("Please Connect to Internet")


def thoughts():
    thought = thought_day()
    Speak(thought)


def init():
    Check_Net()
    face_detection()
