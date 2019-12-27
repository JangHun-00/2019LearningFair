from tkinter import *
import tkinter.font as font # tkinter에서 사용하는 폰트 모듈을 불러옴
from collections import defaultdict # defaultdict: 딕셔너리인데 초기 value값을 설정할 수 있음. 딕셔너리에 key가 없더라도 바로 value를 활용할 수 있다는 장점이 있음.
                                    # 예를 들어, a = defaultdict(int)에서 모든 key의 기본 value 값이 0임. 만약 a에 "국어"라는 key가 없다고 하더라도,
                                    # a["국어"] += 1을 하면 바로 딕셔너리 안에 "국어"라는 key와 그에 대응되는 1이라는 value가 생기게 됨(기본 값은 0이므로).

window = Tk()


NanumBarunGothic11 = font.Font(family='NanumbarunGothic', size=11) # tkinter.font 모듈의 Font 클래스, tkinter에서 새로운 글꼴을 활용할 수 있게 도와줌.
HumanT20 = font.Font(family='휴먼모음T', size=20)

window.option_add( "*font", NanumBarunGothic11) # window Tk창의 기본 폰트를 나눔바른고딕으로 수정하는 메서드.
window.title("전공진입요건 계산 프로그램")
window.geometry("910x720")

selected_계열 = StringVar() # OptionMenu로 선택된 '계열'의 값이 들어가는 변수 
selected_계열.set("계열 선택")
selected_계열_string = StringVar() # 계열이 선택될 경우 그 계열에 맞춰 [OO계열 전공진입요건]으로 바뀌는 문자열
selected_계열_string.set("[계열을 입력하세요]")

selected_지원학과 = StringVar() # OptionMenu로 선택된 '지원학과'의 값이 들어가는 변수 
selected_지원학과.set("지원학과 선택")

explain_전공진입요건 = StringVar() # 계열에 따른 전공진입 설명이 들어가는 변수
explain_전공진입요건.set("")
explain_전공진입요건_HS = "의사소통 4학점, 기본영어+전문영어 4학점, 창의와사유 2학점,\n소프트웨어기초 2학점, 기초인문사회과학 6학점" # 인문(Humanity)&사회(Social)과학계열의 전공진입요건 설명
explain_전공진입요건_N = "의사소통 4학점, 기본영어+전문영어 4학점, 창의와사유 2학점,\n소프트웨어기초 2학점, 기초자연과학 12학점" # 자연과학(Natural)계열의 전공진입요건 설명
explain_전공진입요건_E = "의사소통 4학점, 기본영어+전문영어 4학점,\n창의와사유 2학점, 기초자연과학 15학점, 창의적공학설계" # 공학(Engineering)계열의 전공진입요건 설명

major_entrance_rule_HS = ['의사소통', '기본영어', '전문영어', '창의와사유', '소프트웨어기초', '기초인문사회과학'] # 각 계열의 전공진입 해당 영역(전공진입에 반영되는 영역)
major_entrance_rule_N = ['의사소통', '기본영어', '전문영어', '창의와사유', '소프트웨어기초', '기초자연과학'] # (소속대학 원전공 진입 시에는 이 영역들의 과목만 평점에 반영 됨.)
major_entrance_rule_E = ['의사소통', '기본영어', '전문영어', '창의와사유', '기초자연과학', '창의적공학설계']


explain_전공진입요건_dict = { # key: 계열, value: (그 계열에 해당하는) 전공진입요건 설명
    "인문과학계열": explain_전공진입요건_HS,
    "사회과학계열": explain_전공진입요건_HS,
    "자연과학계열": explain_전공진입요건_N,
    "공학계열": explain_전공진입요건_E
}

GPA_score = {'A+': 4.5, 'A': 4.0, 'B+': 3.5, 'B': 3.0, 'C+': 2.5, 'C': 2.0, 'D+': 1.5, 'D': 1.0, 'F': 0.0} # 영어 평점: 숫자 평점(GPA 계산 때 영어 평점을 숫자로 변환할 때 활용 됨.)

