#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# Windows encoding sorunlarını çöz
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import os
import sys
import threading
import time
import json
from datetime import datetime
import winreg
import ctypes
from ctypes import wintypes
import socket
import requests
import re

class BilgiPopup:
    """Markdown bilgilerini güzel bir popup'ta gösteren sınıf"""
    
    def __init__(self, parent):
        self.parent = parent
        self.popup = None
        
    def show_info(self):
        """Bilgi popup penceresini aç"""
        if self.popup and self.popup.winfo_exists():
            self.popup.lift()
            self.popup.focus()
            return
            
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("📘 GoodBye DPI Manager - Sistem Bilgileri")
        self.popup.geometry("900x650")
        self.popup.configure(bg='#f8f9fa')
        self.popup.resizable(True, True)
        
        # Popup'ı ana pencere üzerinde ortala
        self.popup.transient(self.parent)
        self.popup.grab_set()
        
        self.create_popup_gui()
        self.load_markdown_content()
        
    def create_popup_gui(self):
        """Popup GUI'yi oluştur"""
        # Ana frame
        main_frame = ttk.Frame(self.popup, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(title_frame, 
                               text="📘 GoodBye DPI Manager v2.0 - Sistem Bilgileri",
                               font=('Segoe UI', 16, 'bold'),
                               foreground='#2c3e50')
        title_label.pack(side=tk.LEFT)
        
        # Kapat butonu
        close_btn = ttk.Button(title_frame, text="❌ Kapat", 
                              command=self.popup.destroy,
                              style="Danger.TButton")
        close_btn.pack(side=tk.RIGHT)
        
        # İçerik alanı
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollable text area
        self.text_widget = scrolledtext.ScrolledText(
            content_frame,
            width=100,
            height=35,
            font=('Segoe UI', 10),
            bg='#ffffff',
            fg='#2c3e50',
            wrap=tk.WORD,
            padx=15,
            pady=15,
            insertwidth=0,  # Cursor'ı gizle
            state=tk.DISABLED  # Salt okunur yap
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Alt butonlar
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        ttk.Button(button_frame, text="🔗 GitHub'da Aç", 
                  command=self.open_github).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="📋 Bilgileri Kopyala", 
                  command=self.copy_info).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="💾 Bilgileri Kaydet", 
                  command=self.save_info).pack(side=tk.LEFT)
    
    def load_markdown_content(self):
        """Markdown dosyasını yükle ve formatla"""
        try:
            bilgi_path = os.path.join(os.path.dirname(__file__), "bilgi.md")
            
            if not os.path.exists(bilgi_path):
                self.show_error_content("bilgi.md dosyası bulunamadı!")
                return
                
            with open(bilgi_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            formatted_content = self.markdown_to_text(markdown_content)
            
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert("1.0", formatted_content)
            self.text_widget.config(state=tk.DISABLED)
            
            # Scroll'u en üste götür
            self.text_widget.see("1.0")
            
        except Exception as e:
            self.show_error_content(f"Bilgi dosyası yüklenirken hata: {str(e)}")
    
    def markdown_to_text(self, markdown):
        """Markdown'ı güzel formatlı text'e çevir"""
        text = markdown
        
        # Başlıkları formatla
        text = re.sub(r'^# (.*)', r'═══════════════════════════════════════\n\1\n═══════════════════════════════════════', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.*)', r'\n▓▓▓ \1 ▓▓▓', text, flags=re.MULTILINE)
        text = re.sub(r'^### (.*)', r'\n▶ \1', text, flags=re.MULTILINE)
        
        # Bold text
        text = re.sub(r'\*\*(.*?)\*\*', r'【\1】', text)
        
        # Liste elementleri
        text = re.sub(r'^- (.*)', r'  • \1', text, flags=re.MULTILINE)
        
        # Kod blokları
        text = re.sub(r'`([^`]+)`', r'[\1]', text)
        
        # Linkler
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'🔗 \1', text)
        
        # Satır sonları düzenle
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def show_error_content(self, error_msg):
        """Hata durumunda gösterilecek içerik"""
        error_content = f"""
❌ HATA: {error_msg}

📋 GoodBye DPI Manager v2.0 - BNSWare

Bu yazılım internet sansürünü aşmak için geliştirilmiş
modern bir DPI bypass aracıdır.

🌐 Özellikler:
• Deep Packet Inspection bypass
• 7 farklı DNS sağlayıcısı
• Otomatik DNS failover sistemi  
• Modern Python GUI arayüzü
• Gerçek zamanlı izleme
• Sistem servisi entegrasyonu

⚠️ Önemli: Bu yazılım yalnızca yasal kullanım içindir.

🔗 Daha fazla bilgi: https://github.com/ByNoSoftware
        """
        
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", error_content.strip())
        self.text_widget.config(state=tk.DISABLED)
    
    def open_github(self):
        """GitHub sayfasını aç"""
        try:
            os.system("start https://github.com/ByNoSoftware")
        except:
            pass
    
    def copy_info(self):
        """Bilgileri panoya kopyala"""
        try:
            content = self.text_widget.get("1.0", tk.END)
            self.popup.clipboard_clear()
            self.popup.clipboard_append(content)
            messagebox.showinfo("Başarılı", "Bilgiler panoya kopyalandı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Kopyalama hatası: {str(e)}")
    
    def save_info(self):
        """Bilgileri dosyaya kaydet"""
        try:
            from tkinter import filedialog
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                initialfilename=f"gdpi_sistem_bilgisi_{timestamp}.txt",
                filetypes=[("Metin dosyası", "*.txt"), ("Tüm dosyalar", "*.*")]
            )
            
            if filename:
                content = self.text_widget.get("1.0", tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Başarılı", f"Bilgiler kaydedildi:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydetme hatası: {str(e)}")

class GoodByeDPIManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GoodBye DPI Manager v2.0 - By BNSWare")
        self.root.configure(bg='#f8f9fa')
        
        # Optimal boyut ve oranlar (16:10 golden ratio yakın)
        window_width = 1200
        window_height = 750
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Sabit boyut - yeniden boyutlandırmayı deaktif et
        self.root.resizable(False, False)
        
        # Ekran ortasında konumlandır
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        # Modern window stil
        try:
            self.root.iconbitmap(default="")  # Varsayılan icon'u kaldır
        except:
            pass
        
        # Değişkenler
        self.service_running = tk.BooleanVar()
        self.auto_start = tk.BooleanVar()
        self.dns_enabled = tk.BooleanVar(value=True)
        self.selected_dns = tk.StringVar(value="Google DNS")
        self.failover_enabled = tk.BooleanVar(value=True)
        self.check_interval = tk.IntVar(value=30)
        
        # Failover durumu
        self.current_dns = None
        self.original_dns = None
        self.dns_failed = False
        self.last_dns_check = 0
        
        # Log spam kontrolü
        self.last_status_message = ""
        self.last_failover_status = ""
        self.last_service_status = None
        
        # BNSWare lisans kontrolü
        self.license_valid = False
        self.developer_name = "BNSWare"
        self.github_url = "https://github.com/ByNoSoftware"
        
        # GoodBye DPI yapılandırması
        self.gdpi_path = self.get_gdpi_path()
        self.config_file = os.path.join(os.path.dirname(__file__), "gdpi_config.json")
        
        # Bilgi popup nesnesi
        self.bilgi_popup = None
        
        # DNS listesi ve failover sırası
        self.dns_servers = {
            "Google DNS": {"primary": "8.8.8.8", "secondary": "8.8.4.4", "ipv6": "2001:4860:4860::8888", "priority": 1},
            "Cloudflare DNS": {"primary": "1.1.1.1", "secondary": "1.0.0.1", "ipv6": "2606:4700:4700::1111", "priority": 2},
            "Quad9": {"primary": "9.9.9.9", "secondary": "149.112.112.112", "ipv6": "2620:fe::fe", "priority": 3},
            "AdGuard DNS": {"primary": "94.140.14.14", "secondary": "94.140.15.15", "ipv6": "2a10:50c0::ad1:ff", "priority": 4},
            "Yandex DNS": {"primary": "77.88.8.8", "secondary": "77.88.8.1", "ipv6": "2a02:6b8::feed:0ff", "priority": 5},
            "NextDNS": {"primary": "45.90.28.167", "secondary": "45.90.30.167", "ipv6": "2a07:a8c0::", "priority": 6},
            "Sistem DNS": {"primary": "", "secondary": "", "ipv6": "", "priority": 99}
        }
        
        # Failover DNS sırası (hızdan yavaşa)
        self.failover_order = ["Cloudflare DNS", "Google DNS", "Quad9", "AdGuard DNS"]
        
        self.verify_license()
        self.create_gui()
        self.load_config()  # GUI oluşturulduktan sonra config yükle
        self.check_admin_rights()
        self.update_status()
        
    def verify_license(self):
        """BNSWare lisans doğrulaması"""
        try:
            # Dosya varlığını kontrol et
            script_content = open(__file__, 'r', encoding='utf-8').read()
            
            # Lisans bilgilerini kontrol et
            if self.developer_name in script_content and self.github_url in script_content:
                self.license_valid = True
            else:
                messagebox.showerror("Lisans Hatası", 
                    "Bu yazılım BNSWare tarafından lisanslanmıştır.\n"
                    "Lisans bilgileri değiştirilmiş veya silinmiş!\n\n"
                    "Geliştirici: BNSWare\n"
                    "GitHub: https://github.com/ByNoSoftware")
                sys.exit(1)
        except Exception as e:
            messagebox.showerror("Lisans Hatası", f"Lisans doğrulanmıyor: {str(e)}")
            sys.exit(1)
    
    def check_admin_rights(self):
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                messagebox.showwarning("Yönetici Yetkisi", 
                    "Bu uygulama yönetici yetkisi ile çalıştırılmalıdır.\n"
                    "Uygulamayı sağ tık > 'Yönetici olarak çalıştır' ile başlatın.")
        except:
            pass
    
    def get_gdpi_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        arch = "x86_64" if os.environ.get('PROCESSOR_ARCHITECTURE') == 'AMD64' else "x86"
        return os.path.join(current_dir, arch, "goodbyedpi.exe")
    
    def create_gui(self):
        # Ana container - sabit boyutlara göre optimize edildi
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Sabit grid yapılandırması (1200x750 için optimize)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Sol panel: 450px, Sağ panel: 720px (15px padding hariç)
        main_frame.columnconfigure(0, weight=0, minsize=450)  # Sol panel sabit genişlik
        main_frame.columnconfigure(1, weight=1, minsize=720)  # Sağ panel esnek
        main_frame.rowconfigure(1, weight=1)
        
        # Başlık ve sürüm bilgisi
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(header_frame, text="🎯 GoodBye DPI Manager v2.0", 
                               font=('Segoe UI', 18, 'bold'), foreground='#2c3e50')
        title_label.pack(anchor=tk.W)
        
        # Geliştirici bilgisi
        dev_frame = ttk.Frame(header_frame)
        dev_frame.pack(anchor=tk.W, pady=(5, 0))
        
        dev_label = ttk.Label(dev_frame, text="👨‍💻 Geliştirici: BNSWare", 
                              font=('Segoe UI', 10), foreground='#7f8c8d')
        dev_label.pack(side=tk.LEFT)
        
        github_label = ttk.Label(dev_frame, text="🔗 GitHub: https://github.com/ByNoSoftware", 
                                 font=('Segoe UI', 10), foreground='#3498db', cursor='hand2')
        github_label.pack(side=tk.LEFT, padx=(20, 0))
        github_label.bind("<Button-1>", lambda e: os.system(f"start {self.github_url}"))
        
        # Bilgi butonu
        info_btn = ttk.Button(dev_frame, text="📘 Sistem Bilgileri", 
                             command=self.show_system_info,
                             style="Info.TButton")
        info_btn.pack(side=tk.RIGHT, padx=(20, 0))
        
        # Sol panel - Kontroller
        left_frame = ttk.LabelFrame(main_frame, text=" 🎮 Kontrol Paneli ", padding="15")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 15))
        
        # Servis durumu
        status_frame = ttk.LabelFrame(left_frame, text=" 📡 Servis Durumu ", padding="12")
        status_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 12))
        
        self.status_label = ttk.Label(status_frame, text="Durum: Kontrol ediliyor...", 
                                     font=('Segoe UI', 11, 'bold'))
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Ana kontroller
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 12))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        start_btn = ttk.Button(button_frame, text="▶️ Başlat", command=self.start_service,
                              style="Success.TButton")
        start_btn.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=3, padx=(0, 3))
        
        stop_btn = ttk.Button(button_frame, text="⏹️ Durdur", command=self.stop_service,
                             style="Danger.TButton")
        stop_btn.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=3, padx=(3, 0))
        
        restart_btn = ttk.Button(button_frame, text="🔄 Yeniden Başlat", command=self.restart_service,
                                style="Warning.TButton")
        restart_btn.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(6, 0))
        
        # DNS Ayarları
        dns_frame = ttk.LabelFrame(left_frame, text=" 🌐 DNS Ayarları ", padding="10")
        dns_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Checkbutton(dns_frame, text="DNS değiştirme aktif", 
                       variable=self.dns_enabled, command=self.toggle_dns).grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        ttk.Label(dns_frame, text="DNS Sağlayıcı:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        dns_combo = ttk.Combobox(dns_frame, textvariable=self.selected_dns, 
                                values=list(self.dns_servers.keys()), state="readonly")
        dns_combo.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        dns_combo.bind('<<ComboboxSelected>>', self.on_dns_changed)
        
        # Gelişmiş ayarlar
        advanced_frame = ttk.LabelFrame(left_frame, text=" ⚙️ Gelişmiş Ayarlar ", padding="10")
        advanced_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Checkbutton(advanced_frame, text="Sistem başlangıcında otomatik başlat",
                       variable=self.auto_start, command=self.toggle_auto_start).grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        # DNS Failover Ayarları
        failover_frame = ttk.LabelFrame(left_frame, text=" 🔄 DNS Failover Ayarları ", padding="10")
        failover_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Checkbutton(failover_frame, text="Otomatik DNS failover aktif",
                       variable=self.failover_enabled, command=self.toggle_failover).grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        # Kontrol aralığı
        ttk.Label(failover_frame, text="Kontrol aralığı (saniye):").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        interval_frame = ttk.Frame(failover_frame)
        interval_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        interval_scale = ttk.Scale(interval_frame, from_=10, to=300, variable=self.check_interval, orient=tk.HORIZONTAL)
        interval_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.interval_label = ttk.Label(interval_frame, text="30s")
        self.interval_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Scale değiştiğinde label'ı güncelle
        interval_scale.configure(command=self.update_interval_label)
        
        # Failover durumu
        self.failover_status = ttk.Label(failover_frame, text="Durum: Standby", font=('Arial', 9))
        self.failover_status.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Test butonu
        ttk.Button(failover_frame, text="DNS Bağlantısını Test Et", 
                  command=self.test_dns_connectivity).grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Eylem butonları
        action_frame = ttk.Frame(left_frame)
        action_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        save_btn = ttk.Button(action_frame, text="💾 Kaydet", 
                             command=self.save_config, style="Info.TButton")
        save_btn.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 3))
        
        reset_btn = ttk.Button(action_frame, text="🔄 Sıfırla", 
                              command=self.reset_config, style="Warning.TButton")
        reset_btn.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(3, 0))
        
        # Sağ panel - Loglar ve İzleme
        right_frame = ttk.LabelFrame(main_frame, text=" 📈 Sistem Logları ve İzleme ", padding="15")
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)  # Log alanı için
        
        # Log kontrolleri
        log_controls = ttk.Frame(right_frame)
        log_controls.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Button(log_controls, text="🧹 Temizle", 
                  command=self.clear_logs).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(log_controls, text="💾 Kaydet", 
                  command=self.save_logs).pack(side=tk.LEFT, padx=(0, 5))
        
        #ttk.Button(log_controls, text="📘 Bilgi", 
        #          command=self.show_system_info,
        #          style="Info.TButton").pack(side=tk.RIGHT)
        
        # Ana log alanı
        self.log_text = scrolledtext.ScrolledText(right_frame, 
                                                 height=25,  
                                                 width=60,   
                                                 font=('Consolas', 9),
                                                 bg='#2c3e50',
                                                 fg='#ecf0f1',
                                                 insertbackground='#ecf0f1')
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # İstatistik alanı
        stats_frame = ttk.LabelFrame(right_frame, text=" 📊 Anlık İstatistikler ", padding="8")
        stats_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 0))
        
        self.stats_label = ttk.Label(stats_frame, text="İstatistikler yükleniyor...")
        self.stats_label.grid(row=0, column=0, sticky=tk.W)
        
        # Alt durum çubuğu
        status_bar = ttk.Frame(main_frame, padding="5")
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Durum etiketi
        self.bottom_status = ttk.Label(status_bar, text="🔄 Hazır", 
                                      font=('Segoe UI', 9, 'italic'),
                                      foreground='#7f8c8d')
        self.bottom_status.pack(side=tk.LEFT)
        
        # Sürüm bilgisi sağda
        version_label = ttk.Label(status_bar, text="v2.0 - BNSWare", 
                                 font=('Segoe UI', 8),
                                 foreground='#95a5a6')
        version_label.pack(side=tk.RIGHT)
        
        # Güncelleme thread'i başlat
        self.update_thread_running = True
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()
    
    def check_dns_connectivity(self, dns_name, timeout=5):
        """DNS sunucusunun erişilebilirliğini kontrol eder"""
        if dns_name == "Sistem DNS":
            return True
            
        dns_info = self.dns_servers.get(dns_name)
        if not dns_info:
            return False
            
        primary_dns = dns_info["primary"]
        
        try:
            # DNS sorgusu ile test et
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            sock.connect((primary_dns, 53))
            sock.close()
            
            # HTTP üzerinden de test et
            response = requests.get("http://www.google.com", timeout=timeout, 
                                   headers={'User-Agent': 'Mozilla/5.0'})
            return response.status_code == 200
            
        except Exception:
            return False
    
    def get_next_dns(self, current_dns):
        """Failover sırasına göre sonraki DNS'i döndürür"""
        if current_dns not in self.failover_order:
            return self.failover_order[0] if self.failover_order else None
            
        current_index = self.failover_order.index(current_dns)
        next_index = (current_index + 1) % len(self.failover_order)
        return self.failover_order[next_index]
    
    def perform_dns_failover(self):
        """DNS failover işlemini gerçekleştirir"""
        if not self.failover_enabled.get() or not self.service_running.get():
            return
            
        current_time = time.time()
        if current_time - self.last_dns_check < self.check_interval.get():
            return
            
        self.last_dns_check = current_time
        original_dns = self.original_dns or self.selected_dns.get()
        current_dns = self.current_dns or self.selected_dns.get()
        
        # Ana DNS'i kontrol et
        if self.check_dns_connectivity(original_dns):
            if self.dns_failed and current_dns != original_dns:
                # Ana DNS geri geldi, geri dön
                self.log(f"🔄 Ana DNS ({original_dns}) geri geldi, değiştiriliyor...")
                self.switch_to_dns(original_dns)
                self.dns_failed = False
                self.current_dns = original_dns
            return
        
        # Ana DNS çalışmıyor
        if not self.dns_failed:
            self.log(f"⚠️ Ana DNS ({original_dns}) erişilemez durumda!")
            self.dns_failed = True
            self.original_dns = original_dns
        
        # Mevcut DNS'i kontrol et
        if not self.check_dns_connectivity(current_dns):
            # Sonraki DNS'e geç
            next_dns = self.get_next_dns(current_dns)
            if next_dns and self.check_dns_connectivity(next_dns):
                self.log(f"🔄 Failover: {current_dns} -> {next_dns}")
                self.switch_to_dns(next_dns)
                self.current_dns = next_dns
            else:
                self.log(f"❌ Hiçbir yedek DNS erişilemiyor!")
    
    def switch_to_dns(self, dns_name):
        """DNS'i değiştirir ve servisi yeniden başlatır"""
        old_dns = self.selected_dns.get()
        self.selected_dns.set(dns_name)
        
        # Servisi yeniden başlat
        if self.service_running.get():
            self.restart_service_silent()
        
        self.log(f"🔄 DNS değiştirildi: {old_dns} -> {dns_name}")
    
    def restart_service_silent(self):
        """Sessiz servis yeniden başlatma (log spam olmadan)"""
        try:
            # Servis durdur
            subprocess.run(['sc', 'stop', 'GoodbyeDPI'], 
                          capture_output=True, timeout=5, encoding='utf-8', errors='ignore')
            time.sleep(1)
            
            # Servis başlat
            subprocess.run(['sc', 'start', 'GoodbyeDPI'], 
                          capture_output=True, timeout=5, encoding='utf-8', errors='ignore')
                          
        except Exception:
            pass
    
    def update_status(self):
        try:
            result = subprocess.run(['sc', 'query', 'GoodbyeDPI'], 
                                  capture_output=True, text=True, timeout=5, encoding='utf-8', errors='ignore')
            
            current_service_status = result.returncode == 0 and 'RUNNING' in result.stdout
            
            if current_service_status:
                self.service_running.set(True)
                status_text = "Durum: ✅ Aktif"
                
                # Failover durumunu göster
                if self.dns_failed and self.current_dns:
                    status_text += f" (Failover: {self.current_dns})"
                    self.status_label.config(text=status_text, foreground="orange")
                else:
                    self.status_label.config(text=status_text, foreground="green")
                
                # Sadece durum değiştiğinde log yaz
                if self.last_service_status != True:
                    self.log("✅ Servis aktif durumda")
                    self.last_service_status = True
            else:
                self.service_running.set(False)
                self.status_label.config(text="Durum: ❌ Pasif", foreground="red")
                
                # Sadece durum değiştiğinde log yaz
                if self.last_service_status != False:
                    self.log("❌ Servis pasif durumda")
                    self.last_service_status = False
                    
        except Exception as e:
            self.service_running.set(False)
            self.status_label.config(text="Durum: ❌ Hata", foreground="red")
            self.log(f"Durum kontrolü hatası: {str(e)}")
    
    def start_service(self):
        try:
            self.log("Servis başlatılıyor...")
            self.bottom_status.config(text="Servis başlatılıyor...")
            
            # Önce mevcut servisi durdur
            subprocess.run(['sc', 'stop', 'GoodbyeDPI'], 
                          capture_output=True, timeout=10, encoding='utf-8', errors='ignore')
            subprocess.run(['sc', 'delete', 'GoodbyeDPI'], 
                          capture_output=True, timeout=10, encoding='utf-8', errors='ignore')
            
            # DNS ayarlarını uygula
            dns_params = ""
            if self.dns_enabled.get() and self.selected_dns.get() != "Sistem DNS":
                dns_info = self.dns_servers[self.selected_dns.get()]
                dns_params = f'--dns-addr {dns_info["primary"]} --dns-port 53 --dnsv6-addr {dns_info["ipv6"]} --dnsv6-port 53'
                
                # İlk başlatmada orijinal DNS'i kaydet
                if not self.original_dns:
                    self.original_dns = self.selected_dns.get()
                    self.current_dns = self.selected_dns.get()
            
            # Servis komutunu oluştur
            cmd = f'"{self.gdpi_path}" -5 {dns_params} -r --fake-with-sni google.com --fake-gen 14 --blacklist "{os.path.join(os.path.dirname(__file__), "TR-blacklist.txt")}"'
            
            # Servisi oluştur ve başlat
            create_result = subprocess.run([
                'sc', 'create', 'GoodbyeDPI', 
                f'binPath={cmd}', 
                'start=auto'
            ], capture_output=True, text=True, timeout=10, encoding='utf-8', errors='ignore')
            
            if create_result.returncode == 0:
                subprocess.run(['sc', 'description', 'GoodbyeDPI', 
                               'Passive Deep Packet Inspection blocker'], 
                              capture_output=True, timeout=5, encoding='utf-8', errors='ignore')
                
                start_result = subprocess.run(['sc', 'start', 'GoodbyeDPI'], 
                                            capture_output=True, text=True, timeout=10, encoding='utf-8', errors='ignore')
                
                if start_result.returncode == 0:
                    self.log("✅ Servis başarıyla başlatıldı")
                    self.update_status()
                else:
                    self.log(f"❌ Servis başlatma hatası: {start_result.stderr}")
            else:
                self.log(f"❌ Servis oluşturma hatası: {create_result.stderr}")
                
        except Exception as e:
            self.log(f"❌ Servis başlatma hatası: {str(e)}")
        finally:
            self.bottom_status.config(text="Hazır")
    
    def stop_service(self):
        try:
            self.log("Servis durduruluyor...")
            self.bottom_status.config(text="Servis durduruluyor...")
            
            result = subprocess.run(['sc', 'stop', 'GoodbyeDPI'], 
                                  capture_output=True, text=True, timeout=10, encoding='utf-8', errors='ignore')
            
            if result.returncode == 0 or 'already stopped' in result.stderr.lower():
                self.log("✅ Servis başarıyla durduruldu")
            else:
                self.log(f"⚠️ Servis durdurma uyarısı: {result.stderr}")
                
            self.update_status()
            
        except Exception as e:
            self.log(f"❌ Servis durdurma hatası: {str(e)}")
        finally:
            self.bottom_status.config(text="Hazır")
    
    def restart_service(self):
        self.log("Servis yeniden başlatılıyor...")
        self.stop_service()
        time.sleep(2)
        self.start_service()
    
    def toggle_dns(self):
        if self.dns_enabled.get():
            self.log("DNS değiştirme aktif edildi")
        else:
            self.log("DNS değiştirme deaktif edildi")
    
    def on_dns_changed(self, event=None):
        dns_name = self.selected_dns.get()
        self.log(f"DNS değiştirildi: {dns_name}")
        
        if dns_name != "Sistem DNS":
            dns_info = self.dns_servers[dns_name]
            self.log(f"  Primary: {dns_info['primary']}")
            self.log(f"  Secondary: {dns_info['secondary']}")
    
    def toggle_auto_start(self):
        try:
            if self.auto_start.get():
                subprocess.run(['sc', 'config', 'GoodbyeDPI', 'start=auto'], 
                              capture_output=True, timeout=5, encoding='utf-8', errors='ignore')
                self.log("✅ Otomatik başlatma aktif edildi")
            else:
                subprocess.run(['sc', 'config', 'GoodbyeDPI', 'start=demand'], 
                              capture_output=True, timeout=5, encoding='utf-8', errors='ignore')
                self.log("✅ Otomatik başlatma deaktif edildi")
        except Exception as e:
            self.log(f"❌ Otomatik başlatma ayarı hatası: {str(e)}")
    
    def toggle_failover(self):
        if self.failover_enabled.get():
            self.log("🔄 DNS Failover aktif edildi")
            self.failover_status.config(text="Durum: Aktif", foreground="green")
        else:
            self.log("⏹️ DNS Failover deaktif edildi")
            self.failover_status.config(text="Durum: Deaktif", foreground="red")
            # Failover durumunu sıfırla
            if self.dns_failed and self.original_dns:
                self.selected_dns.set(self.original_dns)
                self.dns_failed = False
                self.current_dns = None
    
    def update_interval_label(self, value):
        try:
            if hasattr(self, 'interval_label') and self.interval_label:
                self.interval_label.config(text=f"{int(float(value))}s")
        except Exception as e:
            print(f"Interval label güncelleme hatası: {e}")
    
    def test_dns_connectivity(self):
        self.log("🔍 DNS bağlantı testi başlatılıyor...")
        self.bottom_status.config(text="DNS testi yapılıyor...")
        
        def test_thread():
            try:
                current_dns = self.selected_dns.get()
                
                if current_dns == "Sistem DNS":
                    self.log("ℹ️ Sistem DNS kullanılıyor, test atlanıyor")
                    return
                
                # Mevcut DNS'i test et
                if self.check_dns_connectivity(current_dns, timeout=10):
                    self.log(f"✅ {current_dns} bağlantısı başarılı")
                else:
                    self.log(f"❌ {current_dns} bağlantısı başarısız")
                
                # Tüm DNS'leri test et
                self.log("🔍 Tüm DNS sunucuları test ediliyor...")
                for dns_name in self.failover_order:
                    if dns_name == current_dns:
                        continue
                    
                    if self.check_dns_connectivity(dns_name, timeout=5):
                        self.log(f"✅ {dns_name}: Erişilebilir")
                    else:
                        self.log(f"❌ {dns_name}: Erişilemez")
                        
                self.log("✅ DNS bağlantı testi tamamlandı")
                
            except Exception as e:
                self.log(f"❌ DNS test hatası: {str(e)}")
            finally:
                self.bottom_status.config(text="Hazır")
        
        threading.Thread(target=test_thread, daemon=True).start()
    
    def show_system_info(self):
        """Sistem bilgileri popup'ını göster"""
        try:
            if not self.bilgi_popup:
                self.bilgi_popup = BilgiPopup(self.root)
            
            self.bilgi_popup.show_info()
            self.log("📘 Sistem bilgileri görüntülendi")
            
        except Exception as e:
            self.log(f"❌ Bilgi popup hatası: {str(e)}")
            messagebox.showerror("Hata", f"Sistem bilgileri gösterilirken hata:\n{str(e)}")
    
    def log(self, message, force=False):
        """Log mesajı ekler, tekrar eden mesajları engeller"""
        # GUI henüz yüklenmemişse konsola yazdır
        if not hasattr(self, 'log_text') or self.log_text is None:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {message}")
            return
            
        # Spam kontrolü
        if not force and message == self.last_status_message:
            return
            
        # Belirli mesajlar için özel spam kontrolü
        spam_keywords = ["Servis aktif durumda", "Durum: Normal", "İstatistikler yükleniyor"]
        if not force and any(keyword in message for keyword in spam_keywords):
            if message == self.last_status_message:
                return
        
        self.last_status_message = message
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        try:
            self.log_text.insert(tk.END, log_message)
            self.log_text.see(tk.END)
            
            # Maksimum log satırı kontrolü
            lines = self.log_text.get("1.0", tk.END).split('\n')
            if len(lines) > 1000:
                self.log_text.delete("1.0", f"{len(lines)-500}.0")
        except Exception as e:
            # Log widget hatası varsa konsola yazdır
            print(f"[{timestamp}] {message}")
            print(f"Log widget hatası: {e}")
    
    def clear_logs(self):
        self.log_text.delete("1.0", tk.END)
        self.log("Loglar temizlendi")
    
    def save_logs(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"gdpi_logs_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.log_text.get("1.0", tk.END))
            
            self.log(f"✅ Loglar kaydedildi: {filename}")
            messagebox.showinfo("Başarılı", f"Loglar {filename} dosyasına kaydedildi")
            
        except Exception as e:
            self.log(f"❌ Log kaydetme hatası: {str(e)}")
    
    def save_config(self):
        try:
            config = {
                "dns_enabled": self.dns_enabled.get(),
                "failover_enabled": self.failover_enabled.get(),
                "check_interval": self.check_interval.get(),
                "selected_dns": self.selected_dns.get(),
                "auto_start": self.auto_start.get(),
                "timestamp": datetime.now().isoformat()
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.log("✅ Konfigürasyon kaydedildi")
            messagebox.showinfo("Başarılı", "Ayarlar kaydedildi")
            
        except Exception as e:
            self.log(f"❌ Konfigürasyon kaydetme hatası: {str(e)}")
    
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                self.dns_enabled.set(config.get("dns_enabled", True))
                self.selected_dns.set(config.get("selected_dns", "Google DNS"))
                self.auto_start.set(config.get("auto_start", False))
                self.failover_enabled.set(config.get("failover_enabled", True))
                self.check_interval.set(config.get("check_interval", 30))
                
                self.log("✅ Konfigürasyon yüklendi")
            else:
                self.log("ℹ️ Konfigürasyon dosyası bulunamadı, varsayılan değerler kullanılıyor")
        except Exception as e:
            self.log(f"⚠️ Konfigürasyon yükleme hatası: {str(e)}")
    
    def reset_config(self):
        try:
            self.dns_enabled.set(True)
            self.selected_dns.set("Google DNS")
            self.auto_start.set(False)
            self.failover_enabled.set(True)
            self.check_interval.set(30)
            
            # Failover durumunu sıfırla
            self.dns_failed = False
            self.original_dns = None
            self.current_dns = None
            
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            
            self.log("✅ Ayarlar sıfırlandı")
            messagebox.showinfo("Başarılı", "Ayarlar sıfırlandı")
            
        except Exception as e:
            self.log(f"❌ Ayar sıfırlama hatası: {str(e)}")
    
    def update_stats(self):
        try:
            # Sistem istatistikleri
            import psutil
            
            # CPU ve RAM kullanımı
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            
            # GoodBye DPI process bilgisi
            gdpi_memory = 0
            gdpi_running = False
            
            for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                try:
                    if 'goodbyedpi' in proc.info['name'].lower():
                        gdpi_memory = proc.info['memory_info'].rss / 1024 / 1024  # MB
                        gdpi_running = True
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            stats_text = f"""Sistem Durumu:
CPU Kullanımı: {cpu_percent}%
RAM Kullanımı: {memory.percent}%
GoodBye DPI Bellek: {gdpi_memory:.1f} MB
Servis Durumu: {'✅ Aktif' if gdpi_running else '❌ Pasif'}
Son Güncelleme: {datetime.now().strftime('%H:%M:%S')}"""
            
            self.stats_label.config(text=stats_text)
            
        except ImportError:
            self.stats_label.config(text="İstatistikler için 'pip install psutil' gerekli")
        except Exception as e:
            self.stats_label.config(text=f"İstatistik hatası: {str(e)}")
    
    def update_loop(self):
        while self.update_thread_running:
            try:
                self.update_status()
                self.update_stats()
                
                # DNS failover kontrolü
                if self.failover_enabled.get():
                    self.perform_dns_failover()
                    
                    # Failover durumunu GUI'de göster
                    if self.dns_failed:
                        self.failover_status.config(
                            text=f"Durum: Failover ({self.current_dns})", 
                            foreground="orange"
                        )
                    else:
                        self.failover_status.config(
                            text="Durum: Normal", 
                            foreground="green"
                        )
                else:
                    self.failover_status.config(
                        text="Durum: Deaktif", 
                        foreground="red"
                    )
                
                time.sleep(5)  # 5 saniyede bir güncelle
            except Exception:
                pass
    
    def on_closing(self):
        self.update_thread_running = False
        self.root.destroy()
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Modern stil ayarları
        style = ttk.Style()
        style.theme_use('clam')
        
        # Özel modern stiller
        style.configure("Success.TButton", 
                       foreground="white", 
                       background="#27ae60",
                       font=('Segoe UI', 9, 'bold'),
                       focuscolor="none")
        style.map("Success.TButton",
                 background=[('active', '#2ecc71'), ('pressed', '#229954')])
        
        style.configure("Danger.TButton", 
                       foreground="white", 
                       background="#e74c3c",
                       font=('Segoe UI', 9, 'bold'),
                       focuscolor="none")
        style.map("Danger.TButton",
                 background=[('active', '#c0392b'), ('pressed', '#a93226')])
        
        style.configure("Warning.TButton", 
                       foreground="white", 
                       background="#f39c12",
                       font=('Segoe UI', 9, 'bold'),
                       focuscolor="none")
        style.map("Warning.TButton",
                 background=[('active', '#e67e22'), ('pressed', '#d35400')])
        
        style.configure("Info.TButton", 
                       foreground="white", 
                       background="#3498db",
                       font=('Segoe UI', 9, 'bold'),
                       focuscolor="none")
        style.map("Info.TButton",
                 background=[('active', '#2980b9'), ('pressed', '#2471a3')])
        
        # Modern Label stili
        style.configure("TLabel", font=('Segoe UI', 9))
        style.configure("TLabelframe.Label", font=('Segoe UI', 10, 'bold'))
        
        # Modern Checkbutton stili
        style.configure("TCheckbutton", font=('Segoe UI', 9))
        
        # Başlangıç mesajları
        self.log("=" * 50, force=True)
        self.log("🚀 GoodBye DPI Manager v2.0 başlatıldı", force=True)
        self.log("👨‍💻 Geliştirici: BNSWare", force=True)
        self.log("🔗 GitHub: https://github.com/ByNoSoftware", force=True)
        self.log("=" * 50, force=True)
        self.log("⚠️ Yönetici yetkisi ile çalıştırıldığından emin olun", force=True)
        self.log(f"📁 GoodBye DPI Path: {self.gdpi_path}", force=True)
        self.log("🔄 DNS Failover sistemi aktif!", force=True)
        self.log("📏 Form boyutları: 1200x750 (Sabit)", force=True)
        self.log("=" * 50, force=True)
        
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = GoodByeDPIManager()
        app.run()
    except KeyboardInterrupt:
        print("\nUygulama kapatılıyor...")
    except Exception as e:
        messagebox.showerror("Hata", f"Uygulama hatası: {str(e)}")