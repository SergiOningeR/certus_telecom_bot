import socket
from datetime import datetime
import logging
from config.config import config

class ZabbixMonitor:
    def __init__(self):
        self.zabbix_host = getattr(config, 'ZABBIX_HOST', 'zabbix.example.com')
        self.zabbix_port = getattr(config, 'ZABBIX_PORT', 10051)
        self.hostname = getattr(config, 'ZABBIX_CLIENT_NAME', 'certus-telecom-bot')
        self.logger = logging.getLogger('zabbix_monitor')

    async def send_metric(self, key: str, value: str):
        """Отправка метрики в Zabbix"""
        timestamp = int(datetime.now().timestamp())
        data = f"{self.hostname} {key} {timestamp} {value}\n"
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.zabbix_host, self.zabbix_port))
                sock.sendall(data.encode('utf-8'))
                self.logger.info(f"Sent to Zabbix: {data.strip()}")
        except Exception as e:
            self.logger.error(f"Zabbix send error: {e}")

    async def track_new_task(self, task_id: int):
        """Отслеживание новой задачи"""
        await self.send_metric('certus.telecom.new_task', task_id)

    async def track_status_change(self, task_id: int, new_status: str):
        """Отслеживание изменения статуса"""
        await self.send_metric(f'certus.telecom.status_change[{task_id}]', new_status)