authorityHSN = [ # 인문, 사회, 자연과학계열의 직권배정 과목(OptionMenu로 계열을 선택하면 (대부분 수강했을 것이므로) 이 과목들은 과목란에 자동으로 채워 줌.) 
    ['기본영어', '2', '영어쓰기'],
    ['소프트웨어기초', '2', '컴퓨팅사고와SW코딩'],
    ['일반선택', '1', 'FYE세미나I', 'P(P/F)'],
    ['기본영어', '2', '영어발표'],
    ['소프트웨어기초', '2', '문제해결과알고리즘'],
    ['일반선택', '1', 'FYE세미나II', 'P(P/F)']
]

authorityE = [ # 공학계열의 직권배정 과목 + 창의적공학설계  (계열제가 듣는 거의 유일한 전공 영역이라 학생들이 영역 선택할 때 헷갈려할 수 있고,
                                                           # 특수 전공진입요건이라 공학계열 대부분은 이 과목을 수강하고, 
                                                           # 과목명이 (계산 과정에서) 특히나 중요한 과목이라 오타 방지를 위해 미리 직권배정과 함께 자동으로 입력해줌.)
    ['기본영어', '2', '영어쓰기'],
    ['기초자연과학', '3', '공학컴퓨터프로그래밍'],
    ['일반선택', '1', 'FYE세미나I', 'P(P/F)'],
    ['기본영어', '2', '영어발표'],
    ['기초자연과학', '3', '프로그래밍기초와실습'],
    ['일반선택', '1', 'FYE세미나II', 'P(P/F)'],
    ['전공', '3', '창의적공학설계']
]

def change_계열(a): # 계열 OptionMenu를 통해 새로운 계열을 선택했을 시 실행되는 함수.
                    # 1. 계열에 맞게 전공진입요건 설명을 수정
                    # 2. 계열에 맞는 직권배정 과목들을 과목란에 채워넣음 
    selected_계열_string.set("[{} 전공진입 요건]".format(a))
    explain_전공진입요건.set(explain_전공진입요건_dict[a])

    if a != '공학계열': 
        for i in range(6): # 직권배정은 총 6과목
            tmp_list = authorityHSN[i] # tmp_list: 직권배정이 담겨있는 리스트
            if i >= 3: # 초반 3과목은 왼쪽 맨 위, 후반 3과목은 오른쪽 맨 위(i=12~)에 입력되게 함.
                i += 9
            territory_string[i].set(tmp_list[0]) # 과목 영역 수정
            credit_string[i].set(tmp_list[1]) # 과목 학점 수정
            name_string[i].set(tmp_list[2]) # 과목명 수정
            if tmp_list[0] == '일반선택': # 일반선택 영역인 FYE세미나는 P/F 과목이므로 평점도 P(P/F)로 수정
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

        territory_string[23].set(authorityE[6][0]) # 창의적공학설계 과목도 마지막 과목란에 추가
        credit_string[23].set(authorityE[6][1])
        name_string[23].set(authorityE[6][2])


title = Label(window, text="전공진입요건 계산 프로그램", font=HumanT20, height=2)
title.grid(row=0, column=0, columnspan=99)

계열 = Label(window, text=" 계열: ")
계열.grid(row=1, column=1)
# OptionMenu 위젯은 tkinter에서 사용자가 선택지를 고를 수 있는 위젯임.
# 아래 OptionMenu를 설명하자면, 총 4개의 선택지가 있고, 선택지를 선택하면 'selected_계열(초기값은 '계열 선택'이라고 설정했음)'이라는 변수에 그 선택지값이 들어감.
# 그리고 command는 이 OptionMenu의 선택지가 바뀌었을 시 실행됨. 매개변수를 하나(새로 선택된 값) 전달해줌.
계열option = OptionMenu(window, selected_계열, "인문과학계열", "사회과학계열", "자연과학계열", "공학계열", command=change_계열) # 계열을 선택하는 OptionMenu
계열option.grid(row=1, column=2, columnspan=2)
지원학과 = Label(window, text=" 지원학과: ")
지원학과.grid(row=1, column=4, columnspan=2)
지원학과option = OptionMenu(window, selected_지원학과, "소속대학 원전공", "글로벌융합학부") # 지원하고자 하는 학과를 선택하는 OptionMenu
지원학과option.grid(row=1, column=6)

