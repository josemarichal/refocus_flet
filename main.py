import flet as ft
import json
from datetime import datetime

DEFAULT_GOALS = [
    {"name": "build soil",            "italic": False, "sep": False},
    {"name": "avoid injury",          "italic": False, "sep": False},
    {"name": "gain strength slowly",  "italic": False, "sep": False},
    {"name": "walk more",             "italic": False, "sep": False},
    {"name": "eat / drink less crap", "italic": False, "sep": False},
    {"name": "drink more green tea",  "italic": False, "sep": False},
    {"name": "learn techniques",      "italic": False, "sep": False},
    {"name": "appreciate / accept",   "italic": False, "sep": False},
    {"name": "write to think",        "italic": False, "sep": False},
    {"name": "reach out to friends",  "italic": False, "sep": False},
    {"name": "create community",      "italic": False, "sep": False},
    {"name": "wrestle with god",      "italic": True,  "sep": True},
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
RED_DELETE    = "#E53935"
CYCLE = [0, 0.25, 0.5, 0.75, 1]

current_goal = 0


def load_state(page):
    try:
        raw = page.client_storage.get("refocus_state")
        if raw:
            d = json.loads(raw)
            # migrate: add goals if missing
            if "goals" not in d:
                d["goals"] = list(DEFAULT_GOALS)
            # sync data length to goal count
            while len(d["data"]) < len(d["goals"]):
                d["data"].append([0] * DAYS)
            d["data"] = d["data"][:len(d["goals"])]
            return d
    except Exception:
        pass
    return {
        "month": datetime.now().strftime("%B %Y"),
        "data":  [[0] * DAYS for _ in DEFAULT_GOALS],
        "goals": list(DEFAULT_GOALS),
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
            content=ft.Icon(ft.Icons.CHECK, color=WHITE, size=size * 0.5),
            alignment=ft.Alignment(0, 0),
        )
    elif value == 0:
        return ft.Container(
            width=size, height=size,
            border_radius=size,
            bgcolor=WHITE,
            border=ft.border.all(1.5, PURPLE_BORDER),
        )
    else:
        # Drawing quadrants for 0.25, 0.5, 0.75
        half = size / 2
        
        def quad(is_filled):
            return ft.Container(
                width=half, height=half,
                bgcolor=PURPLE_MID if is_filled else "transparent",
            )

        return ft.Stack(
            width=size, height=size,
            controls=[
                # Base circle border
                ft.Container(
                    width=size, height=size,
                    border_radius=size,
                    bgcolor=WHITE,
                    border=ft.border.all(2, PURPLE_MID),
                ),
                # Quadrants inside a Column of Rows
                ft.Container(
                    width=size, height=size,
                    padding=1, # Subtly inset for cleaner border look
                    content=ft.Column(
                        [
                            ft.Row([
                                # Top-Left
                                ft.Container(width=half-1, height=half-1, bgcolor=PURPLE_MID if value >= 1.0 else "transparent", 
                                             border_radius=ft.BorderRadius(top_left=half, top_right=0, bottom_left=0, bottom_right=0)),
                                # Top-Right (First step: 0.25)
                                ft.Container(width=half-1, height=half-1, bgcolor=PURPLE_MID if value >= 0.25 else "transparent", 
                                             border_radius=ft.BorderRadius(top_left=0, top_right=half, bottom_left=0, bottom_right=0)),
                            ], spacing=0),
                            ft.Row([
                                # Bottom-Left (Third step: 0.75)
                                ft.Container(width=half-1, height=half-1, bgcolor=PURPLE_MID if value >= 0.75 else "transparent", 
                                             border_radius=ft.BorderRadius(top_left=0, top_right=0, bottom_left=half, bottom_right=0)),
                                # Bottom-Right (Second step: 0.5)
                                ft.Container(width=half-1, height=half-1, bgcolor=PURPLE_MID if value >= 0.5 else "transparent", 
                                             border_radius=ft.BorderRadius(top_left=0, top_right=0, bottom_left=0, bottom_right=half)),
                            ], spacing=0),
                        ],
                        spacing=0,
                    )
                )
            ],
        )


def main(page: ft.Page):
    global current_goal
    page.title = "Refocus"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = PURPLE_PALE
    page.padding = 0

    state = load_state(page)

    # ── TODAY VIEW ────────────────────────────────────────────────
    def build_today(editing=False):
        goals = state["goals"]
        now = datetime.now()
        today_day = now.day
        rows = []

        # Date header row
        rows.append(ft.Container(
            content=ft.Row(
                [
                    ft.Text("TODAY — " + now.strftime("%a %d").upper(),
                            size=11, weight=ft.FontWeight.W_600,
                            color=PURPLE_MID),
                    ft.Text(f"day {today_day} of {DAYS}",
                            size=11, color=PURPLE_MUTED),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.only(bottom=8),
        ))

        # Ritual field (normal mode only)
        if not editing:
            ritual_key = f"ritual_{today_day}"
            ritual_val = state.get("rituals", {}).get(ritual_key, "")

            def on_ritual_change(e):
                if "rituals" not in state:
                    state["rituals"] = {}
                state["rituals"][ritual_key] = e.control.value
                save_state(page, state)

            rows.append(ft.Container(
                content=ft.Column(
                    [
                        ft.Text("ritual", size=10, color=PURPLE_MUTED,
                                weight=ft.FontWeight.W_600,
                                style=ft.TextStyle(letter_spacing=0.8)),
                        ft.TextField(
                            value=ritual_val,
                            hint_text="what is your intention for today?",
                            hint_style=ft.TextStyle(
                                color=PURPLE_BORDER, size=12, italic=True),
                            border_color=PURPLE_BORDER,
                            focused_border_color=PURPLE_MID,
                            cursor_color=PURPLE_MID,
                            text_style=ft.TextStyle(
                                color=TEXT_DARK, size=13, italic=True),
                            min_lines=2,
                            max_lines=4,
                            multiline=True,
                            on_change=on_ritual_change,
                            border_radius=10,
                            content_padding=ft.padding.symmetric(
                                horizontal=10, vertical=8),
                        ),
                    ],
                    spacing=4,
                ),
                bgcolor=WHITE,
                border_radius=12,
                border=ft.border.all(1, PURPLE_LIGHT),
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                margin=ft.margin.only(bottom=10),
            ))

        # Goal rows
        day_idx = min(today_day - 1, DAYS - 1)

        for i, g in enumerate(goals):
            if editing:
                # ── EDIT ROW ──────────────────────────────────────
                def make_delete(idx):
                    def handler(e):
                        state["goals"].pop(idx)
                        state["data"].pop(idx)
                        save_state(page, state)
                        show_view("today", editing=True)
                    return handler

                rows.append(ft.Container(
                    margin=ft.margin.only(bottom=5),
                    content=ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                                icon_color=RED_DELETE,
                                icon_size=22,
                                on_click=make_delete(i),
                            ),
                            ft.Text(
                                g["name"],
                                size=13,
                                italic=g.get("italic", False),
                                color=TEXT_DARK,
                                expand=True,
                            ),
                        ],
                        spacing=4,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=WHITE,
                    border_radius=12,
                    border=ft.border.all(1, PURPLE_LIGHT),
                    padding=ft.padding.symmetric(horizontal=4, vertical=4),
                ))
            else:
                # ── NORMAL ROW ────────────────────────────────────
                if g["sep"]:
                    rows.append(ft.Divider(height=8, color=PURPLE_BORDER))

                val = state["data"][i][day_idx]

                streak = 0
                for d in range(day_idx, -1, -1):
                    if state["data"][i][d] > 0:
                        streak += 1
                    else:
                        break

                def make_cycle(idx, didx):
                    def handler(e):
                        cur_val = state["data"][idx][didx]
                        # find next index in CYCLE
                        try:
                            cur_idx = CYCLE.index(cur_val)
                        except ValueError:
                            cur_idx = 0
                        state["data"][idx][didx] = CYCLE[(cur_idx + 1) % len(CYCLE)]
                        save_state(page, state)
                        show_view("today")
                    return handler

                def make_nav(idx):
                    def handler(e):
                        global current_goal
                        current_goal = idx
                        show_view("month")
                    return handler

                rows.append(ft.Container(
                    margin=ft.margin.only(bottom=5),
                    content=ft.Row(
                        [
                            ft.Container(
                                content=circle_icon(val, size=26),
                                width=44, height=44,
                                alignment=ft.Alignment(0, 0),
                                on_click=make_cycle(i, day_idx),
                            ),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Text(
                                            g["name"],
                                            size=13,
                                            italic=g.get("italic", False),
                                            color=TEXT_DARK,
                                            expand=True,
                                        ),
                                        ft.Text(f"{streak}d", size=10,
                                                color=PURPLE_MUTED),
                                        ft.Icon(ft.Icons.CHEVRON_RIGHT,
                                                color=PURPLE_BORDER, size=18),
                                    ],
                                    spacing=6,
                                ),
                                expand=True,
                                height=44,
                                alignment=ft.Alignment(-1, 0),
                                padding=ft.padding.only(right=10),
                                on_click=make_nav(i),
                            ),
                        ],
                        spacing=0,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=WHITE,
                    border_radius=12,
                    border=ft.border.all(1, PURPLE_LIGHT),
                ))

        # ── ADD GOAL ROW (edit mode only) ─────────────────────────
        if editing:
            new_name_field = ft.TextField(
                hint_text="new goal name…",
                hint_style=ft.TextStyle(color=PURPLE_BORDER, size=12, italic=True),
                border_color=PURPLE_BORDER,
                focused_border_color=PURPLE_MID,
                cursor_color=PURPLE_MID,
                text_style=ft.TextStyle(color=TEXT_DARK, size=13),
                border_radius=10,
                expand=True,
                content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
            )

            def add_goal(e):
                name = new_name_field.value.strip() if new_name_field.value else ""
                if name:
                    state["goals"].append(
                        {"name": name, "italic": False, "sep": False})
                    state["data"].append([0] * DAYS)
                    save_state(page, state)
                    show_view("today", editing=True)

            rows.append(ft.Container(
                margin=ft.margin.only(top=8),
                content=ft.Row(
                    [
                        new_name_field,
                        ft.IconButton(
                            icon=ft.Icons.ADD_CIRCLE,
                            icon_color=PURPLE_MID,
                            icon_size=28,
                            on_click=add_goal,
                        ),
                    ],
                    spacing=4,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=WHITE,
                border_radius=12,
                border=ft.border.all(1, PURPLE_LIGHT),
                padding=ft.padding.symmetric(horizontal=8, vertical=4),
            ))

        # ── ASSEMBLE TODAY VIEW ───────────────────────────────────
        return ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("Refocus", size=20,
                                            weight=ft.FontWeight.W_500,
                                            color=WHITE),
                                    ft.Text(
                                        "edit goals" if editing
                                        else "Today's check-in",
                                        size=11, color="white70"),
                                ],
                                spacing=0,
                                expand=True,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CHECK_CIRCLE_OUTLINE
                                if editing else ft.Icons.EDIT_NOTE,
                                icon_color=WHITE,
                                tooltip="Done" if editing else "Edit goals",
                                on_click=lambda _: show_view(
                                    "today", editing=not editing),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=PURPLE_DARK,
                    padding=ft.padding.only(
                        left=16, right=8, top=12, bottom=12),
                ),
                ft.Container(
                    content=ft.Column(
                        rows,
                        spacing=0,
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                    padding=ft.padding.symmetric(
                        horizontal=12, vertical=10),
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )

    # ── MONTH VIEW ────────────────────────────────────────────────
    def build_month(goal_idx):
        goals = state["goals"]
        # guard against deleted goal
        if goal_idx >= len(goals):
            goal_idx = 0
        g = goals[goal_idx]
        data = state["data"][goal_idx]
        now = datetime.now()
        today_day = now.day

        done   = sum(1 for v in data[:today_day] if v == 1)
        score  = sum(data[:today_day])
        pct    = round((score / today_day) * 100) if today_day > 0 else 0
        streak = 0
        cur    = 0
        for d in range(today_day - 1, -1, -1):
            if data[d] > 0:
                cur += 1
                streak = max(streak, cur)
            else:
                break

        def make_dot(d_idx):
            def handler(e):
                cur_v = state["data"][goal_idx][d_idx]
                try:
                    cur_idx = CYCLE.index(cur_v)
                except ValueError:
                    cur_idx = 0
                state["data"][goal_idx][d_idx] = CYCLE[(cur_idx + 1) % len(CYCLE)]
                save_state(page, state)
                show_view("month")
            return handler

        grid_rows = []
        cells = []
        for d in range(DAYS):
            dn = d + 1
            if dn > today_day:
                dot = ft.Container(
                    width=32, height=32, border_radius=16,
                    bgcolor="#F0EBF9",
                    border=ft.border.all(1, "#E4DAFA"),
                )
            else:
                dot = ft.Container(
                    content=circle_icon(data[d], size=32),
                    width=32, height=32,
                    on_click=make_dot(d),
                )
            cells.append(ft.Container(
                content=ft.Column(
                    [
                        ft.Text(str(dn), size=8, color=PURPLE_MUTED,
                                text_align=ft.TextAlign.CENTER),
                        dot,
                    ],
                    spacing=2,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                expand=True,
            ))
            if len(cells) == 7 or d == DAYS - 1:
                while len(cells) < 7:
                    cells.append(ft.Container(expand=True))
                grid_rows.append(ft.Row(cells, spacing=2))
                cells = []

        return ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                icon_color=WHITE,
                                on_click=lambda _: show_view("today"),
                            ),
                            ft.Column(
                                [
                                    ft.Text(g["name"], size=16,
                                            weight=ft.FontWeight.W_500,
                                            italic=g.get("italic", False),
                                            color=WHITE),
                                    ft.Text("tap a circle to log",
                                            size=10, color="white70"),
                                ],
                                spacing=0,
                                expand=True,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=PURPLE_DARK,
                    padding=ft.padding.only(
                        left=4, right=16, top=8, bottom=12),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text(f"{pct}%", size=22,
                                                    weight=ft.FontWeight.W_500,
                                                    color=PURPLE_MID),
                                            ft.Text("adherence", size=9,
                                                    color=PURPLE_MUTED),
                                        ], spacing=2),
                                        bgcolor=WHITE, border_radius=12,
                                        padding=ft.padding.symmetric(
                                            horizontal=12, vertical=10),
                                        expand=True,
                                    ),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text(str(streak), size=22,
                                                    weight=ft.FontWeight.W_500,
                                                    color=PURPLE_MID),
                                            ft.Text("streak", size=9,
                                                    color=PURPLE_MUTED),
                                        ], spacing=2),
                                        bgcolor=WHITE, border_radius=12,
                                        padding=ft.padding.symmetric(
                                            horizontal=12, vertical=10),
                                        expand=True,
                                    ),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text(str(done), size=22,
                                                    weight=ft.FontWeight.W_500,
                                                    color=PURPLE_MID),
                                            ft.Text("completed", size=9,
                                                    color=PURPLE_MUTED),
                                        ], spacing=2),
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
                                    color=PURPLE_MID,
                                    style=ft.TextStyle(letter_spacing=1)),
                            ft.Container(height=4),
                            ft.Column(grid_rows, spacing=6),
                        ],
                        spacing=12,
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                    padding=ft.padding.all(12),
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )

    # ── STATE-BASED NAVIGATION (Flet 0.80.x compatible) ──────────
    root = ft.Container(expand=True, bgcolor=PURPLE_PALE)
    page.add(root)

    def show_view(name: str, editing: bool = False):
        if name == "month":
            root.content = build_month(current_goal)
        else:
            root.content = build_today(editing=editing)
        root.bgcolor = PURPLE_PALE
        page.update()

    show_view("today")


ft.app(target=main)
