from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from . import db
from .keyboards import (
    KinophilesCallback,
    get_confirmation_keyboard,
    get_edit_field_keyboard,
    get_edit_items_keyboard,
    get_edit_list_category_keyboard,
    get_go_to_private_keyboard,
    get_main_menu_keyboard,
    get_my_list_menu_keyboard,
    get_other_users_keyboard,
    get_view_category_keyboard,
    get_view_items_keyboard,
)
from .states import AddItem, CreateList, EditItem, KinophilesMenu, RenameList

kinophiles_router = Router()


TEXT_MAIN_MENU = """<b>Добро пожаловать в 'Кинофилы'!</b>

Здесь вы можете создавать свои списки рекомендаций фильмов/сериалов и просматривать списки других участников.

- <b>Мой список</b>: Управление вашим личным списком рекомендаций.
- <b>Другие пользователи</b>: Просмотр рекомендаций от других.
"""


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
    """Обработчик для возврата в главное меню (только в лс)."""
    await bot.answer_callback_query(callback.id)
    await state.clear()
    await callback.message.edit_text(
        TEXT_MAIN_MENU, reply_markup=get_main_menu_keyboard(), parse_mode="HTML"
    )


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "my_list"), F.message.chat.type == "private"
)
async def cq_my_list(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Обработчик для меню 'Мой список' (только в лс)."""
    await bot.answer_callback_query(callback.id)
    await (
        state.clear()
    )  # Сбрасываем состояние на случай, если пользователь вышел из другого сценария
    user_list = await db.get_user_list_by_id(callback.from_user.id)

    text = ""
    if user_list:
        _, list_name = user_list
        text = f"Ваш список: <b>{list_name}</b>\n\nВыберите действие:"
    else:
        text = "У вас еще нет списка рекомендаций. Хотите создать?"

    await callback.message.edit_text(
        text,
        reply_markup=get_my_list_menu_keyboard(has_list=bool(user_list)),
        parse_mode="HTML",
    )


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "create_list"),
    F.message.chat.type == "private",
)
async def cq_create_list(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Начало процесса создания списка (только в лс)."""
    await bot.answer_callback_query(callback.id)
    await state.set_state(CreateList.entering_name)
    await callback.message.edit_text(
        "Отлично! Придумайте название для вашего списка (например, 'Цыганские бестселлеры')."
    )


@kinophiles_router.message(CreateList.entering_name, F.chat.type == "private")
async def process_create_list_name(message: Message, state: FSMContext):
    """Обработка введенного имени для списка и его создание (только в лс)."""
    list_name = message.text.strip()
    user_id = message.from_user.id

    if await db.get_list_by_name(list_name):
        await message.answer(
            "Список с таким названием уже существует. Пожалуйста, введите другое."
        )
        return

    if await db.get_user_list_by_id(user_id):
        await message.answer("У вас уже есть список. Вы не можете создать еще один.")
        user_list = await db.get_user_list_by_id(user_id)
        await message.answer(
            f"Ваш список: <b>{user_list[1]}</b>",
            reply_markup=get_my_list_menu_keyboard(has_list=True),
            parse_mode="HTML",
        )
        await state.clear()
        return

    await db.create_user_list(user_id, list_name)
    await state.clear()

    await message.answer(
        f"Ваш список '<b>{list_name}</b>' успешно создан!",
        reply_markup=get_my_list_menu_keyboard(has_list=True),
        parse_mode="HTML",
    )


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "rename_list"),
    F.message.chat.type == "private",
)
async def cq_rename_list_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Начало процесса переименования списка."""
    await bot.answer_callback_query(callback.id)
    await state.set_state(RenameList.entering_new_name)
    await callback.message.edit_text("Введите новое название для вашего списка:")


@kinophiles_router.message(RenameList.entering_new_name, F.chat.type == "private")
async def process_rename_list_name(message: Message, state: FSMContext):
    """Обработка нового имени и переименование списка."""
    new_name = message.text.strip()
    user_id = message.from_user.id

    if await db.get_list_by_name(new_name):
        await message.answer(
            "Список с таким названием уже существует. Пожалуйста, введите другое."
        )
        return

    await db.update_list_name(user_id, new_name)
    await state.clear()

    await message.answer(
        f"Название вашего списка изменено на '<b>{new_name}</b>'!", parse_mode="HTML"
    )

    # Показываем обновленное меню "Мой список"
    user_list = await db.get_user_list_by_id(user_id)
    await message.answer(
        f"Ваш список: <b>{user_list[1]}</b>\n\nВыберите действие:",
        reply_markup=get_my_list_menu_keyboard(has_list=True),
        parse_mode="HTML",
    )


@kinophiles_router.callback_query(KinophilesCallback.filter(F.action == "other_lists"))
async def cq_other_lists(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Показывает списки других пользователей."""
    # await bot.answer_callback_query(callback.id)
    all_lists = await db.get_all_lists()
    other_lists = [lst for lst in all_lists if lst[2] != callback.from_user.id]

    if not other_lists:
        await callback.answer(
            "Пока нет ни одного списка от других пользователей.", show_alert=True
        )
        return

    await callback.message.edit_text(
        "Выберите пользователя, чей список вы хотите посмотреть:",
        reply_markup=get_other_users_keyboard(other_lists),
    )


