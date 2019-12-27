from tkinter import *
import tkinter.font as font
from collections import defaultdict

window = Tk()

HumanT20 = font.Font(family='휴먼모음T', size=20)
HumanT12 = font.Font(family='휴먼모음T', size=12)
ClearGothic10 = font.Font(family='맑은 고딕', size=10)
NanumGothic12 = font.Font(family='NanumbarunGothic', size=11)

#window.option_add( "*font", ClearGothic10)
#window.option_add( "*font", HumanT12)
window.option_add( "*font", NanumGothic12)
window.title("전공진입요건 계산 프로그램")
window.geometry("910x720")

selected_계열 = StringVar()
selected_계열.set("계열 선택")
selected_계열_string = StringVar()
selected_계열_string.set("[계열을 입력하세요]")

selected_지원학과 = StringVar()
selected_지원학과.set("지원학과 선택")

explain_전공진입요건 = StringVar()
explain_전공진입요건.set("")
explain_전공진입요건_1 = "의사소통 4학점, 기본영어+전문영어 4학점, 창의와사유 2학점,\n소프트웨어기초 2학점, 기초인문사회과학 6학점"
explain_전공진입요건_2 = "의사소통 4학점, 기본영어+전문영어 4학점, 창의와사유 2학점,\n소프트웨어기초 2학점, 기초자연과학 12학점"
explain_전공진입요건_3 = "의사소통 4학점, 기본영어+전문영어 4학점,\n창의와사유 2학점, 기초자연과학 15학점, 창의적공학설계"

major_entrance_rule_HS = ['의사소통', '기본영어', '전문영어', '창의와사유', '소프트웨어기초', '기초인문사회과학']
major_entrance_rule_N = ['의사소통', '기본영어', '전문영어', '창의와사유', '소프트웨어기초', '기초자연과학']
major_entrance_rule_E = ['의사소통', '기본영어', '전문영어', '창의와사유', '기초자연과학', '창의적공학설계']


explain_전공진입요건_dict = {
    "인문과학계열": explain_전공진입요건_1,
    "사회과학계열": explain_전공진입요건_1,
    "자연과학계열": explain_전공진입요건_2,
    "공학계열": explain_전공진입요건_3,
}

GPA_score = {'A+': 4.5, 'A': 4.0, 'B+': 3.5, 'B': 3.0, 'C+': 2.5, 'C': 2.0, 'D+': 1.5, 'D': 1.0, 'F': 0.0}

authorityHSN = [
    ['기본영어', '2', '영어쓰기'],
    ['소프트웨어기초', '2', '컴퓨팅사고와SW코딩'],
    ['일반선택', '1', 'FYE세미나I', 'P(P/F)'],
    ['기본영어', '2', '영어발표'],
    ['소프트웨어기초', '2', '문제해결과알고리즘'],
    ['일반선택', '1', 'FYE세미나II', 'P(P/F)']
]

authorityE = [
    ['기본영어', '2', '영어쓰기'],
    ['기초자연과학', '3', '공학컴퓨터프로그래밍'],
    ['일반선택', '1', 'FYE세미나I', 'P(P/F)'],
    ['기본영어', '2', '영어발표'],
    ['기초자연과학', '3', '프로그래밍기초와실습'],
    ['일반선택', '1', 'FYE세미나II', 'P(P/F)'],
    ['전공', '3', '창의적공학설계']
]

def change_계열(a):
    selected_계열_string.set("[{} 전공진입 요건]".format(a))
    explain_전공진입요건.set(explain_전공진입요건_dict[a])

    if a != '공학계열':
        for i in range(6):
            tmp_list = authorityHSN[i]
            if i >= 3:
                i += 9
            territory_string[i].set(tmp_list[0])
            credit_string[i].set(tmp_list[1])
            name_string[i].set(tmp_list[2])
            if tmp_list[0] == '일반선택':
                gpa_string[i].set(tmp_list[3])
    else:
        for i in range(6):
            tmp_list = authorityE[i]
            if i >= 3:
                i += 9
            territory_string[i].set(tmp_list[0])
            credit_string[i].set(tmp_list[1])
            name_string[i].set(tmp_list[2])
            if tmp_list[0] == '일반선택':
                gpa_string[i].set(tmp_list[3])

        territory_string[23].set(authorityE[6][0])
        credit_string[23].set(authorityE[6][1])
        name_string[23].set(authorityE[6][2])




