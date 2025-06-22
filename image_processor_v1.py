#Запуск скрипта
'''
python image_processor_v1.py "d:/мои_скриншоты" "d:/результаты"
Без аргументов (используются папки in и out):
'''
# Импорты библиотек
from PIL import Image
import os
import sys  # Не забудьте импортировать sys для работы с аргументами

# Обработка аргументов
def parse_args():
    """Функция для обработки аргументов командной строки."""
    if len(sys.argv) > 1:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2] if len(sys.argv) > 2 else "out"
    else:
        input_folder = "in"  # Папка по умолчанию
        output_folder = "out"
    return input_folder, output_folder

# Получаем пути из аргументов (ЗАМЕНИЛИ жестко заданные значения)
input_folder, output_folder = parse_args()

# Координаты обрезки (left, upper, right, lower)
crop_box = (383, 280, 1531, 918)  # Подобранные вручную координаты

# Создаем выходную папку, если её нет
os.makedirs(output_folder, exist_ok=True)

# Обработка изображений
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(input_folder, filename)
        try:
            img = Image.open(img_path)
            cropped_img = img.crop(crop_box)
            cropped_img.save(os.path.join(output_folder, filename))
            print(f"Обработано: {filename}")
        except Exception as e:
            print(f"Ошибка при обработке {filename}: {str(e)}")

print(f"Готово! Обработанные изображения сохранены в {output_folder}")