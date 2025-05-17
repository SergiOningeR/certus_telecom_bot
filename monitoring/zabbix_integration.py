from config.config import config
import socket

class ZabbixMonitor:
    def send_metric(self, key: str, value: str):
        data = f"{config.ZABBIX_CLIENT_NAME} {key} {value}"
        with socket.socket() as s:
            s.connect((config.ZABBIX_HOST, config.ZABBIX_PORT))
            s.sendall(data.encode())
