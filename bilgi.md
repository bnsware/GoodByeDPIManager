# 🎯 GoodBye DPI Manager v2.0 - Sistem Bilgileri

## 📋 Genel Bakış

GoodBye DPI Manager, internet sansürünü aşmak ve DPI (Deep Packet Inspection) engellemelerini bypass etmek için geliştirilmiş modern bir yönetim aracıdır. Bu yazılım, ValdikSS'in GoodBye DPI projesi üzerine inşa edilmiş ve BNSWare tarafından Python ile yeniden tasarlanmıştır.

## 🚀 Sistem Özellikleri

### **Temel İşlevler**
- **DPI Bypass**: Paket manipülasyonu ile derin paket incelemesini atlar
- **DNS Değiştirme**: 7 farklı DNS sağlayıcısı desteği
- **Servis Yönetimi**: Windows servis entegrasyonu
- **Otomatik Başlatma**: Sistem açılışında otomatik çalışma

### **Gelişmiş Özellikler**
- **DNS Failover**: Otomatik DNS geçiş sistemi
- **Anti-Spam Loglama**: Akıllı log filtreleme
- **Gerçek Zamanlı İzleme**: Anlık sistem durumu
- **Yapılandırma Yönetimi**: Otomatik ayar kaydetme

## 🌐 Desteklenen DNS Sağlayıcıları

### **1. Google DNS**
- **Primary**: 8.8.8.8
- **Secondary**: 8.8.4.4  
- **IPv6**: 2001:4860:4860::8888
- **Özellik**: Hızlı ve güvenilir

### **2. Cloudflare DNS**
- **Primary**: 1.1.1.1
- **Secondary**: 1.0.0.1
- **IPv6**: 2606:4700:4700::1111
- **Özellik**: En hızlı DNS, gizlilik odaklı

### **3. Quad9**
- **Primary**: 9.9.9.9
- **Secondary**: 149.112.112.112
- **IPv6**: 2620:fe::fe
- **Özellik**: Güvenlik odaklı, kötü amaçlı site engelleme

### **4. AdGuard DNS**
- **Primary**: 94.140.14.14
- **Secondary**: 94.140.15.15
- **IPv6**: 2a10:50c0::ad1:ff
- **Özellik**: Reklam engelleme, aile koruması

### **5. Yandex DNS**
- **Primary**: 77.88.8.8
- **Secondary**: 77.88.8.1
- **IPv6**: 2a02:6b8::feed:0ff
- **Özellik**: Rusya merkezli, hızlı bağlantı

### **6. NextDNS**
- **Primary**: 45.90.28.167
- **Secondary**: 45.90.30.167
- **IPv6**: 2a07:a8c0::
- **Özellik**: Özelleştirilebilir güvenlik

### **7. Sistem DNS**
- **Açıklama**: İşletim sisteminin varsayılan DNS ayarları
- **Özellik**: Değişiklik yapmaz, orijinal ayarları korur

## 🔄 DNS Failover Sistemi

### **Nasıl Çalışır?**
1. **Ana DNS İzleme**: Seçili DNS sürekli kontrol edilir
2. **Bağlantı Kopması**: Ana DNS erişilemez olursa algılanır
3. **Otomatik Geçiş**: Hızlı yedek DNS'e geçilir
4. **Geri Dönüş**: Ana DNS geri gelince otomatik döner

### **Failover Sırası**
1. **Cloudflare DNS** (En hızlı)
2. **Google DNS** (En güvenilir)
3. **Quad9** (En güvenli)
4. **AdGuard DNS** (Reklam engelleme)

### **Ayarlanabilir Parametreler**
- **Kontrol Aralığı**: 10-300 saniye
- **Aktif/Pasif**: Failover sistemini aç/kapat
- **Test Fonksiyonu**: Manuel DNS testi

## ⚙️ Teknik Detaylar

### **GoodBye DPI Parametreleri**
- **-5**: 5. seviye paket manipülasyonu
- **--dns-addr**: DNS sunucu adresi
- **--dns-port**: DNS port (varsayılan: 53)
- **-r**: Raw socket kullanımı
- **--fake-with-sni**: SNI manipülasyonu
- **--fake-gen**: Sahte paket üretimi
- **--blacklist**: Engellenen site listesi

### **Windows Servis Entegrasyonu**
- **Servis Adı**: GoodbyeDPI
- **Başlatma Türü**: Otomatik/Manuel
- **Çalışma Modu**: Arka plan servisi
- **Yetki Seviyesi**: Yönetici gerekli

