## Ukázková pythoní hra

## Komentáře s dvojím dvojkřížkem jsou od autora vzorové hry;
## ostatním doporučuju komentovat jen s jedním #.

## Potřebujeme několik knihoven:
## random na náhodná čísla: https://docs.python.org/3/library/random.html
import random
## a Pyglet na grafiku: https://pyglet.readthedocs.org/
import pyglet

## Na začátku souboru definujeme konstanty, aby pak bylo jasné co které číslo
## znamená: místo "8" napíšeme rozumné jméno, abychom věděli že jde třeba
## o počet sloupců šachovnice.

COLUMNS = 8         ## počet sloupců "šachovnice"
ROWS = 8            ## počet řádků "šachovnice"

SPACING = 20        ## mezera mezi jednotlivými políčky (v pixelech)
MOVE_SPEED = 5      ## rychlost animace přesouvání
EXPLODE_SPEED = 3   ## rychlost animace odstranění obrázku

# Další konstanty jsou specifické pro tuhle konkrétní hru:

## jména souborů
IMG_PATH = 'assets/animal-pack/PNG/Square without details/{}.png'
ACTIVE_PATH = 'assets/animal-pack/PNG/Square (outline)/{}.png'
GREY_PATH = 'assets/animal-pack/PNG/sedy.png'
BLACK_PATH = 'assets/animal-pack/PNG/black.png'

## seznam zvířátek: tohle je seznam dvojic (n-tic), ve kterých je vždy jméno
## zvířátka a číslo, které říká kde je střed obrázku: když zvíře velké zuby
## (které přesahují dolů), je číslo kladné; když má velké uši
## (které přesahují nahoru), je číslo záporné. Víc viz funkce image_load.
ANIMAL_INFO = (
    ('snake', 25),
    ('penguin', 0),
    ('monkey', 0),
    ('giraffe', -45),
    ('panda', -25),
    ('pig', -15),
    ('hippo', -10),
    ('parrot', 0),
    ('rabbit', -65),
    ('elephant', 0),
)


## Teď si načteme potřebné obrázky.
## Pro automatizaci toho, co chceme udělat s každým načteným obrázkem,
## si na to uděláme funkci.

def image_load(filename, offset=0):
    """Načte obrázek z daného souboru

    offset určuje, o kolik je posunutý střed obrázku
    """
    ## Načteme obrázek
    img = pyglet.image.load(filename)
    ## Nastavíme "kotevní bod", který říká, kam se obrázek nakreslí.
    ## U nás je to prostředek obrázku, takže když Pygletu řekneme aby obrázek
    ## nakreslil na souřadnice (100, 200), tak na těchto souřadnicích bude
    ## střed obrázku.
    ## V x-ové ose (doprava/doleva) je to vždycky prostředek:
    img.anchor_x = img.width // 2
    ## V y-ové ose (nahoru/dolů) nám někdy nesedí střed obrázku a střed
    ## čtverce, takže je potřeba přičíst "offset"
    img.anchor_y = img.height // 2 + offset
    ## Jo, a anchor_x/anchor_y v Pygletu musí být celá čísla (int), proto
    ## používáme celočíselné dělení (//).

    ## Nakonec obrázek vrátíme – to je celkem důležité.
    return img

## Načteme normální (čtvercové) obrázky: pro každé jméno z ANIMAL_INFO
## jeden obrázek
pictures = [image_load(IMG_PATH.format(name))
            for name, offset in ANIMAL_INFO]
## Načteme aktivní obrázky (s vyčuhujícíma ušima/zubama): tady použijeme
## offset, druhý prvek z dvojice v ANIMAL_INFO
active_pictures = [image_load(ACTIVE_PATH.format(name), offset)
                   for name, offset in ANIMAL_INFO]
## Pak načteme obrázek, který pak použijeme jako pozadí k vybranému obrázku
active_bg_img = image_load('assets/puzzle-pack-2/PNG/Tiles grey/tileGrey_01.png')
## A na pozadí rovnou vytvoříme i sprite – objekt, který můžeme vykreslit.
bg_sprite = pyglet.sprite.Sprite(active_bg_img)
grey_square = image_load(GREY_PATH)
black_square = image_load(BLACK_PATH)


