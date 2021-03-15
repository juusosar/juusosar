import haravasto as ha
import random as rand
import time


HIIREN_NAPPI = {
    ha.HIIRI_VASEN: "vasen",
    ha.HIIRI_OIKEA: "oikea"
}


aika = {
    "alku": 0,
    "loppu": 0,
}


tila = {
    "kentta": [],
    "vertailu_kentta": [],
    "miinakentta": [],
    "vapaat_ruudut": [],
    "kentan_korkeus": 0,
    "kentan_leveys": 0,
    "miinat": 0,
    "siirrot": 0,
    "lopputulos": ""
}


def hiiren_kasittelija(x, y, nappi, muokkausnappaimet):
    """
    Käsittelijäfunktio, joka määrää mitä tapahtuu kunkin hiiren näppäimen klikkauksella.

    - Vasen näppäin tarkistaa klikatun ruudun tilan ja päivittää kentän.
    - Oikea näppäin asettaa klikattuun ruutuun lipun.
    """
    if HIIREN_NAPPI[nappi] == "vasen":
        tila["siirrot"] += 1
        tarkista_ruutu(x, y, tila["miinakentta"], tila["kentta"], tila["vertailu_kentta"])
    if HIIREN_NAPPI[nappi] == "oikea":
        aseta_lippu(x, y, tila["kentta"])


def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    if tila["kentan_leveys"] < 7:
        koko = 15
    else:
        koko = 20
    ha.tyhjaa_ikkuna()
    ha.piirra_tausta()
    ha.piirra_tekstia("Juuson miinaharava", tila["kentan_leveys"]*40 / 40, tila["kentan_korkeus"]*40, koko=koko)
    ha.aloita_ruutujen_piirto()
    for rivi, sarake in enumerate(tila["kentta"]):
        for x, merkki in enumerate(sarake):
            ha.lisaa_piirrettava_ruutu(merkki, x*40, rivi*40)
    ha.piirra_ruudut()


def main():
    """
    Pelin aloitusnäyttö, näkyy ainoastaan pelitiedoston käynnistyksen yhteydessä.
    """
    print(" ____________________________________\n"
          "| Tervetuloa pelaamaan miinaharavaa! |\n"
          "|       Päävalikko --ENTER--         |")
    input("|____________________________________|\n")
    valikko()


def valikko():
    """
    Pelin tekstimuotoinen päävalikko.
    Pyytää käyttäjältä syötteen ja toimii sen mukaisesti.
    """
    print("\n|\/\/\/\/\/\/\/\/\/\/\/\/\/|\n"
          "|   1. Uusi peli           |\n"
          "|   2. Katsele tilastoja   |\n"
          "|   3. Lopeta peli         |\n"
          "|/\/\/\/\/\/\/\/\/\/\/\/\/\|\n")
    while True:
        try:
            syote = int(input("Tee valinta syöttämällä haluamasi numero: ").strip())
            if syote == 1:
                kaynnista()
                break
            elif syote == 2:
                nayta_tilastot("miinaharava_tulokset.txt")
                break
            elif syote == 3:
                break
            else:
                print("Tätä numeroa ei löydy valikosta...\n")
        except (ValueError, UnboundLocalError):
                    print("Valinnaksi hyväksytään vain numeroita!\n")


def kaynnista():
    """
    Valmistelee miinaharavan pelattavaan kuntoon kutsumalla kentän valmistavia funktioita ja aloittaa pelin.
    """
    ha.lataa_kuvat("spritet")
    print("------------------------------------------------------------------------------------------------------"
          "\nSÄÄNNÖT:\r\nKlikkaamalla haluamaasi ruutua hiiren vasemmalla näppäimellä paljastat ruudun alla olevan laatan.\n"
          "\nTyhjä laatta - Avaa kaikki muut tyhjät laatat tämän ympäriltä ja paljastaa lähimmmät numerolaatat.\n"
          "Numerolaatta - Kertoo kuinka montaa miinaa tämän laatan ympärillä on (myös viistosti).\n"
          "Miinalaatta - Klikkaamalla ruutua, jossa on miina, häviät pelin.\n"
          "Voit asettaa hiiren oikeaa näppäintä klikkaamalla 'lipun' ruutuun, jonka luulet olevan miinalaatta.\n"
          "\nKun luulet löytäneesi kaikki miinalaatat, voit tarkistaa pelin klikkaamalla tyhjää ruutua.\n"
          "\nOnnea matkaan!\n"
          "-------------------------------------------------------------------------------------------------------\n")
    kysy_kentan_tilat()
    ha.luo_ikkuna(tila["kentan_leveys"] * 40, tila["kentan_korkeus"] * 40 + 40)
    ha.aseta_piirto_kasittelija(piirra_kentta)
    ha.aseta_hiiri_kasittelija(hiiren_kasittelija)
    #ha.aseta_toistuva_kasittelija(ajanotto_kasittelija, toistovali=1)
    miinoita(tila["miinakentta"], tila["vertailu_kentta"], tila["miinat"], tila["vapaat_ruudut"])
    numeroi_ruudut(tila["miinakentta"])
    aika["alku"] = time.time()
    ha.aloita()


