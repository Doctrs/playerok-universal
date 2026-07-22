import math
import textwrap
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from settings import Settings as sett

from .. import callback_datas as calls


def bump_groups_text():
    groups = sett.get("auto_bump_items").get("groups", [])
    txt = textwrap.dedent(f"""
        <b>📁 Группы авто-поднятия</b>
        <blockquote><b>(?)</b> Группы имеют свой интервал и набор товаров. Группа важнее индивидуальной настройки: товар, подошедший под группу, не поднимается индивидуально.</blockquote>

        Всего <b>{len(groups)}</b> групп:
    """)
    return txt


def bump_groups_kb(page=0):
    groups: list = sett.get("auto_bump_items").get("groups", [])

    rows = []
    items_per_page = 7
    total_pages = math.ceil(len(groups) / items_per_page)
    total_pages = total_pages if total_pages > 0 else 1

    if page < 0: page = 0
    elif page >= total_pages: page = total_pages - 1

    start_offset = page * items_per_page
    end_offset = start_offset + items_per_page

    for i, group in enumerate(list(groups)[start_offset:end_offset]):
        real_index = start_offset + i
        enabled = "✅" if group.get("enabled") else "❌"
        name = group.get("name") or "Без названия"
        name_frmtd = name[:28] + ("..." if len(name) > 28 else "")
        interval = group.get("interval", 3600)
        rows.append([InlineKeyboardButton(
            text=f"{enabled} {name_frmtd} ・ {interval}с",
            callback_data=calls.BumpGroupPage(index=real_index).pack()
        )])

    if total_pages > 1:
        buttons_row = []
        btn_back = InlineKeyboardButton(text="←", callback_data=calls.BumpGroupsPagination(page=page-1).pack()) if page > 0 else InlineKeyboardButton(text="🛑", callback_data="null_answer")
        buttons_row.append(btn_back)

        btn_pages = InlineKeyboardButton(text=f"{page+1}/{total_pages}", callback_data="null_answer")
        buttons_row.append(btn_pages)

        btn_next = InlineKeyboardButton(text="→", callback_data=calls.BumpGroupsPagination(page=page+1).pack()) if page < total_pages - 1 else InlineKeyboardButton(text="🛑", callback_data="null_answer")
        buttons_row.append(btn_next)
        rows.append(buttons_row)

    rows.append([InlineKeyboardButton(text="➕ Добавить группу", callback_data="enter_new_bump_group_name")])
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.MenuNavigation(to="bump").pack())])

    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb


def bump_groups_float_text(placeholder: str):
    txt = textwrap.dedent(f"""
        <b>📁 Группы авто-поднятия</b>
        \n{placeholder}
    """)
    return txt


def new_bump_group_float_text(placeholder: str):
    txt = textwrap.dedent(f"""
        <b>➕📁 Добавление группы</b>
        \n{placeholder}
    """)
    return txt
