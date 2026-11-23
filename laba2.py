import cv2
import numpy as np
import os
import datetime

def apply_robust_correction(img):
    # Вычисляем 2-й и 98-й перцентили
    p2, p98 = np.percentile(img, (2, 98))
    
    # Растягиваем гистограмму, обрезая значения за пределами [p2, p98]
    if p98 > p2:
        robust_img = np.clip((img - p2) / (p98 - p2) * 255.0, 0, 255).astype(np.uint8)
    else:
        robust_img = img # Защита от деления на ноль, если изображение однотонное
        
    return robust_img

def main():
    # Формирование путей (выносим за цикл, т.к. они не меняются)
    base_dir = "Lab2_Media"
    output_path = os.path.join(base_dir, "data", "output", "result.jpg")
    log_path = os.path.join(base_dir, "logs", "history.txt")
    filter_name = "Гаусс + Робастная коррекция"

    # Бесконечный цикл для повторного ввода при ошибках
    while True:
        # 1. Ввод данных (Потоковый ввод)
        filename = input("Введите имя файла для обработки (например, image1.jpg или image2.png) или 'exit' для выхода: ").strip()
        
        # Условие выхода из программы
        if filename.lower() in ('exit', 'q', ''):
            print("Выход из программы.")
            break

        input_path = os.path.join(base_dir, "data", "input", filename)
        status = "Ошибка доступа"  # Значение по умолчанию
        
        try:
            # 2. Поиск и открытие файла с обработкой ошибок
            # Используем встроенный open для проверки прав на чтение
            with open(input_path, 'rb') as f:
                pass 
                
            # Чтение изображения
            img = cv2.imread(input_path)
            if img is None:
                # Если OpenCV не смог прочитать (например, поврежден файл или неверный формат)
                raise IOError("Не удалось прочитать файл как изображение")

            # 3. Обработка изображения (Задания 1 и 2)
            # Задание 1: Фильтр Гаусса (сглаживание)
            gaussian_img = cv2.GaussianBlur(img, (5, 5), 0)

            # Задание 2: Робастная (устойчивая) коррекция
            result_img = apply_robust_correction(gaussian_img)

            # 5. Сохранение результата
            os.makedirs(os.path.dirname(output_path), exist_ok=True) # Создаем папку output, если ее нет
            cv2.imwrite(output_path, result_img)
            
            print(f"Успешно! Обработанное изображение сохранено в {output_path}")
            status = "Успешно"

        except PermissionError:
            # Обработка ошибки прав доступа (как указано в задании для image2.png)
            print(f"Ошибка: Нет прав на чтение файла {filename}. Обратитесь к администратору")
            status = "Ошибка доступа"
        except FileNotFoundError:
            # Обработка отсутствия файла
            print("Ошибка: Файл не найден")
            status = "Файл не найден"
        except IOError:
            # Обработка других ошибок ввода-вывода
            print(f"Ошибка: Не удалось прочитать файл {filename}. Возможно, он поврежден или имеет неверный формат.")
            status = "Ошибка чтения"
        except Exception as e:
            # Защита от аварийного завершения (без Traceback)
            print(f"Произошла непредвиденная ошибка: {e}")
            status = "Ошибка"
            
        finally:
            # 6. Логирование (Потоковый вывод)
            try:
                # Создаем директорию для логов, если ее нет
                os.makedirs(os.path.dirname(log_path), exist_ok=True)
                
                # Открываем файл в режиме добавления 'a' с кодировкой UTF-8
                with open(log_path, 'a', encoding='UTF-8') as log_file:
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # Формируем строку лога (обязательно добавляем \n в конце)
                    log_entry = f"[{now}] Файл: {filename} | Фильтр: {filter_name} | Статус: {status}\n"
                    log_file.write(log_entry)
            except Exception as log_error:
                print(f"Не удалось записать лог: {log_error}")
        
        # Если обработка прошла успешно — завершаем цикл
        if status == "Успешно":
            break
        else:
            print("Попробуйте ввести другое имя файла.\n")

if __name__ == "__main__":
    main()