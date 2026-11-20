\# OVERVIEW — как работает копия YouTube



\## 1. Цель и границы



Сервис видеохостинга: регистрация/вход, загрузка видео, лента, просмотр с

лайками и комментариями, канал с плейлистами, подписка, поиск по названию,

модерация (жалобы и скрытие), приватные видео с выдачей доступа.



Стек: Python 3.11 + FastAPI + PostgreSQL 16 + MinIO (S3) + Celery (Redis broker)

\+ ffmpeg. Фронт — простой SPA. Деплой — `docker compose up` на чистой Ubuntu.



Роли: `user` (по умолчанию), `moderator`, `admin`.



\## 2. Компоненты



\- \*\*backend (FastAPI)\*\* — REST API, JWT, RBAC, выдача presigned URL, Swagger на `/docs`.

\- \*\*worker (Celery)\*\* — фоновая обработка видео: ffprobe (длительность/кодек),

&#x20; ffmpeg (превью), обновление статуса.

\- \*\*db (PostgreSQL)\*\* — метаданные: пользователи, каналы, видео, комментарии, права.

\- \*\*minio (S3)\*\* — сами файлы: `videos/{id}/source.mp4`, `videos/{id}/thumb.jpg`.

&#x20; Бакет приватный.

\- \*\*frontend\*\* — экраны: Home, Watch, Channel, Search, Upload, Login/Register, Moderation.

\- \*\*redis\*\* — брокер Celery (можно добавить в compose).



\## 3. Поток «загрузка → просмотр» (сердце системы)



1\. Клиент: `POST /videos` с title/description/visibility.

&#x20;  Бэкенд создаёт запись `videos` со `status=uploading` и возвращает

&#x20;  `{video\_id, upload\_url}` — presigned \*\*PUT\*\* в MinIO (TTL 15 мин).

2\. Клиент льёт файл напрямую в MinIO по `upload\_url`, показывает прогресс

&#x20;  (`XMLHttpRequest.upload.onprogress`). Бэкенд гигабайты не проксирует.

3\. Клиент: `POST /videos/{id}/complete` → бэкенд ставит задачу `process\_video`

&#x20;  в Celery, `status=processing`.

4\. Воркер: качает/читает объект, `ffprobe` → `duration\_sec`, `ffmpeg` → `thumb.jpg`,

&#x20;  пишет `status=ready`. При ошибке — `status=failed` + лог.

5\. Просмотр: `GET /videos/{id}/stream`. Бэкенд проверяет права (см. п.5) и

&#x20;  отдаёт presigned \*\*GET\*\* (TTL 10 мин). Если прав нет — 403.

6\. Превью в ленте: `GET /videos/{id}/thumbnail` → presigned GET на `thumb.jpg`.



\## 4. Схема БД (кратко)



\- `users(id, email, password\_hash, role, created\_at)`

\- `channels(id, owner\_id→users, name, description)` — создаётся при регистрации.

\- `videos(id, channel\_id, title, description, status, visibility,

&#x20;  storage\_key, thumbnail\_key, duration\_sec, created\_at)`

&#x20; - `status`: uploading | processing | ready | failed | hidden

&#x20; - `visibility`: public | private | unlisted

\- `video\_access(video\_id, user\_id)` — кому владелец разрешил приватное.

\- `subscriptions(user\_id, channel\_id)`

\- `likes(user\_id, video\_id, value ∈ {-1,1})` — PK (user\_id, video\_id).

\- `comments(id, video\_id, user\_id, parent\_id, body, created\_at, deleted\_at)`

\- `playlists(id, channel\_id, title)`, `playlist\_items(playlist\_id, video\_id, position)`

\- `reports(id, video\_id, reporter\_id, reason, status, resolved\_by, resolved\_at, created\_at)`



Индексы: `videos(status, visibility, created\_at DESC)`, GIN по `title` (pg\_trgm),

`comments(video\_id, created\_at)`, `reports(status)`.



\## 5. Правила доступа (единая функция `can\_view`)



Видео видно, если:

1\. `visibility=public` и `status=ready` — всем (включая анонимов);

