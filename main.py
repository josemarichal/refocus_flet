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

CYCLE = [0, 1, 0.5]   # empty → full → half


def load_state(page: ft.Page):
    raw = page.client_storage.get("refocus_state")
    if raw:
        return json.loads(raw)
    now = datetime.now()
    return {
        "month":  now.strftime("%B %Y"),
        "year":   now.year,
        "month_num": now.month,
        "goals":  [g["name"] for g in GOALS],
        "data":   [[0] * DAYS for _ in GOALS],
        "notes":  [""] * len(GOALS),
    }


def save_state(page: ft.Page, state: dict):
    page.client_storage.set("refocus_state", json.dumps(state))


def circle_widget(value, size=28, on_tap=None):
    """Returns a GestureDetector wrapping a circle that reflects value 0/0.5/1."""
    if value == 1:
        inner = ft.Container(
            width=size, height=size,
            border_radius=size,
            bgcolor=PURPLE_MID,
            content=ft.Icon(ft.icons.CHECK, color=WHITE, size=size * 0.5),
            alignment=ft.alignment.center,
        )
    elif value == 0.5:
        inner = ft.Stack(
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
                        top_left=size, bottom_left=size
                    ),
                ),
            ],
        )
    else:
        inner = ft.Container(
            width=size, height=size,
            border_radius=size,
            bgcolor=WHITE,
            border=ft.border.all(1.5, PURPLE_BORDER),
        )

    return ft.GestureDetector(
        content=inner,
        on_tap=on_tap,
    )


def build_today_view(page, state, on_goal_tap):
    now = datetime.now()
    today_day = now.day
    controls = []

    controls.append(
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
    controls.append(ft.Container(height=8))

    for i, g in enumerate(GOALS):
        if g["sep"]:
            controls.append(
                ft.Divider(height=1, color=PURPLE_BORDER, thickness=0.8)
            )
            controls.append(ft.Container(height=4))

        day_idx = today_day - 1
        val = state["data"][i][day_idx] if day_idx < DAYS else 0

        def make_tap(idx):
            def tap(_):
                d = today_day - 1
                cur = CYCLE.index(state["data"][idx][d])
                state["data"][idx][d] = CYCLE[(cur + 1) % 3]
                save_state(page, state)
                page.views[-1].controls[0] = _make_scaffold(page, state, on_goal_tap)
                page.update()
            return tap

        # streak: count backwards from today
        streak = 0
        for d in range(day_idx, -1, -1):
            if state["data"][i][d] > 0:
                streak += 1
            else:
                break

        row = ft.Container(
            content=ft.Row(
                [
                    circle_widget(val, size=26, on_tap=make_tap(i)),
                    ft.Text(
                        g["name"],
                        size=13,
                        italic=g["italic"],
                        color=TEXT_DARK,
                        expand=True,
                    ),
                    ft.Text(f"{streak}d", size=10, color=PURPLE_MUTED),
                    ft.IconButton(
                        icon=ft.icons.CHEVRON_RIGHT,
                        icon_color=PURPLE_BORDER,
                        icon_size=16,
                        on_click=lambda _, idx=i: on_goal_tap(idx),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=WHITE,
            border_radius=14,
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border=ft.border.all(1.5, PURPLE_LIGHT),
        )
        controls.append(row)
        controls.append(ft.Container(height=5))

    return ft.Column(
        controls,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


def build_month_view(page, state, goal_idx, on_back):
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

    stat_cards = ft.Row(
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"{pct}%", size=20, weight=ft.FontWeight.W_500,
                                color=PURPLE_MID),
                        ft.Text("adherence", size=9, color=PURPLE_MUTED),
                    ],
                    spacing=2, horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                bgcolor=WHITE, border_radius=12,
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                expand=True,
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(str(streak), size=20, weight=ft.FontWeight.W_500,
                                color=PURPLE_MID),
                        ft.Text("streak", size=9, color=PURPLE_MUTED),
                    ],
                    spacing=2, horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                bgcolor=WHITE, border_radius=12,
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                expand=True,
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(str(done), size=20, weight=ft.FontWeight.W_500,
                                color=PURPLE_MID),
                        ft.Text("completed", size=9, color=PURPLE_MUTED),
                    ],
                    spacing=2, horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                bgcolor=WHITE, border_radius=12,
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                expand=True,
            ),
        ],
        spacing=8,
    )

    def make_dot_tap(d_idx):
        def tap(_):
            cur_v = CYCLE.index(state["data"][goal_idx][d_idx])
            state["data"][goal_idx][d_idx] = CYCLE[(cur_v + 1) % 3]
            save_state(page, state)
            page.views[-1].controls[0] = _make_month_scaffold(page, state, goal_idx, on_back)
            page.update()
        return tap

    grid_rows = []
    row_cells = []
    for d in range(DAYS):
        day_num = d + 1
        is_future = day_num > today_day

        if is_future:
            dot = ft.Container(
                width=28, height=28, border_radius=14,
                bgcolor="#F0EBF9",
                border=ft.border.all(1, "#E4DAFA"),
            )
        else:
            dot = circle_widget(data[d], size=28, on_tap=make_dot_tap(d))

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

    month_grid = ft.Column(grid_rows, spacing=6)

    return ft.Column(
        [
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color=WHITE,
                        icon_size=20,
                        on_click=lambda _: on_back(),
                    ),
                    ft.Column(
                        [
                            ft.Text(g["name"], size=16,
                                    weight=ft.FontWeight.W_500,
                                    italic=g["italic"], color=WHITE),
                            ft.Text("tap circles to log", size=10,
                                    color="white54"),
                        ],
                        spacing=0,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            stat_cards,
            ft.Container(height=4),
            ft.Text("APRIL — ALL 30 DAYS", size=10,
                    weight=ft.FontWeight.W_600, color=PURPLE_MID,
                    letter_spacing=1),
            ft.Container(height=4),
            month_grid,
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


def _make_scaffold(page, state, on_goal_tap):
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("Refocus", size=20,
                                            weight=ft.FontWeight.W_500,
                                            color=WHITE),
                                    ft.Text("Today's check-in", size=11,
                                            color="white70"),
                                ],
                                spacing=0,
                            ),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Text(state["month"], size=11,
                                                color=WHITE),
                                        ft.Icon(ft.icons.EXPAND_MORE,
                                                color=WHITE, size=14),
                                    ],
                                    spacing=2,
                                ),
                                bgcolor="white20",
                                border_radius=20,
                                padding=ft.padding.symmetric(
                                    horizontal=10, vertical=4),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=PURPLE_DARK,
                    padding=ft.padding.only(left=16, right=16,
                                            top=10, bottom=16),
                ),
                ft.Container(
                    content=build_today_view(page, state, on_goal_tap),
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        ),
        bgcolor=PURPLE_PALE,
        expand=True,
    )


