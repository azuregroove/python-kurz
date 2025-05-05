# Automatizovane testovani webu https://vtm.zive.cz

# Co testujem:
# 1. Nazev stranky           -> overeni, ze se nacte spravny titulek stranky
# 2. Viditelnost loga VTM    -> kontrola, ze se v zahlavi zobrazuje logo
# 3. Funkcnost hlavniho menu -> kliknuti na polozky jako "POCITACE", "MOBILY", "VEDA" apod.
# 4. Otevreni clanku         -> kliknuti na prvni clanek a kontrola, ze se stranka spravne nacte

# Projektova struktura:
# - slozka "projekt"
# - soubor requirements.txt s knihovnami
# - logovaci soubor "log.csv" pro ukladani vysledku testu

# Pouzite nastroje:
# - Knihovna Playwright pro Python – slouzi k automatizaci weboveho prohlizece
# - Umoznuje simulaci kliknuti, vyhledavani a cteni prvku na strance

# Instalace v PyCharm terminalu:
# 1. pip install -r requirements.txt
# 2. playwright install

# V planu bylo jeste otestovat vyhledavani, prihlaseni a odhlaseni. Bohuzel jsem se zasekal na testu 3.
# Z testerskyho pohledu to nefunguje, protoze nemuzu odhalit proc mi nepravidelne klika/neklika na odkazy v testu 3. Pokazdy test vyjde jinak :-(

from playwright.sync_api import sync_playwright  # Importuju synchronni API z knihovny Playwright pro ovladani prohlizece
from pathlib import Path                         # Importuju Path pro praci se souborovymi cestami
import csv                                       # Importuju modul csv pro praci s CSV soubory
from datetime import datetime                    # Importuju datetime pro ziskani aktualniho datumu a casu


# Cesta k logovacimu souboru "log.csv"
soubor_logu = Path("log.csv")                   # Nastavim cestu k logovacimu souboru "log.csv", ktery se bude pouzivat pro zapis vysledku testu



# Funkce pro zapis vysledku do logu
def zapis_vysledek(nazev_testu, vysledek_testu):                                                          # Definuju funkci pro zapis vysledku testu do CSV logu
    casovy_razitko = datetime.now().strftime("%d-%m-%Y %H:%M:%S")                                         # Vytvorim casovy razitko ve formatu "den-mesic-rok hodina:minuta:vterina"
    try:
        soubor_existuje = soubor_logu.exists()                                                            # Overim, jestli soubor logu uz existuje
        with open(str(soubor_logu), mode="a", newline="", encoding="utf-8") as soubor:                    # Otevru soubor pro zapis (append) – pokud neexistuje, vytvori se; zapisuje se na konec; 'newline'="" zajisti spravne formatovani radku v CSV; 'utf-8' zajisti spravne kodovani znaku; 'soubor' je promenna, pod kterou budu s timto souborem pracovat
            pole = ["cas", "test", "vysledek"]                                                            # Definuju seznam nazvu sloupcu
            zapisovac = csv.DictWriter(soubor, fieldnames=pole)                                           # Vytvorim zapisovac, ktery zapisuje slovniky do CSV podle hlavicek
            if not soubor_existuje:                                                                       # Pokud soubor jeste neexistoval, zapisu hlavicku (prvni radek)
                zapisovac.writeheader()
            zapisovac.writerow({"cas": casovy_razitko, "test": nazev_testu, "vysledek": vysledek_testu})  # Zapisem jeden radek s daty
    except Exception as chyba:                                                                            # Pokud nastane vyjimka (napr. problem se souborem), vypise chybu
        print(f"Chyba pri zapisu do logu: {chyba}")