@kinophiles_router.callback_query(KinophilesCallback.filter(F.action == "view_list"))
async def cq_view_list(
    callback: CallbackQuery,
    callback_data: KinophilesCallback,
    state: FSMContext,
    bot: Bot,
):
    """Показывает категории для выбранного списка."""
    await bot.answer_callback_query(callback.id)
    list_id = callback_data.list_id
    await callback.message.edit_text(
        "Выберите категорию для просмотра:",
        reply_markup=get_view_category_keyboard(list_id),
    )


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "view_category")
)
async def cq_view_category(
    callback: CallbackQuery,
    callback_data: KinophilesCallback,
    state: FSMContext,
    bot: Bot,
):
    """Показывает элементы в выбранной категории с пагинацией."""
    await bot.answer_callback_query(callback.id)
    list_id = callback_data.list_id
    category = callback_data.category
    page = callback_data.page

    items = await db.get_items_from_list(list_id, category, page)
    total_count = await db.get_item_count(list_id, category)
    total_pages = (total_count + 9) // 10

    if not items and page == 1:
        await callback.answer("В этой категории пока нет записей.", show_alert=True)
        return
    elif not items and page > 1:
        page = 1
        items = await db.get_items_from_list(list_id, category, page)
        total_pages = (total_count + 9) // 10

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


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "edit_list_menu"),
    F.message.chat.type == "private",
)
async def cq_edit_list_menu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Показывает меню выбора категории для редактирования."""
    await bot.answer_callback_query(callback.id)
    await state.set_state(KinophilesMenu.editing_items)
    await state.update_data(selected_ids=[])
    await callback.message.edit_text(
        "Выберите, что вы хотите изменить:",
        reply_markup=get_edit_list_category_keyboard(),
    )


async def _draw_edit_items_page(
    message: Message, state: FSMContext, category: str, page: int, list_id: int
):
    """Helper function to draw the 'edit items' page."""
    current_data = await state.get_data()
    selected_ids = current_data.get("selected_ids", [])

    items = await db.get_items_from_list(list_id, category, page)
    total_count = await db.get_item_count(list_id, category)
    total_pages = (total_count + 9) // 10 if total_count > 0 else 1

    if not items and page > 1:
        page -= 1
        items = await db.get_items_from_list(list_id, category, page)
        if items:
            total_pages = (total_count + 9) // 10 if total_count > 0 else 1

    text = f"Ваши <b>{category}ы</b> (страница {page}/{total_pages}):"
    if not items and page == 1:
        text = f"У вас пока нет добавленных {category}ов."

    await message.edit_text(
        text,
        reply_markup=get_edit_items_keyboard(
            items, category, page, total_pages, selected_ids
        ),
        parse_mode="HTML",
    )


@kinophiles_router.callback_query(
    KinophilesCallback.filter(
        F.action.in_({"edit_items_list", "select_item", "cancel_selection"})
    ),
    StateFilter(KinophilesMenu.editing_items, EditItem.choosing_field),
    F.message.chat.type == "private",
)
async def cq_edit_items_list(
    callback: CallbackQuery,
    callback_data: KinophilesCallback,
    state: FSMContext,
    bot: Bot,
):
    """Показывает список элементов для редактирования, обрабатывает выбор и отмену."""
    await bot.answer_callback_query(callback.id)
    user_list = await db.get_user_list_by_id(callback.from_user.id)
    if not user_list:
        await callback.answer("У вас еще нет списка.", show_alert=True)
        return
    list_id, _ = user_list

    # Если мы вернулись из меню редактирования поля, сбрасываем состояние
    if await state.get_state() == EditItem.choosing_field.state:
        await state.set_state(KinophilesMenu.editing_items)

    if callback_data.action == "select_item":
        current_data = await state.get_data()
        selected_ids = current_data.get("selected_ids", [])
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
        list_id=list_id,
    )


# --- Логика удаления (только в лс) ---


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "delete_selected"),
    KinophilesMenu.editing_items,
    F.message.chat.type == "private",
)
async def cq_delete_selected(
    callback: CallbackQuery,
    callback_data: KinophilesCallback,
    state: FSMContext,
    bot: Bot,
):
    """Удаляет выбранные элементы."""
    await bot.answer_callback_query(callback.id)
    user_list = await db.get_user_list_by_id(callback.from_user.id)
    if not user_list:
        await callback.answer("У вас еще нет списка.", show_alert=True)
        return
    list_id, _ = user_list

    current_data = await state.get_data()
    selected_ids = current_data.get("selected_ids", [])

    if not selected_ids:
        await callback.answer("Ничего не выбрано.", show_alert=True)
        return

    await db.delete_items_from_list(selected_ids)
    await callback.answer("Выбранные элементы удалены.", show_alert=True)

    await state.update_data(selected_ids=[])

    await _draw_edit_items_page(
        message=callback.message,
        state=state,
        category=callback_data.category,
        page=callback_data.page,
        list_id=list_id,
    )


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "delete_all_confirm"),
    F.message.chat.type == "private",
)
async def cq_delete_all_confirm(
    callback: CallbackQuery,
    callback_data: KinophilesCallback,
    state: FSMContext,
    bot: Bot,
):
    """Спрашивает подтверждение на удаление всех элементов."""
    await bot.answer_callback_query(callback.id)
    category = callback_data.category
    await callback.message.edit_text(
        f"Вы уверены, что хотите удалить все '{category}' из вашего списка? Это действие необратимо.",
        reply_markup=get_confirmation_keyboard("delete_all", category),
    )


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "delete_all"),
    F.message.chat.type == "private",
)
async def cq_delete_all(
    callback: CallbackQuery,
    callback_data: KinophilesCallback,
    state: FSMContext,
    bot: Bot,
):
    """Удаляет все элементы в категории."""
    await bot.answer_callback_query(callback.id)
    category = callback_data.category
    user_list = await db.get_user_list_by_id(callback.from_user.id)
    list_id = user_list[0]

    await db.delete_all_items_from_list(list_id, category)
    await callback.answer(f"Все '{category}' были удалены.", show_alert=True)

    # Reset selection and use the helper to redraw the page
    await state.update_data(selected_ids=[])
    await _draw_edit_items_page(
        message=callback.message,
        state=state,
        category=category,
        page=1,
        list_id=list_id,
    )


# --- FSM для добавления элемента (только в лс) ---


@kinophiles_router.callback_query(
    KinophilesCallback.filter(F.action == "add_item"), F.message.chat.type == "private"
)
async def cq_add_item_start(
    callback: CallbackQuery,
    callback_data: KinophilesCallback,
    state: FSMContext,
    bot: Bot,
):
    """Начало FSM для добавления нового элемента."""
    await bot.answer_callback_query(callback.id)
    category = callback_data.category
    await state.update_data(category=category)
    await state.set_state(AddItem.entering_title)

    await callback.message.edit_text(
        f"Введите название для нового элемента ('{category}'):"
    )


@kinophiles_router.message(AddItem.entering_title, F.chat.type == "private")
async def process_add_item_title(message: Message, state: FSMContext):
    """Обработка названия и запрос ссылки."""
    await state.update_data(title=message.text.strip())
    await state.set_state(AddItem.entering_link)

    await message.answer(
        "Отлично. Теперь введите ссылку (или напишите 'нет', если ее нет):"
    )


@kinophiles_router.message(AddItem.entering_link, F.chat.type == "private")
async def process_add_item_link(message: Message, state: FSMContext):
    """Обработка ссылки и запрос примечания."""
    link = message.text.strip()
    await state.update_data(link=link if link.lower() != "нет" else None)
    await state.set_state(AddItem.entering_note)

    await message.answer("Теперь введите примечание (или напишите 'нет'):")


@kinophiles_router.message(AddItem.entering_note, F.chat.type == "private")
async def process_add_item_note(message: Message, state: FSMContext):
    """Обработка примечания и сохранение элемента."""
    note = message.text.strip()
    data = await state.get_data()

    user_list = await db.get_user_list_by_id(message.from_user.id)
    list_id = user_list[0]

    await db.add_item_to_list(
        list_id=list_id,
        title=data["title"],
        category=data["category"],
        link=data["link"],
        note=note if note.lower() != "нет" else None,
    )

    await message.answer(f"✅ Элемент '{data['title']}' успешно добавлен!")

    await state.clear()
    await state.set_state(KinophilesMenu.editing_items)
    await state.update_data(selected_ids=[])

    # Re-drawing the edit page as a new message
    category = data["category"]
    page = 1
    items = await db.get_items_from_list(list_id, category, page)
    total_count = await db.get_item_count(list_id, category)
    total_pages = (total_count + 9) // 10 if total_count > 0 else 1
    text = f"Ваши <b>{category}ы</b> (страница {page}/{total_pages}):"
    if not items:
        text = f"У вас пока нет добавленных {category}ов."

    await message.answer(
        text,
        reply_markup=get_edit_items_keyboard(items, category, page, total_pages, []),
        parse_mode="HTML",
    )


# --- FSM для редактирования элемента (только в лс) ---


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
    """Начало FSM для редактирования элемента."""
    await bot.answer_callback_query(callback.id)
    item_id = callback_data.item_id
    category = callback_data.category
    page = callback_data.page

    item = await db.get_item_by_id(item_id)
    if not item:
        await callback.answer("Элемент не найден.", show_alert=True)
        return

    await state.update_data(item_id=item_id, original_category=category, page=page)
    await state.set_state(EditItem.choosing_field)

    text = (
        f"Название: <b>{item['title']}</b>\n"
        f"Ссылка: <b>{item['link']}</b>\n"
        f"Примечание: <b>{item['note']}</b>"
        f"\n\nВыберите поле для изменения:"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_edit_field_keyboard(item_id, category, page),
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
    field = callback_data.field
    await state.update_data(field_to_edit=field)
    await state.set_state(EditItem.entering_value)

    await callback.message.edit_text(f"Введите новое значение для поля '{field}':")


@kinophiles_router.message(EditItem.entering_value, F.chat.type == "private")
async def process_entering_value(message: Message, state: FSMContext):
    """Обработка нового значения и обновление элемента."""
    new_value = message.text.strip()
    data = await state.get_data()
    item_id = data["item_id"]
    field = data["field_to_edit"]
    original_category = data["original_category"]
    page = data.get("page", 1)

    item = await db.get_item_by_id(item_id)
    if not item:
        await message.answer("Ошибка: элемент не найден.", show_alert=True)
        await state.clear()
        return

    item[field] = new_value if new_value.lower() != "нет" else None

    await db.update_item_in_list(
        item_id=item_id,
        title=item["title"],
        category=item["category"],
        link=item["link"],
        note=item["note"],
    )
    if field == "title":
        mess_name_field = "название"
    elif field == "link":
        mess_name_field = "ссылка"
    elif field == "note":
        mess_name_field = "примечание"
    else:
        mess_name_field = field
    await message.answer(
        f"✅ Поле {mess_name_field} успешно обновлено для элемента '{item['title']}'!"
    )

    await state.clear()
    await state.set_state(KinophilesMenu.editing_items)
    await state.update_data(selected_ids=[])

    user_list = await db.get_user_list_by_id(message.from_user.id)
    list_id = user_list[0]

    # Re-drawing the edit page as a new message
    items = await db.get_items_from_list(list_id, original_category, page)
    total_count = await db.get_item_count(list_id, original_category)
    total_pages = (total_count + 9) // 10 if total_count > 0 else 1
    text = f"Ваши <b>{original_category}ы</b> (страница {page}/{total_pages}):"
    if not items:
        text = f"У вас пока нет добавленных {original_category}ов."

    await message.answer(
        text,
        reply_markup=get_edit_items_keyboard(
            items, original_category, page, total_pages, []
        ),
        parse_mode="HTML",
    )


# @kinophiles_router.callback_query()
# async def catch_all_callbacks(callback: CallbackQuery):
#     print("Caught callback query:", callback.data)
#     try:
#         data = KinophilesCallback.unpack(callback.data)
#         print("Unpacked data:", data)
#     except Exception as e:
#         print("Could not unpack data:", e)
#     await callback.answer("This callback was not handled by any specific handler.")
