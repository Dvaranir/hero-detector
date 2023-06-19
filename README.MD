# Что сделано:
## Замена фона и наложение эффектов полностью сделаны. Наложение маски на лицо так же сделано, но нужно подгонять каждую созданную 2D маску. Определение знака сделано наполовину, без нейронки, через брутфорс, часто ошибается. Датасеты для нейронки подготовили, но до тренировки дело не дошло, проект свернули. 

<br>

## Модуль полностью автономный и может быть использован без бота, бот в данном случае просто выступает в качестве интерфейса. Логика обработки выполняется двумя строками ниже в init.py

<br>

```python
controller = Controller(input_save_location, def_pattern)
processed_image = controller.process_image()
```
<br>

## Проект поделен на модули, но большая часть логики находится в modules/controller.py.

<br>

1) В modules/face_replacer.py все что связано с заменой лица
2) В modules/background.py c заменой фона
3) В modules/helpers.py вспомогательный функции
4) В modules/pattern_detector.py обнаружение паттерна на фотографии
5) В modules/photo.py обработка входных изображений

<br>

### В директории models находится модель для обнаружения лица shape_predictor_68_face_landmarks.dat
### В директории masks находится тестовая маска
### В директории backgrounds фоны
### В директории effects - эффекты, вместе с исходниками
### В директории pattern находятся паттерны, которые нужно искать на фотографиях
### В директорию input_images сохраняются присланные фотографии
### В директорию output_images сохраняются обработанные фотографии

<br>

# Настройки:
1) В init.py указывается токен бота, токен можно получить через бота @BotFather в телеграмме, но я так же оставляю свой токен, могу права на токен полностью передать, если будет необходимо
2) Так же бота можно добавить в группу и в init.py указать id этой группы, он будет слать туда все присланные фотографии - это на случай необходимости дебага

<br>

# Запуск бота на Linux Ubuntu

01) Перенесите все файлы на машину с Ubuntu
02) Установите Miniconda https://docs.conda.io/en/latest/miniconda.html#linux-installers
03) Установите необходимые программы и библиотеки<br>
```bash
sudo apt install build-essential cmake
sudo apt install libopenblas-dev libjpeg-dev libpng-dev libtiff-dev libgif-dev
```
04) Перезагрузите терминал
05) В корне проекта выполните команду<br>
```bash 
conda env create -f environment-linux.yml
```
06) Затем активируете собранное окружение<br>
```bash
conda activate hero-detector-telebot
```
07) Запустите бота<br>
```bash
pytnon init.py
```

<br>

# Чтобы бот работал в фоне, его можно сделать сервисом Linux

01) Создаем новый сервис<br>
```bash
sudo nano /etc/systemd/system/NEW_SERVICE_NAME.service
```
02) Внутри сервиса:

```
SERVICE_NAME.service:
[Unit]
Description=telegram-bot
After=network.target

[Service]
User=USER

WorkingDirectory=BOT_DIRECTORY
Environment="PYTHONPATH=PYTHONPATH"
ExecStart=PATH_TO_TARGET_PYTHON3 PATH_TO_INIT.PY

[Install]
WantedBy=multi-user.target
```

03) Перезагружаем даймон systemctl
```bash
sudo systemctl daemon-reload
```

04) Включаем созданный сервис:
```bash
sudo systemctl enable SERVICE_NAME.service
```

05) Запускаем созданный сервис

```bash
sudo systemctl start SERVICE_NAME.service
```