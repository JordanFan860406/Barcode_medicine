# coding=utf-8

import cv2
import numpy as np
import os
from pyzbar.pyzbar import decode
from signal import signal, SIGTERM, SIGINT
import time


#*****************webcam number_setting*****************

barcode_scanner_webcam_number = 1 #barcode scanner webcam number

#*******************************************************

drugA_code_path = "./drugsA_code.txt"
# drugA_code_conver_dis_path = "/home/nvidia/identify_drug/drugA_code.txt"
drugA_code_data = {}

# def Ctrl_c(a, b):
#     if (len(os.listdir("/home/nvidia/identify_drug")) > 0):
#         os.system("rm {0}".format(drugA_code_conver_dis_path))
#     exit(0)

def main():

    # signal(SIGTERM, Ctrl_c)
    # signal(SIGINT, Ctrl_c)
    # if (len(os.listdir("/home/nvidia/identify_drug")) > 0):
    #     os.system("rm {0}".format(drugA_code_conver_dis_path))

    with open(drugA_code_path, 'r') as f:
        # lines = f.readlines()
        # lines = [a.strip() for a in lines]
        # for line in lines:
        #     drugA_code_data[line.split(',')[0]] = line.split(',')[1]

        while True:
            line = f.readline()
            line = line.strip('\n ')
            if line == "":break
            line_tmp = line.split(',')
            drugA_code_data[line_tmp[0]] = line_tmp[1]

    cap = cv2.VideoCapture(barcode_scanner_webcam_number) #barcode scanner webcam number

    while (True):

        if os.path.exists(drugA_code_conver_dis_path):
            barcode_scanner = False
        else:
            barcode_scanner = True

        ret, frame = cap.read()
        assert ret

        cv2.imshow("barcode", frame)
        key = cv2.waitKey(1) & 0XFF
        if (key == 27 or key == ord("q" or "Q")):
            os.system("rm {0}".format(drugA_code_conver_dis_path))
            cap.release()
            cv2.destroyAllWindows()
            break

        if barcode_scanner:
            decodeObjects = decode(frame)
            if(len(decodeObjects) != 0):
                try:#to test the qrcode lenth ,it is not valid if lenth < 6
                    os.system("clear")
                    for obj in decodeObjects:
                        print(obj.data[-6:-1])
                        barcode_tmp = obj.data[-6:-1]
                    if barcode_tmp in drugA_code_data.keys():
                        with open(drugA_code_conver_dis_path, 'w') as fp:
                            fp.write("{0}\n".format(drugA_code_data[barcode_tmp]))
                        fp.close()
                        print("Drug_code detected!!")
                        print("Please put the drug")
                    else:
                        print("No Valid Drug_code")
                        time.sleep(1)
                except:
                    print("No Valid Barcode")
                    time.sleep(1)
            else:
                os.system("clear")
                print("Please scan the barcode identifying the drug.")

    if (len(os.listdir("/home/nvidia/identify_drug")) > 0):
        os.system("rm {0}".format(drugA_code_conver_dis_path))

if __name__ == "__main__":
    main()
    pass