전공진입요건_label = Label(window, textvariable=selected_계열_string, height=2)
전공진입요건_label.grid(row=2, column=0, columnspan=99)
전공진입요건_explainLabel = Label(window, textvariable=explain_전공진입요건, height=3) # 계열에 맞는 전공진입요건 설명이 들어가는 Label
전공진입요건_explainLabel.grid(row=3, column=0, columnspan=99)

영역_label = Label(window, text="영역") # 과목란 위에 과목의 어떤 정보를 넣어야하는지 설명해주는 Label(왼쪽)
학점_label = Label(window, text="학점")
과목명_label = Label(window, text="과목명")
평점_label = Label(window, text="평점")
영역_label2 = Label(window, text="영역") # 오른쪽에도 추가
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

territory = [] # 각 과목의 '영역'을 선택할 수 있는 OptionMenu가 들어갈 리스트
credit = [] # 각 과목의 '학점'을 입력할 수 있는 Entry가 들어갈 리스트
name = [] # 각 과목의 '과목명'을 입력할 수 있는 Entry가 들어갈 리스트
gpa = [] # 각 과목의 '평점'을 선택할 수 있는 OptionMenu가 들어갈 리스트

territory_string = [] # 각 과목의 영역 OptionMenu의 선택값을 담을 StringVar가 들어갈 리스트
credit_string = [] # 각 과목의 학점 Entry의 입력값을 담을 StringVar가 들어갈 리스트
name_string = [] # 각 과목의 과목명 Entry의 입력값을 담을 StringVar가 들어갈 리스트
gpa_string = [] # 각 과목의 평점 OptionMenu의 선택값을 담을 StringVar가 들어갈 리스트

for i in range(24): # 총 입력할 수 있는 과목 개수는 24개
    territory_string.append(StringVar()) 
    territory_string[i].set("영역 선택")
    credit_string.append(StringVar()) 
    credit_string[i].set("0")
    name_string.append(StringVar()) 
    gpa_string.append(StringVar())
    gpa_string[i].set("A+")

    territory.append(OptionMenu(window, territory_string[i], "인성", "리더십", "기본영어", "전문영어", "글로벌문화", # 각 과목의 영역을 선택하는 OptionMenu
                                "의사소통", "창의와사유", "소프트웨어기초", "기초인문사회과학", "기초자연과학",
                                "인간/문화", "사회/역사", "자연/과학/기술", "일반선택", "기타교양", "전공")) 
    credit.append(Entry(window, textvariable=credit_string[i], width=3, justify='center')) # 각 과목의 학점을 입력하는 Entry
    name.append(Entry(window, textvariable=name_string[i])) # 각 과목의 과목명을 입력하는 Entry
    gpa.append(OptionMenu(window, gpa_string[i], "A+", "A", "B+", "B", "C+", "C", "D+", "D", "F", "P(P/F)", "F(P/F)")) # 각 과목의 평점을 선택하는 OptionMenu

    territory[i].config(width=12) # 영역 OptionMenu의 가로 길이를 조정하는 메서드
    gpa[i].config(width=4) # 평점 OptionMenu의 가로 길이를 조정하는 메서드

    if i <= 11: # 12번째 위젯까지는 왼쪽 위에서부터 차례대로 위치
        territory[i].grid(row=i+5, column=0) # 위젯들의 위치: row=5~16, column=0~3
        credit[i].grid(row=i+5, column=1)
        name[i].grid(row=i+5, column=2)
        gpa[i].grid(row=i+5, column=3)
    else: # 13번째 위젯(i >= 12)부터는 오른쪽 위부터 다시 위젯들을 위치시킴(크게 왼쪽에 12과목, 오른쪽에 12과목의 정보를 입력할 수 있게 됨.)
        territory[i].grid(row=i-7, column=4) # 위젯들의 위치: row=5~16, column=4~7
        credit[i].grid(row=i-7, column=5)
        name[i].grid(row=i-7, column=6)
        gpa[i].grid(row=i-7, column=7)

error_message = StringVar() # 오류가 발생했을 경우, 이 변수에 그 오류에 해당하는 오류 메시지 문자열을 담게 됨(set).


