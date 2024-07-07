#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#pip install datetime 
#pip install requests
#pip install beautifulsoup4  
#설치 안됐으면 설치해야된다

from tkinter import *
import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# 창 생성하기
win = Tk()
win.title("로또 모의 연습") #창 제목
win.geometry("800x900") #창 크기 
win.option_add("*Font", "Arial 20")  #기본 글자 크기 설정

# 캔버스 생성하기
cvs = Canvas(win)
bg_color="blue" #배경색 설정 
cvs.configure(background=bg_color)
cvs.config(bd=0, highlightthickness=0)  #이걸 해줘야 캔버스 전체 꽉 차게 채워진다
cvs.pack(fill=BOTH, expand=True)

selected_numbers = []  #내가 선택한 번호 
buttons = []   #숫자 버튼들

# 숫자 버튼 클릭시 
def select_number(btn, num):  #ex) buttons[0], 1일 때 
    #선택되지 않은 숫자, 그리고 이미 선택한 숫자가 6보다 작을 때. 왜냐면 5에서 지금 선택한것까지 추가하면 6되니까. 
    if num not in selected_numbers and len(selected_numbers) < 6: 
        selected_numbers.append(num) #선택한 번호들 리스트에 추가해주고 
        btn.config(bg='#FF3366') #선택된 버튼 색깔 바꾸기 
    elif num in selected_numbers: #이미 선택한 숫자일때 
        selected_numbers.remove(num) #선택한 번호들 리스트에서 빼주고 
        btn.config(bg='SystemButtonFace') #원래 색으로 바꿔주기. 시스템 기본 설정색. 
    count_label.config(text=f"{len(selected_numbers)}/6")  #선택된 버튼 개수 텍스트 바꿔주기 

# 자동 선택 함수
def auto_select():
    global selected_numbers
    #버튼 색 리셋. 이걸 안하면 자동 버튼 누를때마다 계속 추가된다. 
    #buttons에는 1~46개의 버튼들이 들어있다. 모든 버튼의 색들을 기본 색상으로 바꿔주는 과정이다.
    for btn in buttons: 
        btn.config(bg='SystemButtonFace')
    selected_numbers = random.sample(range(1, 47), 6) #랜덤하게 6개 숫자 선택. 1-46 범위 안에서. 
    for num in selected_numbers: 
        buttons[num-1].config(bg='#FF3366')  #선택한 것들 버튼 색깔 바꿔주기
    count_label.config(text=f"{len(selected_numbers)}/6")  #텍스트도 바꿔주기 

# 몇 회차 로또 번호를 확인해야 될까
def number(today):
    base_date = datetime(2024, 6, 22)  # 2024-06-22 1125회차을 기준. 
    base_number = 1125
    input_date = datetime.strptime(today, "%Y%m%d")  # 입력된 날짜를 datetime 객체로 변환
    #datetime 객체를 사용하지 않으면 2024년 1월 1일 - 2023년 12월 22일 같은 계산을 할 때 복잡해진다
    delta_days = (input_date - base_date).days  # 기준 날짜와 입력된 날짜 사이의 차이 계산
    draw_number = base_number + delta_days // 7  # 날짜 차이를 일주일 단위로 나누어 회차 계산
    return draw_number


# 로또 번호 확인
def what_number(n):
    global num_list, bonus
    url = "https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={}".format(n)  #주소
    req = requests.get(url)  #url 주소의 html 문서 가져오기
    soup = BeautifulSoup(req.text, "html.parser")  #req.text 응답을 텍스트화. #"html.parser" 형식으로 아름답게 정리
    txt = soup.find("div", attrs={"class": "win_result"}).get_text()  #원하는 부분 가져오기. 당첨 번호 써있는 부분. 
    #안에 들어가 있는 모든 텍스트 (여는 태그 < >와 닫는 태그<  / > 사이에 있는 텍스트) 추출
    # \n을 기준으로 split 함수를 적용하면 \n 기준으로 양 옆에 있는 문자열을 리스트로 나눠준다
    txt_list = txt.split("\n") 
    num_list = [int(num) for num in txt_list[7:13]] #인덱싱으로 원하는 부분 추출. 당첨 번호 부분
    bonus = int(txt_list[-4]) #인덱싱으로 보너스 번호 추출.

    number = '  '.join(map(str, num_list)) + " / 보너스: " + str(bonus)
    return number


# 등수 함수
def rank():
    #당첨 번호 중 맞은 개수, bonus 맞은 개수 세기 
    count=0
    bonus_count=0
    for num in selected_numbers:
        if num in num_list:
            count += 1
        if num == bonus:
            bonus_count += 1
    cvs.create_text((400, 500), text="맞은 개수: " + str(count), font=("Arial", 25), fill="white")
    
    if count == 6:
        return "1등"
    elif count == 5 and bonus_count == 1:  #5개 맞고 하나가 보너스 번호면 2등
        return "2등"
    elif count == 5:
        return "3등"
    elif count == 4:
        return "4등"
    elif count == 3:
        return "5등"
    else:
        return "낙첨"