### **Ağ Yapılandırması**
- **Protokol**: TCP/UDP
- **Port Aralığı**: 53 (DNS), 80/443 (HTTP/HTTPS)
- **İşletim Sistemi**: Windows 7/8/10/11
- **Mimari**: x86, x86_64

## 🛡️ Güvenlik Özellikleri

### **Güvenli Operasyonlar**
- **Encoding Koruması**: UTF-8 uyumlu
- **Hata Yakalama**: Kapsamlı exception handling
- **Thread Safety**: Güvenli çoklu iş parçacığı
- **Memory Management**: Akıllı bellek yönetimi

## 📊 Performans Özellikleri

### **Sistem Kaynakları**
- **RAM Kullanımı**: ~10-15 MB
- **CPU Kullanımı**: <1%
- **Disk Alanı**: ~5 MB
- **Ağ Trafiği**: Minimal ek yük

### **Hız Optimizasyonları**
- **DNS Caching**: Hızlı DNS çözümleme
- **Paket Önbelleği**: Optimize edilmiş paket işleme
- **Asenkron İşlemler**: Bloklamayan operasyonlar
- **Thread Pooling**: Verimli iş parçacığı yönetimi

## 📱 Kullanıcı Arayüzü

### **Kullanıcı Deneyimi**
- **Tek Tıkla Başlatma**: Kolay kullanım
- **Anlık Geri Bildirim**: Durum göstergeleri
- **Hata Toleransı**: Kullanıcı dostu hata mesajları
- **Otomatik Kayıt**: Ayar hatırlama

## 🔧 Kurulum Gereksinimleri

### **Sistem Gereksinimleri**
- **İşletim Sistemi**: Windows 7 SP1 veya üzeri
- **Python**: 3.6+ (önerilen: 3.9+)
- **RAM**: Minimum 2GB (önerilen: 4GB+)
- **Disk**: 50MB boş alan
- **Yetki**: Yönetici erişimi gerekli

### **Python Bağımlılıkları**
- **psutil**: Sistem bilgileri (≥5.9.0)
- **requests**: HTTP istekleri (≥2.28.0)
- **tkinter**: GUI framework (Python ile birlikte)
- **threading**: Çoklu iş parçacığı (standart kütüphane)

## 📈 Güncellemeler ve Bakım

### **Otomatik Özellikler**
- **Log Rotasyonu**: 1000 satır sınırı
- **Bellek Temizleme**: Otomatik garbage collection  
- **Yapılandırma Senkronizasyonu**: Otomatik kayıt
- **Servis İzleme**: 5 saniyede bir kontrol

### **Bakım İpuçları**
- **Düzenli Yeniden Başlatma**: Haftalık önerilen
- **Log Temizleme**: İhtiyaç halinde manuel
- **Yapılandırma Yedeği**: Ayar dosyası sakla
- **Güncelleme Takibi**: GitHub kontrolü

## ⚠️ Önemli Notlar

### **Yasal Uyarı**
Bu yazılım yalnızca yasal kullanım için tasarlanmıştır. Kullanıcılar bulundukları ülkenin internet yasalarına uymakla yükümlüdür.

### **Sorumluluk Reddi**
BNSWare, yazılımın kötüye kullanımından sorumlu tutulamaz. Yazılım "olduğu gibi" sağlanmaktadır.

### **Teknik Destek**
- **GitHub Issues**: Hata bildirimi ve özellik istekleri
- **Dokümantasyon**: README dosyaları
- **Topluluk Desteği**: Kullanıcı forumları

## 🏆 Kredi ve Teşekkürler

### **Ana Proje**
- **GoodBye DPI**: ValdikSS tarafından geliştirilen orijinal proje
- **GitHub**: https://github.com/ValdikSS/GoodbyeDPI

### **Python Yeniden Yazım**
- **Geliştirici**: BNSWare
- **GitHub**: https://github.com/ByNoSoftware
- **Sürüm**: 2.0 (2024)

### **Açık Kaynak Kütüphaneler**
- **Python**: Guido van Rossum ve Python Software Foundation
- **Tkinter**: Tcl/Tk GUI toolkit
- **PSUtil**: Giampaolo Rodola

---

*Bu yazılım özgür yazılımdır ve eğitim amaçlı geliştirilmiştir.*