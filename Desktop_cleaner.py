from pathlib import Path
import shutil

def scanner(defoult_path = Path.cwd()): 
    """_summary_

    Args:
        defoult_path (_type_, optional): _description_. Defaults to Path.cwd().

    Returns:
        _type_: _description_
    """
    user_input = input(
        f"Введите путь для сканирования\n"
        f"или нажмите Enter, чтобы использовать путь по умолчанию\n"
        f"({defoult_path}): "
    ).strip() or defoult_path
    folder = Path(user_input)
    if not folder.exists():
        print('❌ Ошибка: Такой папки нет!')
        return None, None
    
    if not folder.is_dir():
        print('⚠️  Это файл, а не папка!')
        return None, None

    print(f"\n📂 Сканируем: {folder.absolute()}")
    print("=" * 50)

    categories = { 
        "Изображения": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        "Документы": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
        "Видео": [".mp4", ".avi", ".mov", ".mkv"],
        "Музыка": [".mp3", ".wav", ".flac", ".aac"],
        "Архивы": [".zip", ".rar", ".7z", ".tar"],
        "Программы": [".exe", ".msi", ".bat", ".sh"],
        "Другое": []  
    }

    found_files = {category:[] for category in categories}
    total_files = 0
    
    for file in folder.iterdir():
        if file.is_file():
            if file.name == 'Desktop_cleaner.py':
                print(f"⚠️  Пропускаем скрипт: {file.name}")
                continue  # ← ПРОПУСТИТЬ ЭТУ ИТЕРАЦИЮ
            file_ext = file.suffix.lower()
            gategorised = False
            for category, extensions in categories.items():
                if file_ext in extensions:
                    found_files[category].append(file.name)
                    gategorised = True
                    break
            if not gategorised:
                found_files["Другое"].append(file.name)
            total_files += 1
    print(f"\n✅ Сканирование завершено! Всего файлов: {total_files}")
    print("\n📋 Результаты сканирования:")
    for category, files in found_files.items():
        if files:
            print(f"\n{category} ({len(files)} файлов):")
            for file in files[:5]:
                print(f" - {file}")
            if len(files) > 5:
                print(f" ... и еще {len(files) - 5} файлов")
    print("=" * 50)
    return found_files, folder

def create_category_folders(base_path, categories):
    created_counts = 0
    print("\n📁 Создаем папки для категорий...")
    for category, files in categories.items():
        if not files:
            continue
        print(f"Создаем папку: {category}")
        category_path = base_path / category
        try:
            category_path.mkdir(exist_ok=True)
            if category_path.exists():
                print(f"✅ {category:15} → {category_path.name}/")
                created_counts += 1
            else:
                print(f"❌ Ошибка при создании папки: {category:15}")
        except PermissionError:
            print(f"❌ {category:15} → нет прав на создание")
        except Exception as e:
            print(f"❌ {category:15} → ошибка: {e}")
    print(f"\n📊 Создано папок: {created_counts} из {len(categories)} возможных.")
    
def move_with_rename(base_path, categories_dict):
    """Перемещение файлов с помощью .rename()"""
    for category, files in categories_dict.items():
        if not files:
            continue
            
        category_path = base_path / category
        category_path.mkdir(exist_ok=True)
        
        for filename in files:
            source = base_path / filename
            destination = category_path / filename
            
            if source.exists():
                try:
                    source.rename(destination)
                    print(f"✅ {filename:20} → {category}/")
                except OSError as e:
                    # Ошибка при перемещении между разными дисками
                    print(f"❌ {filename:20} → ошибка: {e}")
                    # Пробуем shutil.move как запасной вариант
                    try:
                        shutil.move(str(source), str(destination))
                        print(f"✅ {filename:20} → {category}/ (через shutil)")
                    except Exception as e2:
                        print(f"❌ {filename:20} → критическая ошибка: {e2}")

def main():
    print("=" * 60)
    print("        ОРГАНИЗАТОР ФАЙЛОВ - ШАГ 1 и 2")
    print("=" * 60)
    print("1. Сканирование и классификация")
    print("2. Создание папок для категорий")
    print("=" * 60)
    found_files, folder = scanner()
    if not found_files or folder is None:
        print("\n❌ Не удалось выполнить сканирование. Выход.")
        return
    create_category_folders(folder, found_files) 
    print("\n✅ Готово! Папки созданы.")
    print(f'Итоговая структура папок в "{folder}"')
    print("=" * 40)
    for item in sorted(folder.iterdir()):
        if item.is_dir():
            count_files = sum(1 for subitem in item.iterdir() if subitem.is_file())
            print(f"📁 {item.name:15} ({count_files:2} файлов)")
        else:
            print(f"📄 {item.name}")
    print("=" * 40)
    move_with_rename(folder, found_files)
    print("\n✅ Готово! Файлы перемещены.")

if __name__ == "__main__":
    main()