# 🚀 Hangisini Seçersin? (Would You Rather?)

Topluluğun tarafını seçtiği, interaktif ve modern neon temalı (Z-Kuşağı odaklı) web uygulaması.

---

## 🎨 Tasarım ve Özellikler

* **Odak Modu (Tinder / Reels Stili):** Ekranda tek bir büyük ikilem kartı gelir. Oy verildiğinde akıcı CSS animasyonlarıyla yüzdeler açılır ve *"Sıradaki İkilem 👉"* butonu ile sıradaki soruya geçilir.
* **Tüm İkilemler Akışı (Feed):** Tüm ikilemlerin alt alta kartlar halinde listelendiği, sayfalama (pagination) destekli keşif akışı.
* **Asenkron Oylama (Vanilla JS / Fetch API):** Sayfa yenilenmeden tek tıkla oy verme, anlık oy ve yüzde hesaplama.
* **Güvenilir Oy Takibi:** Hem misafirler (oturum ve localStorage) hem de kayıtlı kullanıcılar için mükerrer oy koruması.
* **Kullanıcı Sistemi & İkilem Yaratma:**
  * Soru sormak için giriş yapmak zorunludur.
  * Oy vermeyi hem misafirler hem de kayıtlı kullanıcılar yapabilir.
  * **Gizlilik:** Soranların ve oy verenlerin yalnızca `@kullaniciadi` bilgisi gösterilir, e-posta adresleri kesinlikle gizli tutulur ve arayüzde yer almaz.
* **Profil Sayfası:** Kullanıcının sorduğu ikilemleri (ve silme yetkisini) ve daha önce oyladığı seçenekleri görebildiği kişisel panel.

---

## 🛠️ Teknik Altyapı

* **Backend:** Python 3.14, Django 6.1
* **Veritabanı:** Supabase (PostgreSQL - `psycopg` v3 & IPv4 Session Pooler)
* **Frontend:** Modern CSS3 Neon Glow UI, Vanilla JS (Fetch API), Google Fonts Poppins
* **Güvenlik & Yapılandırma:** `.env` (`python-dotenv`, `dj-database-url`)

---

## 🚀 Projeyi Çalıştırma

### 1. Sanal Ortamı Aktif Edin (Gerekirse):
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Geliştirme Sunucusunu Başlatın:
```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Tarayıcınızda şu adrese gidin:
👉 **http://127.0.0.1:8000/**

---

## 🔑 Varsayılan Yönetici (Admin) Hesabı:
* **Kullanıcı Adı:** `murat`
* **Şifre:** `1903`
* **Admin Paneli:** http://127.0.0.1:8000/admin/

---

## 🧪 Testleri Çalıştırma:
```powershell
.\.venv\Scripts\python.exe manage.py test questions --keepdb
```
*(Tüm testler yeşil ve hatasız geçmektedir).*
