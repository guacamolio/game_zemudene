from tkinter import *
from random import randint
from time import sleep, time
from math import sqrt
from PIL import Image, ImageTk
import os

MIN_BURBUĻA_RĀDIUSS = 10
MAX_BURBUĻA_RĀDIUSS = 30
MAX_BURBUĻA_ĀTRUMS = 10
ATSTARPE = 100

BURBUĻI_NEJAUŠI = 10
LAIKA_IEROBEŽOJUMS = 30
PAPILDLAIKA_REZULTĀTS = 200

KUĢA_RĀDIUSS = 50 
KUĢA_ĀTRUMS = 25

BISTAMS_BURBULIS = True
BISTAMS_BURBULIS_IESP = 5  

def play_again():
    global rezultats, papildu, beigas, spele_turpinas, burbuļa_id, burbuļa_rādiuss, burbuļa_ātrums, burbuļa_krāsa

    rezultats = 0
    papildu = 0
    beigas = time() + LAIKA_IEROBEŽOJUMS
    spele_turpinas = True

    for burbulis in burbuļa_id:
        a.delete(burbulis)
    burbuļa_id = []
    burbuļa_rādiuss = []
    burbuļa_ātrums = []
    burbuļa_krāsa = []

    for item in a.find_all():
        if item not in {kuģa_id, laiks_teksts, rezultats_teksts}: 
            a.delete(item)

    paradit_rezultatu(rezultats)
    paradit_laiku(int(beigas - time()))

    a.create_text(50, 30, text='LAIKS', fill='white') 
    a.create_text(150, 30, text='REZULTĀTS', fill='white') 
    while time() < beigas and spele_turpinas:
        if randint(1, BURBUĻI_NEJAUŠI) == 1:
            izveidot_burbuli()

        parvietot_burbulus()
        notirit_burbulus()

        rezultats += sadursme()
        if not spele_turpinas:
            break

        if (int(rezultats / PAPILDLAIKA_REZULTĀTS)) > papildu:
            papildu += 1
            beigas += LAIKA_IEROBEŽOJUMS

        paradit_rezultatu(rezultats)
        paradit_laiku(int(beigas - time()))

        logs.update()
        sleep(0.1)

def end_game():
    top_scores = read_and_update_scoreboard(rezultats)

    a.create_text(screen_width // 2, screen_height // 2,
                  text='SPĒLES BEIGAS', fill='white', font=('Helvetica', 30))
    a.create_text(screen_width // 2, screen_height // 2 + 30,
                  text=f'Rezultāts: {rezultats}', fill='white')
    a.create_text(screen_width // 2, screen_height // 2 + 45,
                  text=f'Papildu laiks: {papildu * LAIKA_IEROBEŽOJUMS}', fill='white')

    y_offset = 80
    a.create_text(screen_width // 2, screen_height // 2 + y_offset,
                  text='TOP 3 rezultāti:', fill='white')
    y_offset += 20
    for i, sc in enumerate(top_scores):
        a.create_text(screen_width // 2, screen_height // 2 + y_offset,
                      text=f"{i+1}. {sc}", fill='white')
        y_offset += 20

    btn_play_again = Button(logs, text="Play Again", font=("Helvetica", 14),
                            command=play_again)
    btn_play_again_window = a.create_window(screen_width // 2 - 60,
                                           screen_height // 2 + y_offset,
                                           window=btn_play_again)

    btn_quit = Button(logs, text="Quit Game", font=("Helvetica", 14),
                      command=logs.destroy)
    btn_quit_window = a.create_window(screen_width // 2 + 60,
                                      screen_height // 2 + y_offset,
                                      window=btn_quit)

def read_and_update_scoreboard(current_score):
    filename = "scoreboard.txt"
    if not os.path.exists(filename):
        open(filename, 'w').close()

    with open(filename, 'r') as f:
        lines = f.read().splitlines()

    scores = []
    for ln in lines:
        try:
            scores.append(int(ln))
        except:
            pass

    scores.append(current_score)
    scores.sort(reverse=True)
    top3 = scores[:3]

    with open(filename, 'w') as f:
        for s in top3:
            f.write(str(s) + "\n")

    return top3

logs = Tk()

screen_width = logs.winfo_screenwidth()
screen_height = logs.winfo_screenheight()

logs.geometry(f"{screen_width}x{screen_height}")
logs.title('Burbuļu spridzinātājs')

a = Canvas(logs, width=screen_width, height=screen_height, bg='darkblue')
a.pack()

attēls = Image.open("zemudene.png")
new_size = (90, 90)
attēls = attēls.resize(new_size, Image.Resampling.LANCZOS)
zemūdene_attēls = ImageTk.PhotoImage(attēls)

