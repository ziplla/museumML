from flask import Flask, request, jsonify, send_file
from ultralytics import YOLO
import cv2
import os
import shutil

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    file.save('uploaded_image.jpg')

    model = YOLO('runs/detect/yolov8s_v8_5e5/weights/best.pt')

    results = model(['uploaded_image.jpg'])

    type = -1

    for result in results:
        boxes = result.boxes
        masks = result.masks
        keypoints = result.keypoints
        probs = result.probs
        result.show()
        result.save(filename='static/result.jpg')
        # a = boxes.conf[0]
        if boxes:
            type = int(boxes.cls[0])
        # c = float(a)
        # e = round(c, 2)

    array = []

    resultArray = []

    if type != -1:
        folder_path = f'train/images/{type}'
        files = os.listdir(folder_path)
        for file_name in files:
            hash1 = CalcImageHash('uploaded_image.jpg')
            hash2 = CalcImageHash(f"train/images/{type}/{file_name}")
            total = CompareHash(hash1, hash2)
            array.append([total, file_name])
        array.sort()

        # resultArray.append(sortedArray.keys()[:10])
        resultArray = array[:10]

        # Указываем путь к целевой папке, куда мы хотим скопировать файлы
        target_folder = 'static'

        # Получаем список файлов в исходной папке

        urlArray = []

        # Копируем каждый файл из исходной папки в целевую папку
        for item in resultArray:
            source_file = os.path.join(folder_path, item[1])
            shutil.copy(source_file, target_folder)
            urlArray.append(f"http://localhost:5000/static/{item[1]}")

    if type != -1:
        response_data = {
            'result': 'http://localhost:5000/static/result.jpg',
            'urlArray': urlArray
        }
        return jsonify(response_data)
    else:
        response_data = {
            'result': 'Объект не обнаружен',
        }
        return response_data

# Функция вычисления хэша
def CalcImageHash(FileName):
    image = cv2.imread(FileName)  # Прочитаем картинку
    resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)  # Уменьшим картинку
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)  # Переведем в черно-белый формат
    avg = gray_image.mean()  # Среднее значение пикселя
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация по порогу

    # Рассчитаем хэш
    _hash = ""
    for x in range(8):
        for y in range(8):
            val = threshold_image[x, y]
            if val == 255:
                _hash = _hash + "1"
            else:
                _hash = _hash + "0"

    return _hash


def CompareHash(hash1, hash2):
    l = len(hash1)
    i = 0
    count = 0
    while i < l:
        if hash1[i] != hash2[i]:
            count = count + 1
        i = i + 1
    return count


if __name__ == '__main__':
    app.run(debug=True)