## Mimochodem, obrázky jsou stažené z těchto zdrojů, a jsou k dispozici
## pod licencí CC0 (http://creativecommons.org/publicdomain/zero/1.0/):
## - http://opengameart.org/content/animal-pack
## - http://opengameart.org/content/puzzle-pack-2-795-assets
## Díky autorovi (http://www.kenney.nl/)!


## To by byly konstanty.
## Další věc, kterou budeme potřebovat, je několik funkcí na převod souřadnic.
## Obrázky totiž budeme kreslit na obrazovku, kde se vzdálenosti měří
## v pixelech, ale pro logiku hry budeme číslovat políčka, takhle:

##
##  -------------------------------------------------------------------------
##  |        |        |        |        |        |        |        |        |
##  | (0, 7) | (1, 7) | (2, 7) | (3, 7) | (4, 7) | (5, 7) | (6, 7) | (7, 7) |
##  |        |        |        |        |        |        |        |        |
##  -------------------------------------------------------------------------
##  |        |        |        |        |        |        |        |        |
##  | (0, 6) | (1, 6) | (2, 6) | (3, 6) | (4, 6) | (5, 6) | (6, 6) | (7, 6) |
##  |        |        |        |        |        |        |        |        |
##  -------------------------------------------------------------------------
##  |        |        |        |        |        |        |        |        |
##  | (0, 5) | (1, 5) | (2, 5) | (3, 5) | (4, 5) | (5, 5) | (6, 5) | (7, 5) |
##  |        |        |        |        |        |        |        |        |
##  -------------------------------------------------------------------------
##  |        |        |        |        |        |        |        |        |
##  | (0, 4) | (1, 4) | (2, 4) | (3, 4) | (4, 4) | (5, 4) | (6, 4) | (7, 4) |
##  |        |        |        |        |        |        |        |        |
##  -------------------------------------------------------------------------
##  |        |        |        |        |        |        |        |        |
##  | (0, 3) | (1, 3) | (2, 3) | (3, 3) | (4, 3) | (5, 3) | (6, 3) | (7, 3) |
##  |        |        |        |        |        |        |        |        |
##  -------------------------------------------------------------------------
##  |        |        |        |        |        |        |        |        |
##  | (0, 2) | (1, 2) | (2, 2) | (3, 2) | (4, 2) | (5, 2) | (6, 2) | (7, 2) |
##  |        |        |        |        |        |        |        |        |
##  -------------------------------------------------------------------------
##  |        |        |        |        |        |        |        |        |
##  | (0, 1) | (1, 1) | (2, 1) | (3, 1) | (4, 1) | (5, 1) | (6, 1) | (7, 1) |
##  |        |        |        |        |        |        |        |        |
##  -------------------------------------------------------------------------
##  |        |        |        |        |        |        |        |        |
##  | (0, 0) | (1, 0) | (2, 0) | (3, 0) | (4, 0) | (5, 0) | (6, 0) | (7, 0) |
##  |        |        |        |        |        |        |        |        |
##  -------------------------------------------------------------------------
##
## Levé spodní políčko, (0, 0), se ale vykreslí na obrazovku na pixelové
## souřadnice třeba (50, 50).


def get_tile_size(window):
    """Vrátí velikost políčka pro dané okno, v pixelech"""
    ## Abychom do herního okýnka dostali určitý počet políček vedle sebe,
    ## vydělíme šířku okýnka počtem sloupců a dostaneme velikost políčka.
    ## Abychom tam dostali určitý počet políček pot sebe, vydělíme šířku
    ## okýnka počtem sloupců.
    ## Když chceme, aby se vešla celá šachovnice, vezmeme menší z těchto
    ## hodnot – tak zajistíme že se šachovnice vejde v obou směrech.
    return min(window.width / COLUMNS, window.height / ROWS)