# 리셋 함수
def reset():
    for wg in win.grid_slaves():  # 전체 창 내부에 있는 위젯 하나씩 불러와서
        wg.destroy()  # 위젯 제거
    cvs.delete("all")  # 캔버스의 모든 요소 삭제
    cvs.configure(background="black")  #캔버스 배경색 바꾸기

# 확인 버튼 함수
def show_selected():
    date = date_entry.get()  #날짜 입력창에 써있는 텍스트 가져오기
    #날짜 형식 안맞을 때 
    try:
        datetime.strptime(date, "%Y%m%d")
    except ValueError:
        print("날짜 형식이 잘못되었습니다. YYYYMMDD 형식으로 입력해주세요.")
        return
    
    #형식에 맞을 때. 번호 6개 다 골랐을 때.
    if len(selected_numbers) == 6:
        print(f"날짜: {date}")
        print(f"선택된 번호: {selected_numbers}") #내 번호 

        n = number(date)  # 회차 
        answer = what_number(n)  #당첨 번호
        print(answer)

        # 화면 리셋과 번호 및 당첨 확인 결과 출력
        reset()
        cvs.create_text((400, 200), text=str(n) + "회차 당첨번호" , font=("Arial", 25), fill="white")
        cvs.create_text((400, 300), text=str(answer), font=("Arial", 25), fill="white")
        cvs.create_text((400, 400), text="내 번호: " + str(selected_numbers), font=("Arial", 25), fill="white")
        cvs.create_text((400, 600), text="등수: " + str(rank()), font=("Arial", 25), fill="white")
    else:
        print("숫자 6개를 모두 선택해주세요.")

# 현재 날짜 설정 함수
def set_current_time():
    current_time = datetime.now().strftime("%Y%m%d")  #현재 날짜  
    date_entry.delete(0, END)  #입력창에 있는 거 지우고 
    date_entry.insert(0, current_time)  #입력창에 현재 날짜 불러오기

# 선택된 개수 표시 라벨
count_label = Label(win, text="0/6", bg=bg_color, fg="white")  #처음에는 0/6. 버튼 클릭하면 텍스트를 바꿔줌. 1/6.. 2/6 이렇게
cvs.create_window(700,50, window=count_label) #count_label.place(x=700, y=50) 이렇게 해도 되는데 그냥 다 캔버스 위에 배치


# 버튼 생성 및 배치
#46개의 버튼. 프레임 생성. 하나로 묶어서. 위치 설정시 같이 이동시킬 수 있어서 편리. 
button_frame = Frame(cvs, bg=bg_color)
cvs.create_window(400, 150, window=button_frame, anchor=N) #북쪽을 기준으로. 

for i in range(1, 47):
    btn = Button(button_frame, text=str(i), width=5, height=2)
    buttons.append(btn)
    #버튼 클릭시 select_number 함수 실행. select_number(btn, num)  
    #i가 1일 때. select_number(buttons[0], 1). 이렇게 매개변수가 설정됨. buttons[0]=1번째 버튼 
    btn.configure(command=lambda b=i: select_number(buttons[b-1], b))
    #버튼 묶음 배치. 7개씩 끊어서 배치. 1부터 7까지는 0행. 8부터 14까지는 2행
    #그리고 1은 i가 1때 0열. i가 2일 때 1열. 여백 적당히 주고. 
    btn.grid(row=(i-1)//7, column=(i-1)%7, padx=5, pady=5)
    

# 자동 선택 버튼
auto_button = Button(win, text="자동", command=auto_select, width=5, height=1)
cvs.create_window(600, 110, window=auto_button) #캔버스에 버튼 배치

# 확인 버튼
confirm_button = Button(win, text="확인", command=show_selected, width=5, height=1)
cvs.create_window(700, 110, window=confirm_button)

# 날짜 입력 라벨 및 입력창
date_label = Label(win, text="날짜 입력", bg=bg_color, fg="white") #라벨
cvs.create_window(100, 110, window=date_label)
date_entry = Entry(win) #입력창
date_entry.insert(0, "20220903")  #기본값으로 20220903 입력. 이런 형식으로 입력하면 된다는 힌트를 줌.
def clear(event):
    if date_entry.get() == "20220903": #기본 값일때만 지운다. 쓰는 중인데 입력창 누를때마다 다 지워버리면 안되니까.
        date_entry.delete(0,len(date_entry.get())) #0(위치. 맨 처음)부터 끝까지 다 지우기
date_entry.bind("<Button-1>", clear) #입력창을 클릭하면 clear 함수 실행
cvs.create_window(350, 110, window=date_entry) #라벨 캔버스에 배치 

# 현재 시간으로 설정 라벨이랑 라벨. 하나로 묶었다.
time_frame = Frame(cvs, bg=bg_color) 
cvs.create_window(220, 50, window=time_frame) #한번에 배치하려고 

time_label = Label(time_frame, text="현재 시간으로 설정하기", bg=bg_color, fg="white")
time_label.pack(side=LEFT)

set_time_button = Button(time_frame, command=set_current_time)  #설정 버튼 클릭시 set_current_time함수 실행하기
set_time_button.configure(text="", bg="red", width=3, height=1)
set_time_button.pack(side=LEFT, padx=10)

win.mainloop()


# In[ ]:




