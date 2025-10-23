# 🎯 GoodBye DPI Manager v2.0

[![badge](https://rozet.vixware.net/icon/coffee/badge/Buy%20Me%20a%20Coffee/yellow?style=single)](https://www.buymeacoffee.com/bnsware)

![github stars](https://rozet.vixware.net/github/bnsware/GoodByeDPIManager/stars)
![github license](https://rozet.vixware.net/github/bnsware/GoodByeDPIManager/license)
![github language](https://rozet.vixware.net/github/bnsware/GoodByeDPIManager/language)
![github lastcommit](https://rozet.vixware.net/github/bnsware/GoodByeDPIManager/lastcommit)
![github forks](https://rozet.vixware.net/github/bnsware/GoodByeDPIManager/forks)

**Modern ve kullanıcı dostu Python tabanlı GoodBye DPI yönetim paneli**

**👨‍💻 Geliştirici:** BNSWare  
**🔗 GitHub:** https://github.com/ByNoSoftware  
**📅 Sürüm:** v2.0 (2025)  

![License](https://rozet.vixware.net/License/Apache-2.0/yellow?style=premium)
![Platform](https://rozet.vixware.net/Platform/Windows%207%2F8%2F10%2F11/blue?style=premium)
![Software](https://rozet.vixware.net/icon/python/badge/3.6%2B/blue?style=single)

## Özellikler

### 🎯 Ana Özellikler
- ✅ **Tek Panel Yönetim**: Tüm işlemleri tek arayüzden kontrol edin
- ✅ **Anlık Durum İzleme**: Servis durumunu gerçek zamanlı takip edin
- ✅ **DNS Yönetimi**: 7 farklı DNS sağlayıcısı arasında seçim yapın
- ✅ **Otomatik DNS Failover**: Bağlantı koptuğunda otomatik yedek DNS'e geçiş
- ✅ **Otomatik Yapılandırma**: Ayarlarınız otomatik kaydedilir
- ✅ **Detaylı Loglama**: Tüm işlemler detaylı olarak loglanır
- ✅ **Sistem İstatistikleri**: CPU, RAM ve servis durumu anlık izleme

### 🔄 DNS Failover Sistemi
- **Otomatik Tespit**: Seçili DNS'in çalışmadığı durumları otomatik algılar
- **Akıllı Geçiş**: Hızlı DNS'lere öncelik verir (Cloudflare → Google → Quad9 → AdGuard)
- **Otomatik Geri Dönüş**: Ana DNS geri geldiğinde otomatik olarak geri döner
- **Yapılandırılabilir**: Kontrol aralığı ve aktivasyon ayarlanabilir
- **Test Fonksiyonu**: DNS bağlantısını manuel test edebilme

### 🔧 DNS Sağlayıcıları
- Google DNS (8.8.8.8)
- Cloudflare DNS (1.1.1.1)
- Quad9 (9.9.9.9)
- AdGuard DNS (94.140.14.14)
- Yandex DNS (77.88.8.8)
- NextDNS (45.90.28.167)
- Sistem DNS (Değiştirmez)

### 📊 İzleme Özellikleri
- Servis durumu (Aktif/Pasif)
- CPU ve RAM kullanımı
- GoodBye DPI bellek kullanımı
- Sistem kaynak monitörü
- Detaylı hata raporlama

## Kurulum

### Gereksinimler
![Windows](https://rozet.vixware.net/Windows/7%2F8%2F10%2F11/blue?style=premium)

![Python ](https://rozet.vixware.net/Python%20/3.6%20veya%20%C3%BCzeri/orange?style=premium)

![Başlatma ](https://rozet.vixware.net/Ba%C5%9Flatma%20/Y%C3%B6netici%20yetkileri/teal?style=premium)

### Hızlı Başlangıç
1. `start_manager.bat` dosyasını **yönetici olarak** çalıştırın
2. Gerekli kütüphaneler otomatik yüklenecek
3. Yönetim paneli açılacak

### Manuel Kurulum
```bash
pip install -r requirements.txt
python manager.py
```

## Kullanım

### İlk Başlatma
1. Uygulamayı **yönetici yetkisi** ile çalıştırın
2. DNS ayarlarınızı seçin
3. "Servisi Başlat" butonuna tıklayın
4. Servis durumunu kontrol edin

### Ana Kontroller
- **Başlat**: Servisi başlatır
- **Durdur**: Servisi durdurur  
- **Yeniden Başlat**: Servisi yeniden başlatır
- **DNS Değiştir**: Farklı DNS sağlayıcıları arasında geçiş

### Ayarlar
- **Otomatik Başlat**: Sistem açılışında otomatik başlatma
- **DNS Aktif**: DNS değiştirme özelliğini aç/kapat
- **Konfigürasyon**: Ayarları kaydet/yükle

## Sorun Giderme

### Yaygın Problemler

**1. "Yönetici yetkisi gerekli" hatası**
- Uygulamayı sağ tık → "Yönetici olarak çalıştır"

**2. Python bulunamadı**
- Python'u https://python.org adresinden indirin
- Kurulum sırasında "Add to PATH" seçeneğini işaretleyin

**3. Servis başlatılamıyor**
- Antivirus yazılımını geçici olarak deaktive edin
- Windows Güvenlik Duvarı ayarlarını kontrol edin
- goodbyedpi.exe dosyasının var olduğunu kontrol edin

**4. DNS değişikliği çalışmıyor**
- İnternet bağlantısını kontrol edin
- DNS cache'i temizleyin: `ipconfig /flushdns`
- Farklı bir DNS sağlayıcısı deneyin

### Log İnceleme
- Sağ panelde tüm işlemler loglanır
- "Logları Kaydet" ile dosyaya aktarabilirsiniz
- Hata mesajları detaylı olarak gösterilir

### Performance İpuçları
- Servis aktifken sistem kaynaklarını monitör edin
- Gereksiz uygulamaları kapatın
- Düzenli olarak logları temizleyin

## Gelişmiş Özellikler

### Yapılandırma Dosyası
Ayarlar `gdpi_config.json` dosyasında saklanır:
```json
{
  "dns_enabled": true,
  "selected_dns": "Google DNS",
  "auto_start": false,
  "timestamp": "2024-01-01T00:00:00"
}
```

### Komut Satırı Kullanımı
```bash
# Doğrudan çalıştırma
python manager.py

# Gereksinimler kurulumu
pip install -r requirements.txt
```

## Güvenlik

- ✅ Yalnızca yasal kullanım için tasarlanmıştır
- ✅ Hiçbir veri dışarı gönderilmez
- ✅ Açık kaynak kodlu
- ✅ Virus taraması yapılmıştır

## 📋 Sürüm Geçmişi

### v2.0 - Modern & Smart Update
#### 🆕 Yeni Özellikler
- 🎨 **Modern UI Tasarım**: Emoji'li, renkli ve profesyonel arayüz
- 🔄 **Akıllı DNS Failover**: Otomatik DNS geçiş sistemi
- 🚫 **Log Spam Önleme**: Tekrar eden mesajları engeller
- 🧹 **Temiz Yapı**: Gereksiz dosyalar arşivlendi

#### 🎨 UI Geliştirmeleri
- Segoe UI font ailesi
- Modern renk paleti (Yeşil, Kırmızı, Turuncu, Mavi)
- Emoji ile zenginleştirilmiş etiketler
- Responsive buton tasarımı
- Geliştirilmiş spacing ve padding

#### 🔧 Teknik İyileştirmeler
- Anti-spam log sistemi
- Performans optimizasyonları
- Hata yakalama geliştirmeleri
- Thread-safe operations

### v1.x
- Temel batch script yönetimi

## Lisans

Bu yazılım GoodBye DPI projesi üzerine geliştirilmiştir.
Orijinal proje: https://github.com/ValdikSS/GoodbyeDPI

## Destek

Sorun yaşadığınızda:
1. Logları kontrol edin
2. Yönetici yetkisi ile çalıştırdığınızdan emin olun
3. Antivirus'ün engellemediğini kontrol edin

4. Sistem gereksinimlerini karşıladığınızdan emin olun





