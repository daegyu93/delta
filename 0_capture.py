import cv2
import sys

def main(argv):
    device_num = int(argv[1])

    save_dir = 'cam_' + str(device_num) + '/'
    dev_cam = '/dev/video' + str(device_num)
    cap = cv2.VideoCapture(dev_cam)

    num = 0
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            print('Error: failed to capture image')
            break

        k = cv2.waitKey(5)

        if k == 27: # esc key to exit
            break
        elif k == ord('s'): # wait for 's' key to save and exit
            cv2.imwrite(save_dir + 'img' + str(num) + '.png', img)
            print("image saved!")
            num += 1

        cv2.imshow('Img',img)

    # Release and destroy all windows before termination
    cap.release()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)