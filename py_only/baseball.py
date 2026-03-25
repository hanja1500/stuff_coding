import random
from tkinter import *

num = 0             #게임 시작시 이닝수를 확인하기 위한 변수
check = 0
tmp = 0

fir_team = [0, 0, 0, 0, 0, 0, 0, 0, 0]      # 각 이닝에 대한 점수 저장 변수
sec_team = [0, 0, 0, 0, 0, 0, 0, 0, 0]

fir_score = 0       
sec_score = 0

fir_total = 0
sec_total = 0

t = 0

chance = 0

out = 0
strike = 0
ball = 0

fir_run = 0
sec_run = 0
thi_run = 0

fspotx = 0
fspoty = 0

curve = 'f'
hit = 5
final = 100

def sb_check():
    global hit
    global final

    global fir_run

def auto():
    print("지나갑니다~")

def auto_2():
    print("넌 못지나간다~")

def game():
    global num
    global check
    global tmp

    num = int(input("사용자는 투수부터 시작합니다. 몇 회부터 시작할까요? (1~9회) : "))

    num = (num-1)*2
    check = 18-num

    for x in range(num):
        print(num)
        auto()
    for y in range(check):
        print(check)
        auto_2()

def info():
    print("이 야구 게임은 스트라이크 존 9칸과 그 주변 볼 존 16칸 총 25칸에 공을 던지거나 칠 수 있습니다.")
    print("좌상단부터 1이고, 왼쪽에서 오른쪽, 위에서 아래로 숫자가 차례로 정해집니다.")
    print("칸에 해당하는 숫자를 누르면 공의 위치가 결정됩니다.")
    print("이 게임에서 투수의 구종은 포심, 투심, 체인지업, 커브, 슬라이더 총 5가지의 구종이 존재합니다.")
    print("포심은 정한 위치에 그대로 들어가고, 투심은 오른쪽으로 1칸 이동합니다.")
    print("체인지업은 아래로 1칸 이동하고, 커브는 아래로 2칸, 슬라이더는 좌하향으로 2칸 이동합니다.")
    print("만약 공을 던져서 25칸 이내로 들어가지 않을 경우 무작위로 어느 칸에 들어갑니다. (제구 난조)")
    print("")
    print("타지의 경우 투수와 같이 자신이 칠 칸을 숫자로 정합니다.")
    print("던진 공의 위치와 치는 위치가 같을 경우 : 75%의 확률로 2루타, 20%의 확률로 3루타, 5%의 확률로 홈런입니다.")
    print("던진 공의 위치와 치는 위치가 1칸 엇나갈 경우 : 50%의 확률로 스트라이크 또는 볼(포수 포구), 30%의 확률로 1루타, 15%의 확률로 아웃, 5%의 확률로 2루타입니다.")
    print("던진 공의 위치와 치는 위치가 2칸 엇나갈 경우 : 90%의 확률로 스트라이크 또는 볼(포수 포구), 10%의 확률로 아웃입니다.")
    print("그 이상의 차이가 날 경우 무조건 스트라이크 또는 볼(포수 포구)입니다.")


###############################################
while True :
    print()
    print("                           야                    구                  ")
    print()
    inn = input("게임 시작을 원하신다면 start,\n게임에 대한 설명을 듣고 싶으시다면 info를 입력해주세요 : ")
    if inn == 'info':
        info()
    elif inn == 'start':
        game()
        break
