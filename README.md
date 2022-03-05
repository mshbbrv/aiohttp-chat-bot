API-сервер чат-бота во Вконтакте для проведения викторины
## Запуск приложения

```
python3 main.py
```


### Реализованные методы:
- запрос на авторизацию администратора
- запрос на информацию об администраторе в текущей сессии
- добавление новой темы вопросов
- запрос, который возвращает список всех доступных тем
- добавление нового вопроса
- запрос, который возвращает список всех вопрос с фильтрацией по категории

### Используемые библиотеки:
```
aiohttp>=3.7.4.post0
pyyaml==5.4.1
marshmallow~=3.13.0
aiohttp-apispec==2.2.1
aiohttp-session==2.9.0
cryptography==3.4.7
markupsafe==2.0.1
```

