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
git clone https://github.com/SergiOningeR/certus_telecom_bot.git
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
### Установите необходимые пакеты:
```bash
sudo apt update
sudo apt install -y python3 python3-pip mysql-server mysql-client
```
### Настройте MySQL:
```bash
sudo mysql_secure_installation
sudo mysql -u root -p
```
### В MySQL создайте пользователя и базу данных:
```sql
CREATE DATABASE certus_telecom;
CREATE USER 'certus_bot'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON certus_telecom.* TO 'certus_bot'@'localhost';
FLUSH PRIVILEGES;
```
### Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/certus_telecom_bot.git
cd certus_telecom_bot
```
### Установите зависимости:
```bash
pip3 install -r requirements.txt
```
### Настройте бота через config/config.py

### Запустите бота (рекомендуется использовать systemd или supervisor для постоянной работы):
```bash
python3 main.py
```
## Расширение функционала
Проект разработан с учетом будущего расширения:
Модульная структура позволяет легко добавлять новые обработчики
Конфигурация вынесена в отдельный файл
База данных спроектирована с учетом возможного роста
Логика работы с задачами инкапсулирована в отдельных функциях
Для добавления новых источников заявок достаточно:
Создать новый модуль в папке handlers
Реализовать преобразование входящих данных в стандартный формат задачи
Использовать существующие функции работы с БД
Этот бот предоставляет полный цикл работы с техническими заявками от создания до завершения, с уведомлениями клиентов и администрированием через телеграм.


## Дополнительные замечания:
1. Для работы с MySQL нужно установить:
```bash
sudo apt install libmysqlclient-dev
pip install mysqlclient
```
