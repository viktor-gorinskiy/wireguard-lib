import subprocess
import ipaddress
import qrcode 



class Wireguard():
    """Данный клас позволяет взаимодействовать с Wireguard через `subprocess` посылая команды в консоль.

    Класс умеет:
        * получать информацию о пирах и серверах
        * добавлять и удалять пиры
        * генерировать конфиги сервера и клиентов
        * получать новый ip адрес из доступных, в том числе из уже освободившихся адресов
        * генерировать QR код для пира
    
    Параметры инициализации класса:
        :server_name: Имя сервера(сервиса systemctl), defaults to 'wg0'
        :server_addres: URL или IP по которому клиенты будут подключаться к Wireguard, defaults to 'wireguard.example.org'
        :server_port: Думаю понятно, defaults to 51820
        :server_ip: IP адрес самого сервера, он же gateway, defaults to '10.10.10.1'
        :peer_ip_mask: Маска IP адреса, которая будет добавляться пирам, defaults to 32
        :peer_allowedIPs: Разрешенный маршруты для пиров, defaults to '0.0.0.0/0' весь трафик в Wireguard
        :dns: Передать клиентам DNS

            Это актуально, если например передаются маршруты во внутреннюю сеть за VPN. Но Ваш DNS сервер должен уметь резолвить так же и внешние адреса.
        :server_private_key: Приватный ключ сервера из него будет генерироваться публичныйключ, который будет добавляться в конфиги пиров, defaults to ''
    """
    def __init__(
        self, 
        server_name = 'wg0', 
        server_addres = 'wireguard.example.org',
        server_port = 51820, 
        server_ip = '10.10.10.1',
        peer_ip_mask = 32, 
        peer_allowedIPs = '0.0.0.0/0', 
        dns = '',
        server_private_key = ''
        ):


        self.server_name = server_name
        self.server_addres = server_addres
        self.server_port = server_port
        self.server_ip = server_ip
        self.peer_ip_mask = peer_ip_mask
        self.peer_allowedIPs = peer_allowedIPs
        self.dns = dns
        self.server_private_key = server_private_key
        

    @property
    def get_private_key(self):
        """Получить приватный ключ

        :return: wireguard private_key
        """
        cmd = f"wg genkey"
        private_key = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').rstrip()
        return private_key

    def get_pub_key(self, private_key):
        """Получить публичный ключ

        :param private_key: Приватный ключ
        :return: wireguard pub_key
        """
        cmd = f"/bin/echo '{private_key}' | wg pubkey"
        pub_key = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').rstrip()
        return pub_key
    
    @property
    def keys(self):
        """Получить пару приватного и публичного ключей

        :return: wireguard keys
        :rtype: dict
        """
        private_key = self.get_private_key
        pub_key = self.get_pub_key(private_key)
        return {'private_key':private_key, 'pub_key': pub_key}
    

    def add(self, public_key='', ip=''):
        """Добавить пир(клиента)

        :param public_key: Публичный ключ пира(клиента)
        """
        ip = str(ip) + '/' + str(self.peer_ip_mask)
        cmd = f"""wg set  '{self.server_name}' peer '{public_key}' allowed-ips '{ip}'"""
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return True
    
    def delete(self, public_key=""):
        """Удаляет пир(клиента) используя его публичный ключ.

        :param public_key: Публичный ключ клиента, defaults to ""
        :type public_key: str, optional
        """

        cmd = f"wg set {self.server_name} peer  {public_key} remove"
        # print(cmd)
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # print(res.communicate()[0].decode('utf-8'))
        return True


    def info(self, who):
        """Возвращает либо ip адреса, либо список список публичных ключей текущих пиров

        :param who: что возвращать peers или ip_addresses. Наверно надо переделать
      
        """
        ip_addresses = []
        peers = []
        cmd = f"wg show '{self.server_name}' allowed-ips"
        result_wg_info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').split('\n')
        print('result_wg_info', result_wg_info)
        for l in result_wg_info:
            if l:
                ip_addresses.append(l.split('\t')[1].split(str(self.peer_ip_mask))[0])
                peers.append(l.split('\t')[0])
        if who == 'ip_addresses':
            return ip_addresses
        if who == 'peers':
            return peers
    

    @property
    def status(self):
        """Статус клиентов сервера

        :return: Возвращает словарь клиентов и их статус
        :rtype: dict
        """
        cmd = f"wg show '{self.server_name}'"
        result_wg_info = \
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8')
        peers_online = {}
        for peer in result_wg_info.split('\n\n'):
            peer_data = peer.split('\n')
            peer = ''
            server_addres = ''
            handshake = ''
            allowed_ip_addresses = ''
            for data in peer_data:
                peer_dict = {}
                if 'peer:' in data:
                    peer = data.split('peer: ')[1]
                if 'server_addres: ' in data:
                    server_addres = data.split('server_addres: ')[1].split(':')[0]
                if 'latest handshake: ' in data:
                    handshake = str(data.split('latest handshake: ')[1].split(':')[0].split('\n')).strip('[]').replace(
                        ' ', '_').replace('\'', '')
                    # print(handshake)
                if 'allowed ip_addresses:' in data:
                    allowed_ip_addresses = data.split('allowed ip_addresses: ')[1].split(':')[0]

                if peer:
                    peer_dict['server_addres'] = server_addres
                    peer_dict['handshake'] = handshake
                    peer_dict['allowed_ip_addresses'] = allowed_ip_addresses
                    peers_online[peer] = peer_dict
        if peers_online:
            return peers_online
        return False


    def get_config_client(self, peer_private_key, peer_ip, allowedIPs=''):
        """Генерирует конфиг клиента.
        Может использоваться для генерации qr кода и/или файла.

        :param peer_private_key: Приватный ключ пира/клиента
        :param peer_ip: ip адрес, который будет назначет клиенту в VPN сети
        :param allowedIPs: Разрешонные сети, куда будет ходить клиент (маршруты) defaults to '0.0.0.0/0'
        :return: Конфиг пира (клиента)
        """
        dns_addr = ''
        if self.dns: dns_addr = f'DNS = {self.dns}{chr(10)}'
        if not allowedIPs: allowedIPs = self.peer_allowedIPs

        server_pub_key = self.get_pub_key(self.server_private_key)

        config_client = (
            f'[Interface]{chr(10)}'
            f'Address = {peer_ip}{chr(10)}'
            f'PrivateKey =  {peer_private_key}{chr(10)}'
            f'{dns_addr}{chr(10)}'

            f'[Peer]{chr(10)}'
            f'PublicKey = {server_pub_key}{chr(10)}'
            f'# PresharedKey ={chr(10)}'
            f'AllowedIPs = {allowedIPs}{chr(10)}'
            f'server_addres = {self.server_addres}')
        return config_client

    @property
    def get_config_server(self):
        """Генерирует конфиг сервера.
        Удобно использовать при первоначальной настройке сервера wireguard
        Стоит обратить внимание, что будет использован приватный ключ переданный при инициализации этого класса.
        Это означает, что сначало надо получить приватный ключ, а потом генерировать конфиг.

        :return: Конфиг сервера
        :rtype: _type_
        """
        config_server = (
            f'[Interface]{chr(10)}'
            f'PrivateKey = {self.server_private_key}{chr(10)}'
            f'Address = {self.server_ip}{chr(10)}'
            f'ListenPort = {self.server_port}'
        )
        return config_server

    @property
    def new_ip(self):
        """Ищет новый IP адрес сортируя имеющиеся, добавляет IP в промежутках.
        Функцию получает все ip адреса пирова (клиенитов), сортирует их в порядке увеличиния.
        Возвращает первый свободный адрес.
        Если между адресами есть свободный адрес выдает первый свободный.

        :return: ip
        :rtype: ip
        """
        ip_addresses = self.info(who='ip_addresses')
        ip_addresses_tmp = []
        for ip in ip_addresses:
            ip_addresses_tmp.append(ip)
            try:
                ipaddress.ip_address(ip)
            except Exception as error:
                ip_addresses_tmp.remove(ip)

        ip_addresses = ip_addresses_tmp
        ip_addresses = sorted([ipaddress.ip_address(addr) for addr in ip_addresses])
        if ip_addresses:
            tmp_ip = ip_addresses[0]
            for ip in ip_addresses:
                if ip == tmp_ip:
                    tmp_ip += 1
                else:
                    return tmp_ip
            return ip + 1
        return ipaddress.ip_address(self.server_ip) + 1
    

    def get_qr(self, peer_private_key, peer_ip, allowedIPs=''):
        config_peer = self.get_config_client(peer_private_key, peer_ip, allowedIPs='')
        qr = qrcode.QRCode()
        qr.add_data(config_peer)
        qr.make()
        img = qr.make_image()
        return img.convert('RGB')


