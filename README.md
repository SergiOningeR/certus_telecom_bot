# Certus Telecom Support Bot

Телеграм-бот для управления техническими заявками компании Certus Telecom.

## Функционал

### Для клиентов:
- Создание заявок с прикреплением изображений
- Просмотр статуса своих заявок
- Отмена заявок

### Для администраторов:
- Просмотр всех заявок
- Управление статусами заявок
- Поиск заявок по клиентам/компаниям
- Комментирование и отчетность по заявкам

## Установка

1. Клонировать репозиторий:
```bash
git clone https://github.com/yourusername/certus_telecom_bot.git
cd certus_telecom_bot
```
2. Установить зависимости:
```bash
pip install -r requirements.txt
```
Настроить конфигурацию в config/config.py

Инициализировать БД:

```bash
python -m database.setup_db
```
Запустить бота:
```bash
python main.py
```

## Развертывание на Debian 12

## Дополнительные замечания:
1. Для работы с MySQL нужно установить:
```bash
sudo apt install libmysqlclient-dev
pip install mysqlclient
```