def calculate(): # 전공진입요건 충족여부 계산하기 버튼을 누를 경우 실행되는 함수
                 # 이 프로그램에서 실질적인 결과 계산의 총괄을 담당하는 함수
                 # 1. 계열 선택 여부 확인, 계열에 맞게 해당 전공진입영역과 전공진입 최소충족요건을 설정
                 # 2. 지원학과 선택 여부 확인
                 # 3. calculate_credit 함수를 통해 수강한 과목들을 영역별로 정리 & 전공진입 최소충족요건을 못 채운 영역이 있으면 less_complete 딕셔너리에 담음.
                 # 4. calculate_GPA 함수를 통해 전공진입에 반영되는 평균 평점을 계산함.
                 # 5. (계산 총 결과에 따라) 결과창을 띄워 줌.
    global successful
    successful = True # calculate, calculate_credit, calculate_GPA 함수 등에서 한 번이라도 오류가 생기면 결과창을 띄우면 안 되므로, 전역변수 successful을 통해 세 함수의 오류 여부를 동시에 확인

    major = selected_계열.get()
    want_to_in = selected_지원학과.get()

    if major == '계열 선택': # 계열을 아직 선택하지 않은 경우
        error_message.set("계열을 선택해주세요.")
        successful = False
        return False # 오류가 발생했을 때는 False를 리턴하고 함수 종료
    elif major in ['인문과학계열', '사회과학계열']:
        rule = major_entrance_rule_HS # rule: 계열별 전공진입 해당 영역
        available_territory = {'의사소통': 4, '기본영어+전문영어': 4, '창의와사유': 2, '소프트웨어기초': 2, '기초인문사회과학': 6} # available_territory: 계열별 전공진입 가능한 영역별 최소 조건("영역": 최소 충족 학점)
    elif major == '자연과학계열':
        rule = major_entrance_rule_N
        available_territory = {'의사소통': 4, '기본영어+전문영어': 4, '창의와사유': 2, '소프트웨어기초': 2, '기초자연과학': 12}
    elif major == '공학계열':
        rule = major_entrance_rule_E
        available_territory = {'의사소통': 4, '기본영어+전문영어': 4, '창의와사유': 2, '기초자연과학': 15, '창의적공학설계': 3}
    else: # 이외의 경우(정상적인 상황에서는 실행될 확률 X)
        error_message.set("계열 관련 오류가 발생했습니다.")
        successful = False
        return False

    if want_to_in == '지원학과 선택': # 지원학과를 아직 선택하지 않은 경우
        error_message.set("지원하고자 하는 학과를 선택해주세요.")
        successful = False
        return False
    elif want_to_in in ['소속대학 원전공', '글로벌융합학부']:
        pass
    else: # 이외의 경우(정상적인 상황에서는 실행될 확률 X)
        error_message.set("지원학과 관련 오류가 발생했습니다.")
        successful = False
        return False

    less_complete = dict() # 전공진입요건 최소 요건을 충족하지 못한 경우, {"부족한 영역 이름": 부족한 학점} 형식으로 저장되는 딕셔너리
    personal_credit = calculate_credit() # 사용자가 수강한 과목들을 영역별로 정리한 딕셔너리(calculate_credit 함수 참고)

    if personal_credit == False:
        error_message.set("요건 충족 여부 판단 중 오류가 발생했습니다.\n학점에 숫자를 입력했는지 확인하세요.")
        successful = False
        return False
    for a in available_territory:
        if available_territory[a] > personal_credit[a]:
            less_complete[a] = available_territory[a] - personal_credit[a]

    personal_GPA = calculate_GPA(major, want_to_in, rule) # 전공진입에 반영되는 평균 평점(calculate_GPA 함수 참고)

    if personal_GPA == False: # calculate_GPA 함수에서 오류가 발생해서 False가 리턴된 경우
        error_message.set("평점 계산 중 오류가 발생했습니다.")
        successful = False
        return False

    if successful:
        if not less_complete: # 전공진입 요건을 충족한 경우와 덜 충족한 경우의 결과창을 다르게 설정
            result(want_to_in, personal_GPA)
        else:
            result(want_to_in, personal_GPA, complete=False, less=less_complete)

