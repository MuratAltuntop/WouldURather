# 🚀 Proje Planı: Hangisini Seçersin? (Would You Rather?)

## 🎯 1. Proje Özeti ve Vizyon
Bu proje, kullanıcıların "Görünmez olmak mı, uçabilmek mi?" gibi zorlu veya eğlenceli ikilemler yarattığı, topluluğun ise bu ikilemlerde tarafını seçtiği interaktif bir web uygulamasıdır. 
*   **Hedef Kitle:** Gençler, üniversite öğrencileri ve eğlenceli vakit geçirmek isteyen herkes.
*   **Ana Odak:** Hızlı etkileşim, anonim oylama kolaylığı ve görsel tatmin.

---

## 🎨 2. Tasarım Dili ve Tema (Genç & Canlı Konsept)
Projenin sıkıcı bir anket sitesi gibi görünmemesi için modern, "Genç işi" (Z kuşağına hitap eden) bir UI/UX benimsenecektir.

*   **Renk Paleti:**
    *   **Arka Plan:** Koyu tema (Dark Mode) varsayılan olacak. Koyu lacivert veya mat siyah (`#121212`).
    *   **A Seçeneği:** Neon / Elektrik Mavisi (`#00f2fe`).
    *   **B Seçeneği:** Canlı Pembe / Macenta (`#fe0979`).
    *   *(Bu zıt renkler, "Tarafını Seç" hissiyatını güçlendirecek).*
*   **Tipografi:** Kalın, okunabilir ve modern fontlar (Google Fonts'tan **Poppins** veya **Montserrat**).
*   **Arayüz Elemanları:** 
    *   Keskin köşeler yerine yuvarlatılmış hatlar (border-radius).
    *   Oylama yapıldığında yüzdelerin dolmasını gösteren akıcı ve renkli CSS animasyonları (Progress bar).
    *   Kart (Card) tasarımlarında hafif neon gölgelendirmeler (box-shadow).

---

## 🛠 3. Teknik Mimari (Tech Stack)
*   **Backend:** Python 3.x, Django 5.x
*   **Veritabanı:** Supabase (PostgreSQL) - `psycopg2-binary` ve `dj-database-url` ile bağlanacak.
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS - Asenkron işlemler için `Fetch API` kullanılacak).
*   **Güvenlik & Ortam:** Hassas veriler `.env` dosyasında `python-dotenv` ile saklanacak.

---

## 🏗 4. Veritabanı Şeması (Database Schema)

### Tablo 1: `auth_user` (Django'nun kendi User modeli)
*   `id` (PK), `username`, `email`, `password`

### Tablo 2: `Question` (İkilemler)
*   `id`: Primary Key (UUID veya AutoField)
*   `title`: Varchar (Maksimum 255 karakter) - Sorunun kendisi.
*   `author`: ForeignKey -> `auth_user` (Soruyu kim sordu?)
*   `created_at`: DateTime (Otomatik oluşturulma tarihi)
*   `is_active`: Boolean (Default: True - Şikayet edilirse gizlemek için)

### Tablo 3: `Choice` (Seçenekler)
*   `id`: Primary Key
*   `question`: ForeignKey -> `Question` (Hangi soruya ait?)
*   `choice_text`: Varchar (Maksimum 100 karakter) - "Görünmez olmak"
*   `votes`: Integer (Default: 0) - Oy sayısı.

---

## 🚀 5. Geliştirme Fazları (Adım Adım Yol Haritası)

### 🟢 FAZ 1: Temel İskelet ve MVP (Minimum Viable Product)
*Buradaki amaç, uygulamanın çalışır halini en hızlı şekilde görmektir. Tasarım bu aşamada çok sade tutulabilir.*

1.  **Kurulumlar:** Django projesinin başlatılması, `.env` dosyasının oluşturulması ve Supabase veritabanı bağlantısının yapılması.
2.  **Modellerin Yazılması:** `Question` ve `Choice` modellerinin `models.py` içine yazılıp, `makemigrations` ve `migrate` komutlarıyla veritabanına aktarılması.
3.  **Admin Paneli:** Django Admin paneline modellerin kaydedilmesi (böylece ilk soruları admin panelinden elle ekleyebiliriz).
4.  **Ana Sayfa (Feed) View & Template:** Veritabanındaki tüm soruların ve seçeneklerinin listelendiği ana sayfanın (`index.html`) oluşturulması.
5.  **Oy Verme İşlemi (Backend):** Kullanıcı bir seçeneğe tıkladığında çalışan, o seçeneğin `votes` değerini 1 artıran ve sayfayı yenileyen temel fonksiyonun yazılması.

### 🟡 FAZ 2: Canlı Tasarım ve Dinamik Yapı (JavaScript & CSS Odaklı)
*Projenin canlandığı, "Genç işi" temanın ve asenkron (sayfa yenilenmeden) işlemlerin eklendiği aşama.*

1.  **CSS Giydirmesi:** Dark mode, neon butonlar ve Poppins fontunun entegrasyonu.
2.  **Asenkron Oylama (Fetch API):** Butona tıklandığında sayfanın yenilenmemesi; JS ile arka planda Django'ya istek atılıp oy sayısının artırılması.
3.  **Animasyonlu Sonuçlar:** Oy verildikten hemen sonra butonların kaybolup, yerine A ve B seçeneklerinin yüzde (%) oranlarını gösteren, soldan sağa doğru animasyonla dolan renkli çubukların (progress bar) gelmesi.
4.  **Mükerrer Oy Engelleme:** Kullanıcının tarayıcısına çerez (Cookie) veya `localStorage` ile hangi sorulara oy verdiğinin kaydedilmesi (üye olmasa bile aynı soruya iki kez oy vermesini engellemek için).

### 🟠 FAZ 3: Kullanıcı Sistemi ve Soru Oluşturma (İleri Seviye)
*Artık kullanıcıların sisteme dahil olduğu aşama.*

1.  **Auth Sistemi:** Django'nun yerleşik auth sistemi ile Kayıt Ol (Register), Giriş Yap (Login) ve Çıkış Yap (Logout) sayfalarının canlı temaya uygun tasarlanması.
2.  **Soru Oluşturma Formu:** Sadece giriş yapmış kullanıcıların görebileceği, soru metni ve 2 seçenek ekleyebildikleri "Yeni İkilem Yarat" sayfasının yapılması.
3.  **Profil Sayfası:** Kullanıcının kendi oluşturduğu soruları görebilmesi ve silebilir olması.

---

## 🗺 6. URL Yapısı (Gelecek Referansı)
*   `/` -> Ana Sayfa (Tüm ikilemler)
*   `/vote/<int:choice_id>/` -> Oy verme işlemini işleyen arka plan URL'i.
*   `/create/` -> Yeni soru oluşturma sayfası (Login required)
*   `/login/`, `/register/`, `/logout/` -> Kullanıcı işlemleri