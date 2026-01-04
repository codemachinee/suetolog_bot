from typing import List, Optional, Tuple

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .db import Item

# --- CallbackData Factory ---


class KinophilesCallback(CallbackData, prefix="kino"):
    """
    Фабрика CallbackData для функции 'Кинофилы'.
    - action: основное действие (например, 'my_list', 'edit_item')
    - item_id: ID фильма/сериала
    - list_id: ID списка пользователя
    - category: 'фильм' или 'сериал'
    - page: номер страницы для пагинации
    - field: поле для редактирования ('title', 'link', 'note')
    """

    action: str
    item_id: Optional[int] = None
    list_id: Optional[int] = None
    category: Optional[str] = None
    page: Optional[int] = None
    field: Optional[str] = None


# --- Генераторы клавиатур ---


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Возвращает клавиатуру главного меню для личного чата."""
    buttons = [
        [
            InlineKeyboardButton(
                text="👤 Мой список",
                callback_data=KinophilesCallback(action="my_list").pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Другие пользователи",
                callback_data=KinophilesCallback(action="other_lists").pack(),
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_my_list_menu_keyboard(has_list: bool) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру для меню 'Мой список'."""
    buttons = []
    if has_list:
        buttons.extend(
            [
                [
                    InlineKeyboardButton(
                        text="✏️ Изменить список",
                        callback_data=KinophilesCallback(
                            action="edit_list_menu"
                        ).pack(),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="✍️ Сменить название",
                        callback_data=KinophilesCallback(action="rename_list").pack(),
                    )
                ],
            ]
        )
    else:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="✨ Создать список",
                    callback_data=KinophilesCallback(action="create_list").pack(),
                )
            ]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=KinophilesCallback(action="main_menu").pack(),
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_edit_list_category_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора категории для редактирования."""
    buttons = [
        [
            InlineKeyboardButton(
                text="🎬 Фильмы",
                callback_data=KinophilesCallback(
                    action="edit_items_list", category="фильм", page=1
                ).pack(),
            ),
            InlineKeyboardButton(
                text="📺 Сериалы",
                callback_data=KinophilesCallback(
                    action="edit_items_list", category="сериал", page=1
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=KinophilesCallback(action="my_list").pack(),
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_button_keyboard(back_to: str, **kwargs) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру с одной кнопкой 'Назад'."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=KinophilesCallback(action=back_to, **kwargs).pack(),
                )
            ]
        ]
    )


def get_other_users_keyboard(lists: List[Tuple[int, str, int]]) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру со списками других пользователей."""
    buttons = []
    for list_id, list_name, user_id in lists:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=list_name,
                    callback_data=KinophilesCallback(
                        action="view_list", list_id=list_id
                    ).pack(),
                )
            ]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=KinophilesCallback(action="main_menu").pack(),
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_view_category_keyboard(list_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для выбора категории для просмотра."""
    buttons = [
        [
            InlineKeyboardButton(
                text="🎬 Фильмы",
                callback_data=KinophilesCallback(
                    action="view_category", list_id=list_id, category="фильм", page=1
                ).pack(),
            ),
            InlineKeyboardButton(
                text="📺 Сериалы",
                callback_data=KinophilesCallback(
                    action="view_category", list_id=list_id, category="сериал", page=1
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="⬅️ К спискам пользователей",
                callback_data=KinophilesCallback(action="other_lists").pack(),
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_confirmation_keyboard(action: str, category: str) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру подтверждения."""
    buttons = [
        [
            InlineKeyboardButton(
                text="Да, удалить все",
                callback_data=KinophilesCallback(
                    action=action, category=category
                ).pack(),
            ),
            InlineKeyboardButton(
                text="Нет, вернуться",
                callback_data=KinophilesCallback(
                    action="edit_items_list", category=category, page=1
                ).pack(),
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_view_items_keyboard(
    list_id: int, category: str, page: int, total_pages: int
) -> InlineKeyboardMarkup:
    """Собирает клавиатуру для просмотра элементов с пагинацией."""
    buttons = []
    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=KinophilesCallback(
                    action="view_category",
                    list_id=list_id,
                    category=category,
                    page=page - 1,
                ).pack(),
            )
        )
    if page < total_pages:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="Вперед ➡️",
                callback_data=KinophilesCallback(
                    action="view_category",
                    list_id=list_id,
                    category=category,
                    page=page + 1,
                ).pack(),
            )
        )
    if pagination_buttons:
        buttons.append(pagination_buttons)

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ К категориям",
                callback_data=KinophilesCallback(
                    action="view_list", list_id=list_id
                ).pack(),
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_edit_items_keyboard(
    items: List[Item],
    category: str,
    page: int,
    total_pages: int,
    selected_ids: List[int] = None,
) -> InlineKeyboardMarkup:
    """
    Собирает клавиатуру для редактирования списка элементов с пагинацией и выбором.
    """
    if selected_ids is None:
        selected_ids = []

    buttons = []
    # Кнопки с элементами
    for item in items:
        is_selected = item["id"] in selected_ids

        item_buttons = []
        # Кнопка для выбора/отмены выбора
        item_text = f"✅ {item['title']}" if is_selected else item["title"]
        item_buttons.append(
            InlineKeyboardButton(
                text=item_text,
                callback_data=KinophilesCallback(
                    action="select_item",
                    item_id=item["id"],
                    category=category,
                    page=page,
                ).pack(),
            )
        )

        # Кнопка редактирования появляется только если элемент не выбран
        if not is_selected:
            item_buttons.append(
                InlineKeyboardButton(
                    text="✏️",  # Edit button
                    callback_data=KinophilesCallback(
                        action="edit_item_start",
                        item_id=item["id"],
                        category=category,
                        page=page,
                    ).pack(),
                )
            )
        buttons.append(item_buttons)

    # Кнопки управления выбором
    if selected_ids:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="🗑️ Удалить выбранное",
                    callback_data=KinophilesCallback(
                        action="delete_selected", category=category, page=page
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data=KinophilesCallback(
                        action="cancel_selection", category=category, page=page
                    ).pack(),
                ),
            ]
        )

    # Кнопки пагинации
    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=KinophilesCallback(
                    action="edit_items_list", category=category, page=page - 1
                ).pack(),
            )
        )
    if page < total_pages:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="Вперед ➡️",
                callback_data=KinophilesCallback(
                    action="edit_items_list", category=category, page=page + 1
                ).pack(),
            )
        )
    if pagination_buttons:
        buttons.append(pagination_buttons)

    # Основные кнопки управления
    buttons.append(
        [
            InlineKeyboardButton(
                text=f"➕ Добавить {'фильм' if category == 'фильм' else 'сериал'}",
                callback_data=KinophilesCallback(
                    action="add_item", category=category
                ).pack(),
            )
        ]
    )
    buttons.append(
        [
            InlineKeyboardButton(
                text="💥 Удалить все",
                callback_data=KinophilesCallback(
                    action="delete_all_confirm", category=category
                ).pack(),
            )
        ]
    )
    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ К выбору категории",
                callback_data=KinophilesCallback(action="edit_list_menu").pack(),
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_edit_field_keyboard(
    item_id: int, category: str, page: int
) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру для выбора поля для редактирования."""
    buttons = [
        [
            InlineKeyboardButton(
                text="Название",
                callback_data=KinophilesCallback(
                    action="choose_field", item_id=item_id, field="title"
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="Ссылка",
                callback_data=KinophilesCallback(
                    action="choose_field", item_id=item_id, field="link"
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="Примечание",
                callback_data=KinophilesCallback(
                    action="choose_field", item_id=item_id, field="note"
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Отмена",
                callback_data=KinophilesCallback(
                    action="edit_items_list", category=category, page=page
                ).pack(),
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_go_to_private_keyboard(bot_username: str) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру с кнопкой для перехода в личный чат."""
    buttons = [
        [
            InlineKeyboardButton(
                text="👉 Перейти в личный чат",
                url=f"https://t.me/{bot_username}?start=kinophiles",
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
