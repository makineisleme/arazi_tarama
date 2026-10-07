# Mimari

## Genel bakış

Proje; görev planlama, misyon güvenlik kontrolleri, sensör edinimi, analiz, raporlama ve yerel web sunumundan oluşan katmanlı bir Python prototipidir. Demo akışı simülasyon/fallback girdileriyle donanım olmadan çalışabilir.

## Katmanlar

### 1. Planlama ve misyon güvenliği

- `terrain_scan_agent/planner.py`: kullanıcı isteğini basit eylem planına ve araç komutlarına dönüştürür.
- `terrain_scan_agent/mission.py`: misyonu oluşturur ve `terrain_scan_agent/safety.py` üzerinden sınırları değerlendirir.

### 2. Araç kontrol adaptörleri

- `terrain_scan_agent/control.py`: örnek komut yürütme arayüzü.
- `terrain_scan_agent/px4_controller.py`, `mavlink_adapter.py`, `ros_bridge.py`, `ros_mavlink_bridge.py`: kontrol protokolü adaptörleri/iskeletleri.

Bu sınıfların başarılı örnek çıktısı gerçek araç bağlantısı veya gerçek uçuş emniyeti doğrulaması değildir.

### 3. Sensör edinimi ve füzyon

- Kamera: `live_camera.py`, `real_camera.py`
- GPS/IMU: `gps_imu_driver.py`, `navigation_fusion.py`
- LiDAR: `lidar_capture.py`
- Sensör yönetimi/akışı: `sensors.py`, `sensor_stream.py`
- Birleştirme ve işleme: `sensor_fusion.py`, `processor.py`

OpenCV kamera kaynağı integer indeks, cihaz yolu veya RTSP/HTTP URL'si olabilir. Headless/test ortamlarında fallback kullanılabilir.

### 4. Algılama, risk ve rapor

- `vision.py`: örnek risk sınıflandırma sezgiseli.
- `risk_map.py`: x/y hücre girdilerinden sayısal grid ve ASCII çıktı üretir; GPS koordinatlarını projeksiyonla haritaya dönüştürmez.
- `reporting.py`: normalleştirilmiş misyon raporunu JSON ve metin olarak kaydeder.

### 5. Runtime ve dashboard

- `field_runtime.py`: örnek saha akışında misyon, kamera, navigasyon ve kontrol katmanlarını koordine eder.
- `dashboard.py`: dashboard HTML'ini üretir ve HTML'e eklenen kullanıcı verilerini escape eder.
- `web_dashboard.py`: standart kütüphane HTTP sunucusu üzerinden `/`, `/api/status` ve `/stream.mjpg` sağlar.

MJPEG istemcileri tek bir paylaşılan kamera yakalama thread'inden kare alır. Kamera kaynak URL'sindeki kullanıcı bilgileri ve query parametreleri API'de gösterilmez. Kamera açılmazsa fallback açıkken placeholder JPEG yayınlanır.

## Temel akış

1. İstek eylem planına çevrilir.
2. Misyon oluşturulur ve basit güvenlik sınırları kontrol edilir.
3. Demo/runtime sensör verisi alır ve füzyon/analiz yapar.
4. Risk grid'i ve JSON/metin raporu üretilir.
5. Dashboard başlangıç raporunu gösterebilir ve kamera durumunu API üzerinden yeniler.

## Çalıştırma yüzeyleri

- `python main.py`: simülasyon örneği; `artifacts/` altına rapor yazar.
- `terrain-scan-dashboard`: canlı HTTP dashboard.
- `setup.sh`: sanal ortam, requirements ve editable paket kurulumu.

## Güvenlik ve sınırlar

- Dashboard varsayılan olarak `127.0.0.1` üzerinde dinler.
- HTTP sunucusunda kimlik doğrulama/TLS yoktur. `--host 0.0.0.0` yalnızca güvenilir, erişim kontrollü ağlarda kullanılmalıdır.
- Gerçek donanım entegrasyonu ve uçuş emniyeti bu prototipte doğrulanmamıştır.
- Fallback, donanım yokluğunda demoyu devam ettirir; sentetik kare gerçek sensör verisi olarak yorumlanmamalıdır.
