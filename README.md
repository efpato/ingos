ingos-kasko-calc
============

ИНГОССТРАХ Калькулятор КАСКО

#Настройка локальной машины для запуска скрипта
 
 1. Установить Firefox
 2. Установить Python (https://www.python.org/downloads/release/python-342/)
 3. Прописать в переменную окружения PATH к установленному каталогу с python.exe (по умолчанию это C:\Python34\) и добавить путь к C:\Python34\Scripts
 4. Установить pip (https://pip.pypa.io/en/latest/installing.html) - если была установлена версия питона более 3.4, то надо только обновить pip: запусть виндовую консоль и ввести
```bash
pip install -U pip
```
 5. Установить git-клиента https://git-scm.com/downloads
 6. Запустить консоль git
 7. Клонировать репозиторий себе на локальную машину
 8. Перейти в склонированный каталог и выполнить:
```bash
pip install -r requirements.txt
```

УСПЕХ! Вы готовы к использованию скрипта локально на своей виндовой машине

#Использование

```bash
python kasko-calc sample.xls
```
На выходе получаем Excel-файл sample.out.xls
