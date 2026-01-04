import aiosqlite
from typing import Optional, List, Tuple, Dict

DB_NAME = "kinophiles.db"

# Типизация для элемента списка
Item = Dict[str, any]

async def init_db() -> None:
    """Инициализирует базу данных и создает таблицы, если они не существуют."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_lists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                list_name TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                list_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                category TEXT NOT NULL CHECK(category IN ('фильм', 'сериал')),
                link TEXT,
                note TEXT,
                FOREIGN KEY (list_id) REFERENCES user_lists (id) ON DELETE CASCADE
            )
        """)
        await db.commit()

# --- Функции для списков пользователей ---

async def create_user_list(user_id: int, list_name: str) -> None:
    """Создает новый список для пользователя."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO user_lists (user_id, list_name) VALUES (?, ?)",
            (user_id, list_name)
        )
        await db.commit()

async def get_user_list_by_id(user_id: int) -> Optional[Tuple[int, str]]:
    """Возвращает список пользователя (id, list_name) по его user_id."""
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT id, list_name FROM user_lists WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()
        return (row['id'], row['list_name']) if row else None

async def get_all_lists() -> List[Tuple[int, str, int]]:
    """Возвращает все списки (list_id, list_name, user_id)."""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT id, list_name, user_id FROM user_lists")
        return await cursor.fetchall()

async def get_list_by_name(list_name: str) -> Optional[Tuple]:
    """Проверяет существование списка по его имени."""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT id FROM user_lists WHERE list_name = ?",
            (list_name,)
        )
        return await cursor.fetchone()

# --- Функции для элементов (фильмов/сериалов) ---

async def add_item_to_list(list_id: int, title: str, category: str, link: Optional[str], note: Optional[str]) -> None:
    """Добавляет новый элемент в список."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO items (list_id, title, category, link, note) VALUES (?, ?, ?, ?, ?)",
            (list_id, title, category, link, note)
        )
        await db.commit()

async def get_items_from_list(list_id: int, category: str, page: int = 1, limit: int = 10) -> List[Item]:
    """Возвращает элементы из списка с пагинацией."""
    offset = (page - 1) * limit
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM items WHERE list_id = ? AND category = ? ORDER BY id DESC LIMIT ? OFFSET ?",
            (list_id, category, limit, offset)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def get_item_count(list_id: int, category: str) -> int:
    """Возвращает количество элементов в списке по категории."""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM items WHERE list_id = ? AND category = ?",
            (list_id, category)
        )
        count = await cursor.fetchone()
        return count[0] if count else 0

async def delete_items_from_list(item_ids: List[int]) -> None:
    """Удаляет выбранные элементы из списка."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            f"DELETE FROM items WHERE id IN ({','.join('?' for _ in item_ids)})",
            item_ids
        )
        await db.commit()

async def delete_all_items_from_list(list_id: int, category: str) -> None:
    """Удаляет все элементы указанной категории из списка."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "DELETE FROM items WHERE list_id = ? AND category = ?",
            (list_id, category)
        )
        await db.commit()

async def get_item_by_id(item_id: int) -> Optional[Item]:
    """Получает один элемент по его ID."""
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None

async def update_item_in_list(item_id: int, title: str, category: str, link: Optional[str], note: Optional[str]) -> None:
    """Обновляет информацию об элементе."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE items SET title = ?, category = ?, link = ?, note = ? WHERE id = ?",
            (title, category, link, note, item_id)
        )
        await db.commit()
