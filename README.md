ingos-kasko-calc
================

ИНГОССТРАХ Калькулятор КАСКО

#Настройка локальной машины для запуска скрипта
 
 1. Установить Google Chrome
 2. Скачать последнюю версию chromedriver (https://sites.google.com/a/chromium.org/chromedriver/downloads) и положить в C:\Windows
 3. Установить Python (https://www.python.org/downloads/release/python-342/)
 4. Прописать в переменную окружения PATH к установленному каталогу с python.exe (по умолчанию это C:\Python34\) и добавить путь к C:\Python34\Scripts
 5. Установить git-клиента https://git-scm.com/downloads
 6. Запустить консоль git
 7. Клонировать репозиторий себе на локальную машину
```bash
git clone https://github.com/efpato/ingos.git
```
 8. Перейти в склонированный каталог и выполнить:
```bash
cd ingos
pip install -r requirements.txt
```

УСПЕХ! Вы готовы к использованию скрипта локально на своей виндовой машине

#Использование

```bash
python kasko-calc sample.xls
```
На выходе получаем Excel-файл sample.out.xls
