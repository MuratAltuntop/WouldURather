# ⚡ Hangisini Seçersin? (Would You Rather?)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-000000?style=for-the-badge&logo=vercel&logoColor=white)
![Status](https://img.shields.io/badge/Tür-Eğitim%20&%20Deneme%20Projesi-FF6B6B?style=for-the-badge)

<br/>

**Topluluğun tarafını seçtiği, Z-Kuşağı odaklı modern neon karanlık temalı interaktif ikilem web uygulaması.**

🌐 **Canlı Proje (Vercel):** [https://vercel.com/murat2402/woulduratherr](https://vercel.com/murat2402/woulduratherr)

</div>

---

> [!NOTE]
> **📚 Eğitim ve Deneme Projesi Notu:**  
> Bu proje; modern full-stack web mimarisini, Django ile bulut tabanlı **Supabase (PostgreSQL)** entegrasyonunu, **Vercel Serverless** dağıtımını ve asenkron JavaScript dinamiklerini deneyimlemek amacıyla geliştirilmiş **eğitim ve portföy amaçlı bir deneme çalışmasıdır**.

---

## ✨ Öne Çıkan Özellikler

* 🎯 **Odak Modu (Tinder / Reels Formatı):**  
  Ana sayfada kullanıcıyı tek bir büyük ikilem kartı karşılar. Kullanıcı tarafını seçtiğinde sayfa yenilenmeden neon efektli yüzde çubukları (`progress-bar`) animasyonla dolar ve hemen altında *"Sıradaki İkilem 👉"* butonu belirir.
* 🔥 **Tüm İkilemler Akışı (Feed):**  
  Topluluğun sorduğu tüm zorlu ikilemlerin alt alta listelendiği, sayfalama (pagination) destekli keşif akışı.
* ⚡ **Asenkron Oylama (Vanilla JS / Fetch API):**  
  Sayfa yenilenmesine gerek kalmadan anlık olarak oy sayısını ve oranları güncelleyen dinamik yapı.
* 🔒 **Gizlilik Odaklı Kullanıcı Deneyimi:**  
  * Soru soranların ve tarafını seçenlerin yalnızca **`@kullaniciadi`** bilgisi gösterilir.  
  * Kullanıcıların **e-posta adresleri hiçbir sayfada veya API yanıtında kesinlikle yer almaz**.
* ✍️ **Kullanıcı Sistemi & İkilem Yaratma:**  
  Giriş yapmış üyeler diledikleri gibi yeni ikilemler yayınlayabilir, kendi sorularını silebilir veya diğer sorulara verdikleri oyları profillerinden takip edebilir.
* 🛡️ **Mükerrer Oy Engelleme:**  
  Hem kayıtlı kullanıcılar (veritabanı kısıtlaması) hem de misafirler (oturum anahtarı ve localStorage) için adil oylama mekanizması.

---

## 🎨 Tasarım Dili (Neon Dark Theme)

* **Arka Plan:** Koyu Tema (Dark Mode - `#0a0c13`)
* **A Seçeneği:** Neon / Elektrik Mavisi (`#00f2fe`)
* **B Seçeneği:** Canlı Pembe / Macenta (`#fe0979`)
* **Orta Rozet:** Neon Sarı VS (`#ffbe0b`)
* **Tipografi:** Google Fonts — **Poppins** (400, 600, 700, 800, 900)

---

## 🛠️ Teknik Mimari (Tech Stack)

| Katman | Teknoloji | Açıklama |
| :--- | :--- | :--- |
| **Backend** | Python 3.14 & Django 6.1 | REST endpoint'leri, Formlar, Kimlik Doğrulama |
| **Veritabanı** | Supabase (PostgreSQL) | Bulut veritabanı, `psycopg` (v3) ve IPv4 Session Pooler |
| **Frontend** | HTML5, CSS3, Vanilla JS | Fetch API, akıcı CSS animasyonları, duyarlı (responsive) tasarım |
| **Statik Dosyalar** | WhiteNoise | Serverless ortamda statik dosyaların hızlıca sunulması |
| **Dağıtım (Deploy)** | Vercel | Serverless WSGI mimarisi (`@vercel/python`) |

---

## 💻 Yerel Geliştirme (Local Development)

Projeyi kendi bilgisayarınızda çalıştırmak için:

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/MuratAltuntop/WouldURather.git
cd WouldURather
```

### 2. Sanal Ortamı Oluşturun ve Aktif Edin
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Çevre Değişkenlerini Tanımlayın (`.env`)
Proje kök dizininde `.env` dosyası oluşturun:
```env
SECRET_KEY=gizli-anahtariniz
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app
DATABASE_URL=postgresql://kullanici:sifre@host:port/veritabani
```

### 5. Veritabanını Güncelleyin ve Örnek Verileri Yükleyin
```bash
python manage.py migrate
python manage.py seed_data
```

### 6. Sunucuyu Başlatın
```bash
python manage.py runserver
```
Tarayıcınızda `http://127.0.0.1:8000/` adresine gidin.

---

## 🧪 Testler

Otomatik test paketini çalıştırmak için:
```bash
python manage.py test questions --keepdb
```

---

## 👨‍💻 Geliştirici
* **Murat Altuntop** — [GitHub Profili](https://github.com/MuratAltuntop)
* **Canlı Dağıtım:** [https://vercel.com/murat2402/woulduratherr](https://vercel.com/murat2402/woulduratherr)
