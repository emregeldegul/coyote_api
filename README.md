# Coyote: Basit Pano Uygulaması
Coyote, basit bir task yönetim uygulamasıdır. Yakın süreçte Jiraya rakip olması beklenmektedir.
Geliştiricisi ile irtibata geçmek için lütfen aşağıdaki bilgileri kullanın.

```text
Core Developer: Yunus Emre Geldegül
E-Mail: yunusemregeldegul@gmail.com
Phone: +90 (541) 661 56 29
```


## Proje Gereksinimleri
Proje, sağlıklı bir şekilde işlevini yerine getirebilmesi için aşağıdaki gereksinimlere ihtyiaç duyar.

- Python 3.8.9
- PostgreSQL 14
- Fastapi 0.85.0

## Proje Ayarları ve Kurulum
Proje içerisindeki bütün ayarlar (Veri tabanı ayarları, proje ismi vs.) 3 şekilde düzenlenebilir.

* Hard-Code: Proje dizinindeki ``settings.py`` dosyası içerisindeki değerler değiştirilebilir.
* ``.env`` dosyası içerisine key-value (`AYAR_ADI = AYAR_DEGERI`) eklenebilir. -> ÖNERİLEN.
* System Environment Variables içerisinde eklenebilir.

Veri tabanı ve mail sunucusu gibi önemli ayarlar girildikten sonra proje kurulumu yapılabilir.
Sanal ortam kurulumu yapıldıktan sontan `requirements.txt` dosyası içerisindeki bağımlıklar yüklenmelidir.
Daha sonra migrationlar çalıştırılarak veri tabanı geçişleri sağlanmalıdır.

```bash
~$ python3.8 -m virtualenv venv && source venv/bin/activate
~$ pip install -r requirements.txt
~$ alembic upgrade head
```

### Projeyi ayağa kaldırmak
Proje, sanal ortam aktifken terminal üzerinden aşağıdaki komut ile ayağa kaldırılır.

`~$ uvicorn app:app --reload --port 8000 --host 0.0.0.0`

Yada istenirse `run.py` dosyası da çalıştırılabilir. Ayrıca sunucuda çalıştırmak için `run.py` içerisindeki `app` nesnesi işaret edilebilir.

## Proje Düzeni
Her geliştirmeden sonra, commit atmadan hemen önce kod kalite ve test için pre-commit scripti çalıştırılmalıdır. Böylece kodlar PEP8 standartları ile uyumlu olarak projeye dahil olur.

`~$ pre-commit run --all-files`
## Proje Yapısı

## Veri Tabanı (Model) Yapısı
Genel olarak `app/models/base.py` içerisinde ki base model kullanılabilir. 
`BaseModel`; `id`, `created_at`, `updated_at` gibi alanları içerisinde bulundurur.