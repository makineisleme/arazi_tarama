# Uygulama Bağlama Rehberi

## Amaç

Kurulum, örnek akışı ve canlı dashboard'u çalıştırma adımlarını açıklar. Gerçek cihaz bağlantısı bu rehberle tek başına doğrulanmış olmaz.

## Gereksinimler

- Python 3.10+
- pip
- USB/OpenCV kamera için opsiyonel kamera donanımı veya RTSP/HTTP kamera adresi

## Kurulum

Repo kökünde:

```bash
./setup.sh
. .venv/bin/activate
```

Kurulum `requirements.txt` bağımlılıklarını yükler ve `terrain-scan-dashboard` komutunu kurmak için paketi editable olarak yükler.

## Örnek simülasyon

```bash
python main.py
```

Demo `artifacts/mission_report.json` ve `artifacts/mission_summary.txt` dosyalarını üretir.

## Canlı web dashboard

Varsayılan kamera (`0`) ile:

```bash
terrain-scan-dashboard
```

Farklı kamera kaynakları ve önceki rapor:

```bash
terrain-scan-dashboard --camera 1
terrain-scan-dashboard --camera /dev/video0 --fps 8
terrain-scan-dashboard --camera 'rtsp://user:password@camera-host/stream'
terrain-scan-dashboard --camera /dev/video0 --report artifacts/mission_report.json
```

Uygulama:

- Dashboard: `http://127.0.0.1:8000/`
- MJPEG video: `http://127.0.0.1:8000/stream.mjpg`
- JSON durum: `http://127.0.0.1:8000/api/status`

Kamera kullanılamıyorsa varsayılan fallback sentetik placeholder frame sunar. Bu durum API'de `camera.status` alanında belirtilir. Fallback olmadan çalıştırmak için `--no-camera-fallback` ekleyin. URL'deki kullanıcı bilgileri ve query parametreleri API'de maskelenir.

Varsayılan sunucu yalnızca localhost'ta dinler ve yerleşik kimlik doğrulama/TLS sağlamaz. `--host 0.0.0.0` seçeneğini yalnızca güvenilir/erişim kontrollü ağlarda kullanın.

## Katmanlar

1. **Kamera:** `LiveCameraCapture` OpenCV ile cihaz indeksi, cihaz yolu veya URL'den frame okur; fallback ayarı sentetik frame sağlar.
2. **GPS + IMU:** `GPSIMUDriver` demo/simülasyon verisi sağlar; `NavigationFusion` değerleri birleştirir. Gerçek sürücü ve canlı korelasyon ayrıca entegre edilmelidir.
3. **LiDAR ve analiz:** `LidarCapture`, risk analizi ve sensör füzyon bileşenleri örnek girdileri işler.
4. **Kontrol:** `Controller` ve PX4/MAVLink/ROS sınıfları entegrasyon katmanlarıdır; saha uçuşu için doğrulanmış değildir.
5. **Raporlama:** `reporting.py` JSON ve metin çıktıları oluşturur; `risk_map.py` x/y hücre risk grid'i üretir.
6. **Dashboard:** `web_dashboard.py` web arayüzünü, API'yi ve MJPEG akışını sunar.

## Test ve sorun giderme

Tüm testler:

```bash
python -m pytest -q
```

`terrain-scan-dashboard: command not found` alırsanız `.venv` etkin olduğundan ve `./setup.sh` tamamlandığından emin olun. OpenCV kamera açamıyorsa kamera indeksini/cihaz izinlerini kontrol edin; akış fallback modunda çalışıyorsa API'deki `camera.status` değerine bakın.
