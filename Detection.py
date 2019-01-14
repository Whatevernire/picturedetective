from PIL import Image
import face_recognition
import os
import cv2
import sqlite3

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

#Удаляем старые фото из папки
list_dir = os.listdir('faces/lots/')
for i in range(len(list_dir)):
    os.remove('faces/lots/lot' + str(i) + '.bmp')
i = 0

#Загружаем фото, которое надо распознать
image = face_recognition.load_image_file("faces/Jeki_family.jpg")

#Выбор размера фотографии, для улучшения быстродействия
image = cv2.resize(image, (0, 0), fx=0.8, fy=0.8)

#Определяем количество лиц в кадре (на фото)
face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0)
if face_locations != 0:
    #Удаляем из базы данных прошлые лица
    cursor.execute("""Delete from lots""")
    for face_location in face_locations:

        top, right, bottom, left = face_location
        face_image = image[top - 10:bottom + 10, left - 10:right + 10]
        #Создаем обрезанные фото и берем с них размеры окна
        pil_image = Image.fromarray(face_image)
        hight = pil_image.size[0]
        weight = pil_image.size[1]
        #Можно не сохранять.
        pil_image.save('faces/lots/lot' + str(i) + '.bmp')
        pil_image = pil_image.tobytes()
        #Вносим значения в виде: bytes, int, int, самого фото и его размеры.
        cursor.execute('''INSERT INTO  lots values (?,?,?)''', (pil_image, hight, weight))
        i = i + 1
        # Вырубаем на четвертом круге.
        if i >= 4:
            break

        print('Is Ok')
    conn.commit()
