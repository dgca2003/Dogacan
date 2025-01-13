import numpy as np           
import pandas as pd

# Boş bir DataFrame oluştur
df = pd.DataFrame(columns=["isim", "yas", "meslek", "test_turu", "test_sonucu"])

while True:
    print("\nMenü:")
    print("1. Yeni kişi ekle")
    print("2. Test türü ve sonucunu ekle/güncelle")
    print("3. Mevcut verileri göster")
    print("4. Verileri kaydet ve Teste başla")
    
    secim = input("Seçiminizi yapın (1/2/3/4): ")
    
    if secim == "1":  # Yeni kişi ekle
        isim = input("İsim girin: ")
        yas = input("Yaş girin: ")
        meslek = input("Meslek girin: ")
        
        # Yeni bir satır oluştur ve DataFrame'e ekle (test türü ve sonucu olmadan)
        yeni_veri = {"isim": isim, "yas": int(yas), "meslek": meslek, "test_turu": None, "test_sonucu": None}
        df = pd.concat([df, pd.DataFrame([yeni_veri])], ignore_index=True)
        print("\nYeni kişi eklendi!")
    
    elif secim == "2":  # Test türü ve sonucunu ekle/güncelle
        isim = input("Test türü ve sonucunu eklemek istediğiniz kişinin adını girin: ")
        
        # İsimle eşleşen satırları bul
        kisi_bilgisi = df[df["isim"].str.lower() == isim.lower()]
        
        if kisi_bilgisi.empty:
            print("\nBu isimde bir kayıt bulunamadı. Lütfen önce kişiyi ekleyin.")
        else:
            print("\nTest Türleri:")
            print("1. Öfke Yönetimi Testi")
            print("2. Odaklanma Testi")
            
            test_turu_secim = input("Test türünü seçin (1/2): ")
            if test_turu_secim == "1":
                test_turu = "Öfke Yönetimi Testi"
            elif test_turu_secim == "2":
                test_turu = "Odaklanma Testi"
            else:
                print("\nGeçersiz seçim. Test türü belirtilmedi.")
                continue
            
            test_sonucu = input("Test sonucunu girin: ")
            
            # Test tamamlandığında veri ekle/güncelle
            print(f"\n{test_turu} testi bitmiştir. Sonuç: {test_sonucu}")
            
            # Aynı kişiye ait aynı test türü var mı?
            mevcut_test = (df["isim"].str.lower() == isim.lower()) & (df["test_turu"] == test_turu)
            
            if mevcut_test.any():
                # Aynı test türü varsa sonucu güncelle
                df.loc[mevcut_test, "test_sonucu"] = test_sonucu
                print("\nTest sonucu güncellendi!")
            else:
                # Aynı test türü yoksa yeni satır olarak ekle
                yeni_test_verisi = {
                    "isim": kisi_bilgisi.iloc[0]["isim"],
                    "yas": kisi_bilgisi.iloc[0]["yas"],
                    "meslek": kisi_bilgisi.iloc[0]["meslek"],
                    "test_turu": test_turu,
                    "test_sonucu": test_sonucu
                }
                df = pd.concat([df, pd.DataFrame([yeni_test_verisi])], ignore_index=True)
                print("\nYeni test sonucu başarıyla eklendi!")

            
    
    elif secim == "3":  # Mevcut verileri göster
        if df.empty:
            print("\nHenüz veri bulunmamaktadır.")
        else:
            print("\nMevcut Veriler:")
            print(df)
    
    elif secim == "4":  # Verileri kaydet ve çık
        df.to_csv("kullanici_verileri.csv", index=False)
        print("\nVeriler 'kullanici_verileri.csv' dosyasına kaydedildi. Çıkılıyor...")
        break
    
    else:
        print("\nGeçersiz bir seçim yaptınız. Lütfen tekrar deneyin.")

# Kullanıcıdan alınan cevapların ortalama puanına göre kategori belirleme
# Kullanıcının 15 soruya verdiği cevaplar
cevaplar = [
    [1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 2],  # Düşük
    [2, 2, 3, 2, 3, 3, 2, 2, 3, 3, 3, 2, 3, 3, 3],  # orta Düşük
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],  # Orta
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],  # Orta yüksek
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]   # Yüksek
]

