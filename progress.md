# Arazi Tarama Projesi - Progress

## Amaç

Kamera ve sensör tabanlı arazi taraması için modüler bir drone/robot prototipi geliştirmek: görev isteğini planlamak, güvenlik kontrollerini uygulamak, sensör verisini işlemek ve sonucu kullanıcıya sunmak.

## Mevcut durum

### Tamamlandı

- [x] Doğal dil girdisinden temel tarama planı ve araç komutları üretimi
- [x] Misyon oluşturma, yükseklik ve güvenlik marjı kontrolleri
- [x] Drone/robot komut adaptörleri ve PX4/MAVLink/ROS benzeri entegrasyon iskeletleri
- [x] Sensör kayıt, kamera, LiDAR, GPS/IMU, füzyon ve telemetri modülleri
- [x] Donanım bulunmayan ortamlarda kamera fallback akışı
- [x] x/y hücre koordinatlarından risk grid'i ve terminal ASCII görünümü
- [x] JSON misyon raporu ve metin özeti dışa aktarımı (`artifacts/`)
- [x] Yerel web dashboard: HTML arayüzü, `/api/status` ve paylaşımlı MJPEG `/stream.mjpg`
- [x] Dashboard CLI ile kamera kaynağı, host, port ve FPS seçimi
- [x] Dashboard'un önceki JSON raporunu yükleyebilmesi
- [x] Kamera URL kullanıcı bilgileri ve query parametrelerinin API'de gizlenmesi
- [x] Paket kurulumu ve `terrain-scan-dashboard` komutu
- [x] Dashboard güvenlik/endpoint/stream davranışları için testler

### Devam ediyor / donanımda doğrulanmadı

- [ ] USB veya RTSP kamera ile hedef saha ortamında bağlantı ve görüntü kalitesi doğrulaması
- [ ] Gerçek GPS/IMU sürücüsü ve zaman/konum korelasyonu
- [ ] Gerçek PX4/MAVLink/ROS2 donanım bağlantısı ve kontrollü saha testi
- [ ] GPS koordinatlarına bağlanan coğrafi risk haritası
- [ ] Uçuş/robot prosedürleri, kalibrasyon ve saha güvenliği doğrulaması

## Katmanlar

### Planlama ve misyon
- [x] Görev planı: `terrain_scan_agent/planner.py`
- [x] Misyon ve güvenlik değerlendirmesi: `terrain_scan_agent/mission.py`, `terrain_scan_agent/safety.py`

### Sensörler ve analiz
- [x] Kamera ve fallback: `terrain_scan_agent/live_camera.py`, `terrain_scan_agent/real_camera.py`
- [x] GPS/IMU, navigasyon füzyonu ve LiDAR
- [x] Risk analizi, sensör füzyonu ve telemetri işleme
- [x] Hücre tabanlı risk haritası: `terrain_scan_agent/risk_map.py`

### Runtime, rapor ve arayüz
- [x] Örnek saha akışı: `terrain_scan_agent/field_runtime.py`, `main.py`
- [x] JSON/metin raporları: `terrain_scan_agent/reporting.py`
- [x] Canlı web dashboard: `terrain_scan_agent/web_dashboard.py`, `terrain_scan_agent/dashboard.py`
- [x] HTML sayfasında misyon bilgisi ve periyodik API durum yenilemesi
- [x] Paylaşılan kamera yakalama döngüsünden MJPEG video akışı

## Doğrulama

Sanal ortamı kurup testleri çalıştırma:

```bash
./setup.sh
. .venv/bin/activate
python -m pytest -q
```

Son doğrulama sonucu: **38 test geçti**.

Dashboard smoke testinde HTML sayfası, durum API'si ve JPEG frame içeren multipart stream doğrulandı. Test cihazı olmadığı için kamera fallback görüntüsü kullanıldı; gerçek USB/RTSP cihaz bağlantısı bu ortamda denenmedi.

Örnek demo:

```bash
python main.py
```

Dashboard:

```bash
terrain-scan-dashboard --camera /dev/video0 --report artifacts/mission_report.json
```

## Kapsam ve güvenlik notu

Risk grid'i şu an GPS koordinatlarından üretilen coğrafi harita değildir. PX4/MAVLink/ROS sınıfları gerçek araç üzerinde doğrulanmış uçuş kontrolü anlamına gelmez. Gerçek araçlarda kullanım öncesinde bağımsız güvenlik katmanları ve yetkili saha testleri gerekir. Web sunucusunda yerleşik kimlik doğrulama/TLS yoktur; varsayılan olarak yalnızca localhost'ta dinler.
