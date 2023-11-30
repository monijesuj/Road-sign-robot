import RPi.GPIO as GPIO
import time
import cv2
import argparse
import numpy as np
from keras.models import model_from_json

enA = 38
enB = 40
in1 = 31
in2 = 33
in3 = 35
in4 = 37

trigPin1 = 11
echoPin1 = 13
trigPin2 = 15
echoPin2 = 16

def main():
    # Parse command line arguments
    arg_parser = argparse.ArgumentParser(description='keras model test')
    arg_parser.add_argument(
        '--model-file',
        required=True,
        help='model json file',
    )
    arg_parser.add_argument(
        '--weights-file',
        required=True,
        help='model weights file',
    )
    arg_parser.add_argument(
        '--input-width',
        type=int,
        default=48,
        help='Input image width',
    )
    arg_parser.add_argument(
        '--input-height',
        type=int,
        default=48,
        help='Input image height',
    )


    args = arg_parser.parse_args()
    assert args.input_width > 0 and args.input_height > 0

    with open(args.model_file, 'r') as file_model:
        model_desc = file_model.read()
        model = model_from_json(model_desc)

    model.load_weights(args.weights_file)

    # camera
    cap = cv2.VideoCapture(0)

    # GPIO

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(enA, GPIO.OUT)
    GPIO.setup(enB, GPIO.OUT)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(in3, GPIO.OUT)
    GPIO.setup(in4, GPIO.OUT)
    GPIO.setup(trigPin, GPIO.OUT)
    GPIO.setup(echoPin, GPIO.IN)
    pwmA = GPIO.PWM(enA, 1000)
    pwmB = GPIO.PWM(enB, 1000)
    pwmA.start(0)
    pwmB.start(0)
    
    def recognize_image():
        ret, orig_image = cap.read()
        assert ret is not None

        resized_image = cv2.resize(orig_image, (args.input_width, args.input_height),).astype(np.float32)
        normalized_image = resized_image / 255.0

        batch = normalized_image.reshape((1, args.input_width, args.input_height, 3))
        result = model.predict(batch)
        class_id = np.argmax(result, axis=1)[0]
        speed2, speed3, speed5, speed6, speed7, speed8, speed_8, speed10, speed12, no_passing, no_passing_3, rotw,\
                priority_road, Yield, stop, no_vehicles, nv_35, no_entry, general_caution, dc_right,\
                    dc_left, double_curve, bumpy_road, slippery_road, rnotright, road_work,\
                        traffic_signals, pedestrians, children_cross, bicycles, ice_snow,\
                            wild, endOfAll, right_ahead, left_ahead, ahead_only,\
                                straigt_right, straigt_left, keepr, keepl, roundabout,\
                                    endonp, endonp3 = result[0]
        classNo = class_id

        if   classNo == 0:
                class_str =  'Speed Limit 20 km/h'
        elif classNo == 1: 
            class_str = 'Speed Limit 30 km/h'
        elif classNo == 2: 
            class_str =  'Speed Limit 50 km/h'
        elif classNo == 3: 
            class_str = 'Speed Limit 60 km/h'
        elif classNo == 4: 
            class_str == 'Speed Limit 70 km/h'
        elif classNo == 5: 
            class_str =  'Speed Limit 80 km/h'
        elif classNo == 6: 
            class_str = 'End of Speed Limit 80 km/h'
        elif classNo == 7: 
            class_str = 'Speed Limit 100 km/h'
        elif classNo == 8: 
            class_str = 'Speed Limit 120 km/h'
        elif classNo == 9: 
            class_str = 'No passing'
        elif classNo == 10: 
            class_str =  'No passing for vechiles over 3.5 metric tons'
        elif classNo == 11: 
            class_str = 'Right-of-way at the next intersection'
        elif classNo == 12:
            class_str = 'Priority road'
        elif classNo == 13:
            class_str = 'Yield'
        elif classNo == 14:
            class_str = 'Stop'
        elif classNo == 15:
            class_str = 'No vechiles'
        elif classNo == 16: 
            class_str = 'Vechiles over 3.5 metric tons prohibited'
        elif classNo == 17:
            class_str = 'No entry'
        elif classNo == 18:
            class_str = 'General caution'
        elif classNo == 19:
            class_str = 'Dangerous curve to the left'
        elif classNo == 20:
            class_str = 'Dangerous curve to the right'
        elif classNo == 21:
            class_str = 'Double curve'
        elif classNo == 22:
            class_str = 'Bumpy road'
        elif classNo == 23:
            class_str = 'Slippery road'
        elif classNo == 24:
            class_str = 'Road narrows on the right'
        elif classNo == 25:
            class_str = 'Road work'
        elif classNo == 26:
            class_str = 'Traffic signals'
        elif classNo == 27:
            class_str = 'Pedestrians'
        elif classNo == 28:
            class_str = 'Children crossing'
        elif classNo == 29:
            class_str = 'Bicycles crossing'
        elif classNo == 30:
            class_str = 'Beware of ice/snow'
        elif classNo == 31:
            class_str = 'Wild animals crossing'
        elif classNo == 32:
            class_str = 'End of all speed and passing limits'
        elif classNo == 33:
            class_str = 'Turn right ahead'
        elif classNo == 34:
            class_str = 'Turn left ahead'
        elif classNo == 35:
            class_str = 'Ahead only'
        elif classNo == 36:
            class_str = 'Go straight or right'
        elif classNo == 37:
            class_str = 'Go straight or left'
        elif classNo == 38:
            class_str = 'Keep right'
        elif classNo == 39:
            class_str = 'Keep left'
        elif classNo == 40:
            class_str = 'Roundabout mandatory'
        elif classNo == 41: 
            class_str = 'End of no passing'
        elif classNo == 42:
            class_str = 'End of no passing by vechiles over 3.5 metric tons'

    def ultasonic_1():
        GPIO.output(trigPin1, 0)
        time.sleep(0.000002)
        GPIO.output(trigPin1, 1)
        time.sleep(0.00001)
        GPIO.output(trigPin1, 0)
        while GPIO.input(echoPin1) == 0:
            global echoStart
            echoStart = time.time()
        while GPIO.input(echoPin1) == 1:
            global echoEnd
            echoEnd = time.time()
        timet = echoEnd - echoStart
        return int(timet * 34000 / 2)
        time.sleep(0.2)
    def ultasonic_2():
        GPIO.output(trigPin2, 0)
        time.sleep(0.000002)
        GPIO.output(trigPin2, 1)
        time.sleep(0.00001)
        GPIO.output(trigPin2, 0)
        while GPIO.input(echoPin2) == 0:
            global echoStart2
            echoStart2 = time.time()
        while GPIO.input(echoPin2) == 1:
            global echoEnd2
            echoEnd2 = time.time()
        timet2 = echoEnd2 - echoStart2
        return int(timet2 * 34000 / 2)
        time.sleep(0.2)
    def forward():
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)
        pwmA.ChangeDutyCycle(80)
        pwmB.ChangeDutyCycle(80)
    def backward():
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)
        pwmA.ChangeDutyCycle(80)
        pwmB.ChangeDutyCycle(80)
    def stop():
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)
        pwmA.ChangeDutyCycle(0)
        pwmB.ChangeDutyCycle(0)
    def left():
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)
        pwmA.ChangeDutyCycle(80)
        pwmB.ChangeDutyCycle(80)
    def right():
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)
        pwmA.ChangeDutyCycle(80)
        pwmB.ChangeDutyCycle(80)
    
    try:
        while True:
            distance1 = ultasonic_1()
            distance2 = ultasonic_2()
            if distance1 > 20 and distance2 > 20:
                sign = recognize_image()
                if sign == 'Stop':
                    print('Stop')
                    stop()
                elif sign == 'Turn right ahead':
                    print('Turn right ahead')
                    right()
                elif sign == 'Turn left ahead':
                    print('Turn left ahead')
                    left()
                else:
                    print('Go straight')
                    forward()
            else:
                stop()
            
            
            print()
    except KeyboardInterrupt():
        GPIO.cleanup()
        print('GPIO Clean up')
        print('Program Ended')
        pwmA.stop()
        pwmB.stop()
        cam.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()