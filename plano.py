import pyautogui as py
import time as t
import keyboard as k
import threading
import os

# Pasta onde estão as imagens (mesma pasta do script)
BASE = os.path.dirname(os.path.abspath(__file__))

def img(nome):
    return os.path.join(BASE, nome)

def localizar_imagem(nome_imagem, confianca=0.8, grayscale=False):
    try:
        tela = py.screenshot(allScreens=True)
        box = py.locate(img(nome_imagem), tela, confidence=confianca, grayscale=grayscale)
        if box:
            return py.center(box)
        return None
    except py.ImageNotFoundException:
        return None
    except Exception as e:
        print(f"Aviso ao procurar {nome_imagem}: {e}")
        return None

i = 20
stop_flag = False

def monitorar_parada():
    global stop_flag
    k.wait('esc')  # Aguarda ESC ser pressionado
    stop_flag = True
    print("⛔ Parada solicitada! Finalizando após a iteração atual...")

# Inicia monitoramento em thread separada
thread_parada = threading.Thread(target=monitorar_parada, daemon=True)
thread_parada.start()

def teclado_acao():
    t.sleep(1)
    k.send('down')
    t.sleep(2)
    k.send('up')
    t.sleep(2)
    k.send('right')
    t.sleep(2)

def clicar(x, y):
    t.sleep(2)
    py.click(x, y)

def clicar_proximo():
    if stop_flag:
        return

    sv = localizar_imagem('salvar.png', confianca=0.8)
    if sv:
        clicar(sv.x, sv.y)
    else:
        print("Imagem 'salvar.png' não encontrada.")

    t.sleep(5)

    imagem = localizar_imagem('proximo.png', confianca=0.8)
    t.sleep(2)
    k.send('enter')
    t.sleep(3)

    if imagem:
        clicar(imagem.x, imagem.y)
    else:
        print("Imagem 'proximo.png' não encontrada.")

    t.sleep(6)

def checkbox1():
    if stop_flag:
        return

    imagem = localizar_imagem('SuperiorClicado.png', confianca=0.8, grayscale=True)
    if imagem:
        clicar(imagem.x, imagem.y)
    else:
        print("Imagem 'SuperiorClicado.png' não encontrada.")

    t.sleep(1)

    bolaUm = localizar_imagem('PrimeiraBola.png', confianca=0.8)
    if bolaUm:
        clicar(bolaUm.x, bolaUm.y)
    else:
        print("Imagem 'PrimeiraBola.png' não encontrada.")

    teclado_acao()
    k.send('space')
    k.send('space')

print("▶ Rodando... Pressione F12 para parar.")

while i > 0 and not stop_flag:
    print(f"Iteração {i}")
    checkbox1()
    clicar_proximo()
    i -= 1

print("✅ Script finalizado.")