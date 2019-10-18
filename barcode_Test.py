import pyzbar.pyzbar as pyzbar
import cv2
import numpy as np
import re
import time
import tkinter as tk


def barcode_decode(image):
    barcodes = pyzbar.decode(image)           # 解碼barcode
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect           # 畫出barcode邊框位子
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        barcodeData = barcode.data.decode('utf-8')
        barcodeType = barcode.type

        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    .5, (0, 0, 125), 2)
        data_list = []
        for i in re.split(r'(;+)', barcodeData):
            if ";" not in i:
                data_list.append(i)
        data_list = data_list[1:-1]
        print(data_list)
        time.sleep(1)
        gui(data_list)
    return image


# 偵測條碼方法
def detect():
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image = barcode_decode(gray)
        cv2.waitKey(5)
        cv2.imshow("camera", image)
    cap.release()
    cv2.destroyAllWindows()

# 讀取藥品代碼與名稱
def medicine():
    medicine_dict = {}
    with open('drugsA_code.txt') as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.split(",")
            medicine_dict[line[0]] = line[1]
    return medicine_dict

def gui(data_list):
    windows = tk.Tk()
    windows.configure(background='black')
    windows.title("藥排核實系統")
    windows.geometry('1500x960')
    canvas = tk.Canvas(windows, height=960, width=1500)
    navbar = canvas.create_rectangle(0, 0, 1500, 100, fill="gray")

    # 工具列
    navbar_title = canvas.create_text(160, 50, text='藥排核實系統', fill='white', font="Times 35 bold")
    next_button = canvas.create_text(1400, 50, text='下一筆', fill='white', font="Times 30 bold")
    last_button = canvas.create_text(1250, 50, text='上一筆', fill='white', font="Times 30 bold")

    # 上方資訊區塊 (['林明昆', '13', '1070814', '14', '張經緯', '25022', '1', 'BID', 'PO', '28'])
    info_first = canvas.create_rectangle(50, 130, 1450, 230, outline="black", width=4)
    name = "姓名: %s" % data_list[0]
    subject = "科目代碼: %s" %data_list[1]
    date = "看診日期: %s" %data_list[2]
    doctor = "醫師: %s" %data_list[4]
    info_first_name = canvas.create_text(200, 180, text=name, fill='black', font="Times 20 bold")
    info_first_subject = canvas.create_text(450, 180, text=subject, fill='black', font="Times 20 bold")
    info_first_date = canvas.create_text(700, 180, text=date, fill='black', font="Times 20 bold")
    info_first_doctor = canvas.create_text(950, 180, text=doctor, fill='black', font="Times 20 bold")
    info_first_id = canvas.create_text(1200, 180, text="病歷號碼: 12123456", fill='black', font="Times 20 bold")

    # 中左資訊區塊
    if data_list[5] not in medicine_dict:
        medicine_name = "查無此藥"
    else:
        medicine_name = medicine_dict[data_list[5]]
    medicine = "藥品名稱: %s" %medicine_name
    medicineID = "藥品代碼: %s" % data_list[5]
    medicineSum = "藥品數量: %s天" % data_list[3]
    info_left = canvas.create_rectangle(50, 270, 1000, 780, outline="black", width=4)
    info_left_medicine = canvas.create_text(70, 320, text=medicine, anchor='nw', fill='black', font="Times 20 bold")
    info_left_medicineID = canvas.create_text(70, 450, text=medicineID, anchor='nw', fill='black',font="Times 20 bold")
    info_left_medicineSum = canvas.create_text(70, 580, text=medicineSum, anchor='nw', fill='black', font="Times 20 bold")

    # 中右資訊區塊
    info_right = canvas.create_rectangle(1020, 270, 1450, 780, outline="black", width=4)
    info_right_title = canvas.create_text(1240, 310, text="檢核結果", fill='black', font="Times 30 bold")

    # 下方資訊區塊
    info_bottom = canvas.create_rectangle(50, 820, 1450, 940, outline="black", width=4)

    canvas.pack()

    windows.mainloop()
    return canvas

def check(canvas):
    test = canvas.create_rectangle(50, 50, 150, 150, outline="black", width=4)
    canvas.pack

def main():
    #detect()
    data_list = ['林明昆', '13', '1070814', '14', '張經緯', '22440', '1', 'BID', 'PO', '28']
    gui(data_list)

if __name__ == '__main__':
    medicine_dict = medicine()  # 載入藥品代碼與藥名
    main()