def logical_to_screen(logical_x, logical_y, window):
    """Převede logické (herní) souřadnice na pixely.

    Vrací dvojici (x, y), souřadnice středu daného políčka.
    """
    ## Budeme potřebovat velikost políčka, kterou umí vypočítat funkce
    ## get_tile_size.
    tile_size = get_tile_size(window)
    ## Spočítáme si, kde bude levé spodní políčko – (0, 0).
    ## Chceme šachovnici uprostřed okýnka, takže na pravé i levé straně
    ## má být stejně velká mezera (mezi šachovnicí a okrajem okna).
    ## Celková šířka obou mezer je šířka okýnka minus šířka šachovnice;
    ## polovina toho je šířka jedné mezery.
    ## A šířka šachovnice je šířka políčka krát počet políček.
    start_x = (window.width - tile_size * COLUMNS) / 2
    # To samé pro y-ovou souřadnici.
    start_y = (window.height - tile_size * ROWS) / 2
    ## A kde budeme vykreslovat naše políčko? Od začátku šachovnice
    ## odpočítáme "X"-krát šířku políčka (a "Y"-krát výšku políčka),
    ## a dostaneme pixelovou souřadnici levého dolního rohu našeho políčka.
    ## A protože chceme střed políčka, přidáme půlku velikosti políčka.
    screen_x = start_x + logical_x * tile_size + tile_size / 2
    screen_y = start_y + logical_y * tile_size + tile_size / 2
    # A výsledek vrátíme.
    return screen_x, screen_y


def screen_to_logical(screen_x, screen_y, window):
    """Převede pixelové souřadnice na logické (herní).

    Vrací dvojici (x, y); potřebuješ-li celá čísla, je potřeba výsledek ještě
    zaokrouhlit.
    """
    ## Začátek je stejný jako u logical_to_screen.
    tile_size = get_tile_size(window)
    start_x = (window.width - tile_size * COLUMNS) / 2
    start_y = (window.height - tile_size * ROWS) / 2
    ## Potom vezmeme vzorečky pro screen_x a screen_y z logical_to_screen,
    ## a vyjádříme z nich logical_x a logical_y.
    logical_x = (screen_x - start_x) / tile_size - 1/2
    logical_y = (screen_y - start_y) / tile_size - 1/2
    # A výsledek vrátíme.
    return logical_x, logical_y


## Tak, to by byly funkce, kde se skrývá většina matematiky z téhle hry :)
## Teď si nadefinujeme třídy, které budeme ve hře používat. Budou to tyto:
## - Tile (políčko) obsahuje všechny informace o jednom políčku šachovnice.
##   Bude umět políǩo vykreslit, posunout animaci, a případně bude obsahovat
##   všechnu herní logiku která se vztahuje jenom na jedno políčko.
## - Board (šachovnice) bude obsahovat seznamy všech políček ve hře
##   a logiku vztahující se k několika políčkům (nebo k výběru konkrétního
##   políčka). A bue umět vykreslit celou šachovnici, nebo posunout všechny
##   animace.
## - Animace: několik tříd, které se budou starat o animace políček.

## Objekty třídy Tile si neuchovávají informaci o tom, kde na šachovnici
## se nacházejí. To může na některýchmístech způsobit trochu složitější program
## (třeba při vykreslování je potřeba pozici pědat jako argument funkce),
## ale výhoda je ta, že informace o pozici každého políčka je v programu jen
## jednou (v objektu třídy Board). Kdyby byla stejná informace na víc místech,
## musí si programátor dávad pozor, aby si všechny výskyty vždy odpovídaly:
## když se něco změní na jednom místě, musí se to změnit i všude jinde.