# Kontrola tlačítka "Souhlasim" -> snaha obejit cookies, protoze jsem nenasel nazev s hodnotou dane cookies, ktera na me vybehla nepravidelne jenom pri otevreni webu pres knihovnu playwright
def kontrola_souhlasim(page):                           # Funkce pro kliknuti na tlacitko "Souhlasim", pokud je viditelny, kliknem; pokud neni, nic nevypise
    btn = page.locator("button:has-text('Souhlasím')")  # Najde tlacitko s textem "Souhlasim"
    if btn.count() > 0:                                 # Pokud je nalezen nejaky prvek
        if btn.first.is_visible():                      # A je viditelny
            btn.first.click(timeout=20000)              # Klikne na nej s timeoutem 20 sekund
        else:
            pass                                        # Pokud neni viditelny, nic nedela



# Test 1 – Overeni titulku stranky
def test_nazev_stranky(page1):                                                               # Definice funkce pro test nazvu stranky, vstupem je objekt 'page'
    print("Test 1 - Testuji titulek stránky")                                                # Vytiskne do konzole, ze probiha test titulku
    try:
        titulek = page1.title()                                                              # Ziska titulek aktualni stranky
        if titulek == "VTM.cz – Věda, technika, zajímavosti, budoucnost":                    # Porovna, zda titulek odpovida ocekavanemu textu
            print("Test 1 – Titulek je správný")                                             # Pokud ano, vypise ze titulek je spravny
            zapis_vysledek("Ověření názvu stránky", "Úspěšný")       # Zapise vysledek testu jako uspesny
        else:
            print("Test 1 – Titulek je nesprávný")                                           # Pokud titulek nesouhlasi, vypise chybu
            zapis_vysledek("Ověření názvu stránky", "Neúspěšný")     # Zapise vysledek testu jako neuspesny
    except Exception as chyba:                                                              # Zachyti chybu, pokud napr. selze nacitani titulku
        print(f"Test 1 – Chyba při načítání titulku: {chyba}")                              # Vytiskne popis chyby
        zapis_vysledek("Ověření názvu stránky", "Chyba")             # Zapise vysledek testu jako chyba



# Test 2 – Overeni viditelnosti loga VTM
def test_viditelnost_loga(page2):                                               # Definice funkce pro test viditelnosti loga, vstupem je objekt 'page'
    print("Test 2 - Testuji viditelnost loga")                                  # Vytiskne info, ze probiha test loga
    try:
        kontrola_souhlasim(page)                                                # Zavola funkci pro potvrzeni souhlasu; tady funkce zafungovala
        logo_locator = page2.locator("img[alt*='VTM']")                         # Vyhleda obrazky, jejichz alt atribut obsahuje retezec "VTM"
        logo_count = logo_locator.count()                                       # Ziska pocet nalezenych obrazku
        found_visible = False                                                   # Inicializuje promennou pro zjisteni, jestli je nektery obrazek viditelny
        for i in range(logo_count):                                             # Prochazi vsechny nalezene obrazky
            try:
                logo = logo_locator.nth(i)                                      # Vybere konkretni obrazek podle indexu
                logo.wait_for(state="visible", timeout=20000)                   # Ceka, az bude obrazek viditelny, maximalne 20 sekund
                if logo.is_visible():                                           # Pokud je obrazek viditelny
                    found_visible = True                                        # Nastavi priznak, ze logo bylo nalezeno
                    break                                                       # Ukonci smycku
            except Exception:                                                   # Ignoruje chybu, pokud napr. prvek neexistuje nebo neni dostupny
                continue                                                        # Pokracuje na dalsi prvek
        if found_visible:                                                       # Pokud bylo logo nalezeno a je viditelny
            print("Test 2 - Logo je viditelné")                                 # Vytiskne zpravu, ze logo je viditelny
            zapis_vysledek("Ověření loga", "Úspěšný")    # Zapise vysledek jako uspesny
        else:                                                                   # Pokud nebyl nalezen zadny viditelny obrazek
            print("Logo není viditelné, i když jsou nalezeny elementy.")        # Informace, ze sice prvky existuji, ale nejsou viditelny
            zapis_vysledek("Ověření loga", "Neúspěšný")  # Zapise vysledek jako neuspesny
    except Exception as e:                                                      # Zachyti chybu pri cele kontrole loga
        print(f"Chyba při ověřování loga: {e}")                                 # Vytiskne popis chyby
        zapis_vysledek("Ověření loga", "Neúspěšný")      # Zapise vysledek jako neuspesny