# Puan aralıklarına göre kategori belirleme fonksiyonu
def kategori_belirle(cevaplar):
    ortalama = np.mean(cevaplar)  # Cevapların ortalamasını al
    if 1.0 <= ortalama < 2.0:
        return "Düşük"
    elif 2.0 <= ortalama < 3.0:
        return "Orta Düşük"
    elif 3.0 <= ortalama < 3.5:
        return "Orta"
    elif 3.5 <= ortalama < 4.5:
        return "Orta Yüksek"
    elif 4.5 <= ortalama <= 5.0:
        return "Yüksek"
    else:
        return "Geçersiz"

def kullanici_cevaplari_al_sorular(sorular_ve_siklar):
    print("\nLütfen aşağıdaki soruları cevaplayın:")
    cevaplar = []

    for soru_no, (soru, siklar) in enumerate(sorular_ve_siklar.items(), start=1):
        while True:
            print(f"\nSoru {soru_no}: {soru}")
            for sik_harf, (aciklama, puan) in siklar.items():
                print(f"{sik_harf}) {aciklama}")
            
            cevap = input("Cevabınız: ").strip().lower()
            if cevap in siklar:  # Geçerli bir şık mı kontrol et
                cevaplar.append(siklar[cevap][1])  # Puanı ekle
                break
            else:
                print("Geçersiz giriş. Lütfen belirtilen şıklardan birini seçin.")
    
    return cevaplar


def test_secin():
    print("Hangi testi yapmak istediğinizi seçin:")
    print("1) Öfke Yönetimi Testi")
    print("2) Odaklanma Testi")
    
    while True:
        secim = input("Seçiminizi yapın (1 veya 2): ").strip()
        if secim in ["1", "2"]:
            return secim
        else:
            print("Geçersiz seçim. Lütfen 1 veya 2 girin.")


