import sqlite3

from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from . import db
from .keyboards import (
    KinophilesCallback,
    get_confirmation_keyboard,
    get_delete_list_confirmation_keyboard,
    get_edit_field_keyboard,
    get_edit_items_keyboard,
    get_edit_list_category_keyboard,
    get_go_to_private_keyboard,
    get_list_management_menu_keyboard,
    get_main_menu_keyboard,
    get_my_lists_menu_keyboard,
    get_other_users_keyboard,
    get_view_category_keyboard,
    get_view_items_keyboard,
)
from .states import AddItem, CreateList, EditItem, KinophilesMenu, RenameList

kinophiles_router = Router()


TEXT_MAIN_MENU = """<b>Добро пожаловать в 'Кинофилы'!</b>

Здесь вы можете создавать свои списки рекомендаций фильмов/сериалов и просматривать списки других участников.

- <b>Мои списки</b>: Управление вашими личными списками рекомендаций.
- <b>Другие пользователи</b>: Просмотр рекомендаций от других.
"""

# --- Основная навигация ---


async def _start_kinophiles_private(message: Message, state: FSMContext):
    """Логика для запуска меню 'Кинофилы' в личном чате."""
    await state.clear()
    await message.answer(
        TEXT_MAIN_MENU, reply_markup=get_main_menu_keyboard(), parse_mode="HTML"
    )


@kinophiles_router.message(Command("kinophiles"))
async def cmd_kinophiles(message: Message, state: FSMContext, bot: Bot):
    """
    Стартовый обработчик для команды /kinophiles.
    Различает личный и групповой чат.
    """
    if message.chat.type == "private":
        await _start_kinophiles_private(message, state)
    else:
        me = await bot.get_me()
        await message.answer(
            "Управление списками доступно только в личном чате с ботом. "
            "Нажмите кнопку ниже, чтобы перейти.",
            reply_markup=get_go_to_private_keyboard(me.username),
        )


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "main_menu"), F.message.chat.type == "private"
)
async def cq_main_menu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Возврат в главное меню (только в лс)."""
    await bot.answer_callback_query(callback.id)
    await state.clear()
    await callback.message.edit_text(
        TEXT_MAIN_MENU, reply_markup=get_main_menu_keyboard(), parse_mode="HTML"
    )


# --- Логика для "Мои списки" ---


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "my_lists"), F.message.chat.type == "private"
)
async def cq_my_lists(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Показывает все списки пользователя."""
    await bot.answer_callback_query(callback.id)
    await state.clear()

    user_lists = await db.get_user_lists(callback.from_user.id)
    text = (
        "У вас пока нет списков. Создайте первый!"
        if not user_lists
        else "Ваши списки:"
    )
    await callback.message.edit_text(
        text, reply_markup=get_my_lists_menu_keyboard(user_lists)
    )


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "my_list_menu"),
    F.message.chat.type == "private",
)
async def cq_my_list_menu(
    callback: CallbackQuery, callback_data: KinophilesCallback, bot: Bot, state: FSMContext
):
    """Меню управления для выбранного списка."""
    await bot.answer_callback_query(callback.id)
    list_id = callback_data.list_id
    await state.update_data(list_id=list_id)

    # Мы не можем получить имя списка из этой точки, поэтому просто общее сообщение
    await callback.message.edit_text(
        "Выбран список. Выберите действие:",
        reply_markup=get_list_management_menu_keyboard(list_id),
    )


