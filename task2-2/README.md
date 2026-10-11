# Задание 2. Упражнение 2.2 — RabbitMQ

Автор: Атаев Перман  
Группа: 13

## Цель

Изучить обмен сообщениями через RabbitMQ на примерах:
Hello World, Work Queues и Publish/Subscribe.

RabbitMQ запускается в Docker.
Python-программы выполняются локально на Windows.

## Окружение

- Python 3.14.7
- Pika 1.4.4
- RabbitMQ 4.3.6 — версия, использованная при выполнении
- Docker Compose

В compose.yaml используется тег rabbitmq:4-management.
При последующем скачивании этот тег может указывать на другую версию.

## Подготовка

Все команды выполняются из каталога task2-2.

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
docker compose up -d --wait
docker compose ps
```

Интерфейс управления: http://localhost:15672

Учебные данные доступа:
- пользователь: labuser;
- пароль: labpass.

Python подключается к 127.0.0.1:5672.

## Урок 1. Hello World

В первом окне PowerShell:

```powershell
.\.venv\Scripts\python.exe .\lesson1\receive.py
```

Во втором окне:

```powershell
.\.venv\Scripts\python.exe .\lesson1\send.py
```

Отправитель публикует Hello World! в очередь hello через обменник
по умолчанию. Получатель выводит сообщение на экран.

Проверка: остановить получателя, отправить сообщение и убедиться,
что Ready равно 1. После запуска получателя сообщение доставляется,
а Ready становится равным 0.

## Урок 2. Work Queues

Запустить по одному обработчику в двух отдельных окнах:

```powershell
.\.venv\Scripts\python.exe .\lesson2\worker.py
```

В третьем окне отправлять задачи:

```powershell
.\.venv\Scripts\python.exe .\lesson2\new_task.py "Task 1..."
.\.venv\Scripts\python.exe .\lesson2\new_task.py "Task 2."
.\.venv\Scripts\python.exe .\lesson2\new_task.py "Task 3.."
```

Каждая точка означает одну секунду обработки.
Обработчики используют общую очередь task_queue.

Особенности:
- подтверждение basic_ack отправляется после обработки;
- prefetch_count=1 ограничивает число неподтверждённых задач
  у каждого обработчика;
- очередь объявлена durable и имеет тип quorum;
- сообщения отправляются с delivery_mode=2;
- отправитель использует подтверждения публикации.

Проверки:
1. Распределение задач между двумя обработчиками.
2. Остановка обработчика до подтверждения и повторная доставка
   незавершённой задачи другому обработчику.
3. Отправка задачи при выключенных обработчиках, перезапуск
   RabbitMQ и получение сохранённой задачи.

## Урок 3. Publish/Subscribe

Запустить по одному подписчику в двух отдельных окнах:

```powershell
.\.venv\Scripts\python.exe .\lesson3\receive_logs.py
```

В третьем окне отправить сообщение:

```powershell
.\.venv\Scripts\python.exe .\lesson3\emit_log.py "Lab2 group13: broadcast test"
```

Обменник logs имеет тип fanout.
Каждый подписчик создаёт собственную временную эксклюзивную очередь
и связывает её с обменником. Оба активных подписчика получают сообщение.

После отключения подписчика его очередь удаляется.
При новом подключении создаётся новая очередь:
сообщения, отправленные во время отсутствия подписчика,
в неё не поступают.

## Завершение работы

Python-получатели останавливаются сочетанием Ctrl+C.

```powershell
docker compose down
```

Именованный том rabbitmq-data сохраняется.
Для сохранения данных не добавлять параметр -v.

## Файлы проекта

- compose.yaml — запуск RabbitMQ и проверка его состояния.
- requirements.txt — версия Python-зависимости.
- lesson1/ — отправитель и получатель Hello World.
- lesson2/ — отправитель задач и обработчик.
- lesson3/ — издатель и подписчик.
- .gitignore — исключения для Git.
- .dockerignore — исключения для возможного контекста сборки.

Сборка собственных образов в этом упражнении не используется,
поэтому .dockerignore при текущем запуске Compose не применяется.

## Источники

- https://www.rabbitmq.com/tutorials/tutorial-one-python
- https://www.rabbitmq.com/tutorials/tutorial-two-python
- https://www.rabbitmq.com/tutorials/tutorial-three-python
