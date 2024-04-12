import requests

hledany_subjekt = input("Zadejte IČO hledané společnosti: ")
hledany_subjekt = hledany_subjekt.strip()

response = requests.get("https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/" + hledany_subjekt)
data = response.json()
# print(len(data))
# print(data.keys())

try:
  if data["ico"] == hledany_subjekt:
    print()
    print(data["obchodniJmeno"] + "\n" +
           data["sidlo"]["textovaAdresa"])
    print()
  else:
    raise KeyError
except KeyError:
  print("Nebyl nalezen žádný subjekt se zadaným identifikačním číslem.")

nazev = input("Zadejte hledaný výraz: ")

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}
data = '{"obchodniJmeno": "' + nazev + '"}'
data = data.encode("utf-8")
resp = requests.post("https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat", headers=headers, data=data)
nalezeno = resp.json()

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}
data = '{"kodCiselniku": "PravniForma", "zdrojCiselniku": "res"}'
forma = requests.post("https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ciselniky-nazevniky/vyhledat", headers=headers, data=data)
ciselniky = forma.json()

print()
print("Počet nalezených subjektů: ", nalezeno["pocetCelkem"])
print()

for item in nalezeno["ekonomickeSubjekty"]:
  kod_subjektu = item["pravniForma"]
  for it in ciselniky["ciselniky"][0]["polozkyCiselniku"]:
       if it["kod"] == kod_subjektu:
          popis = it["nazev"][0]["nazev"]
          print(item["obchodniJmeno"] + ", " + item["ico"] + ", " + popis)