# Test 3 - Funkcnost hlavniho menu
def test_funkcnost_hlavniho_menu(page3):
    print("Test 3 - Testuji hlavni menu")                                   # Vypise zpravu, ze se spousti test hlavniho menu
    odkazy = [
        {"text": "ŽIVĚ.CZ", "url": "https://www.zive.cz/"},
        {"text": "POČÍTAČE", "url": "https://www.zive.cz/pocitace"},
        {"text": "MOBILY", "url": "https://mobilmania.zive.cz/"},
        {"text": "VĚDA A TECHNIKA", "url": "https://vtm.zive.cz/"},
        {"text": "HRY", "url": "https://doupe.zive.cz/"},
        {"text": "FILMY A AV", "url": "https://avmania.zive.cz/"}
    ]                                                                       # Definuje seznam slovniku, kazdy obsahuje text odkazu a ocekavanou URL
    vse_ok = True                                                           # Inicializuje promenou vse_ok na True, ktera indikuje, ze zatim vse funguje spravne
    for odkaz in odkazy:                                                    # Pro kazdy odkaz v seznamu provedeme nasledujici test
        try:
            page3.goto("https://vtm.zive.cz/", timeout=20000)               # Otevre domovskou stranku vtm.zive.cz s casovym limitem 20 sekund
            kontrola_souhlasim(page)                                        # Zavola funkci, ktera kontroluje tlacitko "Souhlasim"
            page3.wait_for_load_state("networkidle", timeout=20000)         # Ceka, az se stranka nacte do stavu "networkidle" (bez site aktivity) s timeout 20 sekund
            link = page3.locator(f"a:has-text('{odkaz['text']}')")          # Hledáme tlačítko podle textu odkazu pomocí page.locator, ktery hleda prvek odkazu (<a>) obsahujici dany text z odkazu; pomoci get_by_role, get_by_text a XPath to hazelo chyby
            kliknutelny_odkaz = None                                        # Inicializuje promenou pro kliknutelny odkaz jako None
            for i in range(link.count()):                                   # Projde vsechny nalezene prvky odkazu
                kandidat = link.nth(i)                                      # Vybere kandidata odkazu podle indexu
                if kandidat.is_visible():                                   # Pokud je kandidát viditelny, ulozi se do "kliknutelny_odkaz" a cyklus se prerusi
                    kliknutelny_odkaz = kandidat
                    break
            if kliknutelny_odkaz is None:                                                           # Pokud neni nalezen zadny viditelny odkaz, vyhodi se vyjimka s chybovou hlaskou
                raise Exception(f"Nenasel jsem viditelny odkaz pro {odkaz['text']}")
            kliknutelny_odkaz.scroll_into_view_if_needed(timeout=20000)                             # Pokud je potreba, odkaz posuneme do viditelne casti stranky
            with page3.expect_navigation(timeout=20000):                                            # Ocekava se navigace, ktera probehne po kliknuti na odkaz (timeout 20 sekund)
                kliknutelny_odkaz.click(timeout=20000)                                              # Klikne na odkaz s casovym limitem 20 sekund
            page3.wait_for_load_state("load", timeout=20000)                                        # Ceka, az se nova stranka plne nacte (stav "load"), opet s timeout 20 sekund
            aktualni_url = page3.url                                                                # Ziska aktualni URL nactene stranky
            print(f"Kliknuto na '{odkaz['text']}', aktualni URL: {aktualni_url}")                   # Vypise informaci o tom, na ktery odkaz bylo kliknuto a jaka je aktualni URL
            if aktualni_url == odkaz["url"]:                                                        # Porovna ziskanou aktualni URL s ocekavanou URL z definice odkazu
                zapis_vysledek(f"Test odkazu: {odkaz['text']}", "Úspěšný")   # Pokud URL odpovida, zapise vysledek testu jako "Uspesny"
            else:
                print("URL nesouhlasi")                                                             # Pokud URL neodpovida, vypise zpravu a zapise test jako "Neuspesny"
                zapis_vysledek(f"Test odkazu: {odkaz['text']}", "Neúspěšný")
                vse_ok = False                                                                      # Nastavi promenou vse_ok na False, coz oznacuje chybu pri danem odkazu
        except Exception as chyba:
            print(f"Chyba pri testovani odkazu {odkaz['text']}: {chyba}")                           # V pripade vyjimky vypise chybovou hlasku, zapise vysledek testu jako "Neuspesny" a nastavi vse_ok na False
            zapis_vysledek(f"Test odkazu: {odkaz['text']}", "Neúspěšný")
            vse_ok = False
    if vse_ok:                                                                                      # Po projiti vsech odkazu, pokud vse_ok zustava True, test probehl uspesne
        print("Test 3 - Hlavni menu funguje spravne")
    else:
        print("Test 3 - Nektere odkazy nefunguji")                                                  # Pokud byla nejaka chyba, vypise, ze nektere odkazy nefunguji



