import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import asyncio

# ---------------------------------------------------------------------------
# Upgrade definitions  (name, base_cost, cookies-per-second, emoji)
# ---------------------------------------------------------------------------
UPGRADES = [
    {"name": "Cursor",   "base_cost": 10,      "cps": 0.1,  "emoji": "👆"},
    {"name": "Grandma",  "base_cost": 100,     "cps": 0.5,  "emoji": "👵"},
    {"name": "Farm",     "base_cost": 1_100,   "cps": 4.0,  "emoji": "🌾"},
    {"name": "Mine",     "base_cost": 12_000,  "cps": 10.0, "emoji": "⛏️"},
    {"name": "Factory",  "base_cost": 130_000, "cps": 40.0, "emoji": "🏭"},
    {"name": "Bank",     "base_cost": 1_400_000, "cps": 100.0, "emoji": "🏦"},
]


class CookieClickerApp(toga.App):

    # ------------------------------------------------------------------
    # Startup
    # ------------------------------------------------------------------
    def startup(self):
        self.cookies: float = 0.0
        self.cps: float = 0.0
        self.counts = [0] * len(UPGRADES)
        self.costs  = [float(u["base_cost"]) for u in UPGRADES]

        # ── Header ────────────────────────────────────────────────────
        self.cookie_label = toga.Label(
            "🍪  0  cookies",
            style=Pack(font_size=24, text_align="center", padding_bottom=2),
        )
        self.cps_label = toga.Label(
            "per second: 0.0",
            style=Pack(font_size=13, text_align="center", padding_bottom=8),
        )

        # ── Big cookie button ─────────────────────────────────────────
        cookie_btn = toga.Button(
            "🍪",
            on_press=self.click_cookie,
            style=Pack(font_size=72, padding=8),
        )

        # ── Upgrade shop ──────────────────────────────────────────────
        shop_label = toga.Label(
            "── Shop ──",
            style=Pack(font_size=15, text_align="center",
                       padding_top=12, padding_bottom=4),
        )

        self.upgrade_btns = []
        upgrade_box = toga.Box(style=Pack(direction=COLUMN))
        for i in range(len(UPGRADES)):
            btn = toga.Button(
                self._upgrade_label(i),
                on_press=lambda w, idx=i: self.buy_upgrade(idx),
                style=Pack(padding=3, font_size=13),
            )
            self.upgrade_btns.append(btn)
            upgrade_box.add(btn)

        # ── Assemble ──────────────────────────────────────────────────
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=12))
        main_box.add(self.cookie_label)
        main_box.add(self.cps_label)
        main_box.add(cookie_btn)
        main_box.add(shop_label)
        main_box.add(upgrade_box)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = toga.ScrollContainer(content=main_box)
        self.main_window.show()

        # Start auto-tick (10 fps for smooth counter)
        self.add_background_task(self.tick)

    # ------------------------------------------------------------------
    # Background tick  — runs every 100 ms
    # ------------------------------------------------------------------
    async def tick(self, app, **kwargs):
        while True:
            await asyncio.sleep(0.1)
            if self.cps > 0:
                self.cookies += self.cps * 0.1
                self.update_display()

    # ------------------------------------------------------------------
    # Click handler
    # ------------------------------------------------------------------
    def click_cookie(self, widget):
        self.cookies += 1
        self.update_display()

    # ------------------------------------------------------------------
    # Buy upgrade
    # ------------------------------------------------------------------
    def buy_upgrade(self, idx: int):
        cost = self.costs[idx]
        if self.cookies >= cost:
            self.cookies -= cost
            self.counts[idx] += 1
            self.cps += UPGRADES[idx]["cps"]
            # Each purchase raises the cost by 15 %
            self.costs[idx] = cost * 1.15
            self.upgrade_btns[idx].text = self._upgrade_label(idx)
            self.update_display()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _upgrade_label(self, i: int) -> str:
        u    = UPGRADES[i]
        cost = int(self.costs[i])
        cnt  = self.counts[i]
        return f"{u['emoji']}  {u['name']}  —  {cost:,} 🍪   [{cnt} owned]"

    def update_display(self):
        self.cookie_label.text = f"🍪  {int(self.cookies):,}  cookies"
        self.cps_label.text    = f"per second: {self.cps:.1f}"


# ---------------------------------------------------------------------------
# Entry point required by Briefcase
# ---------------------------------------------------------------------------
def main():
    return CookieClickerApp("Cookie Clicker", "com.yourname.cookieclicker")