def kysy_kentan_tilat():
    """
    Kysyy käyttäjältä kentän korkeuden, leveyden ja miinojen lukumäärän.
    Luo pääohjelman sanakirjaan dimensioita vastaavat listat kentästä,
    tyhjistä ruuduista koordinaatteineen ja miinakentästä.
    Miinojen lukumäärä lisätään myös listaan.
    """
    while True:
        try:
            korkeus = int(input("Anna kentän korkeus: "))
            leveys = int(input("Anna kentän leveys: "))
            if korkeus < 0 or leveys < 0:
                print("Anna positiivinen luku!")
            elif korkeus == 0 or leveys == 0:
                print("Muistathan antaa kentälle sentään jotain dimensioita!")
            else:
                tila["miinat"] = int(input("Anna miinojen lukumäärä: "))
                if tila["miinat"] <= 0:
                    print("Sinun pitää asettaa ainakin yksi miina!")
                elif tila["miinat"] > korkeus * leveys:
                    print("Miinat eivät mahdu kentälle!")
                else:
                    for rivi in range(korkeus):
                        tila["kentta"].append([])
                        tila["miinakentta"].append([])
                        tila["vertailu_kentta"].append([])
                        for sarake in range(leveys):
                            tila["kentta"][-1].append(" ")
                            tila["miinakentta"][-1].append(" ")
                            tila["vertailu_kentta"][-1].append(" ")
                    for x in range(leveys):
                        for y in range(korkeus):
                            tila["vapaat_ruudut"].append((x, y))
                    tila["kentan_korkeus"], tila["kentan_leveys"] = korkeus, leveys
                    break
        except ValueError:
            print("Annettujen arvojen pitää olla positiivisia kokonaislukuja!")


def miinoita(miinakentta, vertailu_kentta, miinat_lkm, vapaat_ruudut):
    """
    Asettaa sanakirjan 'miinakentta'- ja 'kentta'-listaan miinat_lkm kappaletta miinoja satunnaisesti.

    :param miinakentta: miinakenttaa esittävä lista
    :param vertailu_kentta: pelikenttää esittävä lista
    :param miinat_lkm: käyttäjältä kysytty miinojen lukumäärä
    :param vapaat_ruudut: vapaita ruutuja esittävä lista, jolla on samat dimensiot kuin pelikentällä
    """
    miina = "x"
    i = 0
    while i < miinat_lkm:
        i += 1
        try:
            miinan_koord = rand.choice(vapaat_ruudut)
            vapaat_ruudut.remove(miinan_koord)
            miinan_x, miinan_y = miinan_koord
            miinakentta[miinan_y][miinan_x] = miina
            vertailu_kentta[miinan_y][miinan_x] = miina
        except IndexError:
            break


def numeroi_ruudut(kentta):
    """
    Asettaa miinakentälle miinojen ympärille pelin logiikan mukaan oikeita numeroarvoja esittävät merkit.

    :param kentta: miinakenttää esittävä lista
    """
    for rivi, sarake in enumerate(kentta):
        for ruutu, merkki in enumerate(sarake):
            if merkki != "x":
                miinat = 0
                for y, x_lista in enumerate(kentta):
                    if y in range(rivi - 1, rivi + 2):
                        for x, paikan_merkki in enumerate(x_lista):
                            if x in range(ruutu - 1, ruutu + 2):
                                if paikan_merkki == "x":
                                    miinat += 1
                kentta[rivi][ruutu] = str(miinat)