2\. пользователь — владелец канала видео;

3\. пользователь есть в `video\_access` для этого видео;

4\. роль пользователя — `moderator` или `admin`.



Иначе — 403. Скрытое (`status=hidden`) не попадает в ленту и поиск для всех,

кроме модераторов/админов и владельца.



\## 6. Аутентификация и роли



\- Пароли — Argon2 (passlib). Минимум 8 символов.

\- JWT: access 15 мин (в `Authorization: Bearer`), refresh 7 дней в

&#x20; `HttpOnly; Secure; SameSite=Lax` cookie.

\- RBAC — зависимость `require\_role("moderator")` в FastAPI.

\- Rate limit на `/auth/register` и `/auth/login` (slowapi).



\## 7. API (основное)



```

POST /auth/register, POST /auth/login, POST /auth/refresh

GET  /videos                  лента (public+ready), пагинация

POST /videos                  создать + presigned PUT

POST /videos/{id}/complete    запустить обработку

GET  /videos/{id}             карточка (с проверкой прав)

GET  /videos/{id}/stream      presigned GET или 403

GET  /videos/{id}/thumbnail   presigned GET превью

POST /videos/{id}/like        upsert лайка (+1/-1)

GET  /videos/{id}/comments    список; POST — создать

GET  /search?q=...            ILIKE/pg\_trgm по title

GET  /channels/{id}           видео + плейлисты автора

POST /channels/{id}/subscribe

POST /reports                 жалоба на видео

PATCH /moderation/videos/{id} скрыть/вернуть (moderator/admin)

GET  /docs                    Swagger

```



\## 8. Безопасность (чек-лист)



\- Argon2, без хранения паролей в открытом виде.

\- Короткоживущие presigned URL, бакет приватный (`mc anonymous set none`).

\- Валидация загрузки через ffprobe (реальный контейнер/кодек), лимит размера.

\- CORS только origin фронта.

\- Секреты только из `.env`; `.env` в `.gitignore`, `.env.example` без значений.

\- Аудит модерации: кто/когда/что скрыл — в `reports`.

\- Все проверки прав — на бэкенде, фронт не является защитой.



\## 9. Развёртывание одной командой



```bash

cp .env.example .env

make up      # docker compose up -d --build

make seed    # демо-данные: user/moderator/admin, каналы, видео, комменты

```



После старта: `http://localhost:8000/docs` (Swagger),

`http://localhost:3000` (фронт), `http://localhost:9001` (MinIO console).



Сквозной сценарий для проверки: регистрация → загрузка → просмотр →

лайк + комментарий.



\## 10. Демо-данные (seed)



\- 3 пользователя: `user@example.com`, `moderator@example.com`, `admin@example.com`

&#x20; (пароль `password123`, только для dev).

\- 2 канала, 5 видео (3 public, 1 private с доступом user, 1 unlisted),

&#x20; 10 комментариев, 20 лайков, 2 открытые жалобы.

\- Тестовые mp4 генерируются ffmpeg при сиде (не хранятся в git).



\## 11. Тесты (критичное поведение)



\- Регистрация → логин → доступ к защищённому эндпоинту.

\- Приватное видео: владелец 200, `video\_access`-юзер 200, посторонний 403,

&#x20; аноним 403.

\- Загрузка: create → complete → status=ready (воркер замокан).

\- Лайк идемпотентен, счётчик корректен.

\- Комментарий: создание; запрет на чужое приватное видео.

\- Модерация: moderator скрывает, user получает 403, скрытое не в фиде.

\- Поиск по title.



\## 12. Git и ИИ



\- Атомарные коммиты по шагам, без squash, `.git` сдаётся целиком.

\- Диалоги ИИ — в `prompts/` в исходном формате инструмента

&#x20; (`\*.jsonl` из `\~/.claude/projects/<project>/` или экспорт Cursor/ChatGPT).

\- Обвязка: `CLAUDE.md`, `.claude/{agents,skills,commands,settings.json}`,

&#x20; `.mcp.json` (или `.cursor/` — что использовали).

\- Промпты — декомпозированные: «модель + миграция + тест», а не «сделай YouTube».

