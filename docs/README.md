# Описание

Библиотека для работы с wireguard

## Installation

    python3 -m pip install wireguard-lib

## Пример использования:

Сгенерируем конфиг сервера.  
Для этого нужен приватный ключ.  
Воспользуемся консолью Python для получения приватного ключа:  

```
>>> from wireguard.wireguard import Wireguard
>>> Wireguard().get_private_key
'sBd8jkAY9Ht7wn+q5iGbW4MfShgjdxB1s3oTJsttaHc='
```
Используя полученый ключ сгенерируем конфиг сервера:
```
wg = Wireguard(
    server_private_key = 'sBd8jkAY9Ht7wn+q5iGbW4MfShgjdxB1s3oTJsttaHc=',
    server_addres='wireguard.example.org',
    server_ip='10.10.10.1',
    server_port=51821,
)

server_config = wg.get_config_server
print(server_config)
```
Получим следующий конфиг:  
```
[Interface]
PrivateKey = sBd8jkAY9Ht7wn+q5iGbW4MfShgjdxB1s3oTJsttaHc=
Address = 10.10.10.1
ListenPort = 51821
```

