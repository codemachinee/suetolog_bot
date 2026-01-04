from aiogram.fsm.state import State, StatesGroup

class CreateList(StatesGroup):
    """Состояния для процесса создания нового списка."""
    entering_name = State()

class AddItem(StatesGroup):
    """Состояния для процесса добавления нового элемента (фильма/сериала)."""
    choosing_category = State()
    entering_title = State()
    entering_link = State()
    entering_note = State()
    confirm_add = State()

class EditItem(StatesGroup):
    """Состояния для процесса редактирования элемента."""
    choosing_item = State()
    choosing_field = State()
    entering_value = State()

class KinophilesMenu(StatesGroup):
    """Общие состояния для навигации по меню."""
    main_menu = State()
    my_list_menu = State()
    other_lists_menu = State()
    viewing_items = State()
    editing_items = State()
