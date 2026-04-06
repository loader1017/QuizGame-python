import json
import os

class Menu:
    def __init__(self, startquiz, addquiz, quizlist, scorecheck, quit):
        self.startquiz = startquiz
        self.addquiz = addquiz
        self.quizlist = quizlist
        self.scorecheck = scorecheck
        self.quit = quit

class Quiz:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer


# 퀴즈 프로그램 시작
print("퀴즈 프로그램을 시작합니다. 메뉴를 골라주세요.")
user_input = input("1. 퀴즈 시작 2. 퀴즈 추가 3. 퀴즈 목록 4. 점수 확인 5. 종료\n선택(숫자입력): ")   

menu = Menu(
    startquiz=user_input == "1",
    addquiz=user_input == "2",
    quizlist=user_input == "3",
    scorecheck=user_input == "4",
    quit=user_input == "5"
)

QUIZ_FILE = "data.json"

def load_quizzes():
    if not os.path.exists(QUIZ_FILE):
        return []
    with open(QUIZ_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Quiz(q["question"], q["answer"]) for q in data]

quiz_list = load_quizzes()  

#1. 퀴즈 시작
if menu.startquiz:
    print("퀴즈를 시작합니다! O 또는 X로 답해주세요.")
    print("=" * 40)

    score = 0 #초기화
    for q in quiz_list:
        print(f"Q: {q.question}")
        user_input = input("A (O/X): ").strip().upper()  # .upper() 소문자로 입력해도 대문자로 변환, .strip() 답변에 딸려오는 공백 제거

        if user_input == q.answer:
            print("✅ 정답")
            score = score + 1
        else:
            print(f"❌ 오답. 정답은 {q.answer}입니다.")

        print("-" * 40)

    print(f"퀴즈 종료. 총점: {score}/{len(quiz_list)}")

#2. 퀴즈 추가
elif menu.addquiz:
    print("퀴즈 추가 기능은 아직 구현되지 않았습니다.")

#3. 퀴즈 목록
elif menu.quizlist:
    print("======== 퀴즈 목록 =======")
    for i, q in enumerate(quiz_list, 1):
        print(f"{i}. {q.question} (정답: {q.answer})")
    print("===========================")

#4. 점수 확인
elif menu.scorecheck:
    print(f"마지막으로 푼 퀴즈의 점수는 입니다.")

#5. 종료
elif menu.quit:
    print("퀴즈 프로그램을 종료합니다.")