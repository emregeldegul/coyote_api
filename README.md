# Coyote: Basit Pano Uygulaması
Coyote, basit bir task yönetim uygulamasıdır. Yakın süreçte Jiraya rakip olması beklenmektedir.
Geliştiricisi ile irtibata geçmek için lütfen aşağıdaki bilgileri kullanabilirsiniz.

```text
Core Developer: Yunus Emre Geldegül
E-Mail: yunusemregeldegul@gmail.com
Phone: +90 (541) 661 56 29
```

## Proje Gereksinimleri
Proje, sağlıklı bir şekilde işlevini yerine getirebilmesi için aşağıdaki gereksinimlere ihtiyaç duyar.

- Python 3.8.9
- PostgreSQL 14
- Fastapi 0.85.0
- Redis 7.0.5

## Proje Ayarları ve Kurulum
Proje içerisindeki bütün ayarlar (Veri tabanı ayarları, proje ismi vs.) 3 şekilde düzenlenebilir.

* Hard-Code: Proje dizinindeki ``settings.py`` dosyası içerisindeki değerler değiştirilebilir.
* ``.env`` dosyası içerisine key-value (`AYAR_ADI = AYAR_DEGERI`) eklenebilir. -> ÖNERİLEN.
* System Environment Variables içerisinde eklenebilir.

Veri tabanı ve mail sunucusu gibi önemli ayarlar girildikten sonra proje kurulumu yapılabilir.
Sanal ortam kurulumu yapıldıktan sontan `requirements.txt` dosyası içerisindeki bağımlıklar yüklenmelidir.
Daha sonra migrationlar çalıştırılarak veri tabanı geçişleri sağlanmalıdır.

Örnek `.env`dosyası içeriği.

```
SECRET_KEY = "KabustaRuyadaAyniIkisideGeciyorOmurgibiVakitGibi"
DEVELOPER_MODE = False

POSTGRESQL_USER_NAME = "postgres"
POSTGRESQL_USER_PASSWORD = "coyote"

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0" 

MAIL_USERNAME = "user@mail.com"
MAIL_PASSWORD = "VeriySekrıtSifre"

```

Eğer Veritabanı sunucusu, redis vb. sistemler açıkcsa proje çalıştırılabilir.

```bash
~$ python3.8 -m virtualenv venv && source venv/bin/activate
~$ pip install -r requirements.txt
~$ alembic upgrade head
```

### Projeyi ayağa kaldırmak
Proje, sanal ortam aktifken terminal üzerinden aşağıdaki komut ile ayağa kaldırılır.

`~$ uvicorn app:app --reload --port 8000 --host 0.0.0.0`

Yada istenirse `run.py` dosyası da çalıştırılabilir. Ayrıca sunucuda çalıştırmak için `run.py` içerisindeki `app` nesnesi işaret edilebilir.

Proje dizininde iken Celery worker çalıştırılmalıdır.

```bash
~$ celery -A app.worker.celery_app worker
```

## Proje Düzeni
Her geliştirmeden sonra, commit atmadan hemen önce kod kalite ve test için pre-commit scripti çalıştırılmalıdır. Böylece kodlar PEP8 standartları ile uyumlu olarak projeye dahil olur.

`~$ pre-commit run --all-files`

## Developer Modu
Proje geliştirme & test aşamasında iken daha rahat çalışılabilmesi için developer mod aktif hale getirilebilir.
Proje ayarlarına `DEVELOPER_MODE=True` girilerek mod aktifleştirilebilir.
Mod aktifleştirildikten sonra SMS, Email gibi servisler çalışmayacaktır. Doğrulama kodu kodlar (ayarlardan değiştirilmediği sürece) "123456" varsayılan kodunu kabul edecektir.

## Veri Tabanı (Model) Yapısı
Genel olarak `app/models/base.py` içerisinde ki base model kullanılabilir. 
`BaseModel`; `id`, `created_at`, `updated_at` gibi alanları içerisinde bulundurur.