import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import http.server
import socket
import urllib.parse
import webbrowser
import os
import base64
import io
import shutil
from pathlib import Path
from datetime import datetime
import json

try:
    from PIL import Image, ImageTk
    PIL_OK = True
except ImportError:
    PIL_OK = False

# ── Palette ──────────────────────────────────────────────────────
BG      = "#0a0a0a"
CARD    = "#141414"
SURFACE = "#1a1a1a"
ACCENT  = "#c8102e"
GOLD    = "#f5a623"
TEXT    = "#e8e8e8"
DIM     = "#606060"
GREEN   = "#39d353"
RED     = "#e74c3c"
BORDER  = "#222222"

FT  = ("Courier New", 20, "bold")
FH  = ("Courier New", 10, "bold")
FB  = ("Courier New", 10)
FS  = ("Courier New", 9)
FM  = ("Courier New", 9)

LOGO_B64 = "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"


CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    return {}

def save_config(data):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def safe_path(base_dir, raw_path):
    rel = urllib.parse.unquote(raw_path.split("?", 1)[0].split("#", 1)[0])
    rel = rel.lstrip("/")
    candidate = (base_dir / rel).resolve()
    try:
        candidate.relative_to(base_dir.resolve())
    except Exception:
        return None
    return candidate

class Handler(http.server.SimpleHTTPRequestHandler):
    app_ref = None
    base_dir = None

    def __init__(self, *args, **kwargs):
        self.range = None
        super().__init__(*args, directory=str(self.base_dir), **kwargs)

    def log_message(self, fmt, *args):
        if self.app_ref:
            self.app_ref.log(f"[{self.address_string()}] {fmt % args}")

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_head(self):
        if self.base_dir is None:
            self.send_error(500, "Server folder not configured")
            return None

        path = safe_path(Path(self.base_dir), self.path)
        if path is None or not path.exists():
            self.send_error(404, "File not found")
            return None

        if path.is_dir():
            return super().send_head()

        ctype = "application/octet-stream"
        try:
            f = open(path, "rb")
        except OSError:
            self.send_error(404, "File not found")
            return None

        file_len = os.fstat(f.fileno()).st_size
        range_header = self.headers.get("Range")

        if range_header:
            try:
                unit, rng = range_header.strip().split("=", 1)
                if unit != "bytes":
                    raise ValueError("Unsupported range unit")

                start_str, end_str = rng.split("-", 1)
                if start_str == "":
                    length = int(end_str)
                    start = max(0, file_len - length)
                    end = file_len - 1
                else:
                    start = int(start_str)
                    end = file_len - 1 if end_str == "" else int(end_str)

                if start < 0 or end >= file_len or start > end:
                    raise ValueError("Invalid byte range")

                self.send_response(206)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(end - start + 1))
                self.send_header("Content-Range", f"bytes {start}-{end}/{file_len}")
                self.send_header("Last-Modified", self.date_time_string(os.path.getmtime(path)))
                self.end_headers()

                f.seek(start)
                self.range = (start, end)
                return f
            except Exception:
                f.close()
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{file_len}")
                self.end_headers()
                return None

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(file_len))
        self.send_header("Last-Modified", self.date_time_string(os.path.getmtime(path)))
        self.end_headers()
        self.range = None
        return f

    def copyfile(self, source, outputfile):
        current_range = getattr(self, "range", None)

        if current_range:
            start, end = current_range
            remaining = end - start + 1
            bufsize = 1024 * 1024

            while remaining > 0:
                chunk = source.read(min(bufsize, remaining))
                if not chunk:
                    break
                outputfile.write(chunk)
                remaining -= len(chunk)
        else:
            shutil.copyfileobj(source, outputfile, length=1024 * 1024)

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def fmt_size(b):
    for u in ["B", "KB", "MB", "GB"]:
        if b < 1024:
            return f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.1f} TB"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("DBI Server Online")
        self.root.geometry("760x620")
        self.root.minsize(680, 560)
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        self.server = None
        self.running = False

        config = load_config()
        saved_port = config.get("port", 8000)
        saved_folder = config.get("folder", str(Path.home() / "NSP_Files"))
        auto_start = config.get("auto_start", False)

        self.port = tk.IntVar(value=saved_port if isinstance(saved_port, int) else 8000)
        self.folder = tk.StringVar(value=saved_folder)
        self.auto_start = tk.BooleanVar(value=bool(auto_start))

        Handler.app_ref = self
        self._build()
        Path(self.folder.get()).mkdir(parents=True, exist_ok=True)

        if self.auto_start.get():
            self.root.after(300, self._start)

    def _save_current_config(self):
        save_config({
            "folder": self.folder.get(),
            "port": int(self.port.get()) if str(self.port.get()).isdigit() else 8000,
            "auto_start": bool(self.auto_start.get())
        })

    def _build(self):
        r = self.root

        hdr = tk.Frame(r, bg=BG)
        hdr.pack(fill="x", padx=18, pady=(16, 0))

        if PIL_OK:
            try:
                raw = base64.b64decode(LOGO_B64)
                img = Image.open(io.BytesIO(raw)).resize((52, 52), Image.LANCZOS)
                self._logo_img = ImageTk.PhotoImage(img)
                tk.Label(hdr, image=self._logo_img, bg=BG).pack(side="left", padx=(0, 10))
            except Exception:
                pass

        titles = tk.Frame(hdr, bg=BG)
        titles.pack(side="left")
        tk.Label(titles, text="DBI", font=("Courier New", 22, "bold"),
                 bg=BG, fg=ACCENT).pack(anchor="w")
        tk.Label(titles, text="SERVER ONLINE", font=("Courier New", 11, "bold"),
                 bg=BG, fg=DIM).pack(anchor="w")

        badge = tk.Frame(hdr, bg=BG)
        badge.pack(side="right")
        self.dot = tk.Label(badge, text="●", font=("Courier New", 16, "bold"),
                            bg=BG, fg=RED)
        self.dot.pack(side="right", padx=(4, 0))
        self.stat_lbl = tk.Label(badge, text="OFFLINE", font=FH,
                                 bg=BG, fg=RED)
        self.stat_lbl.pack(side="right")

        tk.Frame(r, bg=ACCENT, height=2).pack(fill="x", padx=18, pady=(10, 0))

        url_card = tk.Frame(r, bg=CARD, pady=10, padx=14)
        url_card.pack(fill="x", padx=18, pady=(10, 0))

        tk.Label(url_card, text="URL para DBI:", font=FS,
                 bg=CARD, fg=DIM).grid(row=0, column=0, sticky="w")
        self.url_var = tk.StringVar(value="—")
        url_lbl = tk.Label(url_card, textvariable=self.url_var,
                           font=("Courier New", 11, "bold"),
                           bg=CARD, fg=GOLD, cursor="hand2")
        url_lbl.grid(row=0, column=1, sticky="w", padx=(10, 0))
        url_lbl.bind("<Button-1>", self._copy_url)
        tk.Label(url_card, text="← clic para copiar", font=FS,
                 bg=CARD, fg=DIM).grid(row=0, column=2, sticky="w", padx=(8, 0))

        tk.Label(url_card, text="Puerto:", font=FS, bg=CARD, fg=DIM).grid(
            row=1, column=0, sticky="w", pady=(6, 0))
        tk.Entry(url_card, textvariable=self.port, width=6,
                 font=FB, bg=SURFACE, fg=TEXT, insertbackground=GOLD,
                 relief="flat", highlightthickness=1,
                 highlightbackground=BORDER, highlightcolor=GOLD).grid(
            row=1, column=1, sticky="w", padx=(10, 0), pady=(6, 0))

        tk.Checkbutton(
            url_card,
            text="Recordar carpeta / puerto y auto iniciar",
            variable=self.auto_start,
            command=self._save_current_config,
            font=FS,
            bg=CARD,
            fg=DIM,
            activebackground=CARD,
            activeforeground=GOLD,
            selectcolor=SURFACE
        ).grid(row=2, column=0, columnspan=3, sticky="w", pady=(8, 0))

        frow = tk.Frame(r, bg=SURFACE, pady=9, padx=14)
        frow.pack(fill="x", padx=18, pady=(10, 0))
        tk.Label(frow, text="📂  CARPETA DE ARCHIVOS NSP", font=FS,
                 bg=SURFACE, fg=DIM).pack(anchor="w")
        inner = tk.Frame(frow, bg=SURFACE)
        inner.pack(fill="x", pady=(5, 0))
        tk.Label(inner, textvariable=self.folder, font=FB,
                 bg=SURFACE, fg=TEXT, anchor="w", wraplength=520,
                 justify="left").pack(side="left", fill="x", expand=True)
        tk.Button(inner, text="CAMBIAR", font=FH,
                  bg=ACCENT, fg="#fff", activebackground="#a00",
                  relief="flat", padx=10, pady=3, cursor="hand2",
                  command=self._pick).pack(side="right")

        lframe = tk.Frame(r, bg=SURFACE)
        lframe.pack(fill="x", padx=18, pady=(8, 0))
        tk.Label(lframe, text="ARCHIVOS EN CARPETA", font=FS,
                 bg=SURFACE, fg=DIM, pady=5, padx=10).pack(anchor="w")
        self.lb = tk.Listbox(lframe, font=FM, bg=CARD, fg=TEXT,
                             selectbackground=ACCENT, selectforeground="#fff",
                             relief="flat", borderwidth=0, height=5,
                             highlightthickness=0)
        self.lb.pack(fill="x", padx=10, pady=(0, 6))
        tk.Button(lframe, text="↻  ACTUALIZAR", font=FS,
                  bg=SURFACE, fg=DIM, relief="flat",
                  activebackground=CARD, activeforeground=GOLD,
                  cursor="hand2", command=self._refresh).pack(
            anchor="e", padx=10, pady=(0, 5))

        btns = tk.Frame(r, bg=BG)
        btns.pack(fill="x", padx=18, pady=(12, 0))

        self.btn_start = tk.Button(btns, text="▶  INICIAR SERVIDOR",
                                   font=("Courier New", 12, "bold"),
                                   bg=GREEN, fg="#000",
                                   activebackground="#2a9e3f",
                                   relief="flat", padx=18, pady=9,
                                   cursor="hand2", command=self._start)
        self.btn_start.pack(side="left", padx=(0, 8))

        self.btn_stop = tk.Button(btns, text="■  DETENER",
                                  font=("Courier New", 12, "bold"),
                                  bg=RED, fg="#fff",
                                  activebackground="#a00",
                                  relief="flat", padx=18, pady=9,
                                  cursor="hand2", state="disabled",
                                  command=self._stop)
        self.btn_stop.pack(side="left")

        tk.Button(btns, text="ABRIR CARPETA", font=FH,
                  bg=CARD, fg=TEXT, activebackground=SURFACE,
                  relief="flat", padx=12, pady=9,
                  cursor="hand2", command=self._open_folder).pack(side="right")

        promo = tk.Frame(r, bg="#1a0a0a", pady=8, padx=14)
        promo.pack(fill="x", padx=18, pady=(10, 0))
        msg = tk.Label(
            promo,
            text="En Patreon tengo 18TB listos que puedes usar aquí",
            font=FS, bg="#1a0a0a", fg=GOLD,
            wraplength=680, justify="left"
        )
        msg.pack(side="left", fill="x", expand=True)
        tk.Button(
            promo, text="Clic Aquí →",
            font=("Courier New", 9, "bold"),
            bg=GOLD, fg="#000",
            activebackground="#d4901f",
            relief="flat", padx=10, pady=4,
            cursor="hand2",
            command=lambda: webbrowser.open("https://www.patreon.com/alucardio")
        ).pack(side="right")

        lf = tk.Frame(r, bg=BG)
        lf.pack(fill="both", expand=True, padx=18, pady=(10, 14))
        tk.Label(lf, text="ACTIVIDAD", font=FS, bg=BG, fg=DIM).pack(
            anchor="w", pady=(0, 3))
        self.log_box = tk.Text(
            lf, font=FM, bg=CARD, fg="#3ddc84",
            insertbackground=GOLD, relief="flat",
            borderwidth=0, state="disabled", wrap="word",
            highlightthickness=1,
            highlightbackground=BORDER, height=6
        )
        self.log_box.pack(fill="both", expand=True)

        self._refresh()
        self.log("Listo. Elige tu carpeta NSP e inicia el servidor.")

    def _pick(self):
        d = filedialog.askdirectory(title="Selecciona carpeta de archivos NSP")
        if d:
            self.folder.set(d)
            self._refresh()
            self._save_current_config()
            self.log(f"Carpeta: {d}")

    def _refresh(self):
        self.lb.delete(0, "end")
        d = self.folder.get()
        if not os.path.isdir(d):
            self.lb.insert("end", "  (carpeta no encontrada)")
            return
        files = [f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]
        if not files:
            self.lb.insert("end", "  (vacía — pon tus .nsp aquí)")
        else:
            for f in sorted(files):
                size = fmt_size(os.path.getsize(os.path.join(d, f)))
                self.lb.insert("end", f"  {f}   [{size}]")

    def _open_folder(self):
        Path(self.folder.get()).mkdir(parents=True, exist_ok=True)
        os.startfile(self.folder.get())

    def _copy_url(self, _=None):
        url = self.url_var.get()
        if url != "—":
            self.root.clipboard_clear()
            self.root.clipboard_append(url)
            self.log("URL copiada ✓")

    def _start(self):
        folder = self.folder.get()
        Path(folder).mkdir(parents=True, exist_ok=True)

        try:
            port = int(self.port.get())
        except Exception:
            messagebox.showerror("Error", "Puerto inválido.")
            return

        self._save_current_config()

        if self.server:
            self._stop()

        Handler.app_ref = self
        Handler.base_dir = Path(folder).resolve()

        try:
            self.server = http.server.ThreadingHTTPServer(("0.0.0.0", port), Handler)
        except OSError as e:
            messagebox.showerror("Error", f"Puerto {port} en uso o sin permisos.\n{e}")
            return

        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.running = True
        ip = get_ip()
        url = f"http://{ip}:{port}"
        self.url_var.set(url)
        self._set_online(True)
        self.log(f"Servidor activo en {url}")
        self.log("En DBI URL → pega la dirección de arriba.")
        self._refresh()

    def _stop(self):
        if self.server:
            srv = self.server
            self.server = None

            def shutdown_server():
                try:
                    srv.shutdown()
                finally:
                    try:
                        srv.server_close()
                    except Exception:
                        pass

            threading.Thread(target=shutdown_server, daemon=True).start()

        self.running = False
        self.url_var.set("—")
        self._set_online(False)
        self.log("Servidor detenido.")

    def _set_online(self, on):
        if on:
            self.dot.config(fg=GREEN)
            self.stat_lbl.config(text="EN LÍNEA", fg=GREEN)
            self.btn_start.config(state="disabled")
            self.btn_stop.config(state="normal")
        else:
            self.dot.config(fg=RED)
            self.stat_lbl.config(text="OFFLINE", fg=RED)
            self.btn_start.config(state="normal")
            self.btn_stop.config(state="disabled")

    def log(self, msg):
        def _do():
            ts = datetime.now().strftime("%H:%M:%S")
            self.log_box.config(state="normal")
            self.log_box.insert("end", f"[{ts}] {msg}\n")
            self.log_box.see("end")
            self.log_box.config(state="disabled")
        self.root.after(0, _do)

if __name__ == "__main__":
    root = tk.Tk()
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        root.iconbitmap(icon_path)
    except Exception:
        pass
    App(root)
    root.mainloop()