# Öfke Yönetimi Soruları ve Şıkları
ofke_yonetimi_sorulari = {
    "Son zamanlarda küçük şeyler yüzünden sinirlendiğinizde, sinirlenme sıklığınız nedir?": {
        "a": ("Hiç sinirlenmem", 1),
        "b": ("Nadiren sinirlenirim", 2),
        "c": ("Ara sıra sinirlenirim", 3),
        "d": ("Sıklıkla sinirlenirim", 4),
        "e": ("Sürekli sinirleniyorum", 5),
    },
    "Sinirlendiğinizde kontrolünüzü kaybetme eğiliminiz nedir?": {
        "a": ("Hiç kontrolümü kaybetmem", 1),
        "b": ("Nadir kontrolümü kaybederim", 2),
        "c": ("Bazen kontrolümü kaybedebilirim", 3),
        "d": ("Çoğu zaman kontrolümü kaybederim", 4),
        "e": ("Her zaman kontrolümü kaybederim", 5),
    },
    "Sinirliyken başkalarına nasıl tepki verirsiniz?": {
        "a": ("Asla olumsuz tepki vermem", 1),
        "b": ("Nadiren olumsuz tepki veririm", 2),
        "c": ("Bazen olumsuz tepki verebilirim", 3),
        "d": ("Çoğu zaman olumsuz tepki veririm", 4),
        "e": ("Her zaman olumsuz tepki veririm", 5),
    },
    "Sinirlendiğinizde hemen sakinleşmek için ne kadar çaba sarf ediyorsunuz?": {
        "a": ("Hemen sakinleşirim", 1),
        "b": ("Hızlıca sakinleşirim", 2),
        "c": ("Orta derecede sakinleşirim", 3),
        "d": ("Sakinleşmek için uzun zaman harcarım", 4),
        "e": ("Hiç sakinleşemem", 5),
    },
    "Sinirli olduğunuzda çevrenizle iletişiminiz nasıl olur?": {
        "a": ("Her zaman sakin ve yapıcı", 1),
        "b": ("Genellikle sakin", 2),
        "c": ("Bazen sakin", 3),
        "d": ("Çoğu zaman stresli", 4),
        "e": ("Her zaman gergin ve olumsuz", 5),
    },
    "Sinirli olduğunuzda yapmayı tercih ettiğiniz etkinlikler nelerdir?": {
        "a": ("Hiçbir şey yapmam, sakinleşirim", 1),
        "b": ("Hafif egzersizler yaparım", 2),
        "c": ("Yürüyüş yaparım", 3),
        "d": ("Fiziksel aktivitelerle öfkemden kurtulmaya çalışırım", 4),
        "e": ("Sinirlendiğimde başkalarına zarar vermeyi düşünürüm", 5),
    },
    "Öfke anında kendinizi nasıl hissedersiniz?": {
        "a": ("Hiçbir şey hissetmem", 1),
        "b": ("Hafif rahatsızlık hissederim", 2),
        "c": ("Orta derecede rahatsızlık hissederim", 3),
        "d": ("Çok rahatsız hissederim", 4),
        "e": ("Kendimi tamamen kaybederim", 5),
    },
    "Sinirlendiğinizde fiziksel belirtiler yaşar mısınız? (örneğin, kalp atışının hızlanması, ellerin titremesi)": {
        "a": ("Hiç fiziksel belirti yaşamam", 1),
        "b": ("Nadiren fiziksel belirti yaşarım", 2),
        "c": ("Bazen yaşarım", 3),
        "d": ("Çoğu zaman yaşarım", 4),
        "e": ("Her zaman yaşarım", 5),
    },
    "Sinirli olduğunuzda çevrenizdeki kişilerin ne kadar etkilenmesine yol açarsınız?": {
        "a": ("Hiçbir şekilde etkilemem", 1),
        "b": ("Az bir şekilde etkilerim", 2),
        "c": ("Orta derecede etkilerim", 3),
        "d": ("Çoğu zaman etkilerim", 4),
        "e": ("Her zaman etkilerim", 5),
    },
    "Öfkenizi başkalarına gösterdiğinizde, sonradan nasıl hissedersiniz?": {
        "a": ("Hiç pişman olmam", 5),
        "b": ("Hafif pişmanlık hissederim", 4),
        "c": ("Orta derecede pişmanlık hissederim", 3),
        "d": ("Çoğu zaman pişman olurum", 2),
        "e": ("Her zaman pişman olurum", 1),
    },
    "Bir tartışmada ne kadar süre boyunca öfkelenirsiniz?": {
        "a": ("Hiç öfkelenmem", 1),
        "b": ("Kısa süreliğine öfkelenirim", 2),
        "c": ("Orta derecede öfkelenirim", 3),
        "d": ("Uzun süre öfkelenirim", 4),
        "e": ("Sürekli öfkelenirim", 5),
    },
    "Sinirlendiğinizde bir konuda ne kadar mantıklı düşünürsünüz?": {
        "a": ("Hiç mantıklı düşünmem", 5),
        "b": ("Nadiren mantıklı düşünürüm", 4),
        "c": ("Bazen mantıklı düşünebilirim", 3),
        "d": ("Çoğu zaman mantıklı düşünürüm", 2),
        "e": ("Her zaman mantıklı düşünürüm", 1),
    },
    "Öfkenizle başa çıkarken dışarıdan yardım alır mısınız?": {
        "a": ("Asla yardıma ihtiyacım olmaz", 1),
        "b": ("Nadiren yardıma başvururum", 2),
        "c": ("Bazen yardım alırım", 3),
        "d": ("Çoğu zaman yardım alırım", 4),
        "e": ("Her zaman yardım alırım", 5),
    },
    "Sinirli olduğunuzda dikkatli ve mantıklı kararlar alabilir misiniz?": {
        "a": ("Asla alamam", 5),
        "b": ("Nadiren alabilirim", 4),
        "c": ("Bazen alabilirim", 3),
        "d": ("Çoğu zaman alırım", 2),
        "e": ("Her zaman alırım", 1),
    },
    "Öfkenizi yönlendirmek için günlük yaşamınıza ne tür sağlıklı alışkanlıklar ekliyorsunuz?": {
        "a": ("Hiçbir sağlıklı alışkanlık eklemiyorum", 5),
        "b": ("Az bir şey ekliyorum", 4),
        "c": ("Orta derecede sağlıklı alışkanlıklar ekliyorum", 3),
        "d": ("Çoğu zaman sağlıklı alışkanlıklar eklerim", 2),
        "e": ("Her zaman sağlıklı alışkanlıklar eklerim", 1),
    }
}

