import sqlite3
from PIL import Image
import os
import face_recognition
import numpy as np

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()
conn.commit()
lots = []
weigh = []
hight = []
i = 0
# Возьмем фото человека, которого мы знаем.
Chunen = face_recognition.load_image_file('faces/Jeki.jpg')
Know_faces = face_recognition.face_encodings(Chunen)

# Выгружаем из базы данных новые лица и размер окна
cursor.execute('''Select count(lot) from lots''')
lenlots = (cursor.fetchone())[0]
cursor.execute('''Select lot from lots''')
for i in range(lenlots):
    lot = (cursor.fetchone())[0]
    lots.append(lot)
cursor.execute('''Select hight from lots''')
for i in range(lenlots):
    lot = (cursor.fetchone())[0]
    weigh.append(lot)
cursor.execute('''Select weigh from lots''')
for i in range(lenlots):
    lot = (cursor.fetchone())[0]
    hight.append(lot)

# Узнаем количество прошлых фото, удаляем их, чтобы загрузить новые.
list_dir = os.listdir('faces/news/')
for i in range(len(list_dir)):
    os.remove('faces/news/lot' + str(i) + '.bmp')

# Воссоздаем из байтов фото с камеры.
for i in range(lenlots):
    b = Image.frombytes(mode='RGB', size=(hight[i], weigh[i]), data=lots[i])
    # Сохранять фото не обязательно, но так легче просмотреть идентичность.
    b.save('faces/news/lot' + str(i) + '.bmp')
    i = i + 1
    # Переводим фото в формат для работы с библиотекой face_recognition
    unknown_face = np.array(b)
    # Для примера берем последнее лицо.
    Unknown = face_recognition.face_encodings(unknown_face)
    q = face_recognition.compare_faces(Know_faces[0], Unknown, tolerance=0.4)
    # Выводим результат
    print(q)






conn.commit()
