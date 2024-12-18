import json

class Ogrenci:
       def __init__(self, ad, soyad, numara):
              self.ad = ad
              self.soyad = soyad
              self.numara = numara
              self.notlar = []

       def not_ekle(self, yeni_not):
              self.notlar.append(yeni_not)

       def not_ortalamasi(self):
              if self.notlar:
                     return sum(self.notlar) / len(self.notlar)
              else:
                     return 0
              
       def to_dict(self):
              return {
                     "ad" : self.ad,
                     "soyad" : self.soyad,
                     "numara" : self.numara,
                     "notlar" : self.notlar
              }
       
       @staticmethod
       def from_dict(data):
              ogrenci = Ogrenci(data["ad"], data["soyad"], data["numara"])
              ogrenci.notlar = data["notlar"]
              return ogrenci
       
              
class OgrenciYonetimSistemi:
       def __init__(self):
              self.ogrenciler = []

       def ogrenci_ekle(self, ogrenci):
              self.ogrenciler.append(ogrenci)

       def ogrenci_sil(self,numara):
              self.ogrenciler = [ogrenci for ogrenci in self.ogrenciler if ogrenci.numara != numara]

       def ogrenci_guncelle(self, numara, yeni_ad=None, yeni_soyad=None, yeni_numara=None):
              for ogrenci in self.ogrenciler:
                     if ogrenci.numara == numara:
                            if yeni_ad:
                                   ogrenci.ad = yeni_ad
                            if yeni_soyad:
                                   ogrenci.soyad = yeni_soyad
                            if yeni_numara:
                                   ogrenci.numara = yeni_numara
                            return True
              return False
       
       def ogrenci_ara(self, numara=None, ad=None):
              if numara:
                     return [ogrenci for ogrenci in self.ogrenciler if ogrenci.numara == numara]
              if ad:
                     return [ogrenci for ogrenci in self.ogrenciler if ogrenci.ad == ad]
              return []

       def ogrenci_bilgilerini_goster(self):
              for ogrenci in self.ogrenciler:
                     print(
                            f"Ad: {ogrenci.ad}, Soyad: {ogrenci.soyad}, Numara: {ogrenci.numara},"
                            f"Not Ortalamasu: {ogrenci.not_ortalamasi():.2f}"
                     )

       def kaydet(self, dosya_adi):
              with open(dosya_adi, "w") as dosya:
                     json.dump([ogrenci.to_dict() for ogrenci in self.ogrenciler], dosya)

       def yukle(self, dosya_adi):
        try:
            with open(dosya_adi, "r") as dosya:
                self.ogrenciler = [
                    Ogrenci.from_dict(data) for data in json.load(dosya)
                ]
        except FileNotFoundError:
            print("Dosya bulunamadı. Yeni bir sistem başlatılıyor.")

def ana_menu():
    sistem = OgrenciYonetimSistemi()
    sistem.yukle("ogrenciler.json")

    while True:
        print("\n--- Öğrenci Yönetim Sistemi ---")
        print("1. Öğrenci Ekle")
        print("2. Öğrenci Sil")
        print("3. Öğrenci Güncelle")
        print("4. Öğrenci Ara")
        print("5. Tüm öğrencileri göster")
        print("6. Kaydet ve Çık")
        secim = input("Seçiminiz: ")

        if secim == "1":
            ad = input("Ad: ")
            soyad = input("Soyad: ")
            numara = int(input("Numara: "))
            ogrenci = Ogrenci(ad, soyad, numara)
            sistem.ogrenci_ekle(ogrenci)
            print("Öğrenci Eklendi!")

        elif secim == "2":
             numara = int(input("Silmek istediğiniz öğrencinin numarası: "))
             sistem.ogrenci_sil(numara)
             print("Öğrenci Silindi!")

        elif secim == "3":
              numara = int(input("Güncellemek istediğiniz öğrencinin numarası: "))
              yeni_ad = input("Yeni Ad (Boş bırakabilirsiniz):")
              yeni_soyad = input("Yeni Soyad (Boş bırakabilirsiniz): ")
              yeni_numara = input("Yeni Numara (Boş bırakabilirsiniz): ")
              yeni_numara = int(yeni_numara) if yeni_numara else None

              if sistem.ogrenci_guncelle(numara, yeni_ad, yeni_soyad, yeni_numara):
                   print("Öğrenci bilgileri güncellendi!")
              else:
                   print("Öğrenci Bulunamadı!")
                     
        elif secim == "4":
              numara = input("Numara ile ara: ")
              ad = input("Ad ile ara: ")

              numara = int(numara) if numara else None
              bulunanlar = sistem.ogrenci_ara(numara=numara, ad=ad)

              if bulunanlar:
                  for ogrenci in bulunanlar:
                        print(f"Ad: {ogrenci.ad}, Soyad: {ogrenci.soyad}, Numara: {ogrenci.numara}")

              else:
                  print("Öğrenci Bulunamadı! ")

                     
        elif secim == "5":
              sistem.ogrenci_bilgilerini_goster()

        elif secim == "6":
              sistem.kaydet("ogrenciler.json")
              print("Veriler kaydedildi. Çıkış yapılıyor...")
              break
        else:
              print("Geçersiz seçim! Tekrar deneyin!")

ana_menu()