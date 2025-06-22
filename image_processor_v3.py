# Импорты библиотек
from PIL import Image
import os
import sys
import logging
from datetime import datetime

# Настройка логирования
def setup_logging():
    """Настройка записи логов в файл"""
    log_filename = f"crop_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("Скрипт запущен")

# Обработка аргументов
def parse_args():
    """Функция для обработки аргументов командной строки."""
    if len(sys.argv) > 1:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2] if len(sys.argv) > 2 else "out"
        
        # Обработка координат, если они переданы
        if len(sys.argv) > 6:
            try:
                crop_box = (
                    int(sys.argv[3]),  # left
                    int(sys.argv[4]),  # upper
                    int(sys.argv[5]),  # right
                    int(sys.argv[6])   # lower
                )
                logging.info(f"Используются переданные координаты: {crop_box}")
                return input_folder, output_folder, crop_box
            except ValueError:
                logging.warning("Некорректные координаты. Используются значения по умолчанию")
                
    else:
        input_folder = "in"
        output_folder = "out"
        logging.info("Используются папки по умолчанию: in/out")
    
    # Координаты по умолчанию
    crop_box = (383, 280, 1531, 918)
    logging.info(f"Используются координаты по умолчанию: {crop_box}")
    return input_folder, output_folder, crop_box

# Основная функция
def main():
    setup_logging()
    
    try:
        input_folder, output_folder, crop_box = parse_args()
        
        # Создаем выходную папку, если её нет
        os.makedirs(output_folder, exist_ok=True)
        logging.info(f"Входная папка: {input_folder}")
        logging.info(f"Выходная папка: {output_folder}")

        processed_count = 0
        error_count = 0
        
        for filename in os.listdir(input_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(input_folder, filename)
                try:
                    img = Image.open(img_path)
                    cropped_img = img.crop(crop_box)
                    output_path = os.path.join(output_folder, filename)
                    cropped_img.save(output_path)
                    logging.info(f"Успешно обработано: {filename}")
                    processed_count += 1
                except Exception as e:
                    error_msg = f"Ошибка при обработке {filename}: {str(e)}"
                    logging.error(error_msg)
                    error_count += 1

        # Итоговый отчет
        logging.info(f"Обработка завершена. Успешно: {processed_count}, Ошибок: {error_count}")
        print(f"\nГотово! Обработано изображений: {processed_count}")
        print(f"Ошибок: {error_count}")
        print(f"Подробности в лог-файле: {logging.getLogger().handlers[0].baseFilename}")
        
    except Exception as e:
        logging.critical(f"Критическая ошибка: {str(e)}")
        raise

if __name__ == "__main__":
    main()