# Odaklanma Soruları ve Şıkları
# ...existing code...
odaklanma_sorulari = {
    "İşinize başladığınızda, ne kadar süre boyunca dikkatiniz dağılmadan çalışabilirsiniz?": {
        "a": ("5 dakikadan az", 5),
        "b": ("10 dakikadan az", 4),
        "c": ("15 dakikadan az", 3),
        "d": ("30 dakikadan az", 2),
        "e": ("30 dakikadan fazla", 1),
    },
    "Dikkatinizi bir iş üzerinde odaklamakta zorlanır mısınız?": {
        "a": ("Hiç zorlanmam", 1),
        "b": ("Az zorlanırım", 2),
        "c": ("Orta derecede zorlanırım", 3),
        "d": ("Çoğu zaman zorlanırım", 4),
        "e": ("Sürekli zorlanırım", 5),
    },
    "Çalışma alanınızın düzeni dikkatinizi toplamanıza yardımcı olur mu?": {
        "a": ("Hiç etkisi yoktur", 1),
        "b": ("Az etkisi vardır", 2),
        "c": ("Orta derecede etkisi vardır", 3),
        "d": ("Çok etkisi vardır", 4),
        "e": ("Tamamen etkisi vardır", 5),
    },
    "Dikkatiniz genellikle ne sıklıkla dağılır?": {
        "a": ("Hiç dağılmaz", 1),
        "b": ("Nadiren dağılır", 2),
        "c": ("Bazen dağılır", 3),
        "d": ("Sıklıkla dağılır", 4),
        "e": ("Her zaman dağılır", 5),
    },
    "Zihninizin bir işe odaklanırken ne kadar net olduğunu hissediyorsunuz?": {
        "a": ("Hiç net değilim", 5),
        "b": ("Az bir netlik hissederim", 4),
        "c": ("Orta derecede netlik hissederim", 3),
        "d": ("Çok netim", 2),
        "e": ("Tamamen netim", 1),
    },
    "Çalışırken sıklıkla başka düşüncelerle mi meşgul oluyorsunuz?": {
        "a": ("Hiç düşünmem", 1),
        "b": ("Az düşünürüm", 2),
        "c": ("Bazen düşünürüm", 3),
        "d": ("Çoğu zaman düşünürüm", 4),
        "e": ("Sürekli düşünürüm", 5),
    },
    "Dikkatinizin dağılmaması için ne kadar çaba sarf ediyorsunuz?": {
        "a": ("Hiç çaba sarf etmiyorum", 1),
        "b": ("Az çaba sarf ediyorum", 2),
        "c": ("Orta derecede çaba sarf ediyorum", 3),
        "d": ("Çok çaba sarf ediyorum", 4),
        "e": ("Sürekli çaba sarf ediyorum", 5),
    },
    "Çalışmaya başladığınızda, tamamlamanız gereken bir işi bitirene kadar odaklanma sürekliliğiniz nasıl olur?": {
        "a": ("Hiç odaklanamam", 5),
        "b": ("Kısa süreli odaklanırım", 4),
        "c": ("Orta süreli odaklanırım", 3),
        "d": ("Uzun süre odaklanırım", 2),
        "e": ("Sürekli odaklanırım", 1),
    },
    "Zihinsel olarak yorgun olduğunuzda, odaklanmanız ne kadar zorlaşır?": {
        "a": ("Hiç zorlaşmaz", 1),
        "b": ("Az zorlaşır", 2),
        "c": ("Orta derecede zorlaşır", 3),
        "d": ("Çok zorlaşır", 4),
        "e": ("Tamamen zorlaşır", 5),
    },
    "Dikkatiniz dağılmadan bir işi ne kadar süreyle yapabilirsiniz?": {
        "a": ("5 dakikadan az", 5),
        "b": ("10 dakikadan az", 4),
        "c": ("15 dakikadan az", 3),
        "d": ("30 dakikadan az", 2),
        "e": ("30 dakikadan fazla", 1),
    },
    "Çalışma sırasında ne kadar süre sosyal medya veya dış dünyadan uzak kalabiliyorsunuz?": {
        "a": ("Hiç uzak kalamam", 5),
        "b": ("Az bir süre uzak kalabilirim", 4),
        "c": ("Orta derecede uzak kalabilirim", 3),
        "d": ("Çoğu zaman uzak kalabilirim", 2),
        "e": ("Sürekli uzak kalabilirim", 1),
    },
    "Hedeflerinize odaklandığınızda, bu hedeflere ulaşmak için ne kadar kararlısınız?": {
        "a": ("Hiç kararlı değilim", 5),
        "b": ("Az kararlıyım", 4),
        "c": ("Orta derecede kararlıyım", 3),
        "d": ("Çok kararlıyım", 2),
        "e": ("Tamamen kararlıyım", 1),
    },
    "Yapılacak işinize başladığınızda nasıl bir motivasyon hissedersiniz?": {
        "a": ("Hiç motivasyonum yoktur", 5),
        "b": ("Az bir motivasyon hissederim", 4),
        "c": ("Orta derecede motivasyon hissederim", 3),
        "d": ("Çok motivasyonlu hissederim", 2),
        "e": ("Tamamen motive olurum", 1),
    },
    "Odaklanmayı artırmak için zihinsel veya fiziksel egzersizler yapar mısınız?": {
        "a": ("Hiç yapmam", 5),
        "b": ("Az yaparım", 4),
        "c": ("Bazen yaparım", 3),
        "d": ("Sıklıkla yaparım", 2),
        "e": ("Her zaman yaparım", 1),
    },
    "Çalışma yaparken dışarıdan gelen gürültüler dikkatinizi ne kadar dağıtır?": {
        "a": ("Hiç dağılmaz", 1),
        "b": ("Az dağılır", 2),
        "c": ("Orta derecede dağılır", 3),
        "d": ("Çok dağılır", 4),
        "e": ("Tamamen dağılır", 5),
    }
}

