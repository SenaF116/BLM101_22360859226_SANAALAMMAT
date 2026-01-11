# RLE (Run-Length Encoding) Sıkıştırıcı

## Proje Hakkında

Bu proje, Sanaa Lammat (Öğrenci Numarası: 22360859226) tarafından **Bilgisayar Mühendisliği Giriş** dersi için geliştirilmiş bir öğrenme projesidir.

Proje, farklı veri türleri için Run-Length Encoding (RLE) sıkıştırma algoritmasını uygulayan kullanıcı dostu bir arayüz sunmaktadır.
      ## Youtube linki :
      https://youtu.be/7AodeZKXHCs

## Projenin Amacı

- RLE sıkıştırma algoritmasının nasıl çalıştığını öğrenmek
- Farklı veri türleri üzerinde sıkıştırma uygulamak
- Python ve Tkinter kütüphanesi ile GUI geliştirme pratiği yapmak
- Dosya işlemleri ve veri manipülasyonu deneyimi kazanmak

## Kullanılan Teknolojiler ve Kütüphaneler

### Programlama Dili
- **Python 3.13**

### Kullanılan Kütüphaneler
- **tkinter**: Grafiksel kullanıcı arayüzü (GUI) oluşturmak için
- **PIL (Pillow)**: Görüntü işleme ve görüntü dosyalarını yönetmek için
- **numpy**: Sayısal veri işlemleri ve ses verisi manipülasyonu için
- **wave**: WAV ses dosyalarını okumak ve yazmak için
- **os**: Dosya yolu işlemleri için
- **re**: Metin işlemleri ve desen eşleştirme için

## Proje Özellikleri

### Desteklenen Veri Türleri
1. **Metin (Text)**: 
   - TXT dosyalarını okuma ve işleme
   - Metin üzerinde RLE sıkıştırma/deşifre etme

2. **Görüntü (Image)**:
   - PNG, JPG, JPEG, BMP formatlarını destekler
   - Görüntüleri gri tonlamaya çevirerek RLE uygular
   - Görüntü önizleme özelliği

3. **Ses (Audio)**:
   - WAV formatını destekler
   - Ses verisi üzerinde RLE sıkıştırma/deşifre etme

### Ana Fonksiyonlar

#### RLE Sıkıştırma (Encode)
```python
def encode_text(self):
    # Metin verisi için RLE sıkıştırması
    # Örnek: "AAAAABBBCCDAA" → "5A3B2C1D2A"
```

#### RLE Deşifre Etme (Decode)
```python
def decode_text(self):
    # RLE formatındaki veriyi orijinal metine çevirme
    # Örnek: "5A3B2C1D2A" → "AAAAABBBCCDAA"
```

#### Görüntü İşleme
```python
def encode_image(self):
    # Görüntüyü piksel piksel işler
    # Gri tonlamaya çevirir ve RLE uygular
```

#### Ses İşleme
```python
def encode_audio(self):
    # WAV dosyasını okur
    # Ses örnekleri üzerinde RLE uygular
```

### Arayüz Özellikleri
- **Modern ve Kullanıcı Dostu Arayüz**: Kolay kullanım için tasarlanmış
- **Renkli Butonlar**: Görsel geri bildirim için
- **Durum Çubuğu**: İşlem sonuçlarını gösterir
- **Dosya Yükleme**: Kolay dosya seçimi
- **Çıktı Kaydetme**: Sonuçları kaydetme imkanı

## Nasıl Kullanılır?

1. **Veri Türü Seçimi**: Metin, Görüntü veya Ses radyo düğmelerinden birini seçin
2. **Dosya Yükle**: "Load File" butonuna tıklayarak dosyanızı seçin
3. **İşlem Yapın**: 
   - "Encode" butonu ile sıkıştırma
   - "Decode" butonu ile deşifre etme
4. **Sonuçları Görüntüle**: Çıktı penceresinde sonuçları ve sıkıştırma oranını görün
5. **Kaydet**: "Save Output" ile sonuçları kaydedin
6. **Temizle**: "Clear All" ile tüm alanları temizleyin

## RLE Algoritması Nedir?

Run-Length Encoding (RLE), veri sıkıştırma için basit ancak etkili bir algoritmadır:

- **Temel Fikir**: Aynı değere sahip ardışık elemanları sayarak sıkıştırma yapar
- **Örnek**: "AAAABBBCC" → "4A3B2C"
- **Avantajları**: Basit implementasyon, hızlı çalışma
- **Dezavantajları**: Tekrar eden verilerde etkili, rastgele verilerde genişleme yapabilir

## Sıkıştırma Oranı Hesaplama

```python
ratio = (1 - (compressed_size / original_size)) * 100
```

Bu formül, orijinal veri boyutuna göre ne kadar yer tasarrufu yapıldığını gösterir.

## Proje Yapısı

```
rle_compressor.py     # Ana program dosyası
requirements.txt      # Gerekli kütüphaneler
README.md           # Proje dokümantasyonu
```

## Sistem Gereksinimleri

- Python 3.13 veya üzeri
- Gerekli kütüphaneler:
  - numpy
  - Pillow (PIL)

## Kurulum

```bash
pip install numpy Pillow
python rle_compressor.py
```


## Gelecek Geliştirmeler

- Daha fazla sıkıştırma algoritması ekleme (Huffman, LZW)
- Toplu dosya işleme
- Daha fazla görüntü formatı desteği
- Sıkıştırma karşılaştırma araçları
- Web arayüzü geliştirme
  **Not**: Bu proje sadece eğitim amaçlıdır ve öğrenme sürecini desteklemek için geliştirilmiştir.



---

**Not**: Bu proje sadece eğitim amaçlıdır ve öğrenme sürecini desteklemek için geliştirilmiştir.
