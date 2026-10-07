# Arazi Tarama Prototipi

Kamera ve sensör tabanlı arazi taraması için drone/robot uyumlu, modüler bir Python prototipi. Örnek akış görev planı ve güvenlik kontrolü üretir; kamera, GPS/IMU ve LiDAR benzeri girdileri işler; risk özeti ve rapor oluşturur.

## Mevcut özellikler

- Doğal dil görevinden basit plan ve drone/robot komutları üretme
- Misyon yüksekliği ve güvenlik marjı için güvenlik kontrolleri
- Simülasyon/fallback kamera, GPS/IMU, LiDAR, füzyon ve telemetri katmanları
- x/y hücre koordinatlarından sayısal risk grid'i ve ASCII görünüm üretme
- JSON ve metin misyon raporlarını `artifacts/` altına kaydetme
- USB/OpenCV ve RTSP/HTTP kamera kaynağı için MJPEG web dashboard
- Dashboard HTML sayfası, `/api/status` JSON endpoint'i ve `/stream.mjpg` görüntü akışı
- Kamera erişilemiyorsa varsayılan placeholder/fallback akışı

Gerçek PX4/MAVLink, ROS2 ve sensör modülleri entegrasyon iskeletleri/adaptörleridir; bu prototip gerçek araçta otonom uçuş veya saha güvenliğini doğrulamaz.

## Kurulum

Python 3.10+ ve pip gerekir. Kurulum betiği sanal ortamı oluşturur, gereksinimleri yükler ve projeyi editable modda kurar:

```bash
./setup.sh
. .venv/bin/activate
```

## Hızlı başlatma

Örnek simülasyon akışı:

```bash
python main.py
```

Bu komut terminale misyon, telemetri ve risk özeti yazar; JSON ve metin raporlarını `artifacts/mission_report.json` ve `artifacts/mission_summary.txt` dosyalarına kaydeder.

## Canlı web dashboard

Varsayılan kamera indeksi `0` ile localhost dashboard'u başlatın:

```bash
terrain-scan-dashboard
```

Kamera kaynağı, yayın hızı ve örnek misyon raporu seçilebilir:

```bash
terrain-scan-dashboard --camera 1
terrain-scan-dashboard --camera /dev/video0 --fps 8
terrain-scan-dashboard --camera 'rtsp://user:password@camera-host/stream'
terrain-scan-dashboard --camera /dev/video0 --report artifacts/mission_report.json
```

Varsayılan adresler:

- Dashboard: `http://127.0.0.1:8000/`
- Kamera akışı: `http://127.0.0.1:8000/stream.mjpg`
- Durum API'si: `http://127.0.0.1:8000/api/status`

Kamera açılamazsa sunucu varsayılan olarak bir placeholder görüntüsü yayınlar ve API'de `fallback` durumunu bildirir. Fallback'i kapatmak için `--no-camera-fallback` kullanın. Sunucu varsayılan olarak yalnızca `127.0.0.1` üzerinde dinler. `--host 0.0.0.0` ile ağ arayüzlerine açılabilir; ancak kimlik doğrulama veya TLS sunucuya dahil değildir. Bunu yalnızca güvenilir ağda, uygun erişim denetimi/ters proxy arkasında kullanın. Kamera URL'sindeki kullanıcı adı, parola ve query parametreleri status API yanıtında maskelenir.

## Risk haritası kullanımı

Risk haritası şu anda coğrafi/GPS haritası değil, x/y hücre koordinatlı bir grid'dir:

```python
from terrain_scan_agent.risk_map import build_risk_map, render_risk_map

risk_map = build_risk_map(
    [
        {"x": 1, "y": 1, "risk": "high", "label": "obstacle"},
        {"x": 3, "y": 2, "risk": "medium", "label": "anomaly"},
    ],
    width=6,
    height=6,
)
print(risk_map["summary"])
print(render_risk_map(risk_map))
```

## Testler

Sanal ortam etkin durumdayken tüm testleri çalıştırın:

```bash
python -m pytest -q
```

Son doğrulama: **38 test geçti**. Fiziksel USB/RTSP kamera veya uçuş donanımı bu test ortamında doğrulanmış değildir.

## Proje rehberi

- [Mimari](docs/ARCHITECTURE.md)
- [Uygulama bağlama ve çalıştırma](docs/UYGULAMA_BAGLAMA.md)
- [Kendi sunucunda barındırma](docs/SELF_HOSTING_GUIDE.md)
- [Veri kaydetme](docs/DATA_SAVING_GUIDE.md)
- [Değişiklik günlüğü](docs/CHANGELOG.md)
- [İlerleme durumu](progress.md)

## Güvenlik notu

Bu yazılım prototip düzeyindedir. Gerçek drone/robot kontrolünden önce bağımsız güvenlik sistemleri, saha prosedürleri, kalibrasyon ve yetkili testler gerekir. Bu depo tek başına uçuşa elverişlilik veya operasyonel güvenlik sağlamaz.