def tarkista_ruutu(x_koord, y_koord, miinakentta, kentta, vertailu_kentta):
    """
    Tarkistaa klikatun ruudun tilan ja toimii miinakentän logiikan mukaisesti.

    :param x_koord: klikkauksen x-koordinaatti
    :param y_koord: klikkauksen y-koordinaatti
    :param miinakentta: numeroitua miinakenttää esittävä lista
    :param kentta: näkyvää pelikenttää esittävä lista
    :param vertailu_kentta: pelkät miinat sisältävä lista
    """
    x = x_koord // 40
    y = y_koord // 40
    if vertailu_kentta == miinakentta:
        print("\n--ONNISTUIT LÖYTÄMÄÄN KAIKKI MIINAT--\n")
        print("\n--VOITIT PELIN--\n")
        tila["lopputulos"] = "Voitto"
        haravoinnin_loppu()
    else:
        try:
            if miinakentta[y][x] == "0":
                tutkimus = [(x, y)]
                while tutkimus:
                    x_ruutu, y_ruutu = tutkimus.pop(-1)
                    for y_korkeus, x_paikka in enumerate(vertailu_kentta):
                        if y_korkeus in range(y_ruutu - 1, y_ruutu + 2):
                            for x_leveys, x_sijainti in enumerate(x_paikka):
                                if x_leveys in range(x_ruutu - 1, x_ruutu + 2):
                                    if x_sijainti == "x":
                                        break
                                    elif x_sijainti == " ":
                                        if miinakentta[y_korkeus][x_leveys] != "0":
                                            for i in range(1, 9):
                                                if miinakentta[y_korkeus][x_leveys] == str(i):
                                                    kentta[y_korkeus][x_leveys] = str(i)
                                                    vertailu_kentta[y_korkeus][x_leveys] = str(i)
                                        elif miinakentta[y_korkeus][x_leveys] == "0":
                                            kentta[y_korkeus][x_leveys] = "0"
                                            vertailu_kentta[y_korkeus][x_leveys] = "0"
                                            tutkimus.append((x_leveys, y_korkeus))
            elif miinakentta[y][x] != "x":
                for i in range(1, 9):
                    if miinakentta[y][x] == str(i):
                        kentta[y][x] = str(i)
                        vertailu_kentta[y][x] = str(i)
            elif miinakentta[y][x] == "x":
                kentta[y][x] = "x"
                time.sleep(1)
                print("\n--OSUIT MIINAAN--\n"
                      "\n--HÄVISIT--\n")
                tila["lopputulos"] = "Häviö"
                haravoinnin_loppu()
        except IndexError:
            print("Tämä ruutu ei ole kentällä!")


def aseta_lippu(x_koord, y_koord, kentta):
    """
    Asettaa hiiren oikealla näppäimellä valittuun ruutuun 'lipun'.
    Lippua uudelleen klikkaaminen poistaa sen.

    :param x_koord: hiirellä painettu x-koordinaatti
    :param y_koord: hiirellä painettu y-koordinaatti
    :param kentta:  pelikenttää esittävä lista
    """
    if kentta[y_koord // 40][x_koord // 40] == "f":
        kentta[y_koord // 40][x_koord // 40] = " "
    else:
        kentta[y_koord // 40][x_koord // 40] = "f"


def tallenna_tulokset(tiedosto):
    """
    Tallentaa pelatun pelin tulokset erilliseen tekstiedostoon.

    :param tiedosto: tiedosto, johon tallennus tapahtuu
    """
    aika["loppu"] = time.time()
    with open(tiedosto, 'a+') as tulokset:
        tulokset.write('--------------------------------------------------------------------------\n'
                       'Päivämäärä: {paiva}\nKesto: {aika:.2f} min\nSiirrot: {siirrot}\nKentän korkeus: {korkeus}\n'
                       'Kentän leveys: {leveys}\nMiinojen lukumäärä: {miinat}\nTulos: {lopputulos}\r\n'.format(
            paiva=time.strftime('%c'),
            aika=(aika["loppu"] - aika["alku"]) / 60,
            miinat=tila["miinat"],
            korkeus=tila["kentan_korkeus"],
            leveys=tila["kentan_leveys"],
            lopputulos=tila["lopputulos"],
            siirrot=tila["siirrot"]
        ))


def nayta_tilastot(tiedosto):
    """
    Lukee pyydettäessä tallennettujen pelien tilastot ja printtaa ne esiin.
    Tilastot näytettyään palaa valikkoon.

    :param tiedosto: tiedosto, johon tulokset on tallennettu
    """
    try:
        with open(tiedosto, 'r') as tilastot:
            print(tilastot.read())
    except FileNotFoundError:
        print("Sinun pitää ensin pelata peliä, ennen kuin voit katsella tilastojasi!")
    input("--paina ENTER palataksesi valikkoon--")
    valikko()


def haravoinnin_loppu():
    """
    Pelin päättyessä kutsuu tallenna-funktiota, lopettaa pelin suorituksen ja nollaa kentät ja siirrot sanakirjasta.
    Lopuksi palaa päävalikkoon.
    """
    tallenna_tulokset("miinaharava_tulokset.txt")
    ha.lopeta()
    tila["kentta"], tila["miinakentta"], tila["vertailu_kentta"], tila["vapaat_ruudut"] = [], [], [], []
    tila["siirrot"] = 0
    input("--paina ENTER palataksesi valikkoon--\n")
    valikko()


if __name__ == "__main__":
    main()

