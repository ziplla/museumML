import os
import shutil


def distribute_images(text_folder, image_folder):
    # Получаем список файлов из папки с текстовыми файлами
    text_files = [f for f in os.listdir(text_folder) if
                  os.path.isfile(os.path.join(text_folder, f)) and f.endswith('.txt')]

    # Перебираем каждый текстовый файл
    for text_file in text_files:
        text_file_path = os.path.join(text_folder, text_file)

        # Читаем первый символ из текстового файла
        with open(text_file_path, 'r') as file:
            first_char = file.read(1)
            if not first_char.isdigit():
                continue  # Пропускаем файлы, где первый символ не является цифрой

            # Создаем папку с соответствующим номером, если её нет
            target_folder = os.path.join(image_folder, first_char)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            # Получаем имя соответствующего изображения
            image_file = os.path.splitext(text_file)[
                             0] + '.jpg'  # Предполагается, что изображения имеют расширение .jpg
            image_file_path = os.path.join(image_folder, image_file)

            # Перемещаем изображение в соответствующую папку
            if os.path.exists(image_file_path):
                shutil.move(image_file_path, os.path.join(target_folder, image_file))


# Укажите путь к папке с текстовыми файлами и папке с изображениями
text_folder_path = 'labels'
image_folder_path = 'images'

# Вызываем функцию для распределения изображений
distribute_images(text_folder_path, image_folder_path)
