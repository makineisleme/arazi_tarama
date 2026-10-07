# Uygulama Bağlama Rehberi

## Amaç

Bu rehber, projenin nasıl çalıştırılacağını ve hangi katmanların bağlandığını kısa ve pratik şekilde anlatır.

## Gereksinimler

- Python 3.10+
- pip
- çalışma alanı klasörü
- opsiyonel: OpenCV için gerçek kamera desteği

## Kurulum

```bash
cd /workspaces/arazi_tarama
./setup.sh
```

## Çalıştırma

```bash
cd /workspaces/arazi_tarama
./run.sh
```

Alternatif olarak:

```bash
cd /workspaces/arazi_tarama
PYTHONPATH=/workspaces/arazi_tarama python main.py
```

## Katman bağlama

### 1. Kamera
- `RealCameraReader` gerçek kamera desteği sağlar.
- eğer kamera erişilemezse `fallback` moduyla çalışır.

### 2. GPS + IMU
- `GPSIMUDriver` sensör verisini simülasyon veya gerçek sürücüden okur.
- `NavigationFusion` bu veriyi net navigasyon durumu haline getirir.

### 3. LiDAR
- `LidarCapture` sensör akışını okur ve engel tespiti yapar.

### 4. Kontrol
- `Controller` temel komut akışını yönetir.
- `PX4Controller` güvenli uçuş komutlarını hazırlar.

### 5. Dashboard
- `build_dashboard_html` rapor çıktısını HTML olarak oluşturur.

## Sorun giderme

### Import hatası
```bash
export PYTHONPATH=/workspaces/arazi_tarama
```

### Test çalışmıyorsa
```bash
PYTHONPATH=/workspaces/arazi_tarama /usr/local/py-utils/venvs/pytest/bin/python -m pytest -q tests/test_action_planner.py
```

## Sonraki adım

Gerçek saha testlerine geçmeden önce simülasyon modülü güvenli ve doğrulanmış çalışmalıdır.