class Tile:
    """Políčko šachovnice"""
    def __init__(self):
        ## Inicializační funkce
        ## Každé políčko může mít nastavenou jednu aktuální animaci.
        ## Když žádná animace neprobíhá, nastavíme políčko na None.
        self.animation = None
        ## Zbytek funkce je specifický pro naši hru.
        ## Každé políčko v této hře má číselnou hodnotu, které určuje
        ## jaké zvířátku na políčku je.
        ## Čím víc je možností, tím je hra těžší.
        self.value = random.randrange(8)
        ## Každé políčko má k dispozici dva "sprity" – obrázky, které
        ## se dají vykreslovat na danou pozici. Jeden s normálním obrázkem,
        ## jeden pro políčko které je zrovna pod myší.
        self.sprite = pyglet.sprite.Sprite(grey_square)
        self.active_sprite = pyglet.sprite.Sprite(active_pictures[self.value])
        self.sprite_done = pyglet.sprite.Sprite(black_square)



    def draw(self, x, y, window, selected=False, done=False):
        """Vykreslí tohle políčko na obrazovku, na dané souřadnici

        Argumenty: x, y jsou souřadnice; window je okno do kterého kreslíme,
        selected je True pokud je tohle políčko aktivní (t.j. právě pod myší).
        """
        ## Nejdřív vybereme obrázek (sprite), který budeme používat
        if selected:
            sprite = self.active_sprite
        elif done:
            sprite = self.sprite_done
        else:
            sprite = self.sprite

        sprite.rotation=0
        ## Nastavíme pozici spritu podle toho, kam máme kreslit.
        screen_x, screen_y = logical_to_screen(x, y, window)
        sprite.x = screen_x
        sprite.y = screen_y
        ## Nastavíme velikost obrázku. To se dělá pomocí atributu "scale",
        ## který určuje jak moc se obrázek zvětší: scale=1 znamená normální
        ## velikost, scale=2 dvojnásobnou, scale=1/2 poloviční.
        ## My víme jak má být políčko velké – nebo aspoň na to máme funkci.
        ## Od velikosti políčka odečteme velikost mezery mezi obrázky,
        ## aby vyšla velikost samotného obrázku.
        tile_size = get_tile_size(window) - SPACING
        ## ... a víme jak je velký jeden obrázek (vezmeme třeba šířku prvního
        ## obrázku v seznamu, hada) ...
        img_width = pictures[0].width
        ## ... takže stačí tahle čísla podělit:
        sprite.scale = tile_size / img_width

        ## A nakonec obrázek vykreslíme. Je-li aktivní animace, použijeme ji;
        ## jinak jen nakreslíme obrázek.
        if self.animation:
            self.animation.draw(self, x, y, window)
        else:
            sprite.draw()



