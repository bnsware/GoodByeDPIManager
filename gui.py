import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import os
import sys
import ctypes
import platform
import time
import queue
import json
import webbrowser
from datetime import datetime


if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    BUNDLE_DIR = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
    BUNDLE_DIR = application_path

BASE_DIR = BUNDLE_DIR
ARCH = "x86_64" if (platform.machine().endswith("64") or os.environ.get("PROCESSOR_ARCHITEW6432")) else "x86"
EXE_PATH = os.path.join(BASE_DIR, ARCH, "goodbyedpi.exe")
CONFIG_DOSYASI = os.path.join(application_path, "gui_config.json")

KALICI_MODLAR = [
    {
        "isim": "Ana Mod  —  Önerilen",
        "aciklama": "Çoğu engeli aşar. Discord, Roblox için idealdir. Otomatik DNS kullanır.",
        "argümanlar": ["-5", "--set-ttl", "5", "--dns-addr", "77.88.8.8", "--dns-port", "1253",
                       "--dnsv6-addr", "2a02:6b8::feed:0ff", "--dnsv6-port", "1253"],
        "dns_gerekli": False,
        "tag": "DNS Yönlendirme",
    },
    {
        "isim": "Alternatif 1  —  Hafif Bypass",
        "aciklama": "Yalnızca paket süresi ayarlar. DNS'i kendiniz değiştirmeniz gerekir.",
        "argümanlar": ["--set-ttl", "3"],
        "dns_gerekli": True,
        "tag": "Manuel DNS",
    },
    {
        "isim": "Alternatif 2  —  SNI Bypass",
        "aciklama": "Paket imzasını gizler. DNS'i kendiniz değiştirmeniz gerekir.",
        "argümanlar": ["-5"],
        "dns_gerekli": True,
        "tag": "Manuel DNS",
    },
    {
        "isim": "Alternatif 3  —  TTL + DNS",
        "aciklama": "Paket süresi ayarı + Yandex DNS. Discord için etkili.",
        "argümanlar": ["--set-ttl", "3", "--dns-addr", "77.88.8.8", "--dns-port", "1253",
                       "--dnsv6-addr", "2a02:6b8::feed:0ff", "--dnsv6-port", "1253"],
        "dns_gerekli": False,
        "tag": "DNS Yandex",
    },
    {
        "isim": "Alternatif 4  —  Epic/Steam",
        "aciklama": "SNI bypass + Yandex DNS. Epic Games ve Steam için önerilir.",
        "argümanlar": ["-5", "--dns-addr", "77.88.8.8", "--dns-port", "1253",
                       "--dnsv6-addr", "2a02:6b8::feed:0ff", "--dnsv6-port", "1253"],
        "dns_gerekli": False,
        "tag": "DNS Yandex",
    },
    {
        "isim": "Alternatif 5  —  TTNet/YouTube",
        "aciklama": "Güçlü bypass + Yandex DNS. TTNet ve YouTube için önerilir.",
        "argümanlar": ["-9", "--dns-addr", "77.88.8.8", "--dns-port", "1253",
                       "--dnsv6-addr", "2a02:6b8::feed:0ff", "--dnsv6-port", "1253"],
        "dns_gerekli": False,
        "tag": "DNS Yandex",
    },
    {
        "isim": "Alternatif 6  —  Güçlü Bypass",
        "aciklama": "En agresif mod. DNS'i kendiniz değiştirmeniz gerekir.",
        "argümanlar": ["-9"],
        "dns_gerekli": True,
        "tag": "Manuel DNS",
    },
]

TEK_SEFERLIK_MODLAR = [
    {
        "isim": "Ana Mod  —  Önerilen",
        "aciklama": "Çoğu engeli aşar. Otomatik DNS ile çalışır. Discord/Roblox için ideal.",
        "argümanlar": ["-5", "--set-ttl", "5", "--dns-addr", "77.88.8.8", "--dns-port", "1253",
                       "--dnsv6-addr", "2a02:6b8::feed:0ff", "--dnsv6-port", "1253"],
        "tag": "DNS Yönlendirme",
    },
    {
        "isim": "Alternatif 1  —  Hafif Bypass",
        "aciklama": "Yalnızca paket süresi ayarlar. Hafif ve hızlı.",
        "argümanlar": ["--set-ttl", "3"],
        "tag": "TTL 3",
    },
    {
        "isim": "Alternatif 2  —  SNI Bypass",
        "aciklama": "Paket imzasını gizler, DNS değiştirmez.",
        "argümanlar": ["-5"],
        "tag": "Mode 5",
    },
    {
        "isim": "Alternatif 3  —  TTL + DNS",
        "aciklama": "Paket süresi ayarı + Yandex DNS. Discord için etkili.",
        "argümanlar": ["--set-ttl", "3", "--dns-addr", "77.88.8.8", "--dns-port", "1253",
                       "--dnsv6-addr", "2a02:6b8::feed:0ff", "--dnsv6-port", "1253"],
        "tag": "DNS Yandex",
    },
    {
        "isim": "Alternatif 4  —  Epic/Steam",
        "aciklama": "SNI bypass + Yandex DNS. Epic Games ve Steam için önerilir.",
        "argümanlar": ["-5", "--dns-addr", "77.88.8.8", "--dns-port", "1253",
                       "--dnsv6-addr", "2a02:6b8::feed:0ff", "--dnsv6-port", "1253"],
        "tag": "DNS Yandex",
    },
    {
        "isim": "Alternatif 5  —  TTNet/YouTube",
        "aciklama": "Güçlü bypass + Yandex DNS. TTNet ve YouTube için önerilir.",
        "argümanlar": ["-9", "--dns-addr", "77.88.8.8", "--dns-port", "1253",
                       "--dnsv6-addr", "2a02:6b8::feed:0ff", "--dnsv6-port", "1253"],
        "tag": "DNS Yandex",
    },
    {
        "isim": "Alternatif 6  —  Güçlü Bypass",
        "aciklama": "En agresif mod. DNS değiştirmez.",
        "argümanlar": ["-9"],
        "tag": "Mode 9",
    },
]

C = {
    "bg0":        "#06080C",
    "bg1":        "#0A0E16",
    "bg2":        "#0F1520",
    "bg3":        "#151D2B",
    "bg4":        "#1C2738",
    "bg5":        "#243044",

    "border":     "#1A2540",
    "border2":    "#223050",
    "border_hi":  "#2C3D5C",

    "cyan":       "#38BDF8",
    "cyan_dim":   "#0EA5E9",
    "cyan_dark":  "#0C3A5A",
    "cyan_glow":  "#38BDF822",

    "green":      "#34D399",
    "green_dim":  "#10B981",
    "green_dark": "#064E3B",

    "red":        "#FB7185",
    "red_dim":    "#F43F5E",
    "red_dark":   "#4C0519",

    "amber":      "#FBBF24",
    "amber_dim":  "#F59E0B",
    "amber_dark": "#451A03",

    "purple":     "#C084FC",
    "purple_dim": "#A855F7",
    "purple_dark":"#3B0764",

    "txt_hi":     "#F1F5F9",
    "txt_mid":    "#94A3B8",
    "txt_lo":     "#475569",
    "txt_inv":    "#06080C",

    "scrollbar":  "#1A2540",
}

