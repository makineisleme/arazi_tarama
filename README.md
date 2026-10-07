# Arazi Tarama Prototipi

Bu proje, kamera ve sensör tabanlı arazi tarama için yerleşik/embedded yapay zeka mantığına sahip küçük bir örnek mimari sunar. Amaç, kullanıcıdan gelen doğal dil komutunu alan ve ardından drone/robot için uyumlu eylem komutları üreten bir akış kurmaktır.

## Özellikler

- Doğal dil ile görev anlama
- Tarama planı üretimi
- Drone / robot uyumlu komut dönüşümü
- Yerel işleme için modüler proje yapısı
- Genişletilebilir sensör ve kontrol katmanı

## Proje yapısı

- `terrain_scan_agent/planner.py`: görevden eylem planı çıkarma
- `terrain_scan_agent/compat.py`: aracın kontrol arayüzleri
- `terrain_scan_agent/config.py`: varsayılan sensör ve araç yapılandırması
- `main.py`: örnek yürütme noktası

## Hızlı başlatma

```bash
python main.py
```

## Örnek görev

```python
from terrain_scan_agent.planner import build_action_plan, generate_vehicle_commands

plan = build_action_plan("Bu arazide tarama yap ve riskli alanları bul")
commands = generate_vehicle_commands(plan, vehicle="drone")
print(plan)
print(commands)
```

## Geliştirme hedefi

Bu prototip, gerçek sistem için temel iskelet görevi görür. Geliştirme ilerledikçe şunlar eklenebilir:

- kamera görüntüsü işleme
- LiDAR + IMU + GPS senkronizasyonu
- yerel LLM veya edge model entegrasyonu
- ROS2 veya MAVLink kontrol katmanı
- web arayüzü ve raporlama

## Not

Bu örnek, işlevsel bir temel prototiptir; gerçek drone/robot kontrolü için üretim ortamında güvenlik, kalibrasyon ve sistem kontrol katmanı eklenmelidir.