class Board:
    """Šachovnice s herní logikou"""
    def __init__(self):
        self.turn_number = 0
        self.player_number = 0
        self.score = [0, 0]
        self.show = set()
        self.done = set()
        self.last_mouse_pos = (-1,-1)
        ## Inicializace: Vytvoříme seznam seznamů s objekty Tile.
        ## Bude to seznam sloupců šachovnice, kde každý sloupec je seznam
        ## jednotlivých políček.
        self.content = [[Tile() for i in range(ROWS)]
                        for j in range(COLUMNS)]

        self.selected_tile = None


    def draw(self, window):
        """Vykreslí celou šachovnici"""
        ## Nejdřív vykreslíme podklad pro vybrané políčko, pokud tedy
        ## nějaké vybrané je.
        if self.selected_tile is not None:
            ## Nastavíme spritu souřadnice
            logical_x, logical_y = self.selected_tile
            x, y = logical_to_screen(logical_x, logical_y, window)
            bg_sprite.x = x
            bg_sprite.y = y


        logical_x, logical_y = self.last_mouse_pos
        x, y = logical_to_screen(logical_x, logical_y, window)
        bg_sprite.x = x
        bg_sprite.y = y

        if self.player_number == 0:
            bg_sprite.color = 162, 201, 0
            bg_sprite.draw()
        else:
            bg_sprite.color = 255, 186, 0
            bg_sprite.draw()


        ## Teď projdeme celou šachovnici, a vykreslíme všechna políčka na ní.
        ## Použijeme funkci "enumerate", která bere nějakou sekvenci (např.
        ## seznam, a vrací sekvenci dvojic (index, prvek).
        ## Takže v tomhle cyklu bude "x" souřadnice (0, 1, 2, ...) a "column"
        ## sloupec:
        for x, column in enumerate(self.content):
            ## A v tomhle cyklu bude "y" souřadnice (0, 1, 2, ...) a "tile"
            ## už dané políčko.
            for y, tile in enumerate(column):
                ## Políčko stačí vykreslit.
                if (x, y) in self.show:
                    tile.draw(x, y, window, selected=True)
                elif (x,y) in self.done:
                    tile.draw(x, y, window, done=True)
                else:
                    tile.draw(x, y, window, selected=False)




    def action(self, x, y):
        """Udělá to, co se má stát po kliknutí na dané místo na šachovnici

        x a y jsou logické souřadnice
        """
        ## Kliknutí má efekt jen pokud hráč klikl dovnitř do šachovnice
        if not (0 <= x < COLUMNS and 0 <= y < ROWS):
            return
        ## Vezměme políčko, na které hráč kliknul
        self.current_tile = self.content[x][y]

        ## Pokud se tohle políčko právě animuje (padá, nebo se vyměňuje
        ## s jiným), tak kliknutí budeme ignorovat.
        #if current_tile.animation:
            #return
        ## Co uděláme dál závisí na tom, jestli už je něco vybrané.
        ## A je to specifické pro tuhle hru.

        if len(self.show) == 2:
            x1,y1=self.show.pop()
            x2,y2=self.show.pop()
            tile1=self.content[x1][y1]
            tile2=self.content[x2][y2]


            if tile1.value==tile2.value:
                self.done.add((x1,y1))
                self.done.add((x2,y2))
                self.score[self.player_number] +=1

        elif len(self.show) == 1:
            x1,y1 = list(self.show)[0]
            tile1 = self.content[x1][y1]

            if tile1.value==self.current_tile.value:
                self.turn_number += 2
                self.player_number=self.turn_number%2
            else:
                self.turn_number += 1
                self.player_number=self.turn_number%2

        if len(self.show) in (0,1):
            if (x, y) not in self.done:
                self.show.add((x,y))



## A teď už zbývá jen vytvořit objekt typu Board (což vytvoří celou
## šachovnici i s obsahem), nějaké to grafické okýnko, a říct Pygletu
## jak to všechno spolu souvisí.

def main():
    """Hlavní funkce programu – celá hra"""
    ## Vytvoříme si hru a okýnko
    board = Board()
    window = pyglet.window.Window()

    ## To, co se má stát když nastane nějaká událost, Pygletu řekneme
    ## pomocí dekorátoru @window.event.
    ## Ten udělá to, že přiřadí funkci k události stejného jména.
    ## Seznam událostí je v dokumentaci Pygletu:
    ## https://pyglet.readthedocs.org/en/pyglet-1.2-maintenance/api/pyglet/window/pyglet.window.Window.html
    ## (sekce Events)

    @window.event
    def on_draw():
        """Zavolá se, když je potřeba překreslit okno"""
        ## Smazat případný předchozí obsah
        window.clear()
        ## Vykreslit šachovnici
        board.draw(window)

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        """Zavolá se, když hráč pohne myší"""
        ## Vezmeme si logické souřadnice
        logical_x, logical_y = screen_to_logical(x, y, window)
        ## Zaokrouhlíme je na celá čísla
        logical_x = round(logical_x)
        logical_y = round(logical_y)
        ## A pak nastavíme poslední známou pozici myši
        board.last_mouse_pos = logical_x, logical_y

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        """Zavolá se, když hráč klikne myší"""
        ## Vezmeme si logické souřadnice
        logical_x, logical_y = screen_to_logical(x, y, window)
        ## Zaokrouhlíme je na celá čísla
        logical_x = round(logical_x)
        logical_y = round(logical_y)
        ## A delegujeme na šachovnici...
        board.action(logical_x, logical_y)


    ## A pak řekneme Pygletu, ať čeká na události a volá příslušné
    ## funkce.
    pyglet.app.run()

## 3, 2, 1... Start!
main()
