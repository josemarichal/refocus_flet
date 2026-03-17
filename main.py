import flet as ft
import json
from datetime import datetime

GOALS = [
    {"name": "build soil",           "italic": False, "sep": False},
    {"name": "avoid injury",         "italic": False, "sep": False},
    {"name": "gain strength slowly", "italic": False, "sep": False},
    {"name": "walk more",            "italic": False, "sep": False},
    {"name": "eat / drink less crap","italic": False, "sep": False},
    {"name": "drink more green tea", "italic": False, "sep": False},
    {"name": "learn techniques",     "italic": False, "sep": False},
    {"name": "appreciate / accept",  "italic": False, "sep": False},
    {"name": "write to think",       "italic": False, "sep": False},
    {"name": "reach out to friends", "italic": False, "sep": False},
    {"name": "create community",     "italic": False, "sep": False},
    {"name": "wrestle with god",     "italic": True,  "sep": True},
]

DAYS = 30
PURPLE_DARK   = "#2D1B69"
PURPLE_MID    = "#7F77DD"
PURPLE_LIGHT  = "#EEEDFE"
PURPLE_PALE   = "#F6F0FF"
PURPLE_MUTED  = "#9E8FBF"
PURPLE_BORDER = "#C8BFEA"
WHITE         = "#FFFFFF"
TEXT_DARK     = "#1C1B2E"
CYCLE = [0, 1, 0.5]


def load_state(page):
    try:
        raw = page.client_storage.get("refocus_state")
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    now = datetime.now()
    return {
        "month": now.strftime("%B %Y"),
        "data":  [[0] * DAYS for _ in GOALS],
    }


def save_state(page, state):
    try:
        page.client_storage.set("refocus_state", json.dumps(state))
    except Exception:
        pass


def circle_icon(value, size=26):
    if value == 1:
        return ft.Container(
            width=size, height=size,
            border_radius=size,
            bgcolor=PURPLE_MID,
            content=ft.Icon(ft.icons.CHECK, color=WHITE, size=size * 0.5),
            alignment=ft.alignment.center,
        )
    elif value == 0.5:
        return ft.Stack(
            width=size, height=size,
            controls=[
                ft.Container(
                    width=size, height=size,
                    border_radius=size,
                    bgcolor=WHITE,
                    border=ft.border.all(2, PURPLE_MID),
                ),
                ft.Container(
                    width=size / 2, height=size,
                    bgcolor=PURPLE_MID,
                    border_radius=ft.border_radius.only(
                        top_left=size, bottom_left=size),
                ),
            ],
        )
    else:
        return ft.Container(
            width=size, height=size,
            border_radius=size,
            bgcolor=WHITE,
            border=ft.border.all(1.5, PURPLE_BORDER),
        )