title = Label(window, text="전공진입요건 계산 프로그램", font=HumanT20, height=2)
title.grid(row=0, column=0, columnspan=99)

계열 = Label(window, text=" 계열: ")
계열.grid(row=1, column=1)
계열option = OptionMenu(window, selected_계열, "인문과학계열", "사회과학계열", "자연과학계열", "공학계열", command=change_계열)
계열option.grid(row=1, column=2, columnspan=2)
지원학과 = Label(window, text=" 지원학과: ")
지원학과.grid(row=1, column=4, columnspan=2)
지원학과option = OptionMenu(window, selected_지원학과, "소속대학 원전공", "글로벌융합학부")
지원학과option.grid(row=1, column=6)

전공진입요건_label = Label(window, textvariable=selected_계열_string, height=2)
전공진입요건_label.grid(row=2, column=0, columnspan=99)
전공진입요건_explainLabel = Label(window, textvariable=explain_전공진입요건, height=3)
전공진입요건_explainLabel.grid(row=3, column=0, columnspan=99)

영역_label = Label(window, text="영역")
학점_label = Label(window, text="학점")
과목명_label = Label(window, text="과목명")
평점_label = Label(window, text="평점")
영역_label2 = Label(window, text="영역")
학점_label2 = Label(window, text="학점")
과목명_label2 = Label(window, text="과목명")
평점_label2 = Label(window, text="평점")
영역_label.grid(row=4, column=0)
학점_label.grid(row=4, column=1)
과목명_label.grid(row=4, column=2)
평점_label.grid(row=4, column=3)
영역_label2.grid(row=4, column=4)
학점_label2.grid(row=4, column=5)
과목명_label2.grid(row=4, column=6)
평점_label2.grid(row=4, column=7)

territory = []
credit = []
name = []
gpa = []

territory_string = []
credit_string = []
name_string = []
gpa_string = []

for i in range(24):
    territory_string.append(StringVar())
    territory_string[i].set("영역 선택")
    credit_string.append(StringVar())
    credit_string[i].set("0")
    name_string.append(StringVar())
    gpa_string.append(StringVar())
    gpa_string[i].set("A+")

    territory.append(OptionMenu(window, territory_string[i], "인성", "리더십", "기본영어", "전문영어", "글로벌문화",
                                "의사소통", "창의와사유", "소프트웨어기초", "기초인문사회과학", "기초자연과학",
                                "인간/문화", "사회/역사", "자연/과학/기술", "일반선택", "기타교양", "전공"))
    credit.append(Entry(window, textvariable=credit_string[i], width=3, justify='center'))
    name.append(Entry(window, textvariable=name_string[i]))
    gpa.append(OptionMenu(window, gpa_string[i], "A+", "A", "B+", "B", "C+", "C", "D+", "D", "F", "P(P/F)", "F(P/F)"))

    territory[i].config(width=12)
    gpa[i].config(width=4)

    if i <= 11:
        territory[i].grid(row=i+5, column=0)
        credit[i].grid(row=i+5, column=1)
        name[i].grid(row=i+5, column=2)
        gpa[i].grid(row=i+5, column=3)
    else:
        territory[i].grid(row=i-7, column=4)
        credit[i].grid(row=i-7, column=5)
        name[i].grid(row=i-7, column=6)
        gpa[i].grid(row=i-7, column=7)


result_of_calculation = StringVar()

Calculate_button = Button(window, text='전공진입요건 충족여부 계산하기!')
Calculate_button.grid(row=17, column=0, columnspan=99)

Calculate_result = Label(window, textvariable=result_of_calculation)
Calculate_result.grid(row=18, column=0, columnspan=99)


window.mainloop()