def calculate_credit(): # 사용자가 수강한 과목들을 통해 영역별 수강학점을 딕셔너리(personal_credit)에 정리하는 함수
                        # for문에서 과목별 tmp_t(territory), tmp_c(credit), tmp_n(name)을 활용하여 영역별 수강학점을 정리
                        # personal_credit에는 {"영역명": 총 수강 학점} 으로 담김.
                        # 기본영어와 전문영어는 전공진입 때 동시에 계산하므로 동일 영역에 넣음. 창의적공학설계는 전공 영역이지만 특수한 케이스이므로 영역처럼 간주하고 저장.
    global successful
    personal_credit = defaultdict(int) # defauldict 설명은 코드 맨 위 모듈 불러오는 곳 참고
    for i in range(24):
        tmp_t = territory_string[i].get()
        try: # try~except문: try절 안에 들어있는 코드들을 실행하고, 만약 중간에 오류가 발생하면 except문을 실행하는 문법. (else, finally 등도 사용하지만 이 프로그램에서는 사용 X)
             # 이 프로그램에서는 숫자를 입력해야하는 Entry에 글자를 입력한 경우, int 치환 과정에서 ValueError가 발생하므로 이를 방지하고자 이 문법을 사용함.
            tmp_c = int(credit_string[i].get())
        except ValueError:
            successful = False
            return False

        if tmp_t == '영역 선택':
            pass
        elif tmp_t in ['기본영어', '전문영어']:
            personal_credit['기본영어+전문영어'] += tmp_c
        elif tmp_t == '전공':
            tmp_n = name_string[i].get()
            if tmp_n == '창의적공학설계':
                tmp_t = '창의적공학설계'
            personal_credit[tmp_t] += tmp_c
        else:
            personal_credit[tmp_t] += tmp_c

    return personal_credit


def calculate_GPA(major, want_to_in, rule): # 전공진입에 반영되는 전공진입 평균 평점을 계산하는 함수.
                                            # (매개변수 설명) major: 현재 계열, want_to_in: 현재 지원하고자 하는 학과, rule: 현재 계열의 전공진입 해당 영역 
                                            # 지원학과에 따라 계산 방식이 다르므로 if문을 활용
                                            # 소속대학 원전공은 전공진입 해당 영역 과목들(rule에 들어있는 과목들)만 계산
                                            # 글로벌융합학부는 전체 과목 계산
    global successful
    personal_credit = 0
    total_gpa = 0
    if want_to_in == '소속대학 원전공':
        for i in range(24):
            tmp_t = territory_string[i].get()
            if (major == '공학계열') and (tmp_t == '전공'):
                creative_or_not = name_string[i].get()
                if creative_or_not == '창의적공학설계':
                    tmp_t = '창의적공학설계'

            try: # try~except문 (calculate_credit 함수의 설명 참고)
                tmp_c = int(credit_string[i].get())
            except ValueError:
                successful = False
                return False

            tmp_g = gpa_string[i].get()

            if tmp_t in rule:
                if tmp_g not in ['P(P/F)', 'F(P/F)']: # P/F 과목은 평점 계산에 반영 X
                    personal_credit += tmp_c
                    total_gpa += tmp_c * GPA_score[tmp_g]

        if personal_credit == 0: # ZeroDivisionError(0으로 숫자를 나눌 경우 발생하는 오류) 방지
            successful = False
            return False

        GPA_result = total_gpa / personal_credit
        return GPA_result

    elif want_to_in == '글로벌융합학부':
        for i in range(24):
            try: # try~except문 (calculate_credit 함수의 설명 참고)
                tmp_c = int(credit_string[i].get())
            except ValueError:
                successful = False
                return False

            tmp_g = gpa_string[i].get()

            if tmp_g not in ['P(P/F)', 'F(P/F)']: # P/F 과목은 평점 계산에 반영 X
                personal_credit += tmp_c
                total_gpa += tmp_c * GPA_score[tmp_g]

        if personal_credit == 0: # ZeroDivisionError(0으로 숫자를 나눌 경우 발생하는 오류) 방지
            successful = False
            return False

        GPA_result = total_gpa / personal_credit
        return GPA_result

    elif want_to_in == '지원학과 선택':
        successful = False
        return False
    else:
        successful = False
        return False


