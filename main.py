import cv2
import nexmo

# Nexmo messaging
client = nexmo.Client(key='Your nexmo key', secret='Your nexmo secret key')
number = "your phone number with the country code"
message = "Pigeons have entered your farm"


# initalizing the camera
cap = cv2.VideoCapture('birds.mp4')
birdsCascade = cv2.CascadeClassifier("birds1.xml")
MAX_NUM_BIRDS = 5
running = True
count = 0

# Detecting the birds
while running:
    if count == 1:
        response = client.send_message({
            'from': 'GYMAALE',
            'to': number,
            'text': message,
        })
        response = response['messages'][0]
        if response['status'] == '0':
            print("MESSAGE DELIVERED SUCCESSFULLY", response['message-id'])
        else:
            print("ERROR SENDING MESSAGE", response['error-text'])
    count += 1
    ret, frame = cap.read()
    print("Ret is ", ret)
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        birds = birdsCascade.detectMultiScale(
            gray,
            scaleFactor=1.4,
            minNeighbors=1,
            # minSize=(10,10),
            maxSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if (len(birds) >= MAX_NUM_BIRDS):
            print("Detected {0} Birds.".format(len(birds)))

        # Drawing a rectangle around a bird approaching the farm
        for (x, y, w, h) in birds:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 200, 0), 2)

        # Displaying the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
    else:
        running = False


cap.release()
cv2.destroyAllWindows()
