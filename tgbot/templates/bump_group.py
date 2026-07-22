import textwrap
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from settings import Settings as sett
from utils import get_event_next_time

from .. import callback_datas as calls


def bump_group_page_text(index: int):
    group = sett.get("auto_bump_items").get("groups", [])[index]

    enabled = "✅" if group.get("enabled") else "❌"
    all_mode = "Все товары" if group.get("all") else "Указанные товары"
    interval = group.get("interval", 3600)
    below_position = group.get("below_position", 0)
    below_position_str = f"ниже {below_position}" if below_position else "❌ Выкл"
    included = len(group.get("included", []))
    excluded = len(group.get("excluded", []))
    name = group.get("name") or "Без названия"

    last_time_iso = group.get("last_time", "")
    last_time = datetime.fromisoformat(last_time_iso).strftime("%d.%m.%Y %H:%M:%S") if last_time_iso else "никогда"

    if group.get("enabled"):
        if not last_time_iso:
            next_time = "прямо сейчас"
        else:
            next_time = get_event_next_time(last_time_iso, interval).strftime("%d.%m.%Y %H:%M:%S")
    else:
        next_time = "никогда"

    txt = textwrap.dedent(f"""
        <b>📄📁 Группа: {name}</b>

        <b>💡 Включено:</b> {enabled}
        <b>⏰ Интервал:</b> {interval} сек.
        <b>📍 Позиция:</b> {below_position_str}
        <b>📦 Поднимать:</b> {all_mode}
        <blockquote><b>(?)</b> Если «Все товары» — все, кроме исключений группы. Если «Указанные» — только включённые (фразы через запятую), минус исключения.</blockquote>

        <b>➕ Включенные:</b> {included}
        <b>➖ Исключенные:</b> {excluded}

        ⏮️ Последний раз было <b>{last_time}</b>
        ⏭️ Следующий раз будет <b>{next_time}</b>
    """)
    return txt


def bump_group_page_kb(index: int, page: int = 0):
    group = sett.get("auto_bump_items").get("groups", [])[index]

    enabled = "✅" if group.get("enabled") else "❌"
    all_mode = "Все товары" if group.get("all") else "Указанные товары"
    interval = group.get("interval", 3600)
    below_position = group.get("below_position", 0)
    below_position_str = f"ниже {below_position}" if below_position else "❌ Выкл"
    included = len(group.get("included", []))
    excluded = len(group.get("excluded", []))
    name = group.get("name") or "Без названия"

    rows = [
        [InlineKeyboardButton(text=f"✏️ Название: {name}", callback_data="enter_bump_group_name")],
        [InlineKeyboardButton(text=f"💡 Включено: {enabled}", callback_data="switch_bump_group_enabled")],
        [InlineKeyboardButton(text=f"📦 Поднимать: {all_mode}", callback_data="switch_bump_group_all")],
        [InlineKeyboardButton(text=f"⏰ Интервал: {interval} сек.", callback_data="enter_bump_group_interval")],
        [InlineKeyboardButton(text=f"📍 Позиция: {below_position_str}", callback_data="enter_bump_group_below_position")],
        [
            InlineKeyboardButton(text=f"➕ Включенные: {included}", callback_data=calls.IncludedBumpGroupItemsPagination(group_index=index, page=0).pack()),
            InlineKeyboardButton(text=f"➖ Исключенные: {excluded}", callback_data=calls.ExcludedBumpGroupItemsPagination(group_index=index, page=0).pack()),
        ],
        [InlineKeyboardButton(text="🗑️ Удалить", callback_data="confirm_deleting_bump_group")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.BumpGroupsPagination(page=page).pack())],
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb


def bump_group_page_float_text(placeholder: str):
    txt = textwrap.dedent(f"""
        <b>📄📁 Группа авто-поднятия</b>
        \n{placeholder}
    """)
    return txt