# Testi Seç
def analiz_ve_oneri(test_tipi, ortalama):
    """
    Kullanıcının ortalama puanına göre analiz, öneri ve detaylı antrenman planı sağlar.
    """
    if test_tipi == "öfke":
        if 1.0 <= ortalama < 2.0:
            return (
                "Öfke yönetiminde harikasınız! Küçük şeylere bile sabırlı davranıyorsunuz. Bu tutumunuzu koruyun.",
                [
                    "Günlük meditasyon: Sabah uyandıktan sonra 5-10 dakika boyunca sakin bir ortamda oturun ve derin nefes alıp vererek zihninizi boşaltmaya çalışın.",
                    "Yoga: Haftada 3 kez, her biri 20 dakika süren hafif yoga seansları yapın. Özellikle 'Child Pose' ve 'Cat-Cow Pose' gibi rahatlatıcı pozisyonları tercih edin.",
                    "Kitap Okuma: Sakinleştirici etkisi olan kitaplar okuyarak zihinsel dinginliği artırabilirsiniz."
                ]
            )
        elif 2.0 <= ortalama < 3.0:
            return (
                "Öfke yönetiminde genelde iyisiniz, ancak ara sıra sinirli olabiliyorsunuz. Daha fazla sakinleşme teknikleri deneyebilirsiniz.",
                [
                    "4-7-8 Nefes Tekniği: 4 saniye nefes alın, 7 saniye nefesinizi tutun ve 8 saniyede nefes verin. Sinirli hissettiğinizde bu tekniği 5 kez tekrar edin.",
                    "Yürüyüş: Günlük 20-30 dakikalık sakin bir yürüyüş yaparak hem fiziksel hem zihinsel rahatlama sağlayabilirsiniz.",
                    "Sanatsal Aktiviteler: Resim yapmayı, yazı yazmayı veya bir enstrüman çalmayı deneyerek öfkenizi yapıcı bir şekilde ifade edin."
                ]
            )
        elif 3.0 <= ortalama < 4.0:
            return (
                "Öfke yönetiminde orta düzeydesiniz. Daha fazla uygulama ile öfke kontrolünüzü geliştirebilirsiniz.",
                [
                    "Mindfulness Egzersizleri: Günde iki kez, sabah ve akşam 10 dakika mindfulness egzersizi yaparak anda kalmayı öğrenin.",
                    "Yüksek Tempolu Egzersiz: Haftada 5 gün 30 dakika koşu, bisiklet veya hızlı yürüyüş yaparak enerjinizi kontrol edin.",
                    "Sosyal Destek: Haftada bir kez arkadaşlarınız veya ailenizle pozitif duygular üzerine sohbet edin."
                ]
            )
        elif 4.0 <= ortalama <= 5.0:
            return (
                "Öfke kontrolünde gelişime ihtiyacınız var. Daha yoğun bir antrenman programı ve destek önerilir.",
                [
                    "Profesyonel Yardım: Bir psikologla haftalık görüşmeler planlayarak öfke yönetimi üzerine çalışın.",
                    "Yüksek Tempolu Spor: Haftada 5 gün, her biri 45 dakikalık yüksek tempolu kardiyo egzersizleri (koşu, spinning) yapın.",
                    "Günlük Günlük Tutma: Her gün, öfkelendiğiniz anları ve bu anlarda neler hissettiğinizi yazın. Kendinizi tanımanıza yardımcı olacaktır."
                ]
            )

    elif test_tipi == "odaklanma":
        if 1.0 <= ortalama < 2.0:
            return (
                "Odaklanma konusunda mükemmelsiniz! Dikkatiniz dağılmadan uzun süre çalışabiliyorsunuz.",
                [
                    "Beyin Egzersizleri: Her gün Sudoku veya bulmaca çözerek zihninizi aktif tutun.",
                    "Meditasyon: Günlük 10 dakikalık meditasyon seanslarıyla mevcut odaklanma kapasitenizi artırın.",
                    "Düzenli Çalışma Ortamı: Çalışma alanınızı temiz ve düzenli tutmaya devam edin."
                ]
            )
        elif 2.0 <= ortalama < 3.0:
            return (
                "Odaklanma konusunda iyi durumdasınız. Dikkat dağıtıcıları azaltarak performansınızı daha da artırabilirsiniz.",
                [
                    "Pomodoro Tekniği: 25 dakika çalışma, 5 dakika ara prensibiyle çalışarak odak sürenizi optimize edin.",
                    "Fiziksel Egzersizler: Haftada 3 kez 20-30 dakikalık hafif egzersizler (yoga, esneme hareketleri) yaparak zihinsel ve fiziksel denge sağlayın.",
                    "Çalışma Öncesi Planlama: Günlük işleriniz için yapılacaklar listesi hazırlayarak dikkatinizi toplamayı kolaylaştırın."
                ]
            )
        elif 3.0 <= ortalama < 4.0:
            return (
                "Odaklanma konusunda orta düzeydesiniz. Zihinsel ve fiziksel egzersizlerle odaklanmanızı güçlendirebilirsiniz.",
                [
                    "Mindfulness Çalışmaları: Günde iki kez, sabah ve akşam 10 dakikalık mindfulness egzersizleri yaparak anda kalmayı öğrenin.",
                    "Egzersiz: Haftada 4 gün tempolu yürüyüş veya hafif koşu yaparak odaklanmanızı geliştirin.",
                    "Dikkat Artırıcı Uygulamalar: Mobil uygulamalardan (Headspace, Calm) faydalanarak odaklanma tekniklerini öğrenin.",
                    "Okuma Egzersizleri: Her gün en az 30 dakika odaklanarak kitap okuyun."
                ]
            )
        elif 4.0 <= ortalama <= 5.0:
            return (
                "Odaklanma konusunda gelişime ihtiyacınız var. Daha yoğun bir çalışma düzeni ve egzersiz programı önerilir.",
                [
                    "Meditasyon ve Nefes Çalışmaları: Her sabah ve akşam 10-15 dakika nefes egzersizleri yaparak güne odaklı bir başlangıç yapın.",
                    "Sosyal Medyadan Uzak Durma: Çalışma sırasında telefonunuzu uçak moduna alın veya başka bir odada tutun.",
                    "Egzersiz: Haftada 5 gün, her biri 40 dakika tempolu koşu, bisiklet veya yoga yaparak zihinsel berraklık sağlayın.",
                    "Odaklanma Günlükleri: Her gün çalışma sırasında ne kadar odaklanabildiğinizi yazın ve bunu geliştirmek için stratejiler oluşturun."
                ]
            )