def main(page: ft.Page):
    page.title = "Refocus"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = PURPLE_PALE
    page.padding = 0

    state = load_state(page)

    def show_today():
        now = datetime.now()
        today_day = now.day

        rows = []
        rows.append(
            ft.Row(
                [
                    ft.Text("TODAY — " + now.strftime("%a %d").upper(),
                            size=11, weight=ft.FontWeight.W_600,
                            color=PURPLE_MID),
                    ft.Text(f"day {today_day} of {DAYS}",
                            size=11, color=PURPLE_MUTED),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        )
        rows.append(ft.Container(height=8))

        for i, g in enumerate(GOALS):
            if g["sep"]:
                rows.append(ft.Divider(height=1, color=PURPLE_BORDER))
                rows.append(ft.Container(height=4))

            day_idx = min(today_day - 1, DAYS - 1)
            val = state["data"][i][day_idx]

            streak = 0
            for d in range(day_idx, -1, -1):
                if state["data"][i][d] > 0:
                    streak += 1
                else:
                    break

            def make_circle_tap(idx, didx):
                def tap(_):
                    cur = CYCLE.index(state["data"][idx][didx])
                    state["data"][idx][didx] = CYCLE[(cur + 1) % 3]
                    save_state(page, state)
                    show_today()
                return tap

            def make_chevron_tap(idx):
                def tap(_):
                    show_month(idx)
                return tap

            row = ft.Container(
                content=ft.Row(
                    [
                        ft.GestureDetector(
                            content=ft.Container(
                                content=circle_icon(val, size=26),
                                width=44,
                                height=44,
                                alignment=ft.alignment.center,
                            ),
                            on_tap=make_circle_tap(i, day_idx),
                            behavior=ft.HitTestBehavior.OPAQUE,
                        ),
                        ft.GestureDetector(
                            content=ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Text(
                                            g["name"],
                                            size=13,
                                            italic=g["italic"],
                                            color=TEXT_DARK,
                                            expand=True,
                                        ),
                                        ft.Text(f"{streak}d", size=10,
                                                color=PURPLE_MUTED),
                                        ft.Icon(ft.icons.CHEVRON_RIGHT,
                                                color=PURPLE_BORDER, size=20),
                                    ],
                                    spacing=8,
                                ),
                                padding=ft.padding.only(right=8),
                            ),
                            expand=True,
                            on_tap=make_chevron_tap(i),
                            behavior=ft.HitTestBehavior.OPAQUE,
                        ),
                    ],
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=WHITE,
                border_radius=14,
                border=ft.border.all(1.5, PURPLE_LIGHT),
            )
            rows.append(row)
            rows.append(ft.Container(height=5))

        today_view = ft.View(
            "/",
            bgcolor=PURPLE_PALE,
            padding=0,
            controls=[
                ft.Column(
                    [
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Text("Refocus", size=20,
                                                    weight=ft.FontWeight.W_500,
                                                    color=WHITE),
                                            ft.Text("Today's check-in",
                                                    size=11, color="white70"),
                                        ],
                                        spacing=0,
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            state["month"], size=11,
                                            color=WHITE),
                                        bgcolor="#44FFFFFF",
                                        border_radius=20,
                                        padding=ft.padding.symmetric(
                                            horizontal=10, vertical=4),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            bgcolor=PURPLE_DARK,
                            padding=ft.padding.only(
                                left=16, right=16, top=10, bottom=16),
                        ),
                        ft.Container(
                            content=ft.Column(
                                rows,
                                spacing=0,
                                scroll=ft.ScrollMode.AUTO,
                                expand=True,
                            ),
                            padding=ft.padding.symmetric(
                                horizontal=12, vertical=8),
                            expand=True,
                        ),
                    ],
                    spacing=0,
                    expand=True,
                )
            ],
        )

        page.views.clear()
        page.views.append(today_view)
        page.update()

    def show_month(goal_idx):
        g = GOALS[goal_idx]
        data = state["data"][goal_idx]
        now = datetime.now()
        today_day = now.day

        done = sum(1 for v in data[:today_day] if v == 1)
        partial = sum(1 for v in data[:today_day] if v == 0.5)
        score = done + partial * 0.5
        pct = round((score / today_day) * 100) if today_day > 0 else 0

        streak = cur = 0
        for d in range(today_day - 1, -1, -1):
            if data[d] > 0:
                cur += 1
                streak = max(streak, cur)
            else:
                break

        def make_dot_tap(d_idx):
            def tap(_):
                cur_v = CYCLE.index(state["data"][goal_idx][d_idx])
                state["data"][goal_idx][d_idx] = CYCLE[(cur_v + 1) % 3]
                save_state(page, state)
                show_month(goal_idx)
            return tap

        grid_rows = []
        row_cells = []
        for d in range(DAYS):
            day_num = d + 1
            is_future = day_num > today_day

            if is_future:
                dot = ft.Container(
                    width=30, height=30,
                    border_radius=15,
                    bgcolor="#F0EBF9",
                    border=ft.border.all(1, "#E4DAFA"),
                )
            else:
                dot = ft.GestureDetector(
                    content=circle_icon(data[d], size=30),
                    on_tap=make_dot_tap(d),
                )

            cell = ft.Column(
                [
                    ft.Text(str(day_num), size=8, color=PURPLE_MUTED,
                            text_align=ft.TextAlign.CENTER),
                    dot,
                ],
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            row_cells.append(ft.Container(content=cell, expand=True))

            if len(row_cells) == 7 or d == DAYS - 1:
                while len(row_cells) < 7:
                    row_cells.append(ft.Container(expand=True))
                grid_rows.append(
                    ft.Row(row_cells, spacing=4,
                           alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
                row_cells = []

        month_view = ft.View(
            "/month",
            bgcolor=PURPLE_PALE,
            padding=ft.padding.all(12),
            appbar=ft.AppBar(
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color=WHITE,
                    on_click=lambda _: go_back(),
                ),
                title=ft.Column(
                    [
                        ft.Text(g["name"], size=16,
                                weight=ft.FontWeight.W_500,
                                italic=g["italic"], color=WHITE),
                        ft.Text("tap circles to log",
                                size=10, color="white70"),
                    ],
                    spacing=0,
                ),
                bgcolor=PURPLE_DARK,
                color=WHITE,
            ),
            controls=[
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(f"{pct}%", size=22,
                                                    weight=ft.FontWeight.W_500,
                                                    color=PURPLE_MID),
                                            ft.Text("adherence", size=9,
                                                    color=PURPLE_MUTED),
                                        ],
                                        spacing=2,
                                    ),
                                    bgcolor=WHITE, border_radius=12,
                                    padding=ft.padding.symmetric(
                                        horizontal=12, vertical=10),
                                    expand=True,
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(str(streak), size=22,
                                                    weight=ft.FontWeight.W_500,
                                                    color=PURPLE_MID),
                                            ft.Text("streak", size=9,
                                                    color=PURPLE_MUTED),
                                        ],
                                        spacing=2,
                                    ),
                                    bgcolor=WHITE, border_radius=12,
                                    padding=ft.padding.symmetric(
                                        horizontal=12, vertical=10),
                                    expand=True,
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(str(done), size=22,
                                                    weight=ft.FontWeight.W_500,
                                                    color=PURPLE_MID),
                                            ft.Text("completed", size=9,
                                                    color=PURPLE_MUTED),
                                        ],
                                        spacing=2,
                                    ),
                                    bgcolor=WHITE, border_radius=12,
                                    padding=ft.padding.symmetric(
                                        horizontal=12, vertical=10),
                                    expand=True,
                                ),
                            ],
                            spacing=8,
                        ),
                        ft.Container(height=8),
                        ft.Text("ALL 30 DAYS", size=10,
                                weight=ft.FontWeight.W_600,
                                color=PURPLE_MID, letter_spacing=1),
                        ft.Container(height=4),
                        ft.Column(grid_rows, spacing=6),
                    ],
                    spacing=12,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                )
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        page.views.append(month_view)
        page.update()

    def go_back():
        if len(page.views) > 1:
            page.views.pop()
            page.update()

    page.on_view_pop = lambda _: go_back()

    show_today()


ft.app(target=main)