def _make_month_scaffold(page, state, goal_idx, on_back):
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=build_month_view(page, state, goal_idx, on_back),
                    padding=ft.padding.only(left=12, right=12,
                                            top=8, bottom=8),
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        ),
        bgcolor=PURPLE_PALE,
        expand=True,
    )


def main(page: ft.Page):
    page.title = "Refocus"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = PURPLE_PALE
    page.padding = 0
    page.window_width = 390
    page.window_height = 844

    state = load_state(page)

    nav = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.icons.HOME_OUTLINED,
                selected_icon=ft.icons.HOME,
                label="Today",
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.CALENDAR_MONTH_OUTLINED,
                selected_icon=ft.icons.CALENDAR_MONTH,
                label="Month",
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.PERSON_OUTLINE,
                selected_icon=ft.icons.PERSON,
                label="Profile",
            ),
        ],
        bgcolor=PURPLE_DARK,
        indicator_color=PURPLE_LIGHT,
        label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
        selected_index=0,
    )

    content_area = ft.Ref[ft.Container]()

    def go_to_goal(idx):
        def go_back():
            content_area.current.content = _make_scaffold(page, state, go_to_goal)
            page.update()

        content_area.current.content = _make_month_scaffold(
            page, state, idx, go_back
        )
        page.update()

    main_view = _make_scaffold(page, state, go_to_goal)

    page.add(
        ft.Column(
            [
                ft.Container(
                    ref=content_area,
                    content=main_view,
                    expand=True,
                ),
                nav,
            ],
            spacing=0,
            expand=True,
        )
    )


ft.app(target=main)