# Test 4 – Otevreni clanku
def test_otevreni_clanku(page4):                                                         # Definice funkce pro test otevirani clanku, vstupem je objekt 'page'
    print("Test 4 - Testuji otevreni clanku")                                            # Vytiskne info, ze probiha test otevirani clanku
    home_url = "https://vtm.zive.cz/"                                                    # URL domovske stranky, odkud zacina test
    page4.goto(home_url, timeout=20000)                                                  # Nacte domovskou stranku
    kontrola_souhlasim(page)                                                             # Zavola funkci pro potvrzeni souhlasu
    page4.wait_for_load_state("load", timeout=20000)                                     # Ceka, az se stranka zcela nacte
    article_link = page4.locator("article a").first                                      # Najde prvni odkaz v clanku (v ramci prvku 'article')
    article_link.wait_for(state="visible", timeout=20000)                                # Ceka, az bude odkaz viditelny
    with page4.expect_navigation(timeout=20000):                                         # Ocekava, ze po kliknuti dojde k nacteni nove stranky
        article_link.click(timeout=20000)                                                # Klikne na odkaz, ktery vede k clanku
    page4.wait_for_load_state("load", timeout=20000)                                     # Ceka, az se nova stranka zcela nacte
    current_url = page4.url                                                              # Ziska aktualni URL po kliknuti
    if current_url == home_url:                                                          # Pokud URL zustane stejne jako na domovske strance
        print("Clanek se neotevrel spravne, URL je stale homepage.")                     # Vytiskne, ze se clanek neotevrel
        zapis_vysledek("Otevření článku", "Neúspěšný")            # Zapise vysledek testu jako neuspesny
    else:                                                                                # Pokud URL neni stejne, clanek byl uspesne otevren
        print(f"Test 4 - Otevreni clanku bylo uspesny, aktualni URL: {current_url}")     # Vytiskne uspesny test
        zapis_vysledek("Otevření článku", "Úspěšný")              # Zapise vysledek testu jako uspesny



# Spusteni testu s Playwright
with sync_playwright() as p:                                         # Pouzivam synchronni Playwright pro spusteni testu
    browser = p.chromium.launch(headless=False, slow_mo=500)         # Spusti prohlizec (chromium), viditelny pro uzivatele, kazdou akci zpomali o 500ms
    page = browser.new_page()                                        # Otevre novou stranku v prohlizeci
    page.goto("https://vtm.zive.cz/", timeout=20000)                 # Nacte stranku https://vtm.zive.cz/ s timeoutem 20 sekund
    kontrola_souhlasim(page)                                         # Zavola funkci pro potvrzeni souhlasu
    try:
        test_nazev_stranky(page)                                     # Test 1 – Titulek stranky
        test_viditelnost_loga(page)                                  # Test 2 – Viditelnost loga
        test_funkcnost_hlavniho_menu(page)                           # Test 3 – Funkcnost hlavniho menu
        test_otevreni_clanku(page)                                   # Test 4 – Otevreni clanku
    finally:
        browser.close()                                              # Zavre prohlizec po spusteni vsech testu

