import cv2
from boot_sequence import BootSequence
from os import listdir
from os.path import isfile, join
import random

class Video:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.window_name = 'face'
        self.faces = [f for f in listdir('faces') if isfile(join('faces', f))]
        self.videos = [v for v in listdir('videos') if (isfile(join('videos', v)) and v[-4:] == ".mp4")]

        return
        
    def run(self, face_id, stage_id):

        f_id = -1
        s_id = -1
        break_video = False
        break_esc = False

        while True: # First loop resets every stage
            cap = cv2.VideoCapture('videos/' + random.choice(self.videos))

            while True: # Second loop resets every time the face changes
                img = cv2.imread('faces/' + self.faces[face_id.value])

                # Resize image
                img = cv2.resize(img, (400, 400))

                img_height, img_width, img_channels = img.shape

                while(cap.isOpened()):

                    ret, frame = cap.read() 

                    if ret:

                        # Resize frame
                        frame = cv2.resize(frame, (self.width, self.height))
                            
                        # img = cv2.copyMakeBorder(img, 0, 0, 100, 100, cv2.BORDER_CONSTANT)

                        frame_height, frame_width, frame_channels = frame.shape

                        x_offset = int((frame_width - img_width)/2)
                        y_offset = int((frame_height - img_height)/2)

                        y1, y2 = y_offset, y_offset + img_height
                        x1, x2 = x_offset, x_offset + img_width

                        alpha_s = img[:, :, 2] / 255.0
                        alpha_l = 1.0 - alpha_s

                        for c in range(0, 3):
                            frame[y1:y2, x1:x2, c] = (alpha_s * img[:, :, c] +
                                                    alpha_l * frame[y1:y2, x1:x2, c])

                        cv2.imshow('face', frame)
                        cv2.namedWindow("face", cv2.WINDOW_NORMAL)
                        #cv2.setWindowProperty("face",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN) #Disable when on large monitor
                        cv2.resizeWindow("face", self.width, self.height) #Enable when on large monitor

                    else:
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue

                    # If face has changed, resetart loop
                    if f_id != face_id.value:
                        f_id = face_id.value
                        print("face changed")
                        break
                        
                    # If stage id has changed, resetart loop
                    if s_id != stage_id.value:
                        s_id = stage_id.value
                        break_video = True
                        print("stage changed")
                        break

                    k = cv2.waitKey(10)
                    if k==27:    # Esc key to stop
                        break_esc = True
                        break
                
                if break_esc or break_video:
                    break_video = False
                    break

            if break_esc:
                break




if __name__ == "__main__":
    my_vid = Video()
    print(my_vid.videos)