# Arazi Tarama Prototipi

Bu proje, kamera ve sensör tabanlı arazi tarama için modüler bir örnek mimari sunar. Kullanıcıdan gelen doğal dil komutunu alan, güvenlik kontrolü yapan, senaryoyu planlayan ve ardından drone/robot için uyumlu eylem komutlarını üreten bir akış kurar.

## Özellikler

- Doğal dil ile görev anlama
- Güvenlik kontrollü misyon oluşturma
- Drone / robot uyumlu komut üretimi
- Canlı kamera ve fallback kamera akışı
- LiDAR, GPS ve IMU verilerini birleştirme
- ROS2 ve MAVLink benzeri köprü katmanları
- PX4 benzeri güvenli uçuş komut katmanı
- Saha çalışma akışı: canlı tarama + raporlama
- gerçek kamera / GPS-IMU / mini dashboard entegre katmanları
- gerçek cihaz benzeri veri akışı için fallback ve simülasyon desteği

## Mevcut mimari

- terrain_scan_agent/planner.py: görev planı üretimi
- terrain_scan_agent/mission.py: güvenlikli görev ve misyon oluşturma
- terrain_scan_agent/control.py: temel kontrol akışı
- terrain_scan_agent/sensors.py: sensör kayıt ve yönetimi
- terrain_scan_agent/live_camera.py: canlı kamera ve fallback desteği
- terrain_scan_agent/lidar_capture.py: LiDAR tarama
- terrain_scan_agent/navigation_fusion.py: GPS + IMU füzyonu
- terrain_scan_agent/ros_bridge.py: ROS benzeri yayın katmanı
- terrain_scan_agent/mavlink_adapter.py: MAVLink benzeri komut adaptörü
- terrain_scan_agent/ros_mavlink_bridge.py: ROS2/MAVLink köprü katmanı
- terrain_scan_agent/px4_controller.py: güvenli PX4 benzeri uçuş kontrol katmanı
- terrain_scan_agent/field_runtime.py: canlı saha tarama akışı
- terrain_scan_agent/real_camera.py: gerçek kamera okuyucu ve fallback
- terrain_scan_agent/gps_imu_driver.py: GPS + IMU veri sürücüsü
- terrain_scan_agent/dashboard.py: mini dashboard HTML arayüzü
- main.py: örnek tamamlanmış çalışma akışı

## Hızlı başlatma

```bash
cd /workspaces/arazi_tarama
PYTHONPATH=/workspaces/arazi_tarama python main.py
```

## Örnek görev

```python
from terrain_scan_agent.planner import build_action_plan, generate_vehicle_commands

plan = build_action_plan("Bu arazide tarama yap ve riskli alanları bul")
commands = generate_vehicle_commands(plan, vehicle="drone")
print(plan)
print(commands)
```

## Test ve doğrulama

Proje için temel regresyon testi hazırdır:

```bash
cd /workspaces/arazi_tarama
PYTHONPATH=/workspaces/arazi_tarama /usr/local/py-utils/venvs/pytest/bin/python -m pytest -q tests/test_action_planner.py
```

Son doğrulama sonucu:
- 25 passed in 0.03s

## Geliştirme hedefi

Bu prototip, gerçek dünya entegrasyonu için temel iskelet ve güvenli operasyon modeli sunar. Mevcut sürüm, simülasyon ve gerçek cihaz benzeri akışlar için hazır bir temel sağlamaktadır; bir sonraki adım gerçek kamera, GPS/IMU ve PX4/MAVLink canlı akışı ile saha testlerine geçmektir.

## Not

Bu örnek, üretim güvenlik katmanlarıyla birlikte çalışan bir prototype seviyesindedir. Gerçek drone/robot kontrolü için saha koşulları, kalibrasyon, bakım ve güvenlik politikaları eklenmelidir.
