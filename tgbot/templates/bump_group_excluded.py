import math
import textwrap
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from settings import Settings as sett

from .. import callback_datas as calls


def bump_group_excluded_text(group_index: int):
    group = sett.get("auto_bump_items").get("groups", [])[group_index]
    excluded = group.get("excluded", [])
    name = group.get("name") or "Без названия"
    txt = textwrap.dedent(f"""
        <b>⬆️➖ Исключенные · {name}</b>
        Всего <b>{len(excluded)}</b> исключенных товаров:
    """)
    return txt


def bump_group_excluded_kb(group_index: int, page=0):
    group = sett.get("auto_bump_items").get("groups", [])[group_index]
    excluded: list[list] = group.get("excluded", [])

    rows = []
    items_per_page = 7
    total_pages = math.ceil(len(excluded) / items_per_page)
    total_pages = total_pages if total_pages > 0 else 1

    if page < 0: page = 0
    elif page >= total_pages: page = total_pages - 1

    start_offset = page * items_per_page
    end_offset = start_offset + items_per_page

    for keyphrases in list(excluded)[start_offset:end_offset]:
        keyphrases_frmtd = ", ".join(keyphrases) or "❌ Не указано"
        rows.append([
            InlineKeyboardButton(text=f"{keyphrases_frmtd}", callback_data="null_answer"),
            InlineKeyboardButton(text=f"🗑️", callback_data=calls.DeleteExcludedBumpGroupItem(group_index=group_index, index=excluded.index(keyphrases)).pack()),
        ])

    if total_pages > 1:
        buttons_row = []
        btn_back = InlineKeyboardButton(text="←", callback_data=calls.ExcludedBumpGroupItemsPagination(group_index=group_index, page=page-1).pack()) if page > 0 else InlineKeyboardButton(text="🛑", callback_data="null_answer")
        buttons_row.append(btn_back)

        btn_pages = InlineKeyboardButton(text=f"{page+1}/{total_pages}", callback_data="null_answer")
        buttons_row.append(btn_pages)

        btn_next = InlineKeyboardButton(text="→", callback_data=calls.ExcludedBumpGroupItemsPagination(group_index=group_index, page=page+1).pack()) if page < total_pages - 1 else InlineKeyboardButton(text="🛑", callback_data="null_answer")
        buttons_row.append(btn_next)
        rows.append(buttons_row)

    rows.append([
        InlineKeyboardButton(text="➕ Добавить", callback_data="enter_new_excluded_bump_group_item_keyphrases"),
        InlineKeyboardButton(text="➕📄 Добавить много", callback_data="send_new_excluded_bump_group_items_keyphrases_file"),
    ])
    rows.append([
        InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.BumpGroupPage(index=group_index).pack()),
    ])

    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb


def bump_group_excluded_float_text(placeholder: str):
    txt = textwrap.dedent(f"""
        <b>⬆️➖ Исключенные группы</b>
        \n{placeholder}
    """)
    return txt


def new_bump_group_excluded_float_text(placeholder: str):
    txt = textwrap.dedent(f"""
        <b>⬆️➖ Добавление исключенного товара группы</b>
        \n{placeholder}
    """)
    return txt