# --- FSM для создания списка ---


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "create_list"),
    F.message.chat.type == "private",
)
async def cq_create_list(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Начало процесса создания списка."""
    await bot.answer_callback_query(callback.id)
    await state.set_state(CreateList.entering_name)
    await callback.message.edit_text(
        "Отлично! Придумайте название для вашего списка (например, 'Цыганские бестселлеры')."
    )


@kinophiles_router.message(CreateList.entering_name, F.chat.type == "private")
async def process_create_list_name(message: Message, state: FSMContext):
    """Обработка введенного имени для списка и его создание."""
    list_name = message.text.strip()
    user_id = message.from_user.id

    try:
        await db.create_user_list(user_id, list_name)
        await state.clear()
        await message.answer(f"Ваш список '<b>{list_name}</b>' успешно создан!", parse_mode="HTML")

        user_lists = await db.get_user_lists(user_id)
        await message.answer(
            "Ваши списки:", reply_markup=get_my_lists_menu_keyboard(user_lists)
        )
    except sqlite3.IntegrityError:
        await message.answer(
            "У вас уже есть список с таким названием. Пожалуйста, введите другое."
        )


# --- FSM для переименования списка ---


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "rename_list"),
    F.message.chat.type == "private",
)
async def cq_rename_list_start(
    callback: CallbackQuery, callback_data: KinophilesCallback, state: FSMContext, bot: Bot
):
    """Начало процесса переименования списка."""
    await bot.answer_callback_query(callback.id)
    await state.update_data(list_id=callback_data.list_id)
    await state.set_state(RenameList.entering_new_name)
    await callback.message.edit_text("Введите новое название для вашего списка:")


@kinophiles_router.message(RenameList.entering_new_name, F.chat.type == "private")
async def process_rename_list_name(message: Message, state: FSMContext):
    """Обработка нового имени и переименование списка."""
    new_name = message.text.strip()
    data = await state.get_data()
    list_id = data["list_id"]

    try:
        await db.update_list_name(list_id, new_name)
        await state.clear()
        await message.answer(f"Название списка изменено на '<b>{new_name}</b>'!", parse_mode="HTML")
        await message.answer(
            "Выбран список. Выберите действие:",
            reply_markup=get_list_management_menu_keyboard(list_id),
        )
    except sqlite3.IntegrityError:
        await message.answer(
            "У вас уже есть список с таким названием. Пожалуйста, введите другое."
        )


# --- Логика удаления списка ---


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "delete_list_confirm"),
    F.message.chat.type == "private",
)
async def cq_delete_list_confirm(
    callback: CallbackQuery, callback_data: KinophilesCallback, bot: Bot
):
    """Подтверждение удаления списка."""
    await bot.answer_callback_query(callback.id)
    await callback.message.edit_text(
        "<b>Вы уверены, что хотите удалить этот список и все его содержимое?</b>\n\nЭто действие необратимо.",
        reply_markup=get_delete_list_confirmation_keyboard(callback_data.list_id),
        parse_mode="HTML",
    )


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "delete_list"),
    F.message.chat.type == "private",
)
async def cq_delete_list(
    callback: CallbackQuery, callback_data: KinophilesCallback, bot: Bot, state: FSMContext
):
    """Удаление списка."""
    await bot.answer_callback_query(callback.id)
    await db.delete_list(callback_data.list_id)
    await callback.answer("Список успешно удален.", show_alert=True)

    user_lists = await db.get_user_lists(callback.from_user.id)
    text = "У вас больше нет списков." if not user_lists else "Ваши списки:"
    await callback.message.edit_text(
        text, reply_markup=get_my_lists_menu_keyboard(user_lists)
    )


# --- Просмотр чужих списков (без изменений) ---

@kinophiles_router.callback_query(KinophilesCallback.filter(F.action == "other_lists"))
async def cq_other_lists(callback: CallbackQuery, bot: Bot):
    """Показывает списки других пользователей."""
    all_lists = await db.get_all_lists()
    other_lists = [lst for lst in all_lists if lst[2] != callback.from_user.id]

    if not other_lists:
        await callback.answer("Пока нет ни одного списка от других пользователей.", show_alert=True)
        return

    await callback.message.edit_text(
        "Выберите пользователя, чей список вы хотите посмотреть:",
        reply_markup=get_other_users_keyboard(other_lists),
    )


@kinophiles_router.callback_query(KinophilesCallback.filter(F.action == "view_list"))
async def cq_view_list(
    callback: CallbackQuery, callback_data: KinophilesCallback, bot: Bot
):
    """Показывает категории для выбранного списка."""
    await bot.answer_callback_query(callback.id)
    await callback.message.edit_text(
        "Выберите категорию для просмотра:",
        reply_markup=get_view_category_keyboard(callback_data.list_id),
    )


@kinophiles_router.callback_query(KinophilesCallback.filter(F.action == "view_category"))
async def cq_view_category(
    callback: CallbackQuery, callback_data: KinophilesCallback, bot: Bot
):
    """Показывает элементы в выбранной категории с пагинацией."""
    await bot.answer_callback_query(callback.id)
    list_id, category, page = callback_data.list_id, callback_data.category, callback_data.page
    items = await db.get_items_from_list(list_id, category, page)
    total_count = await db.get_item_count(list_id, category)
    total_pages = (total_count + 9) // 10 or 1

    if not items:
        await callback.answer("В этой категории пока нет записей.", show_alert=True)
        return

    text = f"<b>{category.capitalize()}</b> (страница {page}/{total_pages})\n\n"
    for item in items:
        text += f"🎬 <b>{item['title']}</b>\n"
        if item.get("link"):
            text += f"   <a href='{item['link']}'>Ссылка</a>\n"
        if item.get("note"):
            text += f"   <i>Примечание: {item['note']}</i>\n"
        text += "\n"

    await callback.message.edit_text(
        text,
        reply_markup=get_view_items_keyboard(list_id, category, page, total_pages),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


# --- Редактирование содержимого списка ---

@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "edit_list_menu"),
    F.message.chat.type == "private",
)
async def cq_edit_list_menu(
    callback: CallbackQuery, callback_data: KinophilesCallback, state: FSMContext, bot: Bot
):
    """Показывает меню выбора категории для редактирования."""
    await bot.answer_callback_query(callback.id)
    await state.set_state(KinophilesMenu.editing_items)
    await state.update_data(selected_ids=[], list_id=callback_data.list_id)
    await callback.message.edit_text(
        "Выберите, что вы хотите изменить:",
        reply_markup=get_edit_list_category_keyboard(callback_data.list_id),
    )


async def _draw_edit_items_page(
    message: Message, state: FSMContext, category: str, page: int, list_id: int
):
    """Helper-функция для отрисовки страницы редактирования элементов."""
    data = await state.get_data()
    selected_ids = data.get("selected_ids", [])

    items = await db.get_items_from_list(list_id, category, page)
    total_count = await db.get_item_count(list_id, category)
    total_pages = (total_count + 9) // 10 or 1

    # Коррекция страницы, если она стала пустой
    if not items and page > 1:
        page -= 1
        items = await db.get_items_from_list(list_id, category, page)

    text = f"Ваши <b>{category}ы</b> (страница {page}/{total_pages}):"
    if not items:
        text = f"У вас пока нет добавленных {category}ов."

    await message.edit_text(
        text,
        reply_markup=get_edit_items_keyboard(
            list_id, items, category, page, total_pages, selected_ids
        ),
        parse_mode="HTML",
    )


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action.in_({"edit_items_list", "select_item", "cancel_selection"})),
    StateFilter(KinophilesMenu.editing_items, EditItem.choosing_field),
    F.message.chat.type == "private",
)
async def cq_edit_items_list(
    callback: CallbackQuery, callback_data: KinophilesCallback, state: FSMContext, bot: Bot
):
    """Обрабатывает навигацию и выбор на экране редактирования элементов."""
    await bot.answer_callback_query(callback.id)

    if await state.get_state() == EditItem.choosing_field:
        await state.set_state(KinophilesMenu.editing_items)

    if callback_data.action == "select_item":
        data = await state.get_data()
        selected_ids = data.get("selected_ids", [])
        item_id_to_toggle = callback_data.item_id
        if item_id_to_toggle in selected_ids:
            selected_ids.remove(item_id_to_toggle)
        else:
            selected_ids.append(item_id_to_toggle)
        await state.update_data(selected_ids=selected_ids)
    elif callback_data.action == "cancel_selection":
        await state.update_data(selected_ids=[])

    await _draw_edit_items_page(
        message=callback.message,
        state=state,
        category=callback_data.category,
        page=callback_data.page,
        list_id=callback_data.list_id,
    )


# --- Логика удаления элементов ---

@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "delete_selected"),
    KinophilesMenu.editing_items, F.message.chat.type == "private",
)
async def cq_delete_selected(
    callback: CallbackQuery, callback_data: KinophilesCallback, state: FSMContext, bot: Bot
):
    """Удаляет выбранные элементы."""
    await bot.answer_callback_query(callback.id)
    data = await state.get_data()
    selected_ids = data.get("selected_ids", [])

    if not selected_ids:
        await callback.answer("Ничего не выбрано.", show_alert=True)
        return

    await db.delete_items_from_list(selected_ids)
    await callback.answer("Выбранные элементы удалены.", show_alert=True)
    await state.update_data(selected_ids=[])

    await _draw_edit_items_page(
        message=callback.message, state=state, category=callback_data.category,
        page=callback_data.page, list_id=callback_data.list_id
    )


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "delete_all_confirm"),
    F.message.chat.type == "private",
)
async def cq_delete_all_confirm(
    callback: CallbackQuery, callback_data: KinophilesCallback, bot: Bot
):
    """Подтверждение удаления всех элементов категории."""
    await bot.answer_callback_query(callback.id)
    await callback.message.edit_text(
        f"Вы уверены, что хотите удалить все '{callback_data.category}' из этого списка? Действие необратимо.",
        reply_markup=get_confirmation_keyboard(callback_data.list_id, callback_data.category),
    )


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "delete_all_execute"),
    F.message.chat.type == "private",
)
async def cq_delete_all_execute(
    callback: CallbackQuery, callback_data: KinophilesCallback, state: FSMContext, bot: Bot
):
    """Удаляет все элементы категории."""
    await bot.answer_callback_query(callback.id)
    await db.delete_all_items_from_list(callback_data.list_id, callback_data.category)
    await callback.answer(f"Все '{callback_data.category}' были удалены.", show_alert=True)
    await state.update_data(selected_ids=[])
    await _draw_edit_items_page(
        message=callback.message, state=state, category=callback_data.category,
        page=1, list_id=callback_data.list_id
    )


# --- FSM для добавления элемента ---

@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "add_item"), F.message.chat.type == "private"
)
async def cq_add_item_start(
    callback: CallbackQuery, callback_data: KinophilesCallback, state: FSMContext, bot: Bot
):
    """Начало FSM добавления элемента."""
    await bot.answer_callback_query(callback.id)
    await state.update_data(category=callback_data.category, list_id=callback_data.list_id)
    await state.set_state(AddItem.entering_title)
    await callback.message.edit_text(f"Введите название для нового элемента ('{callback_data.category}'):")


@kinophiles_router.message(AddItem.entering_title, F.chat.type == "private")
async def process_add_item_title(message: Message, state: FSMContext):
    """Обработка названия и запрос ссылки."""
    await state.update_data(title=message.text.strip())
    await state.set_state(AddItem.entering_link)
    await message.answer("Отлично. Теперь введите ссылку (или напишите 'нет', если ее нет):")


@kinophiles_router.message(AddItem.entering_link, F.chat.type == "private")
async def process_add_item_link(message: Message, state: FSMContext):
    """Обработка ссылки и запрос примечания."""
    link = message.text.strip()
    await state.update_data(link=None if link.lower() == "нет" else link)
    await state.set_state(AddItem.entering_note)
    await message.answer("Теперь введите примечание (или напишите 'нет'):")


@kinophiles_router.message(AddItem.entering_note, F.chat.type == "private")
async def process_add_item_note(message: Message, state: FSMContext):
    """Обработка примечания и сохранение элемента."""
    note = message.text.strip()
    data = await state.get_data()
    await db.add_item_to_list(
        list_id=data["list_id"],
        title=data["title"],
        category=data["category"],
        link=data["link"],
        note=None if note.lower() == "нет" else note,
    )
    await message.answer(f"✅ Элемент '{data['title']}' успешно добавлен!")

    await state.set_state(KinophilesMenu.editing_items)
    await state.update_data(selected_ids=[])

    # ИСПРАВЛЕНИЕ: Отправляем новое сообщение вместо редактирования
    category = data["category"]
    list_id = data["list_id"]
    page = 1
    items = await db.get_items_from_list(list_id, category, page)
    total_count = await db.get_item_count(list_id, category)
    total_pages = (total_count + 9) // 10 or 1
    text = f"Ваши <b>{category}ы</b> (страница {page}/{total_pages}):"
    await message.answer(
        text,
        reply_markup=get_edit_items_keyboard(
            list_id, items, category, page, total_pages, []
        ),
        parse_mode="HTML",
    )


# --- FSM для редактирования элемента ---


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "edit_item_start"),
    F.message.chat.type == "private",
)
async def cq_edit_item_start(
    callback: CallbackQuery,
    callback_data: KinophilesCallback,
    state: FSMContext,
    bot: Bot,
):
    """Начало FSM редактирования элемента."""
    await bot.answer_callback_query(callback.id)
    item = await db.get_item_by_id(callback_data.item_id)
    if not item:
        await callback.answer("Элемент не найден.", show_alert=True)
        return

    await state.update_data(
        item_id=callback_data.item_id,
        original_category=callback_data.category,
        page=callback_data.page,
        list_id=callback_data.list_id,
    )
    await state.set_state(EditItem.choosing_field)
    text = (
        f"Название: <b>{item['title']}</b>\nСсылка: <b>{item['link']}</b>\n"
        f"Примечание: <b>{item['note']}</b>\n\nВыберите поле для изменения:"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_edit_field_keyboard(
            callback_data.item_id,
            callback_data.list_id,
            callback_data.category,
            callback_data.page,
        ),
        parse_mode="HTML",
    )


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "choose_field"),
    EditItem.choosing_field,
    F.message.chat.type == "private",
)
async def cq_choose_field(
    callback: CallbackQuery,
    callback_data: KinophilesCallback,
    state: FSMContext,
    bot: Bot,
):
    """Обработка выбора поля для редактирования."""
    await bot.answer_callback_query(callback.id)
    await state.update_data(field_to_edit=callback_data.field)
    await state.set_state(EditItem.entering_value)
    await callback.message.edit_text(
        f"Введите новое значение для поля '{callback_data.field}':"
    )


@kinophiles_router.message(EditItem.entering_value, F.chat.type == "private")
async def process_entering_value(message: Message, state: FSMContext):
    """Обработка нового значения и обновление элемента."""
    new_value = message.text.strip()
    data = await state.get_data()
    item_id, field = data["item_id"], data["field_to_edit"]

    item = await db.get_item_by_id(item_id)
    if not item:
        await message.answer("Ошибка: элемент не найден.")
        await state.clear()
        return

    item[field] = None if new_value.lower() == "нет" else new_value
    await db.update_item_in_list(
        item_id, item["title"], item["category"], item["link"], item["note"]
    )
    await message.answer(f"✅ Поле '{field}' успешно обновлено для элемента '{item['title']}'!")

    await state.set_state(KinophilesMenu.editing_items)
    await state.update_data(selected_ids=[])

    # ИСПРАВЛЕНИЕ: Отправляем новое сообщение вместо редактирования
    category = data["original_category"]
    list_id = data["list_id"]
    page = data.get("page", 1)
    items = await db.get_items_from_list(list_id, category, page)
    total_count = await db.get_item_count(list_id, category)
    total_pages = (total_count + 9) // 10 or 1
    text = f"Ваши <b>{category}ы</b> (страница {page}/{total_pages}):"
    await message.answer(
        text,
        reply_markup=get_edit_items_keyboard(
            list_id, items, category, page, total_pages, []
        ),
        parse_mode="HTML",
    )
