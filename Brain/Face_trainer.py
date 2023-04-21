def Sample():
    import cv2

    cam = cv2.VideoCapture(0,
                           cv2.CAP_DSHOW)  # create a video capture object which is helpful to capture videos through webcam
    cam.set(3, 640)  # set video FrameWidth
    cam.set(4, 480)  # set video FrameHeight

    detector = cv2.CascadeClassifier('Brain\\haarcascade_frontalface_default.xml')
    # Haar Cascade classifier is an effective object detection approach

    face_id = input("Enter a Numeric user ID  here:  ")
    # Use integer ID for every Face_dect face (0,1,2,3,4,5,6,7,8,9........)

    print("Taking samples, look at camera ....... ")
    count = 0  # Initializing sampling face count

    while True:

        ret, img = cam.read()  # read the frames using the above created object
        converted_image = cv2.cvtColor(img,
                                       cv2.COLOR_BGR2GRAY)  # The function converts an input image from one color space to another
        faces = detector.detectMultiScale(converted_image, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # used to draw a rectangle on any image
            count += 1

            cv2.imwrite("Brain\\samples\\face." + str(face_id) + '.' + str(count) + ".jpg", converted_image[y:y + h, x:x + w])
            # To capture & Save images into the datasets folder

            cv2.imshow('image', img)  # Used to display an image in a window

        k = cv2.waitKey(100) & 0xff  # Waits for a pressed key
        if k == 27:  # Press 'ESC' to stop
            break
        elif count >= 10:  # Take 50 sample (More sample --> More accuracy)
            break

    print("Samples taken now closing the program....")
    cam.release()
    cv2.destroyAllWindows()


def Train():
    import cv2
    import numpy as np
    from PIL import Image  # pillow package
    import os

    path = 'Brain\\samples'  # Path for samples already taken

    recognizer = cv2.face.LBPHFaceRecognizer_create()  # Local Binary Patterns Histograms
    detector = cv2.CascadeClassifier("Brain\\haarcascade_frontalface_default.xml")

    # Haar Cascade classifier is an effective object detection approach

    def Images_And_Labels(path):  # function to fetch the images and labels

        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        ids = []

        for imagePath in imagePaths:  # to iterate particular image path

            gray_img = Image.open(imagePath).convert('L')  # convert it to grayscale
            img_arr = np.array(gray_img, 'uint8')  # creating an array

            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_arr)

            for (x, y, w, h) in faces:
                faceSamples.append(img_arr[y:y + h, x:x + w])
                ids.append(id)

        return faceSamples, ids

    print("Training faces. It will take a few seconds. Wait ...")

    faces, ids = Images_And_Labels(path)
    recognizer.train(faces, np.array(ids))

    recognizer.write('Brain\\trainer\\trainer.yml')  # Save the trained model as trainer.yml

    print("Model trained, Now we can recognize your face.")


def Face_training():
    Sample()
    Train()