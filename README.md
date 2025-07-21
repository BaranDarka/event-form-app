# Event Kayıt Formu

Bu proje, Streamlit kullanılarak oluşturulmuş bir etkinlik kayıt formudur ve verileri Google Firebase Firestore veritabanına kaydeder.

## Özellikler
- Katılımcı bilgilerini toplar
- Misafir/çocuk ekleme desteği
- Firestore'a kayıt

## Kurulum

1. **Depoyu klonlayın:**
   ```bash
   git clone <repo-url>
   cd <repo-klasörü>
   ```

2. **Gerekli paketleri yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Firebase Ayarları:**
   - [Firebase Console](https://console.firebase.google.com/) üzerinden bir proje oluşturun.
   - Hizmet hesabı anahtarınızı (serviceAccountKey.json) indirin.
   - Bu anahtarın içeriğini `secrets.toml` veya Streamlit Cloud'da `st.secrets` olarak ekleyin.

   Örnek `secrets.toml`:
   ```toml
   type = "service_account"
   project_id = "..."
   private_key_id = "..."
   private_key = "..."
   client_email = "..."
   client_id = "..."
   auth_uri = "..."
   token_uri = "..."
   auth_provider_x509_cert_url = "..."
   client_x509_cert_url = "..."
   universe_domain = "..."
   ```

4. **Uygulamayı başlatın:**
   ```bash
   streamlit run form.py
   ```

## Kullanım
- Zorunlu alanları doldurun.
- Misafir eklemek için ilgili alanı kullanın.
- "Kaydı Tamamla" butonuna tıklayın.

## Notlar
- Firestore erişimi için doğru yetkilere sahip bir servis hesabı anahtarı gereklidir.
- Telefon numarası formatı: Başında ülke kodu olmadan 10 haneli (örn: 5XX XXX XX XX). 