from PIL import Image  # библиотека для работы с изображениями
import cv2  # для работы с потоком (веб-камера)
import pytesseract  # библиотека для распознавания текста с картинок
import numpy as np  # библиотека, поддерживающая массивы, матрицы, сложные мат.функции


def prov(x, y, w, h, a):
    for i in a:
        if (x > i[0] - 70 and x < i[0] + 70) and (y > i[1] - 70 and y < i[1] + 70) and (
                w > i[2] - 70 and w < i[2] + 70) and (h > i[3] - 70 and h < i[3] + 70):
            return False
    return True


print("Хотите обнаружить объект?\n1. Да\n2. Нет\nВвод: ")
select = input()

cap = cv2.VideoCapture(0)  # запускаем видеопоток, т.к. одна прописываем 0

if select == "1":

    print("Что хотите обнаружить?\n1. Прямоугольник\n2. Текст\nВвод:")
    select = input()

    if select == "1":
        isRectangle = False

        kol = 0

        end = 0

        a = [[0, 0, 0, 0]]

        while end < 200:
            end = end + 1

            _, frame = cap.read()  # чтение по кадру

            _, threshold = cv2.threshold(frame, 105, 255,
                                         cv2.THRESH_BINARY_INV)  # разбивает на цветовые каналы возвращает изображение инвертируем в бинарный вид, чтобы проще было отделить чёрный цвет от других

            low_black = np.array([150, 170, 150])  # ненасыщенный чёрный код цвета
            upper_black = np.array([255, 255, 255])  # насыщенный чёрный

            mask = cv2.inRange(threshold, low_black,
                               upper_black)  # позволяет наложить на кадр цветовой фильтр в заданном диапазоне (начальный цвет и конечный), чёрный объекты становятся белыми
            kernel = np.ones((5, 5), np.uint8)  # убираем шумы (маленькие точки)
            mask = cv2.erode(mask, kernel)  # подавляет шумы

            contours, _ = cv2.findContours(mask, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)  # возвращает ирархию контуров, ставит несколько точек  и соединяет линию

            for cnt in contours:  # обработка контуров
                area = cv2.contourArea(cnt)  # находит площадь контура
                approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True),
                                          True)  # разбиения граней контура, периметр и перевод в проценты, возвращает кол-во наших граней

                if area > 400:  # находим площадь, для того, чтобы не захватывал мелкие объекты
                    (x, y, w, h) = cv2.boundingRect(
                        approx)  # разделение периметра на длину ширину(дабл ю ) высоту и глубину
                    aspectRatio = float(w) / h  # угол наклона

                    if len(approx) == 4 and not (
                            aspectRatio >= 0.89 and aspectRatio <= 1.3):  # делим высоту на ширину, поэтому это квадрат
                        cv2.drawContours(frame, [approx], 0, (0, 0, 255),
                                         5)  # чётвертый -цвет(красный), толщина линии, рисуется на камере
                        isRectangle = True

                        if (prov(x, y, w, h, a) == True):
                            kol = kol + 1
                            a.append([x, y, w, h])
                        break

            cv2.imshow("VideoCapture", frame)  # выводится кадры

            key = cv2.waitKey(1)

        cap.release()
        cv2.destroyAllWindows()

        print("Вывести информацию об объекте?\n1. Да\n2. Нет")
        select = input()

        if select == "1":
            print("Это прямоугольник? - {0}".format(isRectangle), "\nКоличество: ", kol)
            input()
        elif select == "2":
            exit(0)




    elif select == "2":
        while True:
            _, frame = cap.read()

            _, threshold = cv2.threshold(frame, 105, 255, cv2.THRESH_BINARY_INV)

            low_black = np.array([150, 170, 150])
            upper_black = np.array([255, 255, 255])

            mask = cv2.inRange(threshold, low_black, upper_black)
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.erode(mask, kernel)

            cv2.imshow("Frame", frame)

            key = cv2.waitKey(1)
            if key == 27:
                cv2.imwrite("text.png", frame);
                break

        print('Вывести текст в консоль?\n1. Да\n2. Нет\nВвод:')
        select = input()

        if select == '1':
            answer = pytesseract.image_to_string(Image.open("text.png"), lang='rus+eng')
            ln = len(answer)

            print('Распознанный текст: {0}'.format(answer[:ln - 2]))
            input()
        elif select == '2':
            exit(0)

elif select == "2":
    exit(0)

