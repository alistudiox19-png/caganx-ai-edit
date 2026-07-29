#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import time
import sqlite3
import threading
import subprocess
import psutil
import json
import urllib.request
import urllib.parse
import tkinter as tk
from tkinter import ttk, messagebox

# Set Working Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

DB_PATH = os.path.join(BASE_DIR, "caganx_admin.db")

# Start background server if not already running
def start_backend():
    try:
        import admin_server
    except Exception as e:
        print("Backend starting in thread...", e)

threading.Thread(target=start_backend, daemon=True).start()
time.sleep(1)

# Modern Dark Theme Colors
BG_DARK = "#09090b"
CARD_BG = "#121215"
CARD_BORDER = "#27272a"
TEXT_COLOR = "#f4f4f5"
MUTED_COLOR = "#a1a1aa"
ACCENT_PURPLE = "#8b5cf6"
GREEN_COLOR = "#22c55e"
RED_COLOR = "#ef4444"

class AdminApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🛡️ caganx AI edit - Özel Masaüstü Admin Kontrol Paneli")
        self.geometry("1150x760")
        self.configure(bg=BG_DARK)
        self.minsize(950, 650)

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        # Build UI Structure
        self.create_header()
        self.create_stats_cards()
        self.create_control_bar()
        self.create_tabs()

        # Start Realtime Polling
        self.running = True
        self.poll_data()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def configure_styles(self):
        self.style.configure('.', background=BG_DARK, foreground=TEXT_COLOR)
        self.style.configure('TNotebook', background=BG_DARK, borderwidth=0)
        self.style.configure('TNotebook.Tab', background=CARD_BG, foreground=MUTED_COLOR, padding=[16, 10], font=('Segoe UI', 10, 'bold'), borderwidth=1, focuscolor='')
        self.style.map('TNotebook.Tab', background=[('selected', ACCENT_PURPLE)], foreground=[('selected', '#ffffff')])
        
        self.style.configure('Treeview', background=CARD_BG, foreground=TEXT_COLOR, fieldbackground=CARD_BG, rowheight=32, font=('Segoe UI', 9))
        self.style.configure('Treeview.Heading', background='#18181c', foreground=MUTED_COLOR, font=('Segoe UI', 9, 'bold'))
        self.style.map('Treeview', background=[('selected', '#27272a')], foreground=[('selected', '#ffffff')])

    def create_header(self):
        header_frame = tk.Frame(self, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1, height=65)
        header_frame.pack(fill='x', side='top')

        logo_label = tk.Label(header_frame, text="🛡️ caganx AI edit", font=('Segoe UI', 15, 'bold'), bg=CARD_BG, fg='#ffffff')
        logo_label.pack(side='left', padx=20, pady=14)

        badge_label = tk.Label(header_frame, text="MASAÜSTÜ UYGULAMASI V1.0", font=('Segoe UI', 8, 'bold'), bg='#1e1b4b', fg='#c4b5fd', px=8, py=3)
        badge_label.pack(side='left', pady=14)

        self.status_label = tk.Label(header_frame, text="🟢 CANLI SUNUCU BAĞLANTISI AKTİF", font=('Segoe UI', 9, 'bold'), bg=CARD_BG, fg=GREEN_COLOR)
        self.status_label.pack(side='right', padx=20)

    def create_stats_cards(self):
        cards_frame = tk.Frame(self, bg=BG_DARK)
        cards_frame.pack(fill='x', padx=20, pady=16)

        # Card 1: Active Users
        self.card_active = self.build_card(cards_frame, "🟢 ANLIK AKTİF ZİYARETÇİ", "0", "Şu anda sitede gezen kişi sayısı")
        self.card_active.pack(side='left', expand=True, fill='x', padx=6)

        # Card 2: Total Edits
        self.card_edits = self.build_card(cards_frame, "🎬 BUGÜN YAPILAN İŞLEM", "0", "Son 24 saatteki 45 özellik aksiyonu")
        self.card_edits.pack(side='left', expand=True, fill='x', padx=6)

        # Card 3: CPU & RAM
        self.card_sys = self.build_card(cards_frame, "💻 CPU & RAM MONİTÖRÜ", "0%", "RAM: 0 MB / 0 MB")
        self.card_sys.pack(side='left', expand=True, fill='x', padx=6)

        # Card 4: Bans
        self.card_bans = self.build_card(cards_frame, "⛔ YASAKLI IP SAYISI", "0", "Engellenen kullanıcılar")
        self.card_bans.pack(side='left', expand=True, fill='x', padx=6)

    def build_card(self, parent, title, value, hint):
        f = tk.Frame(parent, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1, padx=16, pady=14)
        
        lbl_title = tk.Label(f, text=title, font=('Segoe UI', 8, 'bold'), bg=CARD_BG, fg=MUTED_COLOR)
        lbl_title.pack(anchor='w')

        lbl_val = tk.Label(f, text=value, font=('Segoe UI', 18, 'bold'), bg=CARD_BG, fg='#ffffff')
        lbl_val.pack(anchor='w', pady=4)
        f.val_lbl = lbl_val

        lbl_hint = tk.Label(f, text=hint, font=('Segoe UI', 8), bg=CARD_BG, fg=MUTED_COLOR)
        lbl_hint.pack(anchor='w')
        f.hint_lbl = lbl_hint

        return f

    def create_control_bar(self):
        ctrl_frame = tk.Frame(self, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1, padx=18, pady=12)
        ctrl_frame.pack(fill='x', padx=20, pady=(0, 16))

        # Maintenance Switch
        self.maint_var = tk.BooleanVar(value=False)
        self.btn_maint = tk.Button(ctrl_frame, text="🛠️ BAKIM MODU: KAPALI", font=('Segoe UI', 9, 'bold'), bg='#27272a', fg='#ffffff',
                                   activebackground=RED_COLOR, activeforeground='#ffffff', relief='flat', px=12, py=6, command=self.toggle_maint)
        self.btn_maint.pack(side='left')

        # Announcement Input
        lbl_ann = tk.Label(ctrl_frame, text="📢 Canlı Duyuru:", font=('Segoe UI', 9, 'bold'), bg=CARD_BG, fg='#ffffff')
        lbl_ann.pack(side='left', padx=(30, 8))

        self.ent_ann = tk.Entry(ctrl_frame, font=('Segoe UI', 9), bg='#18181c', fg='#ffffff', insertbackground='#ffffff', relief='flat', highlightbackground=CARD_BORDER, highlightthickness=1)
        self.ent_ann.pack(side='left', fill='x', expand=True, padx=(0, 10), ipady=4)

        btn_send_ann = tk.Button(ctrl_frame, text="Yayınla", font=('Segoe UI', 9, 'bold'), bg=ACCENT_PURPLE, fg='#ffffff', relief='flat', px=14, py=5, command=self.save_announcement)
        btn_send_ann.pack(side='left')

    def create_tabs(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Tab 1: Live Stream Logs
        self.tab_stream = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(self.tab_stream, text="⚡ Canlı Hareket Akışı")
        
        self.txt_stream = tk.Text(self.tab_stream, bg='#0c0c0e', fg='#e4e4e7', font=('Consolas', 10), relief='flat', highlightbackground=CARD_BORDER, highlightthickness=1, padx=12, pady=12)
        self.txt_stream.pack(fill='both', expand=True)

        # Tab 2: Active Users Table
        self.tab_users = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(self.tab_users, text="👥 Aktif Ziyaretçiler")
        
        self.tree_users = ttk.Treeview(self.tab_users, columns=('ip', 'page', 'ua', 'last_seen'), show='headings')
        self.tree_users.heading('ip', text='IP Adresi')
        self.tree_users.heading('page', text='Mevcut Sayfa')
        self.tree_users.heading('ua', text='Tarayıcı / Cihaz')
        self.tree_users.heading('last_seen', text='Son Görülme')
        self.tree_users.column('ip', width=150)
        self.tree_users.column('page', width=120)
        self.tree_users.column('ua', width=500)
        self.tree_users.column('last_seen', width=120)
        self.tree_users.pack(fill='both', expand=True)

        # Tab 3: Error Logs
        self.tab_errors = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(self.tab_errors, text="⚠️ Hata Logları")
        
        self.tree_errors = ttk.Treeview(self.tab_errors, columns=('time', 'ip', 'page', 'error'), show='headings')
        self.tree_errors.heading('time', text='Zaman')
        self.tree_errors.heading('ip', text='IP')
        self.tree_errors.heading('page', text='Sayfa')
        self.tree_errors.heading('error', text='Hata Mesajı')
        self.tree_errors.column('time', width=120)
        self.tree_errors.column('ip', width=140)
        self.tree_errors.column('page', width=120)
        self.tree_errors.column('error', width=550)
        self.tree_errors.pack(fill='both', expand=True)

        # Tab 4: Bans
        self.tab_bans = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(self.tab_bans, text="⛔ IP Ban Yönetimi")
        
        ban_ctrl = tk.Frame(self.tab_bans, bg=BG_DARK, pady=10)
        ban_ctrl.pack(fill='x')

        tk.Label(ban_ctrl, text="IP:", bg=BG_DARK, fg='#fff', font=('Segoe UI', 9, 'bold')).pack(side='left', padx=(0, 6))
        self.ent_ban_ip = tk.Entry(ban_ctrl, font=('Segoe UI', 9), bg='#18181c', fg='#fff', insertbackground='#fff', relief='flat', width=20)
        self.ent_ban_ip.pack(side='left', padx=(0, 14), ipady=3)

        tk.Label(ban_ctrl, text="Sebep:", bg=BG_DARK, fg='#fff', font=('Segoe UI', 9, 'bold')).pack(side='left', padx=(0, 6))
        self.ent_ban_reason = tk.Entry(ban_ctrl, font=('Segoe UI', 9), bg='#18181c', fg='#fff', insertbackground='#fff', relief='flat', width=25)
        self.ent_ban_reason.pack(side='left', padx=(0, 14), ipady=3)

        btn_ban = tk.Button(ban_ctrl, text="⛔ IP Engelle", font=('Segoe UI', 9, 'bold'), bg=RED_COLOR, fg='#fff', relief='flat', px=12, py=4, command=self.add_ban)
        btn_ban.pack(side='left')

        self.tree_bans = ttk.Treeview(self.tab_bans, columns=('ip', 'reason', 'time'), show='headings')
        self.tree_bans.heading('ip', text='Yasaklı IP')
        self.tree_bans.heading('reason', text='Sebep')
        self.tree_bans.heading('time', text='Zaman')
        self.tree_bans.column('ip', width=200)
        self.tree_bans.column('reason', width=450)
        self.tree_bans.column('time', width=200)
        self.tree_bans.pack(fill='both', expand=True, pady=(10, 0))

    def poll_data(self):
        if not self.running:
            return
        try:
            req = urllib.request.Request("http://127.0.0.1:9090/admin/api/stats")
            with urllib.request.urlopen(req, timeout=2) as response:
                data = json.loads(response.read().decode('utf-8'))
                self.update_ui(data)
        except Exception as e:
            self.status_label.config(text="🟡 SUNUCU BAĞLANTISI YENİDEN DENENİYOR...", fg=MUTED_COLOR)
        
        self.after(2000, self.poll_data)

    def update_ui(self, data):
        self.status_label.config(text="🟢 CANLI SUNUCU BAĞLANTISI AKTİF", fg=GREEN_COLOR)

        # Update Cards
        self.card_active.val_lbl.config(text=str(data.get("active_users", 0)))
        self.card_edits.val_lbl.config(text=str(data.get("edits_today", 0)))
        
        sys_data = data.get("system", {})
        self.card_sys.val_lbl.config(text=f"{sys_data.get('cpu', 0)}%")
        self.card_sys.hint_lbl.config(text=f"RAM: {sys_data.get('ram_used_mb', 0)} MB / {sys_data.get('ram_total_mb', 0)} MB (%{sys_data.get('ram_percent', 0)})")

        bans_list = data.get("bans", [])
        self.card_bans.val_lbl.config(text=str(len(bans_list)))

        # Update Maintenance Button
        is_maint = data.get("settings", {}).get("maintenance") == "1"
        self.maint_var.set(is_maint)
        if is_maint:
            self.btn_maint.config(text="🛠️ BAKIM MODU: AÇIK (AKTİF)", bg=RED_COLOR)
        else:
            self.btn_maint.config(text="🛠️ BAKIM MODU: KAPALI", bg='#27272a')

        # Update Announcement
        ann_text = data.get("settings", {}).get("announcement", "")
        if self.focus_get() != self.ent_ann:
            self.ent_ann.delete(0, tk.END)
            self.ent_ann.insert(0, ann_text)

        # Update Logs Stream
        self.txt_stream.config(state='normal')
        self.txt_stream.delete('1.0', tk.END)
        for log in data.get("recent_logs", []):
            t_str = time.strftime('%H:%M:%S', time.localtime(log.get('timestamp', time.time())))
            line = f"[{t_str}]  [{log.get('action')}]  IP: {log.get('ip')}  -  {log.get('details', '')}\n"
            self.txt_stream.insert(tk.END, line)
        self.txt_stream.config(state='disabled')

        # Update Active Users Tree
        for item in self.tree_users.get_children():
            self.tree_users.delete(item)
        for u in data.get("active_list", []):
            t_str = time.strftime('%H:%M:%S', time.localtime(u.get('last_seen', time.time())))
            self.tree_users.insert('', tk.END, values=(u.get('ip'), u.get('page'), u.get('user_agent'), t_str))

        # Update Error Logs Tree
        for item in self.tree_errors.get_children():
            self.tree_errors.delete(item)
        for err in data.get("error_logs", []):
            t_str = time.strftime('%H:%M:%S', time.localtime(err.get('timestamp', time.time())))
            self.tree_errors.insert('', tk.END, values=(t_str, err.get('ip'), err.get('page'), err.get('error_msg')))

        # Update Bans Tree
        for item in self.tree_bans.get_children():
            self.tree_bans.delete(item)
        for b in bans_list:
            t_str = time.strftime('%H:%M:%S', time.localtime(b.get('created_at', time.time())))
            self.tree_bans.insert('', tk.END, values=(b.get('ip'), b.get('reason'), t_str))

    def toggle_maint(self):
        new_val = not self.maint_var.get()
        payload = json.dumps({"maintenance": new_val}).encode('utf-8')
        req = urllib.request.Request("http://127.0.0.1:9090/admin/api/toggle_maintenance", data=payload, headers={'Content-Type': 'application/json'})
        try:
            urllib.request.urlopen(req)
        except Exception as e:
            messagebox.showerror("Hata", f"Bakım modu değiştirilemedi: {e}")

    def save_announcement(self):
        txt = self.ent_ann.get()
        payload = json.dumps({"text": txt}).encode('utf-8')
        req = urllib.request.Request("http://127.0.0.1:9090/admin/api/set_announcement", data=payload, headers={'Content-Type': 'application/json'})
        try:
            urllib.request.urlopen(req)
            messagebox.showinfo("Başarılı", "📢 Duyuru yayınlandı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Duyuru yayınlanamadı: {e}")

    def add_ban(self):
        ip = self.ent_ban_ip.get().strip()
        reason = self.ent_ban_reason.get().strip() or "Kural ihlali"
        if not ip:
            messagebox.showwarning("Uyarı", "Lütfen bir IP adresi girin.")
            return
        payload = json.dumps({"ip": ip, "reason": reason}).encode('utf-8')
        req = urllib.request.Request("http://127.0.0.1:9090/admin/api/ban_ip", data=payload, headers={'Content-Type': 'application/json'})
        try:
            urllib.request.urlopen(req)
            self.ent_ban_ip.delete(0, tk.END)
            self.ent_ban_reason.delete(0, tk.END)
            messagebox.showinfo("Başarılı", f"⛔ {ip} adresi engellendi!")
        except Exception as e:
            messagebox.showerror("Hata", f"IP engellenemedi: {e}")

    def on_close(self):
        self.running = False
        self.destroy()

if __name__ == "__main__":
    app = AdminApp()
    app.mainloop()