kuģa_id = a.create_image(screen_width // 2, screen_height // 2, image=zemūdene_attēls)

burbuļa_id = []
burbuļa_rādiuss = []
burbuļa_ātrums = []
burbuļa_krāsa = []

rezultats = 0
papildu = 0
beigas = time() + LAIKA_IEROBEŽOJUMS
spele_turpinas = True  

a.create_text(50, 30, text='LAIKS', fill='white')
a.create_text(150, 30, text='REZULTĀTS', fill='white')
laiks_teksts = a.create_text(50, 50, fill='white')
rezultats_teksts = a.create_text(150, 50, fill='white')

def parvietot_kugi(notikums):
    x, y = iegut_koordinates(kuģa_id)

    if (notikums.keysym == 'Up' or notikums.keysym == 'w' or notikums.keysym == 'W') and y - KUĢA_RĀDIUSS > 0:
        a.move(kuģa_id, 0, -KUĢA_ĀTRUMS)
    elif (notikums.keysym == 'Down' or notikums.keysym == 's' or notikums.keysym == 'S') and y + KUĢA_RĀDIUSS < screen_height:
        a.move(kuģa_id, 0, KUĢA_ĀTRUMS)
    elif (notikums.keysym == 'Left' or notikums.keysym == 'a' or notikums.keysym == 'A') and x - KUĢA_RĀDIUSS > 0:
        a.move(kuģa_id, -KUĢA_ĀTRUMS, 0)
    elif (notikums.keysym == 'Right' or notikums.keysym == 'd' or notikums.keysym == 'D') and x + KUĢA_RĀDIUSS < screen_width:
        a.move(kuģa_id, KUĢA_ĀTRUMS, 0)


def izveidot_burbuli():
    x = screen_width + ATSTARPE
    y = randint(0, screen_height)
    r = randint(MIN_BURBUĻA_RĀDIUSS, MAX_BURBUĻA_RĀDIUSS)

    if BISTAMS_BURBULIS and randint(1, BISTAMS_BURBULIS_IESP) == 1:
        krasa = 'red'
    else:
        krasa = 'blue'

    burbulis = a.create_oval(x - r, y - r, x + r, y + r, outline='white', fill=krasa)

    burbuļa_id.append(burbulis)
    burbuļa_rādiuss.append(r)
    burbuļa_ātrums.append(randint(1, MAX_BURBUĻA_ĀTRUMS))
    burbuļa_krāsa.append(krasa)

def parvietot_burbulus():
    for i in range(len(burbuļa_id)):
        a.move(burbuļa_id[i], -burbuļa_ātrums[i], 0)

def iegut_koordinates(obj_id):
    pozicija = a.coords(obj_id)
    if len(pozicija) == 2:
        return pozicija[0], pozicija[1]
    elif len(pozicija) >= 4:
        x = (pozicija[0] + pozicija[2]) / 2
        y = (pozicija[1] + pozicija[3]) / 2
        return x, y
    else:
        return 0, 0

def dzest_burbuli(i):
    del burbuļa_rādiuss[i]
    del burbuļa_ātrums[i]
    del burbuļa_krāsa[i]
    a.delete(burbuļa_id[i])
    del burbuļa_id[i]

def notirit_burbulus():
    for i in range(len(burbuļa_id) - 1, -1, -1):
        x, _ = iegut_koordinates(burbuļa_id[i])
        if x < -ATSTARPE: 
            dzest_burbuli(i)

def attalums(id1, id2):
    x1, y1 = iegut_koordinates(id1)
    x2, y2 = iegut_koordinates(id2)
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def sadursme():
    global spele_turpinas
    punkti = 0
    for i in range(len(burbuļa_id) - 1, -1, -1):
        dist = attalums(kuģa_id, burbuļa_id[i])
        
        if dist < (KUĢA_RĀDIUSS + burbuļa_rādiuss[i]):
            if burbuļa_krāsa[i] == 'red':
                spele_turpinas = False
                return punkti
            else:
                punkti += (burbuļa_rādiuss[i] + burbuļa_ātrums[i])
                dzest_burbuli(i)
    return punkti

def paradit_rezultatu(r):
    a.itemconfig(rezultats_teksts, text=str(r))

def paradit_laiku(laiks_palicis):
    a.itemconfig(laiks_teksts, text=str(laiks_palicis))

a.bind_all('<Key>', parvietot_kugi)

while time() < beigas and spele_turpinas:
    if randint(1, BURBUĻI_NEJAUŠI) == 1:
        izveidot_burbuli()

    parvietot_burbulus()
    notirit_burbulus()

    rezultats += sadursme()
    if not spele_turpinas:
        break

    if (int(rezultats / PAPILDLAIKA_REZULTĀTS)) > papildu:
        papildu += 1
        beigas += LAIKA_IEROBEŽOJUMS

    paradit_rezultatu(rezultats)
    paradit_laiku(int(beigas - time()))

    logs.update()
    sleep(0.1)

end_game()
end_game()

logs.mainloop()

#Pievienoju attēlu zēmūdenei bet zem attēla ir aplis kas uztver visus burbulus ka ari ievero speles borderus
#Arī pievienoju lai varētu pārvietoties ar wasd pogām kā arī jigadijumā ir ieslēgts caps lock vai vienkārši tur shift tad strādās parvietošanās jo var parvietoties ar lielajiem WASD burtiem arī
#Pievienoju arī sarkanos burbuļus kuriem zemūdene uzbraucot virsū beidzas spēle
#Kad beidzas spēle tiek parādīts high scores un atlikušais laiks kā arī pogas quit game un play again
#Pašu spēles width un height es arī nomainīju lai ietilptu pa visu ekrānu