FONT = "Segoe UI"
FONT_MONO = "Cascadia Code"


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def sc_komutu_calistir(arglar):
    try:
        result = subprocess.run(
            arglar,
            capture_output=True,
            text=True,
            encoding="cp1254",
            errors="replace",
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return -1, "", str(e)


def servis_durumu_kontrol():
    code, out, err = sc_komutu_calistir(["sc", "query", "GoodbyeDPI"])
    if code == 0:
        if "RUNNING" in out:
            return "running"
        elif "STOPPED" in out:
            return "stopped"
        elif "START_PENDING" in out:
            return "starting"
        elif "STOP_PENDING" in out:
            return "stopping"
        else:
            return "unknown"
    return "not_installed"


# ── Antifailover engine (unchanged logic) ─────────────────────────────────────
class AntifailoverMotoru:
    def __init__(self, log_fn, durum_fn):
        self.log = log_fn
        self.durum_guncelle = durum_fn
        self.aktif = False
        self.thread = None
        self.kontrol_araligi = 5
        self.hata_sayaci = 0
        self.max_hata = 3
        self.mevcut_mod_index = 0
        self.modlar = KALICI_MODLAR
        self._lock = threading.Lock()

    def baslat(self, baslangic_mod_index=0):
        with self._lock:
            if self.aktif:
                return
            self.aktif = True
            self.mevcut_mod_index = baslangic_mod_index
            self.hata_sayaci = 0
        self.thread = threading.Thread(target=self._dongu, daemon=True)
        self.thread.start()
        self.log("Anti-failover motoru başlatıldı.", "sistem")

    def durdur(self):
        with self._lock:
            self.aktif = False
        self.log("Anti-failover motoru durduruldu.", "sistem")

    def _dongu(self):
        while True:
            with self._lock:
                if not self.aktif:
                    break
            time.sleep(self.kontrol_araligi)
            with self._lock:
                if not self.aktif:
                    break
            durum = servis_durumu_kontrol()
            self.durum_guncelle(durum)
            if durum not in ("running", "starting"):
                self.hata_sayaci += 1
                self.log(
                    f"Servis yanıt vermiyor! ({self.hata_sayaci}/{self.max_hata}) Durum: {durum}",
                    "uyari",
                )
                if self.hata_sayaci >= self.max_hata:
                    self.log("Maksimum hata sayısına ulaşıldı. Failover devreye giriyor...", "hata")
                    self._failover()
            else:
                if self.hata_sayaci > 0:
                    self.log("Servis tekrar çalışıyor. Hata sayacı sıfırlandı.", "basari")
                self.hata_sayaci = 0

    def _failover(self):
        bir_sonraki = (self.mevcut_mod_index + 1) % len(self.modlar)
        mod = self.modlar[bir_sonraki]
        self.log(f"Failover: {mod['isim']} moduna geçiliyor...", "uyari")
        sc_komutu_calistir(["sc", "stop", "GoodbyeDPI"])
        sc_komutu_calistir(["sc", "delete", "GoodbyeDPI"])
        time.sleep(2)
        bin_path = f'"{EXE_PATH}" ' + " ".join(mod["argümanlar"])
        code, out, err = sc_komutu_calistir([
            "sc", "create", "GoodbyeDPI",
            "binPath=", bin_path,
            "start=", "auto"
        ])
        if code == 0:
            sc_komutu_calistir(["sc", "start", "GoodbyeDPI"])
            self.mevcut_mod_index = bir_sonraki
            self.hata_sayaci = 0
            self.log(f"Failover başarılı! Yeni mod: {mod['isim']}", "basari")
        else:
            self.log(f"Failover başarısız: {err}", "hata")


# ── Helper: rounded rectangle on canvas ───────────────────────────────────────
def round_rect(canvas, x1, y1, x2, y2, r=8, **kw):
    points = [
        x1+r, y1, x2-r, y1, x2, y1,
        x2, y1+r, x2, y2-r, x2, y2,
        x2-r, y2, x1+r, y2, x1, y2,
        x1, y2-r, x1, y1+r, x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kw)


# ── Custom Tooltip ─────────────────────────────────────────────────────────────
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        frame = tk.Frame(self.tip, bg=C["bg3"], bd=1, relief="solid",
                         highlightbackground=C["border2"], highlightthickness=1)
        frame.pack()
        tk.Label(frame, text=self.text, font=(FONT, 9),
                 bg=C["bg3"], fg=C["txt_mid"], padx=8, pady=4).pack()

    def hide(self, event=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None


# ── Custom modern button ───────────────────────────────────────────────────────
class ModernButton(tk.Frame):
    """
    A flat, pill-shaped button with hover glow effect.
    style: 'primary' | 'danger' | 'ghost' | 'icon'
    """
    STYLES = {
        "primary": {
            "bg": C["cyan_dark"], "fg": C["cyan"], "border": C["cyan_dim"],
            "hover_bg": C["cyan_dark"], "hover_border": C["cyan"],
        },
        "success": {
            "bg": C["green_dark"], "fg": C["green"], "border": C["green_dim"],
            "hover_bg": C["green_dark"], "hover_border": C["green"],
        },
        "danger": {
            "bg": C["red_dark"], "fg": C["red"], "border": C["red_dim"],
            "hover_bg": C["red_dark"], "hover_border": C["red"],
        },
        "amber": {
            "bg": C["amber_dark"], "fg": C["amber"], "border": C["amber_dim"],
            "hover_bg": C["amber_dark"], "hover_border": C["amber"],
        },
        "purple": {
            "bg": C["purple_dark"], "fg": C["purple"], "border": C["purple_dim"],
            "hover_bg": C["purple_dark"], "hover_border": C["purple"],
        },
        "ghost": {
            "bg": C["bg2"], "fg": C["txt_mid"], "border": C["border"],
            "hover_bg": C["bg4"], "hover_border": C["border2"],
        },
    }

    def __init__(self, parent, text, command=None, style="primary",
                 width=None, icon=None, **kwargs):
        s = self.STYLES.get(style, self.STYLES["ghost"])
        super().__init__(parent, bg=parent["bg"] if hasattr(parent, "__getitem__") else C["bg1"],
                         highlightbackground=s["border"],
                         highlightthickness=1,
                         **kwargs)
        self._s = s
        self._command = command
        self._normal_border = s["border"]
        self._hover_border = s["hover_border"]

        inner = tk.Frame(self, bg=s["bg"], cursor="hand2")
        inner.pack(fill="both", expand=True, padx=0, pady=0)
        self._inner = inner

        label_text = f"{icon}  {text}" if icon else text
        self._lbl = tk.Label(inner, text=label_text, font=(FONT, 10, "bold"),
                             bg=s["bg"], fg=s["fg"],
                             padx=18, pady=10, cursor="hand2")
        self._lbl.pack(fill="both", expand=True)

        if width:
            self._lbl.configure(width=width)

        for w in (self, inner, self._lbl):
            w.bind("<Button-1>", self._click)
            w.bind("<Enter>", self._enter)
            w.bind("<Leave>", self._leave)

    def _click(self, e=None):
        if self._command:
            self._command()

    def _enter(self, e=None):
        self.configure(highlightbackground=self._hover_border)
        self._inner.configure(bg=self._s["hover_bg"])
        self._lbl.configure(bg=self._s["hover_bg"])

    def _leave(self, e=None):
        self.configure(highlightbackground=self._normal_border)
        self._inner.configure(bg=self._s["bg"])
        self._lbl.configure(bg=self._s["bg"])

    def set_text(self, text, icon=None):
        label_text = f"{icon}  {text}" if icon else text
        self._lbl.configure(text=label_text)

    def set_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self._lbl.configure(state=state)


# ── Status LED widget ──────────────────────────────────────────────────────────
class StatusLED(tk.Canvas):
    STATUS_COLORS = {
        "running":       C["green"],
        "stopped":       C["red"],
        "starting":      C["amber"],
        "stopping":      C["amber"],
        "not_installed": C["txt_lo"],
        "unknown":       C["txt_lo"],
    }

    def __init__(self, parent, size=14, **kw):
        super().__init__(parent, width=size+6, height=size+6,
                         bg=parent["bg"] if hasattr(parent, "__getitem__") else C["bg2"],
                         highlightthickness=0, bd=0, **kw)
        self._size = size
        self._color = C["txt_lo"]
        self._glow = self.create_oval(0, 0, size+5, size+5, fill="", outline="", width=0)
        self._oval = self.create_oval(3, 3, size+3, size+3, fill=C["txt_lo"], outline="")
        self._blink_job = None
        self._blink_state = True

    def set_status(self, status: str):
        color = self.STATUS_COLORS.get(status, C["txt_lo"])
        self._color = color
        if self._blink_job:
            self.after_cancel(self._blink_job)
            self._blink_job = None
        if status in ("starting", "stopping"):
            self._blink()
        else:
            self.itemconfig(self._oval, fill=color)
            self.itemconfig(self._glow, fill=color, outline=color)

    def _blink(self):
        self._blink_state = not self._blink_state
        self.itemconfig(self._oval, fill=self._color if self._blink_state else C["bg2"])
        self.itemconfig(self._glow, fill=self._color if self._blink_state else "",
                        outline=self._color if self._blink_state else "")
        self._blink_job = self.after(600, self._blink)


# ── Mode selector card ─────────────────────────────────────────────────────────
class ModeSelector(tk.Frame):
    """
    Wrapping grid of clickable mode cards — shows all modes at once.
    Cards wrap to next row when width runs out (3 per row).
    """
    COLS = 3  # cards per row

    def __init__(self, parent, modes, on_select=None, **kw):
        super().__init__(parent, bg=C["bg2"], **kw)
        self._modes = modes
        self._on_select = on_select
        self._selected = 0
        self._cards = []       # card Frame refs
        self._card_bg_widgets = []  # list of lists: widgets whose bg tracks card bg

        self._grid_frame = tk.Frame(self, bg=C["bg2"])
        self._grid_frame.pack(fill="x", padx=0, pady=0)

        for i, mode in enumerate(modes):
            self._make_card(i, mode)

    def _make_card(self, idx, mode):
        is_sel = idx == self._selected
        bg = C["bg4"] if is_sel else C["bg3"]
        border = C["cyan"] if is_sel else C["border"]

        row = idx // self.COLS
        col = idx % self.COLS

        self._grid_frame.columnconfigure(col, weight=1)

        card = tk.Frame(self._grid_frame, bg=bg, height=88,
                        highlightbackground=border, highlightthickness=2,
                        cursor="hand2")
        card.grid(row=row, column=col, sticky="ew",
                  padx=(0, 6) if col < self.COLS - 1 else 0, pady=(0, 6))
        card.grid_propagate(False)

        tag = mode.get("tag", "")
        tag_color = C["cyan"] if "DNS" in tag else C["amber"]
        pill_bg = C["cyan_dark"] if "DNS" in tag else C["amber_dark"]

        pill_frame = tk.Frame(card, bg=pill_bg,
                              highlightbackground=tag_color, highlightthickness=1)
        pill_frame.place(x=8, y=8)
        tk.Label(pill_frame, text=tag, font=(FONT, 7, "bold"),
                 bg=pill_bg, fg=tag_color, padx=5, pady=1).pack()

        name_lbl = tk.Label(card, text=mode["isim"], font=(FONT, 9, "bold"),
                            bg=bg, fg=C["txt_hi"], anchor="w")
        name_lbl.place(x=8, y=34)

        desc_lbl = tk.Label(card, text=mode["aciklama"], font=(FONT, 7),
                            bg=bg, fg=C["txt_lo"], anchor="w", wraplength=120)
        desc_lbl.place(x=8, y=56)

        # widgets whose bg must follow the card bg (pill labels excluded)
        bg_widgets = [card, name_lbl, desc_lbl]
        self._card_bg_widgets.append(bg_widgets)

        def _click(e, i=idx):
            self.select(i)

        def _enter(e, c=card, bw=bg_widgets):
            c.configure(highlightbackground=C["cyan"], highlightthickness=2)
            for w in bw:
                w.configure(bg=C["bg4"])

        def _leave(e, i=idx, c=card, bw=bg_widgets):
            sel_border = C["cyan"] if i == self._selected else C["border"]
            sel_bg = C["bg4"] if i == self._selected else C["bg3"]
            c.configure(highlightbackground=sel_border)
            for w in bw:
                w.configure(bg=sel_bg)

        for w in (card, name_lbl, desc_lbl):
            w.bind("<Button-1>", _click)
            w.bind("<Enter>", _enter)
            w.bind("<Leave>", _leave)

        self._cards.append(card)

    def _apply_card_state(self, idx, selected: bool):
        bg = C["bg4"] if selected else C["bg3"]
        border = C["cyan"] if selected else C["border"]
        card = self._cards[idx]
        card.configure(highlightbackground=border, highlightthickness=2, bg=bg)
        for w in self._card_bg_widgets[idx]:
            w.configure(bg=bg)

    def select(self, idx):
        if 0 <= self._selected < len(self._cards):
            self._apply_card_state(self._selected, selected=False)
        self._selected = idx
        self._apply_card_state(idx, selected=True)
        if self._on_select:
            self._on_select(idx)

    def current(self):
        return self._selected

    def set_current(self, idx):
        if 0 <= idx < len(self._cards):
            self.select(idx)


# ── Section card container ─────────────────────────────────────────────────────
def make_section(parent, title, icon="", accent=C["cyan"], pady_bottom=12):
    outer = tk.Frame(parent, bg=C["bg1"])
    outer.pack(fill="x", pady=(0, pady_bottom))

    accent_bar = tk.Frame(outer, bg=accent, height=2)
    accent_bar.pack(fill="x")

    card = tk.Frame(outer, bg=C["bg2"],
                    highlightbackground=C["border"],
                    highlightthickness=1)
    card.pack(fill="x")

    header = tk.Frame(card, bg=C["bg3"])
    header.pack(fill="x")

    tk.Frame(header, bg=accent, width=3, height=20).pack(side="left", padx=(12, 0), pady=8)

    tk.Label(header, text=f"{icon}  {title}" if icon else title,
             font=(FONT, 11, "bold"),
             bg=C["bg3"], fg=accent,
             padx=8, pady=10).pack(side="left")

    body = tk.Frame(card, bg=C["bg2"], padx=16, pady=14)
    body.pack(fill="x")

    return card, header, body


# ── Log panel ──────────────────────────────────────────────────────────────────
class LogPanel(tk.Frame):
    STYLES = {
        "bilgi":   (C["cyan"],    "ℹ"),
        "basari":  (C["green"],   "✓"),
        "hata":    (C["red"],     "✗"),
        "uyari":   (C["amber"],   "⚠"),
        "sistem":  (C["purple"],  "◈"),
    }

    def __init__(self, parent):
        super().__init__(parent, bg=C["bg1"])
        self._queue = queue.Queue()
        self._build()
        self.after(80, self._flush)

    def _build(self):
        hdr = tk.Frame(self, bg=C["bg3"],
                       highlightbackground=C["border"], highlightthickness=1)
        hdr.pack(fill="x")

        tk.Frame(hdr, bg=C["purple"], width=3, height=20).pack(side="left", padx=(12, 0), pady=8)

        tk.Label(hdr, text="◈  CANLI LOG", font=(FONT, 11, "bold"),
                 bg=C["bg3"], fg=C["purple"],
                 padx=8, pady=10).pack(side="left")

        clear_btn = ModernButton(hdr, "Temizle", command=self._clear,
                                 style="ghost")
        clear_btn.pack(side="right", padx=8, pady=4)

        # text area
        txt_frame = tk.Frame(self, bg=C["bg0"],
                             highlightbackground=C["border"], highlightthickness=1)
        txt_frame.pack(fill="both", expand=True)

        self._text = tk.Text(
            txt_frame,
            state="disabled",
            bg=C["bg0"],
            fg=C["txt_hi"],
            font=(FONT_MONO, 10),
            relief="flat",
            padx=14, pady=10,
            wrap="word",
            insertbackground=C["txt_hi"],
            selectbackground=C["cyan_dark"],
            selectforeground=C["cyan"],
            spacing1=3, spacing3=3,
        )
        sb = tk.Scrollbar(txt_frame, command=self._text.yview,
                          bg=C["bg3"], troughcolor=C["bg0"],
                          activebackground=C["border2"])
        self._text.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self._text.pack(side="left", fill="both", expand=True)

        # configure tags
        self._text.tag_configure("time",   foreground=C["txt_lo"], font=(FONT_MONO, 10))
        self._text.tag_configure("icon_i", foreground=C["cyan"],   font=(FONT_MONO, 10, "bold"))
        self._text.tag_configure("icon_b", foreground=C["green"],  font=(FONT_MONO, 10, "bold"))
        self._text.tag_configure("icon_e", foreground=C["red"],    font=(FONT_MONO, 10, "bold"))
        self._text.tag_configure("icon_w", foreground=C["amber"],  font=(FONT_MONO, 10, "bold"))
        self._text.tag_configure("icon_s", foreground=C["purple"], font=(FONT_MONO, 10, "bold"))
        self._text.tag_configure("bilgi",  foreground=C["txt_hi"])
        self._text.tag_configure("basari", foreground=C["green"])
        self._text.tag_configure("hata",   foreground=C["red"])
        self._text.tag_configure("uyari",  foreground=C["amber"])
        self._text.tag_configure("sistem", foreground=C["purple"])

    def log(self, msg, tur="bilgi"):
        self._queue.put((msg, tur))

    def _flush(self):
        try:
            while True:
                msg, tur = self._queue.get_nowait()
                self._write(msg, tur)
        except queue.Empty:
            pass
        self.after(80, self._flush)

    def _write(self, msg, tur):
        self._text.configure(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        color, icon = self.STYLES.get(tur, (C["txt_mid"], "•"))
        icon_tag = {"bilgi":"icon_i","basari":"icon_b","hata":"icon_e",
                    "uyari":"icon_w","sistem":"icon_s"}.get(tur, "icon_i")
        self._text.insert("end", f"[{ts}] ", "time")
        self._text.insert("end", f"{icon} ", icon_tag)
        self._text.insert("end", f"{msg}\n", tur)
        self._text.see("end")
        self._text.configure(state="disabled")

    def _clear(self):
        self._text.configure(state="normal")
        self._text.delete("1.0", "end")
        self._text.configure(state="disabled")
        self.log("Log temizlendi.", "sistem")


# ── Main Application ───────────────────────────────────────────────────────────
class GoodbyeDPIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GoodbyeDPI  ·  Türkiye")
        self.root.configure(bg=C["bg0"])
        self.root.resizable(True, True)
        self.root.minsize(1180, 760)

        try:
            self.root.iconbitmap(default="")
        except Exception:
            pass

        # state
        self.tek_seferlik_proses = None
        self._service_status = "unknown"

        self._build_ui()

        # backend init
        self.antifailover = AntifailoverMotoru(
            self.log.log,
            self._on_status_update,
        )

        self.log.log("GoodbyeDPI GUI başlatıldı.", "sistem")
        self.log.log(f"Mimari: {ARCH} | Dizin: {BASE_DIR}", "bilgi")
        if not is_admin():
            self.log.log("YÖNETİCİ YETKİSİ YOK! Servis işlemleri başarısız olabilir.", "hata")

        self._config_load()
        self._status_refresh()
        self._periodic_refresh()

    # ── UI construction ──────────────────────────────────────────────────────
    def _build_ui(self):
        self._build_titlebar()

        # ── Tab bar ─────────────────────────────────────────────────────────
        tab_bar = tk.Frame(self.root, bg=C["bg1"], height=48)
        tab_bar.pack(fill="x")
        tab_bar.pack_propagate(False)
        tk.Frame(self.root, bg=C["border"], height=1).pack(fill="x")

        self._tab_frames = {}
        self._tab_btns = {}
        _tab_indicators = {}

        def _switch_tab(name):
            for n, f in self._tab_frames.items():
                f.pack_forget()
            self._tab_frames[name].pack(fill="both", expand=True)
            for n, b in self._tab_btns.items():
                if n == name:
                    b.configure(fg=C["cyan"], bg=C["bg1"])
                    _tab_indicators[n].configure(bg=C["cyan"])
                else:
                    b.configure(fg=C["txt_lo"], bg=C["bg1"])
                    _tab_indicators[n].configure(bg=C["bg1"])
            if hasattr(self, "_info_scroll_fn") and hasattr(self, "_info_inner"):
                self._bind_info_scroll(self._info_inner)

        for tab_name, tab_icon in [("Ana Panel", "⚙"), ("Bilgi", "ⓘ")]:
            tab_wrap = tk.Frame(tab_bar, bg=C["bg1"])
            tab_wrap.pack(side="left")
            btn = tk.Label(tab_wrap, text=f"   {tab_icon}  {tab_name}   ",
                           font=(FONT, 10, "bold"), bg=C["bg1"], fg=C["txt_lo"],
                           cursor="hand2", pady=10)
            btn.pack(fill="x")
            ind = tk.Frame(tab_wrap, bg=C["bg1"], height=3)
            ind.pack(fill="x")
            btn.bind("<Button-1>", lambda e, n=tab_name: _switch_tab(n))
            tab_wrap.bind("<Button-1>", lambda e, n=tab_name: _switch_tab(n))
            self._tab_btns[tab_name] = btn
            _tab_indicators[tab_name] = ind

        # ── Main body: 2-column grid ────────────────────────────────────────
        main_frame = tk.Frame(self.root, bg=C["bg0"])
        self._tab_frames["Ana Panel"] = main_frame

        # ── 2-column: Sol scroll + Sağ (platform testi + log) ──────────────
        body = tk.Frame(main_frame, bg=C["bg0"])
        body.pack(fill="both", expand=True, padx=16, pady=(12, 16))
        body.columnconfigure(0, weight=0)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        # ── SOL: Scrollable kontroller ───────────────────────────────────────
        left_canvas = tk.Canvas(body, bg=C["bg0"], highlightthickness=0,
                                bd=0, width=450)
        left_canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        left_canvas.grid_propagate(False)

        left_inner = tk.Frame(left_canvas, bg=C["bg0"])
        left_win = left_canvas.create_window((0, 0), window=left_inner, anchor="nw")

        def _left_configure(e):
            left_canvas.configure(scrollregion=left_canvas.bbox("all"))
        def _left_canvas_resize(e):
            left_canvas.itemconfig(left_win, width=e.width)
        left_inner.bind("<Configure>", _left_configure)
        left_canvas.bind("<Configure>", _left_canvas_resize)
        left_canvas.bind("<MouseWheel>",
            lambda e: left_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        def _bind_left_scroll(widget):
            widget.bind("<MouseWheel>",
                lambda e: left_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
            for child in widget.winfo_children():
                _bind_left_scroll(child)

        self._build_status_card(left_inner)
        self._build_service_card(left_inner)
        self._build_oneshot_card(left_inner)
        self._build_antifailover_card(left_inner)

        left_inner.update_idletasks()
        _bind_left_scroll(left_inner)

        # ── SAĞ: Platform testi (üst) + Log (alt, genişler) ─────────────────
        right = tk.Frame(body, bg=C["bg0"])
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        pt_frame = tk.Frame(right, bg=C["bg0"])
        pt_frame.grid(row=0, column=0, sticky="ew")
        self._build_platform_test_card(pt_frame)

        self.log = LogPanel(right)
        self.log.grid(row=1, column=0, sticky="nsew", pady=(8, 0))

        # ── Bilgi sekmesi ────────────────────────────────────────────────────
        info_frame = tk.Frame(self.root, bg=C["bg0"])
        self._tab_frames["Bilgi"] = info_frame
        self._build_info_tab(info_frame)

        _switch_tab("Ana Panel")

    def _build_info_tab(self, parent):
        """Bilgi sekmesi - proje, kullanim ve gelistirici bilgileri."""
        # scrollable canvas
        canvas = tk.Canvas(parent, bg=C["bg0"], highlightthickness=0, bd=0)
        sb = tk.Scrollbar(parent, orient="vertical", command=canvas.yview,
                          bg=C["bg3"], troughcolor=C["bg0"])
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=C["bg0"])
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def _on_canvas_resize(e):
            canvas.itemconfig(win_id, width=e.width)
        inner.bind("<Configure>", _on_configure)
        canvas.bind("<Configure>", _on_canvas_resize)
        def _scroll(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        self._info_scroll_fn = _scroll

        def _bind_scroll_recursive(widget):
            widget.bind("<MouseWheel>", _scroll)
            for child in widget.winfo_children():
                _bind_scroll_recursive(child)

        self._bind_info_scroll = _bind_scroll_recursive

        canvas.bind("<MouseWheel>", _scroll)

        pad = tk.Frame(inner, bg=C["bg0"])
        pad.pack(fill="x", padx=20, pady=16)

        # ── Hero banner ──────────────────────────────────────────────────────
        hero = tk.Frame(pad, bg=C["bg2"],
                        highlightbackground=C["cyan_dim"], highlightthickness=2)
        hero.pack(fill="x", pady=(0, 18))

        hero_top = tk.Frame(hero, bg=C["cyan_dark"])
        hero_top.pack(fill="x")

        tk.Label(hero_top, text="  GoodbyeDPI  —  Türkiye Paketi",
                 font=(FONT, 18, "bold"), bg=C["cyan_dark"], fg=C["txt_hi"],
                 padx=24, pady=16).pack(side="left")

        # developer badge
        dev_badge = tk.Frame(hero_top, bg=C["bg3"],
                             highlightbackground=C["border2"], highlightthickness=1,
                             cursor="hand2")
        dev_badge.pack(side="right", padx=16, pady=10)
        dev_lbl = tk.Label(dev_badge, text="  Gelistirici: bnsware  ",
                           font=(FONT, 10, "bold"), bg=C["bg3"], fg=C["cyan"],
                           padx=6, pady=4, cursor="hand2")
        dev_lbl.pack()
        for w in (dev_badge, dev_lbl):
            w.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/bnsware"))
            w.bind("<Enter>", lambda e: (dev_badge.configure(highlightbackground=C["cyan"]),
                                         dev_lbl.configure(fg=C["txt_hi"])))
            w.bind("<Leave>", lambda e: (dev_badge.configure(highlightbackground=C["border2"]),
                                         dev_lbl.configure(fg=C["cyan"])))

        hero_body = tk.Frame(hero, bg=C["bg2"])
        hero_body.pack(fill="x", padx=24, pady=14)
        tk.Label(hero_body,
                 text="GoodbyeDPI, Türkiye ISP altyapısı tarafından uygulanan DPI (Deep Packet Inspection) "
                      "engellerini ve DNS sansürünü aşmak için tasarlanmış açık kaynaklı bir araçtır. "
                      "Bu GUI, goodbyedpi.exe aracını kolayca yönetmenizi sağlar.",
                 font=(FONT, 10), bg=C["bg2"], fg=C["txt_mid"],
                 wraplength=800, justify="left").pack(anchor="w")

        # ── GitHub link banner ───────────────────────────────────────────────
        gh_banner = tk.Frame(pad, bg=C["bg3"],
                             highlightbackground=C["border2"], highlightthickness=1,
                             cursor="hand2")
        gh_banner.pack(fill="x", pady=(0, 16))
        gh_inner_row = tk.Frame(gh_banner, bg=C["bg3"])
        gh_inner_row.pack(fill="x", padx=16, pady=12)

        tk.Label(gh_inner_row, text="[GitHub]", font=(FONT, 13, "bold"),
                 bg=C["bg3"], fg=C["cyan"]).pack(side="left", padx=(0, 12))

        gh_text_col = tk.Frame(gh_inner_row, bg=C["bg3"])
        gh_text_col.pack(side="left", fill="x", expand=True)
        tk.Label(gh_text_col, text="github.com/bnsware", font=(FONT, 11, "bold"),
                 bg=C["bg3"], fg=C["txt_hi"]).pack(anchor="w")
        tk.Label(gh_text_col, text="Projenin kaynak koduna erişebilir, sorunları bildirebilir ve katkı sağlayabilirsiniz.",
                 font=(FONT, 9), bg=C["bg3"], fg=C["txt_lo"],
                 wraplength=700, justify="left").pack(anchor="w")

        open_btn = tk.Label(gh_inner_row, text=" GitHub'a Git › ",
                            font=(FONT, 9, "bold"), bg=C["cyan_dark"], fg=C["cyan"],
                            padx=12, pady=6, cursor="hand2")
        open_btn.pack(side="right")
        open_btn.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/bnsware"))

        for w in (gh_banner, gh_inner_row, gh_text_col, open_btn):
            w.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/bnsware"))

        # ── Mod aciklamalari ─────────────────────────────────────────────────
        def _info_section(title, icon, accent, items):
            sec = tk.Frame(pad, bg=C["bg2"],
                           highlightbackground=accent, highlightthickness=1)
            sec.pack(fill="x", pady=(0, 12))
            hdr = tk.Frame(sec, bg=C["bg3"])
            hdr.pack(fill="x")
            tk.Label(hdr, text=f"{icon}  {title}", font=(FONT, 10, "bold"),
                     bg=C["bg3"], fg=accent, padx=12, pady=8).pack(side="left")
            body2 = tk.Frame(sec, bg=C["bg2"])
            body2.pack(fill="x", padx=12, pady=8)
            for label, desc in items:
                row = tk.Frame(body2, bg=C["bg2"])
                row.pack(fill="x", pady=2)
                tk.Label(row, text=label, font=(FONT, 9, "bold"),
                         bg=C["bg2"], fg=C["txt_hi"], width=18, anchor="w").pack(side="left")
                tk.Label(row, text=desc, font=(FONT, 9),
                         bg=C["bg2"], fg=C["txt_mid"],
                         wraplength=650, justify="left", anchor="w").pack(side="left", fill="x", expand=True)

        _info_section("Modlar Hakkında", "[MOD]", C["cyan"], [
            ("Ana Mod",        "-5 + TTL 5 + DNS Yandex. Çoğu ISP için en iyi başlangıç noktası. Discord, Roblox için önerilir."),
            ("Alternatif 1",   "--set-ttl 3. Sadece TTL manipülasyonu yapar. Manuel DNS gereklidir."),
            ("Alternatif 2",   "-5. Sadece SNI bypass. Manuel DNS gereklidir."),
            ("Alternatif 3",   "--set-ttl 3 + DNS Yandex. TTL + DNS kombinasyonu. Discord için etkili."),
            ("Alternatif 4",   "-5 + DNS Yandex. Epic Games ve Steam için önerilir."),
            ("Alternatif 5",   "-9 + DNS Yandex. TTNet/Türk Telekom kullanıcıları için. YouTube için etkili."),
            ("Alternatif 6",   "-9. Agresif bypass. Manuel DNS gerektirir."),
        ])

        _info_section("Özellikler", "[INFO]", C["purple"], [
            ("Kalıcı Servis",     "Windows servisi olarak yüklenir. Bilgisayar açıldığında otomatik başlar. SC komutu ile yönetilir."),
            ("Tek Seferlik",      "GUI açık kaldığı sürece çalışır. Servis yüklemez, doğrudan exe çalıştırır."),
            ("Anti-Failover",     "Servis çökerse otomatik yeniden başlatır ve alternatif modlara geçiş yapar."),
            ("Platform Testi",    "Discord, Steam, Epic, YouTube gibi platformlara erişim durumunu test eder ve mod önerisi sunar."),
            ("Canlı Log",         "Tüm işlemler zaman damgalı olarak gerçek zamanlı gösterilir."),
        ])

        _info_section("ISP Önerileri", "[ISP]", C["amber"], [
            ("TTNet / Türk Telekom",  "Alternatif 5 (-9 + DNS Yandex) veya Ana Mod."),
            ("Superonline",           "Alternatif 4 (-5 + DNS Yandex). DNS portu değişikliği gerekebilir."),
            ("Vodafone",              "Ana Mod veya Alternatif 3."),
            ("Türkcell Fiber",        "Ana Mod. Sorun yaşanırsa Alternatif 5 deneyin."),
        ])

        # ── Sorumluluk reddi ─────────────────────────────────────────────────
        disc = tk.Frame(pad, bg=C["red_dark"],
                        highlightbackground=C["red_dim"], highlightthickness=1)
        disc.pack(fill="x", pady=(0, 18))
        tk.Label(disc, text="⚠  Yasal Uyarı",
                 font=(FONT, 10, "bold"), bg=C["red_dark"], fg=C["red"],
                 padx=14, pady=8).pack(anchor="w")
        tk.Label(disc,
                 text="Bu araç yalnızca eğitim ve araştırma amaçlıdır. Kullanımdan doğan sorumluluk "
                      "tamamen kullanıcıya aittir. Lütfen bulunduğunuz ülkenin yasalarına uygun hareket edin.",
                 font=(FONT, 9), bg=C["red_dark"], fg=C["txt_mid"],
                 wraplength=800, justify="left",
                 padx=14, pady=10).pack(anchor="w", pady=(0, 16))

        # bind scroll to all child widgets after everything is built
        inner.update_idletasks()
        _bind_scroll_recursive(inner)
        self._info_inner = inner

    def _build_platform_test_card(self, parent):
        card, hdr, body = make_section(parent, "Platform Erişim Testi", "◎", C["amber"], pady_bottom=0)

        # ── Default platform list (name, host, port) ──────────────────────────
        self._default_platforms = [
            ("Discord",       "discord.com",             443),
            ("Roblox",        "www.roblox.com",          443),
            ("Epic Games",    "epicgames.com",           443),
            ("Steam",         "store.steampowered.com",  443),
            ("YouTube",       "www.youtube.com",         443),
            ("Twitch",        "www.twitch.tv",           443),
            ("Twitter/X",     "x.com",                   443),
            ("Reddit",        "www.reddit.com",          443),
            ("GitHub",        "github.com",              443),
            ("Spotify",       "open.spotify.com",        443),
        ]
        # extra user-added platforms: list of (name, host, port)
        self._extra_platforms = []

        self._platform_result_labels = {}
        self._platform_results = {}

        # ── Platform list (scrollsuz, tüm liste) ────────────────────────────
        list_outer = tk.Frame(body, bg=C["bg0"],
                              highlightbackground=C["border"], highlightthickness=1)
        list_outer.pack(fill="x", pady=(0, 6))

        # Dummy canvas attrs (used by _rebuild_platform_rows / configure handlers)
        self._platform_canvas = tk.Canvas(list_outer, bg=C["bg0"],
                                          highlightthickness=0, bd=0)
        self._platform_canvas.pack_forget()  # not shown, kept for compat

        self._platform_list_frame = tk.Frame(list_outer, bg=C["bg0"])
        self._platform_list_frame.pack(fill="x")
        self._platform_canvas_win = None

        self._platform_rows = {}   # name → row Frame (for removal)
        self._rebuild_platform_rows()

        # ── Add custom platform row ───────────────────────────────────────────
        add_frame = tk.Frame(body, bg=C["bg3"],
                             highlightbackground=C["border"], highlightthickness=1)
        add_frame.pack(fill="x", pady=(0, 8))

        tk.Label(add_frame, text="+ Özel Sunucu:", font=(FONT, 9, "bold"),
                 bg=C["bg3"], fg=C["txt_mid"], padx=10, pady=8).pack(side="left")

        self._custom_url_var = tk.StringVar()
        url_entry = tk.Entry(add_frame, textvariable=self._custom_url_var,
                             font=(FONT, 9), bg=C["bg2"], fg=C["txt_hi"],
                             insertbackground=C["txt_hi"], relief="flat", bd=0,
                             highlightbackground=C["border"], highlightthickness=1)
        url_entry.pack(side="left", fill="x", expand=True, padx=4, pady=5, ipady=3)
        url_entry.insert(0, "örn: example.com veya example.com:8080")
        url_entry.configure(fg=C["txt_lo"])
        url_entry.bind("<FocusIn>",  lambda e: (url_entry.delete(0, "end"),
                                                url_entry.configure(fg=C["txt_hi"]))
                       if url_entry.get().startswith("örn") else None)
        url_entry.bind("<FocusOut>", lambda e: (url_entry.insert(0, "örn: example.com veya example.com:8080"),
                                                url_entry.configure(fg=C["txt_lo"]))
                       if not url_entry.get().strip() else None)
        url_entry.bind("<Return>", lambda e: self._add_custom_platform())

        ModernButton(add_frame, "Ekle", command=self._add_custom_platform,
                     style="ghost").pack(side="right", padx=4, pady=4)

        # ── Suggestion area — compact single row ────────────────────────────
        sug_frame = tk.Frame(body, bg=C["bg3"],
                             highlightbackground=C["border"], highlightthickness=1)
        sug_frame.pack(fill="x", pady=(0, 6))

        sug_row = tk.Frame(sug_frame, bg=C["bg3"])
        sug_row.pack(fill="x", padx=10, pady=6)
        sug_row.columnconfigure(1, weight=1)
        sug_row.columnconfigure(3, weight=1)

        tk.Label(sug_row, text="⚙", font=(FONT, 9, "bold"),
                 bg=C["bg3"], fg=C["cyan"]).grid(row=0, column=0, sticky="w", padx=(0,5))
        self._platform_suggest_kalici = tk.Label(sug_row, text="—", font=(FONT, 9),
                                                  bg=C["bg3"], fg=C["txt_lo"],
                                                  wraplength=220, justify="left", anchor="w")
        self._platform_suggest_kalici.grid(row=0, column=1, sticky="ew")

        tk.Label(sug_row, text="⚡", font=(FONT, 9, "bold"),
                 bg=C["bg3"], fg=C["amber"], padx=8).grid(row=0, column=2, sticky="w")
        self._platform_suggest_tek = tk.Label(sug_row, text="—", font=(FONT, 9),
                                               bg=C["bg3"], fg=C["txt_lo"],
                                               wraplength=220, justify="left", anchor="w")
        self._platform_suggest_tek.grid(row=0, column=3, sticky="ew")

        # keep old attribute for log compatibility
        self._platform_suggest_lbl = self._platform_suggest_kalici

        self._platform_test_btn = ModernButton(body, "Platformları Test Et",
                                               command=self._platform_test,
                                               style="amber", icon="▶")
        self._platform_test_btn.pack(fill="x")

    def _build_titlebar(self):
        bar = tk.Frame(self.root, bg=C["bg1"], height=70)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        sep = tk.Frame(self.root, bg=C["cyan_dark"], height=1)
        sep.pack(fill="x")

        left = tk.Frame(bar, bg=C["bg1"])
        left.pack(side="left", padx=20, pady=0)

        dot_canvas = tk.Canvas(left, width=14, height=14, bg=C["bg1"],
                               highlightthickness=0)
        dot_canvas.create_oval(2, 2, 12, 12, fill=C["cyan"], outline=C["cyan_dim"])
        dot_canvas.pack(side="left", padx=(0, 10))
        self._title_dot = dot_canvas
        self._title_dot_state = True
        self._animate_title_dot()

        title_col = tk.Frame(left, bg=C["bg1"])
        title_col.pack(side="left")

        title_row = tk.Frame(title_col, bg=C["bg1"])
        title_row.pack(anchor="w")
        tk.Label(title_row, text="GoodbyeDPI", font=(FONT, 17, "bold"),
                 bg=C["bg1"], fg=C["txt_hi"]).pack(side="left")
        tk.Label(title_row, text="  Türkiye", font=(FONT, 12),
                 bg=C["bg1"], fg=C["cyan"]).pack(side="left")

        ver_row = tk.Frame(title_col, bg=C["bg1"])
        ver_row.pack(anchor="w")
        tk.Label(ver_row, text="v4.0", font=(FONT, 8, "bold"),
                 bg=C["bg1"], fg=C["txt_lo"]).pack(side="left")
        tk.Label(ver_row, text="  ·  ", font=(FONT, 8),
                 bg=C["bg1"], fg=C["txt_lo"]).pack(side="left")
        gh_lbl = tk.Label(ver_row, text="bnsware", font=(FONT, 8, "bold"),
                          bg=C["bg1"], fg=C["cyan_dim"], cursor="hand2")
        gh_lbl.pack(side="left")
        gh_lbl.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/bnsware"))
        gh_lbl.bind("<Enter>", lambda e: gh_lbl.configure(fg=C["cyan"]))
        gh_lbl.bind("<Leave>", lambda e: gh_lbl.configure(fg=C["cyan_dim"]))

        right_grp = tk.Frame(bar, bg=C["bg1"])
        right_grp.pack(side="right", padx=20)

        gh_frame = tk.Frame(right_grp, bg=C["bg3"],
                            highlightbackground=C["border2"], highlightthickness=1,
                            cursor="hand2")
        gh_frame.pack(side="right", padx=(10, 0))
        gh_inner = tk.Label(gh_frame, text="  GitHub  ",
                            font=(FONT, 8, "bold"),
                            bg=C["bg3"], fg=C["txt_mid"], padx=10, pady=4,
                            cursor="hand2")
        gh_inner.pack()
        for w in (gh_frame, gh_inner):
            w.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/bnsware"))
            w.bind("<Enter>", lambda e: (gh_frame.configure(highlightbackground=C["cyan_dim"]),
                                         gh_inner.configure(fg=C["cyan"])))
            w.bind("<Leave>", lambda e: (gh_frame.configure(highlightbackground=C["border2"]),
                                         gh_inner.configure(fg=C["txt_mid"])))

        arch_frame = tk.Frame(right_grp, bg=C["cyan_dark"],
                              highlightbackground=C["cyan_dim"], highlightthickness=1)
        arch_frame.pack(side="right", padx=(10, 0))
        tk.Label(arch_frame, text=f"  {ARCH}  ", font=(FONT, 8, "bold"),
                 bg=C["cyan_dark"], fg=C["cyan"], pady=4).pack()

        if not is_admin():
            warn = tk.Frame(right_grp, bg=C["amber_dark"],
                            highlightbackground=C["amber_dim"], highlightthickness=1)
            warn.pack(side="right", padx=(10, 0))
            tk.Label(warn, text="  ⚠ Yönetici Yetkisi Yok  ",
                     font=(FONT, 8, "bold"),
                     bg=C["amber_dark"], fg=C["amber"], pady=4).pack()

    def _animate_title_dot(self):
        self._title_dot_state = not self._title_dot_state
        color = C["cyan"] if self._title_dot_state else C["cyan_dark"]
        try:
            self._title_dot.itemconfig(1, fill=color)
        except Exception:
            pass
        self.root.after(1200, self._animate_title_dot)

    def _build_status_card(self, parent):
        card, hdr, body = make_section(parent, "Servis Durumu", "◉", C["cyan"])

        # LED + status + detail + refresh — all in one compact row
        row = tk.Frame(body, bg=C["bg2"])
        row.pack(fill="x", pady=(0, 8))

        self._led = StatusLED(row, size=16)
        self._led.pack(side="left", padx=(0, 12))

        info = tk.Frame(row, bg=C["bg2"])
        info.pack(side="left", fill="x", expand=True)

        self._status_lbl = tk.Label(info, text="Kontrol ediliyor…",
                                    font=(FONT, 13, "bold"),
                                    bg=C["bg2"], fg=C["txt_hi"], anchor="w")
        self._status_lbl.pack(anchor="w")

        self._service_detail = tk.Label(info, text="—",
                                        font=(FONT, 9),
                                        bg=C["bg2"], fg=C["txt_lo"], anchor="w")
        self._service_detail.pack(anchor="w")

        refresh_btn = ModernButton(row, "⟳", command=self._status_refresh,
                                   style="ghost")
        refresh_btn.pack(side="right")

        # Kaldır butonu inline
        remove_btn = ModernButton(body, "Servisi ve Sürücüyü Kaldır",
                                  command=self._servisi_kaldir,
                                  style="danger", icon="✕")
        remove_btn.pack(fill="x", pady=(8, 0))

    def _build_service_card(self, parent):
        card, hdr, body = make_section(parent, "Kalıcı Servis", "⚙", C["cyan"])

        # Combobox row
        sel_row = tk.Frame(body, bg=C["bg2"])
        sel_row.pack(fill="x", pady=(0, 6))
        tk.Label(sel_row, text="Mod:", font=(FONT, 9, "bold"),
                 bg=C["bg2"], fg=C["txt_mid"], width=5, anchor="w").pack(side="left")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("K.TCombobox",
                        fieldbackground=C["bg0"], background=C["bg3"],
                        foreground=C["txt_hi"], selectbackground=C["bg0"],
                        selectforeground=C["txt_hi"], arrowcolor=C["cyan"],
                        bordercolor=C["border2"], lightcolor=C["border2"],
                        darkcolor=C["border2"], insertcolor=C["txt_hi"],
                        relief="flat", padding=4)
        style.map("K.TCombobox",
                  fieldbackground=[("readonly", C["bg0"])],
                  foreground=[("readonly", C["txt_hi"])],
                  selectbackground=[("readonly", C["bg0"])],
                  selectforeground=[("readonly", C["txt_hi"])])

        self._kalici_combo_var = tk.StringVar()
        self._kalici_combo = ttk.Combobox(
            sel_row, textvariable=self._kalici_combo_var,
            values=[f"{m['isim']}  —  {m['aciklama']}" for m in KALICI_MODLAR],
            state="readonly", width=46, style="K.TCombobox", font=(FONT, 9))
        self._kalici_combo.pack(side="left", padx=(6, 0), ipady=3)
        self._kalici_combo.current(0)
        self._kalici_combo.bind("<<ComboboxSelected>>",
                                lambda e: (self._kalici_combo.selection_clear(),
                                           self._kalici_desc_update(),
                                           self._config_save()))

        # Description label
        self._kalici_desc_lbl = tk.Label(body, text=KALICI_MODLAR[0]["aciklama"],
                                          font=(FONT, 9), bg=C["bg2"], fg=C["txt_mid"],
                                          anchor="w", wraplength=400, justify="left")
        self._kalici_desc_lbl.pack(anchor="w", pady=(0, 8))

        self._kalici_btn = ModernButton(body, "Servisi Yükle ve Başlat",
                                        command=self._kalici_toggle,
                                        style="success", icon="▶")
        self._kalici_btn.pack(fill="x")

    def _kalici_desc_update(self):
        idx = self._kalici_combo.current()
        if 0 <= idx < len(KALICI_MODLAR):
            m = KALICI_MODLAR[idx]
            dns_warn = "  ⚠ Manuel DNS gerekli" if m.get("dns_gerekli") else ""
            self._kalici_desc_lbl.configure(text=m["aciklama"] + dns_warn)

    def _build_oneshot_card(self, parent):
        card, hdr, body = make_section(parent, "Tek Seferlik", "⚡", C["amber"], pady_bottom=6)

        sel_row = tk.Frame(body, bg=C["bg2"])
        sel_row.pack(fill="x", pady=(0, 6))
        tk.Label(sel_row, text="Mod:", font=(FONT, 9, "bold"),
                 bg=C["bg2"], fg=C["txt_mid"], width=5, anchor="w").pack(side="left")

        self._tek_combo_var = tk.StringVar()
        self._tek_combo = ttk.Combobox(
            sel_row, textvariable=self._tek_combo_var,
            values=[f"{m['isim']}  —  {m['aciklama']}" for m in TEK_SEFERLIK_MODLAR],
            state="readonly", width=46, style="K.TCombobox", font=(FONT, 9))
        self._tek_combo.pack(side="left", padx=(6, 0), ipady=3)
        self._tek_combo.current(0)
        self._tek_combo.bind("<<ComboboxSelected>>",
                             lambda e: (self._tek_combo.selection_clear(),
                                        self._tek_desc_update(),
                                        self._config_save()))

        self._tek_desc_lbl = tk.Label(body, text=TEK_SEFERLIK_MODLAR[0]["aciklama"],
                                       font=(FONT, 9), bg=C["bg2"], fg=C["txt_mid"],
                                       anchor="w", wraplength=400, justify="left")
        self._tek_desc_lbl.pack(anchor="w", pady=(0, 8))

        self._tek_toggle_btn = ModernButton(body, "Başlat",
                                           command=self._tek_toggle,
                                           style="primary", icon="▶")
        self._tek_toggle_btn.pack(fill="x")

    def _tek_desc_update(self):
        idx = self._tek_combo.current()
        if 0 <= idx < len(TEK_SEFERLIK_MODLAR):
            self._tek_desc_lbl.configure(text=TEK_SEFERLIK_MODLAR[idx]["aciklama"])


    def _build_antifailover_card(self, parent):
        card, hdr, body = make_section(parent, "Anti-Failover Motoru", "🛡", C["purple"], pady_bottom=6)

        # status badge in header
        self._af_badge = tk.Label(hdr, text="● KAPALI",
                                  font=(FONT, 9, "bold"),
                                  bg=C["bg3"], fg=C["red"],
                                  padx=14)
        self._af_badge.pack(side="right")

        # interval row
        interval_row = tk.Frame(body, bg=C["bg2"])
        interval_row.pack(fill="x", pady=(0, 8))

        tk.Label(interval_row, text="Kontrol aralığı (sn):",
                 font=(FONT, 10), bg=C["bg2"], fg=C["txt_mid"]).pack(side="left")

        self._aralik_var = tk.StringVar(value="5")
        self._aralik_var.trace_add("write", lambda *_: self._config_save())

        spin = tk.Spinbox(
            interval_row, from_=3, to=120,
            textvariable=self._aralik_var,
            width=6, font=(FONT, 10),
            bg=C["bg3"], fg=C["txt_hi"],
            buttonbackground=C["bg4"],
            relief="flat", bd=0,
            insertbackground=C["txt_hi"],
            highlightbackground=C["border"],
            highlightthickness=1,
        )
        spin.pack(side="left", padx=(10, 0))

        af_row = tk.Frame(body, bg=C["bg2"])
        af_row.pack(fill="x")
        af_row.columnconfigure(0, weight=1)
        af_row.columnconfigure(1, weight=1)

        ModernButton(af_row, "Başlat", command=self._af_baslat, style="purple", icon="▶")            .grid(row=0, column=0, sticky="ew", padx=(0, 3))
        ModernButton(af_row, "Durdur", command=self._af_durdur, style="ghost", icon="■")            .grid(row=0, column=1, sticky="ew", padx=(3, 0))

    # ── Status helpers ───────────────────────────────────────────────────────
    STATUS_LABELS = {
        "running":       ("ÇALIŞIYOR", C["green"]),
        "stopped":       ("DURDURULDU", C["red"]),
        "starting":      ("BAŞLATILIYOR…", C["amber"]),
        "stopping":      ("DURDURULUYOR…", C["amber"]),
        "not_installed": ("KURULU DEĞİL", C["txt_lo"]),
        "unknown":       ("BİLİNMİYOR", C["txt_lo"]),
    }

    def _on_status_update(self, status: str):
        self.root.after(0, lambda: self._apply_status(status))

    def _apply_status(self, status: str):
        self._service_status = status
        label, color = self.STATUS_LABELS.get(status, ("?", C["txt_lo"]))
        self._status_lbl.configure(text=label, fg=color)
        self._led.set_status(status)
        self._service_detail.configure(text=f"Servis: GoodbyeDPI  ·  {ARCH}")
        # Update smart toggle buttons
        if status == "running":
            self._kalici_btn.set_text("Servisi Durdur", icon="■")
            self._kalici_btn._s = ModernButton.STYLES["danger"]
            self._kalici_btn._normal_border = C["red_dim"]
            self._kalici_btn._hover_border = C["red"]
            self._kalici_btn.configure(highlightbackground=C["red_dim"])
            self._kalici_btn._inner.configure(bg=C["red_dark"])
            self._kalici_btn._lbl.configure(bg=C["red_dark"], fg=C["red"])
        else:
            self._kalici_btn.set_text("Servisi Yükle ve Başlat", icon="▶")
            self._kalici_btn._s = ModernButton.STYLES["success"]
            self._kalici_btn._normal_border = C["green_dim"]
            self._kalici_btn._hover_border = C["green"]
            self._kalici_btn.configure(highlightbackground=C["green_dim"])
            self._kalici_btn._inner.configure(bg=C["green_dark"])
            self._kalici_btn._lbl.configure(bg=C["green_dark"], fg=C["green"])
        # Update tek seferlik button
        self._update_tek_btn()

    def _status_refresh(self):
        def _check():
            s = servis_durumu_kontrol()
            self._on_status_update(s)
            self.root.after(0, lambda: self.log.log(f"Servis durumu: {s}", "bilgi"))
        threading.Thread(target=_check, daemon=True).start()

    def _periodic_refresh(self):
        def _check():
            s = servis_durumu_kontrol()
            self._on_status_update(s)
        threading.Thread(target=_check, daemon=True).start()
        self.root.after(8000, self._periodic_refresh)

    # ── Actions ──────────────────────────────────────────────────────────────
    def _kalici_yukle(self):
        idx = self._kalici_combo.current()
        mod = KALICI_MODLAR[idx]
        self.log.log(f"Kalıcı mod yükleniyor: {mod['isim']} — {mod['aciklama']}", "sistem")
        if mod.get("dns_gerekli"):
            self.log.log("Bu mod için Windows'tan DNS değişikliği yapmanız gerekiyor!", "uyari")

        def _do():
            sc_komutu_calistir(["sc", "stop", "GoodbyeDPI"])
            self.root.after(0, lambda: self.log.log("Eski servis durduruldu.", "bilgi"))
            time.sleep(1)
            sc_komutu_calistir(["sc", "delete", "GoodbyeDPI"])
            self.root.after(0, lambda: self.log.log("Eski servis silindi.", "bilgi"))
            time.sleep(1)

            bin_path = f'"{EXE_PATH}" ' + " ".join(mod["argümanlar"])
            code, out, err = sc_komutu_calistir([
                "sc", "create", "GoodbyeDPI",
                "binPath=", bin_path,
                "start=", "auto"
            ])
            if code == 0:
                self.root.after(0, lambda: self.log.log("Servis oluşturuldu.", "basari"))
                sc_komutu_calistir([
                    "sc", "description", "GoodbyeDPI",
                    f"Türkiye için DNS zorlamasını kaldırır. {mod['isim']}"
                ])
                code2, _, err2 = sc_komutu_calistir(["sc", "start", "GoodbyeDPI"])
                if code2 == 0:
                    self.root.after(0, lambda: self.log.log("Servis başlatıldı!", "basari"))
                else:
                    self.root.after(0, lambda: self.log.log(f"Başlatma hatası: {err2}", "hata"))
            else:
                self.root.after(0, lambda: self.log.log(f"Servis oluşturma hatası [{code}]: {err}", "hata"))

            time.sleep(2)
            s = servis_durumu_kontrol()
            self._on_status_update(s)

        threading.Thread(target=_do, daemon=True).start()

    def _tek_baslat(self):
        if self.tek_seferlik_proses and self.tek_seferlik_proses.poll() is None:
            self.log.log("Zaten çalışan bir oturum var. Önce durdurun.", "uyari")
            return
        idx = self._tek_combo.current()
        mod = TEK_SEFERLIK_MODLAR[idx]
        self.log.log(f"Tek seferlik başlatılıyor: {mod['isim']}", "sistem")

        def _do():
            try:
                cmd = [EXE_PATH] + mod["argümanlar"]
                self.tek_seferlik_proses = subprocess.Popen(
                    cmd,
                    cwd=os.path.join(BASE_DIR, ARCH),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="cp1254",
                    errors="replace",
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
                self.root.after(0, lambda: self.log.log("GoodbyeDPI çalışıyor.", "basari"))
                self.root.after(0, self._update_tek_btn)

                for line in self.tek_seferlik_proses.stdout:
                    line = line.strip()
                    if line:
                        self.root.after(0, lambda l=line: self.log.log(l, "bilgi"))

                self.root.after(0, lambda: self.log.log("GoodbyeDPI oturumu sona erdi.", "uyari"))
                self.root.after(0, self._update_tek_btn)
            except Exception as ex:
                self.root.after(0, lambda: self.log.log(f"Başlatma hatası: {ex}", "hata"))

        threading.Thread(target=_do, daemon=True).start()

    def _tek_durdur(self):
        if self.tek_seferlik_proses and self.tek_seferlik_proses.poll() is None:
            self.tek_seferlik_proses.terminate()
            self.tek_seferlik_proses = None
            self.log.log("Tek seferlik oturum durduruldu.", "uyari")
            self._update_tek_btn()
        else:
            self.log.log("Çalışan bir oturum bulunamadı.", "uyari")

    def _servisi_kaldir(self):
        if not messagebox.askyesno(
            "Onay",
            "GoodbyeDPI servisi ve WinDivert sürücüsü kaldırılacak.\n\nDevam edilsin mi?",
            icon="warning"
        ):
            return
        self.log.log("Servis kaldırma başladı…", "sistem")

        def _do():
            for svc in ["GoodbyeDPI", "WinDivert", "WinDivert14"]:
                c1, _, _ = sc_komutu_calistir(["sc", "stop", svc])
                self.root.after(0, lambda s=svc, c=c1:
                                self.log.log(f"{s} durduruldu (kod: {c})", "bilgi"))
                time.sleep(0.5)
                c2, _, _ = sc_komutu_calistir(["sc", "delete", svc])
                self.root.after(0, lambda s=svc, c=c2:
                                self.log.log(f"{s} silindi (kod: {c})",
                                             "bilgi" if c == 0 else "uyari"))
            self.root.after(0, lambda: self.log.log("Kaldırma işlemi tamamlandı!", "basari"))
            time.sleep(2)
            s = servis_durumu_kontrol()
            self._on_status_update(s)

        threading.Thread(target=_do, daemon=True).start()

    def _update_tek_btn(self):
        """Update tek seferlik toggle button based on process state."""
        running = self.tek_seferlik_proses and self.tek_seferlik_proses.poll() is None
        if running:
            self._tek_toggle_btn.set_text("Çalışıyor — Durdur", icon="■")
            self._tek_toggle_btn._s = ModernButton.STYLES["danger"]
            self._tek_toggle_btn._normal_border = C["red_dim"]
            self._tek_toggle_btn._hover_border = C["red"]
            self._tek_toggle_btn.configure(highlightbackground=C["red_dim"])
            self._tek_toggle_btn._inner.configure(bg=C["red_dark"])
            self._tek_toggle_btn._lbl.configure(bg=C["red_dark"], fg=C["red"])
        else:
            self._tek_toggle_btn.set_text("Başlat", icon="▶")
            self._tek_toggle_btn._s = ModernButton.STYLES["primary"]
            self._tek_toggle_btn._normal_border = C["cyan_dim"]
            self._tek_toggle_btn._hover_border = C["cyan"]
            self._tek_toggle_btn.configure(highlightbackground=C["cyan_dim"])
            self._tek_toggle_btn._inner.configure(bg=C["cyan_dark"])
            self._tek_toggle_btn._lbl.configure(bg=C["cyan_dark"], fg=C["cyan"])

    def _kalici_toggle(self):
        """Toggle: if service running → stop it; else → install and start."""
        if self._service_status == "running":
            self._kalici_durdur()
        else:
            self._kalici_yukle()

    def _kalici_durdur(self):
        """Stop (but do not delete) the running GoodbyeDPI service."""
        self.log.log("Servis durduruluyor…", "sistem")
        def _do():
            code, _, err = sc_komutu_calistir(["sc", "stop", "GoodbyeDPI"])
            if code == 0:
                self.root.after(0, lambda: self.log.log("Servis durduruldu.", "basari"))
            else:
                self.root.after(0, lambda: self.log.log(f"Durdurma hatası: {err}", "hata"))
            time.sleep(2)
            s = servis_durumu_kontrol()
            self._on_status_update(s)
        threading.Thread(target=_do, daemon=True).start()

    def _tek_toggle(self):
        """Toggle tek seferlik: start if not running, stop if running."""
        running = self.tek_seferlik_proses and self.tek_seferlik_proses.poll() is None
        if running:
            self._tek_durdur()
        else:
            self._tek_baslat()

    def _on_platform_list_configure(self, e):
        pass  # no canvas scroll needed

    def _on_platform_canvas_configure(self, e):
        pass  # no canvas scroll needed

    def _rebuild_platform_rows(self):
        """Destroy and recreate all platform rows in the scrollable frame."""
        for w in self._platform_list_frame.winfo_children():
            w.destroy()
        self._platform_result_labels.clear()
        self._platform_rows.clear()

        all_platforms = self._default_platforms + self._extra_platforms
        for i, entry in enumerate(all_platforms):
            name = entry[0]
            is_extra = i >= len(self._default_platforms)
            row_bg = C["bg3"] if i % 2 == 0 else C["bg2"]
            row = tk.Frame(self._platform_list_frame, bg=row_bg)
            row.pack(fill="x")

            # remove button for custom entries
            if is_extra:
                def _remove(n=name):
                    self._extra_platforms = [p for p in self._extra_platforms if p[0] != n]
                    self._rebuild_platform_rows()
                rem = tk.Label(row, text="✕", font=(FONT, 8, "bold"),
                               bg=row_bg, fg=C["red_dim"], padx=4, cursor="hand2")
                rem.pack(side="right", pady=4)
                rem.bind("<Button-1>", lambda e, fn=_remove: fn())
                rem.bind("<Enter>", lambda e, w=rem: w.configure(fg=C["red"]))
                rem.bind("<Leave>", lambda e, w=rem, c=row_bg: w.configure(fg=C["red_dim"]))

            tk.Label(row, text=name, font=(FONT, 9, "bold"),
                     bg=row_bg, fg=C["cyan"] if is_extra else C["txt_hi"],
                     padx=12, pady=7, width=16, anchor="w").pack(side="left")

            result_lbl = tk.Label(row, text="—", font=(FONT, 9),
                                  bg=row_bg, fg=C["txt_lo"], padx=12, anchor="e")
            result_lbl.pack(side="right")
            self._platform_result_labels[name] = result_lbl
            self._platform_rows[name] = row

    def _add_custom_platform(self):
        raw = self._custom_url_var.get().strip()
        if not raw or raw.startswith("örn"):
            return
        # strip protocol
        for prefix in ("https://", "http://"):
            if raw.startswith(prefix):
                raw = raw[len(prefix):]
        raw = raw.rstrip("/")
        # parse port
        if ":" in raw:
            parts = raw.rsplit(":", 1)
            host = parts[0]
            try:
                port = int(parts[1])
            except ValueError:
                port = 443
        else:
            host = raw
            port = 443
        name = host  # display name = host
        # avoid duplicates
        existing = [p[0] for p in self._default_platforms + self._extra_platforms]
        if name in existing:
            self.log.log(f"'{name}' zaten listede.", "uyari")
            self._custom_url_var.set("")
            return
        self._extra_platforms.append((name, host, port))
        self._custom_url_var.set("")
        self._rebuild_platform_rows()
        self.log.log(f"Özel sunucu eklendi: {host}:{port}", "sistem")

    def _platform_test(self):
        """Test reachability of all platforms and suggest best kalıcı & tek seferlik modes."""
        all_platforms = self._default_platforms + self._extra_platforms
        self._platform_results.clear()
        for lbl in self._platform_result_labels.values():
            lbl.configure(text="Test ediliyor…", fg=C["txt_lo"])
        self._platform_suggest_kalici.configure(text="—", fg=C["txt_lo"])
        self._platform_suggest_tek.configure(text="—", fg=C["txt_lo"])
        self._platform_test_btn.set_text("Test Ediliyor…", icon="⟳")

        def _do():
            import socket
            results = {}
            for name, host, port in all_platforms:
                try:
                    sock = socket.create_connection((host, port), timeout=4)
                    sock.close()
                    results[name] = True
                except Exception:
                    results[name] = False

            def _update():
                blocked = [n for n, ok in results.items() if not ok]
                accessible = [n for n, ok in results.items() if ok]
                for name, ok in results.items():
                    if name in self._platform_result_labels:
                        self._platform_result_labels[name].configure(
                            text="✓ Erişilebilir" if ok else "✗ Erişilemiyor",
                            fg=C["green"] if ok else C["red"]
                        )
                sug_kalici = self._suggest_mode(blocked, accessible, mod_tipi="kalici")
                sug_tek    = self._suggest_mode(blocked, accessible, mod_tipi="tek")
                self._platform_suggest_kalici.configure(text=sug_kalici,
                    fg=C["cyan"] if not blocked else C["amber"])
                self._platform_suggest_tek.configure(text=sug_tek,
                    fg=C["cyan"] if not blocked else C["amber"])
                for name, ok in results.items():
                    self.log.log(f"Platform testi — {name}: {'OK' if ok else 'BLOKLU'}",
                                 "bilgi" if ok else "uyari")
                if sug_kalici:
                    self.log.log(f"Kalıcı öneri: {sug_kalici}", "sistem")
                if sug_tek:
                    self.log.log(f"Tek seferlik öneri: {sug_tek}", "sistem")
                self._platform_test_btn.set_text("Tekrar Test Et", icon="▶")
            self.root.after(0, _update)

        threading.Thread(target=_do, daemon=True).start()

    def _suggest_mode(self, blocked, accessible, mod_tipi="kalici"):
        """Return a suggestion string tailored to kalici or tek seferlik modes."""
        total = len(self._default_platforms) + len(self._extra_platforms)
        if not blocked:
            return "Tüm platformlar erişilebilir — mevcut mod yeterli."

        epic_blocked    = "Epic Games" in blocked
        discord_blocked = "Discord"    in blocked
        roblox_blocked  = "Roblox"     in blocked
        steam_blocked   = "Steam"      in blocked
        yt_blocked      = "YouTube"    in blocked
        all_blocked     = len(blocked) >= min(total, 5)

        if mod_tipi == "kalici":
            # Kalıcı servis mod önerileri
            if all_blocked:
                return ("Tüm platformlar bloklu. Öneri: Alternatif 5 (kalıcı, -9 + DNS Yandex). "
                        "TTNet/Turk Telekom için -9 genellikle daha iyi çalışır.")
            if epic_blocked and steam_blocked and not discord_blocked:
                return ("Epic+Steam bloklu. Öneri: Alternatif 4 (-5 + DNS Yandex) "
                        "veya Alternatif 5 (-9 + DNS Yandex). SNI bypass kritik.")
            if epic_blocked and not discord_blocked:
                return ("Epic Games bloklu. Öneri: Alternatif 4 (-5 + DNS Yandex) deneyin.")
            if discord_blocked and roblox_blocked and not epic_blocked:
                return ("Discord/Roblox bloklu. Öneri: Ana Mod (-5 --set-ttl 5 + DNS Yandex). "
                        "TTL manipülasyonu bu platformlar için etkili.")
            if discord_blocked and not roblox_blocked:
                return "Discord bloklu. Öneri: Alternatif 3 (--set-ttl 3 + DNS Yandex)."
            if yt_blocked:
                return ("YouTube bloklu. Öneri: Alternatif 5 (-9 + DNS Yandex) veya "
                        "Alternatif 6 (-9, manuel DNS).")
            if roblox_blocked:
                return ("Roblox bloklu. Öneri: Alternatif 4 (-5 + DNS Yandex). "
                        "Superonline kullanıcıları alternatif DNS portları denesin.")
            return f"{', '.join(blocked)} bloklu. Ana Mod ile başlayıp alternatifler deneyin."

        else:
            # Tek seferlik mod önerileri (farklı mod isimleri/argümanlar)
            if all_blocked:
                return ("Tüm platformlar bloklu. Öneri: Alternatif 5 (tek, -9 + DNS Yandex). "
                        "TTNet/Turk Telekom için -9 tercih edilir.")
            if epic_blocked and steam_blocked and not discord_blocked:
                return ("Epic+Steam bloklu. Öneri: Alternatif 4 (-5 + DNS Yandex, tek seferlik).")
            if epic_blocked and not discord_blocked:
                return "Epic Games bloklu. Öneri: Alternatif 4 (-5 + DNS Yandex, tek seferlik)."
            if discord_blocked and roblox_blocked and not epic_blocked:
                return ("Discord/Roblox bloklu. Öneri: Ana Mod (tek seferlik, -5 --set-ttl 5 + DNS Yandex).")
            if discord_blocked and not roblox_blocked:
                return "Discord bloklu. Öneri: Alternatif 3 (tek, --set-ttl 3 + DNS Yandex)."
            if yt_blocked:
                return "YouTube bloklu. Öneri: Alternatif 5 (tek, -9 + DNS Yandex)."
            if roblox_blocked:
                return "Roblox bloklu. Öneri: Alternatif 4 (tek, -5 + DNS Yandex)."
            return f"{', '.join(blocked)} bloklu. Ana Mod (tek) ile başlayıp alternatifler deneyin."

    def _af_baslat(self):
        if self.antifailover.aktif:
            self.log.log("Anti-failover zaten çalışıyor.", "uyari")
            return
        try:
            aralik = max(3, int(self._aralik_var.get()))
        except ValueError:
            aralik = 5
        self.antifailover.kontrol_araligi = aralik
        self.antifailover.baslat(self._kalici_combo.current())
        self._af_badge.configure(text="● AKTİF", fg=C["green"])
        self.log.log(f"Anti-failover aktif. Kontrol aralığı: {aralik} sn", "basari")
        self._config_save()

    def _af_durdur(self):
        self.antifailover.durdur()
        self._af_badge.configure(text="● KAPALI", fg=C["red"])
        self._config_save()

    # ── Config ───────────────────────────────────────────────────────────────
    def _config_save(self):
        try:
            data = {
                "kalici_mod_index": self._kalici_combo.current(),
                "tek_mod_index": self._tek_combo.current(),
                "antifailover_aktif": self.antifailover.aktif,
                "antifailover_aralik": self._aralik_var.get(),
            }
            with open(CONFIG_DOSYASI, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _config_load(self):
        try:
            if not os.path.exists(CONFIG_DOSYASI):
                return
            with open(CONFIG_DOSYASI, "r", encoding="utf-8") as f:
                data = json.load(f)
            ki = data.get("kalici_mod_index", 0)
            if 0 <= ki < len(KALICI_MODLAR):
                self._kalici_combo.current(ki); self._kalici_desc_update()
            ti = data.get("tek_mod_index", 0)
            if 0 <= ti < len(TEK_SEFERLIK_MODLAR):
                self._tek_combo.current(ti); self._tek_desc_update()
            self._aralik_var.set(str(data.get("antifailover_aralik", "5")))
            self.log.log("Yapılandırma yüklendi.", "sistem")
            if data.get("antifailover_aktif", False):
                self.root.after(600, self._af_baslat)
        except Exception:
            pass


# ── Entry point ────────────────────────────────────────────────────────────────
def main():
    try:
        if not is_admin():
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable,
                f'"{os.path.abspath(__file__)}"', None, 1
            )
            return

        root = tk.Tk()
        root.geometry("1340x850")
        try:
            root.tk.call("tk", "scaling", 1.0)
        except Exception:
            pass

        # load fonts if possible
        try:
            import tkinter.font as tkfont
            tkfont.Font(family=FONT, size=11)
        except Exception:
            pass

        app = GoodbyeDPIApp(root)
        root.mainloop()

    except Exception as e:
        import traceback
        err_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gui_hata.txt")
        with open(err_file, "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        try:
            messagebox.showerror("Kritik Hata", f"GUI başlatılamadı:\n\n{e}\n\nDetaylar: gui_hata.txt")
        except Exception:
            pass


if __name__ == "__main__":
    main()