# Test seçme ve soru-cevap alma mantığı (önceki kodlarla aynı)

secim = test_secin()

if secim == "1":
    print("\nÖfke Yönetimi Testi Başlıyor!")
    cevaplar = kullanici_cevaplari_al_sorular(ofke_yonetimi_sorulari)
    ortalama = sum(cevaplar) / len(cevaplar)
    print(f"\nÖfke Yönetimi Testi Ortalama Puanınız: {ortalama:.2f}")
    analiz, antrenmanlar = analiz_ve_oneri("öfke", ortalama)
    print(f"\nAnaliz:\n{analiz}")
    print("\nAntrenman Önerileri:")
    for antrenman in antrenmanlar:
        print(f"- {antrenman}")
elif secim == "2":
    print("\nOdaklanma Testi Başlıyor!")
    cevaplar = kullanici_cevaplari_al_sorular(odaklanma_sorulari)
    ortalama = sum(cevaplar) / len(cevaplar)
    print(f"\nOdaklanma Testi Ortalama Puanınız: {ortalama:.2f}")
    analiz, antrenmanlar = analiz_ve_oneri("odaklanma", ortalama)
    print(f"\nAnaliz:\n{analiz}")
    print("\nAntrenman Önerileri:")
    for antrenman in antrenmanlar:
        print(f"- {antrenman}")


     