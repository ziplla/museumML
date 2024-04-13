from flask import Flask, request, jsonify, send_file
from ultralytics import YOLO

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Здесь вы можете сохранить файл на сервере или обработать его как вам нужно
    # Например, сохранить файл в определенной папке:
    file.save('uploaded_image.jpg')

    model = YOLO('runs/detect/yolov8s_v8_5e/weights/best.pt')

    results = model(['uploaded_image.jpg'])

    for result in results:
        boxes = result.boxes
        masks = result.masks
        keypoints = result.keypoints
        probs = result.probs
        result.show()
        result.save(filename='result.jpg')
        a = boxes.conf[0]
        b = boxes.cls[0]
        c = float(a)
        d = int(b)
        e = round(c, 2)


    return send_file('result.jpg', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
