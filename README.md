# Wireguard

Библиотека для работы с wireguard

## Installation

    python3 -m pip install wireguard-lib

## Configuration

wg = wireguard(
    server_name = 'wg-server',  
    server_ip='10.10.10.1',  
    server_addres = 'vpn_server',  
    server_private_key='8HE2V8gZawY5baiCUNOD9gUwnAjsSiD8V57+kFWX9Uw=',  
    dns = '8.8.8.8',  
    peer_allowedIPs= '10.10.0.0/18, 192.168.0.0/16'  
)

## License

[GPL-3.0](LICENSE)