def result(want_to_in, gpa_result, complete=True, less=None): # 계산 결과를 바탕으로 새 창에 결과를 보여주는 함수
                                                              # (매개변수 설명) want_to_in: 지원학과, gpa_result: 전공진입에 반영되는 평균 평점(calculate_GPA로 계산된 값)
                                                              #                 complete: 전공진입 요건을 충족했을 경우 True 유지(아닐 경우 False로 바꿈)
                                                              #                 less: (충족 못한 경우) 영역별 부족한 학점이 담겨있는 딕셔너리
                                                              # 전공진입요건 충족 여부에 따라 결과창을 다르게 설정
                                                              # 충족한 경우, 축하 메세지를 표시함.
                                                              # 충족하지 못한 경우, 위로의 메세지와 함께, 아직 덜 충족한 영역별 학점을 표시해 줌.
                                                              # 두 경우 모두 창 맨 아래에 (want_to_in) 진입시 반영되는 평점의 평균은 (gpa_result)입니다. 라는 메세지를 출력
                                                              
    result_window = Toplevel(window) # Toplevel: Tkinter에서 새 창을 띄울 때 사용하는 위젯
    result_window.title('전공진입요건 계산 결과')

    if complete:
        final = Label(result_window, text="축하드립니다!", font=('NanumbarunGothic', 25), fg="green3", width=20, height=2)
        final2 = Label(result_window, text="전공진입요건을 충족하셨습니다!", font=('NanumbarunGothic', 15))
        final.grid(row=0, column=0, rowspan=2, columnspan=2)
        final2.grid(row=2, column=0, columnspan=2, sticky='n')

        final_gpa = Label(result_window, text="{} 진입시 반영되는".format(want_to_in), font=('NanumbarunGothic', 18), anchor='s', height=2)
        final_gpa2 = Label(result_window, text="평점의 평균은 {}입니다!".format(gpa_result), font=('NanumbarunGothic', 18))
        final_gpa.grid(row=3, column=0, columnspan=2)
        final_gpa2.grid(row=4, column=0, columnspan=2)
    else:
        final = Label(result_window, text="충족하지 못했습니다...", font=('NanumbarunGothic', 25), fg="red3", width=20, height=2)
        final2 = Label(result_window, text="전공진입 영역별로 아직 채우지 못한 학점입니다.", anchor='n')
        final.grid(row=0, column=0, rowspan=2, columnspan=2)
        final2.grid(row=2, column=0, columnspan=2, sticky='n')

        less_frames = []
        for terri, cre in less.items():
            tmp_frame = Frame(result_window)
            terri_label = Label(tmp_frame, text=terri, width=15, height=2, anchor='s', font=('NanumbarunGothic', 14))
            cre_label = Label(tmp_frame, text="{}학점".format(cre), width=15, height=2, anchor='n', font=('NanumbarunGothic', 14))
            terri_label.pack(fill=BOTH)
            cre_label.pack(fill=BOTH)
            less_frames.append(tmp_frame)

        row_count = 2
        for i, frame in enumerate(less_frames): # enumerate 함수: (for문에서는) iterable한 자료형(리스트, 튜플 등)의 자료들을 인덱스와 함께 돌려주는 함수
                                                # 예를 들어, ["A", "B", "C"]라는 리스트가 있다면 첫 for문의 1번째 카운터변수는 0(인덱스), 2번째 카운터변수는 "A"(자료)가 됨.
            if i % 2 == 0:
                row_count += 1
                now_column = 0
            else:
                now_column = 1
            frame.grid(row=row_count, column=now_column, sticky=W+E)

        final_gpa = Label(result_window, text="{} 진입시 반영되는".format(want_to_in), font=('NanumbarunGothic', 18), anchor='s', height=2)
        final_gpa2 = Label(result_window, text="평점의 평균은 현재까지 {}입니다.".format(round(gpa_result, 2)), font=('NanumbarunGothic', 18))
        final_gpa.grid(row=98, column=0, columnspan=2)
        final_gpa2.grid(row=99, column=0, columnspan=2)
    result_window.mainloop()




Calculate_button = Button(window, text='전공진입요건 충족여부 계산하기!', command=calculate)
Calculate_button.grid(row=17, column=0, columnspan=99)

Calculate_error = Label(window, textvariable=error_message)
Calculate_error.grid(row=18, column=0, columnspan=99)


window.mainloop()
