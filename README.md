# Автоматизация загрузки фотографий космоса от Hubble и запусков ракет SpaceX в Instagram
Для автоматизации используются три скрипта:
- fetch_hubble.py - скрипт скачивания фото с телескопа Hubble.
- fetch_spacex.py - скрипт скачивания фото запусков компании SpaceX.
- load_instagram.py - скрипт загрузки фото в Instagram.

### Требования
- Для работы необходим Python 3.6+
- Подключение к сети Интернет

### Как установить
- Скачиваем скрипт с [github](https://github.com/dumbturtle/api_4)
- Переименовываем `env_template` в `.env`. В данном файле необходимо указать регистрационные данные для Instagram. Более подробно смотри раздел [Параметры скриптов](#параметры-скриптов).
- Устанавливаем необходимые пакеты: 
     
```
$ pip install -r requirements.txt
```
- Запуск скрипта скачивания фото с телескопа Hubble:  
    
```
$ python fetch_hubble.py
``` 
- Запуск скрипта скачивания фото запусков компании SpaceX:  
    
```
$ python fetch_spacex.py
``` 
- Запуск скрипта загрузки фото в Instagram:  
    
```
$ python load_instagram.py
``` 

Если при запуске возникнет ошибка, будет выведено соответствующее сообщение в консоли.

### Параметры скриптов
Параметры работы скриптов указаны в файле `.env`.

#### Параметры скрипта скачивания фото с телескопа Hubble (fetch_hubble.py).

- `HUBBLE_IMAGE_API_LINK` в данном параметре указывается ссылка на раздел API с фотографиями. 
- `HUBBLE_COLLECTION_API_LINK` в данном параметре указывается ссылка на раздел API с коллекциями фотографий.
- `HUBBLE_COLLECTION_NAME` в данном параметре указывается название коллекции. Список коллекций [ссылка](http://hubblesite.org/api/documentation#images).

Пример раздела `Hubble API settings` в файле конфигурации:
```
#Hubble API settings
HUBBLE_IMAGE_API_LINK="http://hubblesite.org/api/v3/image/"
HUBBLE_COLLECTION_API_LINK="http://hubblesite.org/api/v3/images/"
HUBBLE_COLLECTION_NAME="stsci_gallery"
```

#### Параметры скрипта скачивания фото запусков компании SpaceX (fetch_spacex.py).

- `SPACEX_IMAGE_API_LINK` в данном параметре указывается ссылка на раздел API в котором хранятся фотографии запусков.
- `LAUNCH_ID` в данном параметре указывается номер запуска. Для получения фотографий последнего запуска, необходимо присвоить переменной значение `last`.

Пример раздела `SpaceX API settings` в файле конфигурации:
```
#SpaceX API settings
SPACEX_IMAGE_API_LINK="https://api.spacexdata.com/v3/launches" 
LAUNCH_ID="64"
```

#### Параметры скрипта загрузки фото в Instagram (load_instagram.py).
- `INSTAGRAM_USERNAME` в данном параметре указывается имя пользователя для Instagram.
- `INSTAGRAM_PASSWORD` в данном параметре указывается пароль для Instagram.

Пример раздела `Instagram credential` в файле конфигурации:
```
#Instagram credential
INSTAGRAM_USERNAME="Your login"
INSTAGRAM_PASSWORD="Your password"
```
