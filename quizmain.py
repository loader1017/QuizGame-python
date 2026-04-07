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
LSCORE = "score.json"

# 퀴즈 데이터 불러오기 함수
def load_quizzes():
    if not os.path.exists(QUIZ_FILE):
        return []
    with open(QUIZ_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    return [Quiz(q["question"], q["answer"]) for q in data]

#점수 데이터 불러오기 및 저장 함수
def save_score(score, total):
    with open(LSCORE, "w", encoding="utf-8") as file:
        json.dump({"last_score": f"{score}/{total}"}, file)

def load_score():
    with open(LSCORE, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["last_score"]

quiz_list = load_quizzes()  

#1. 퀴즈 시작
if menu.startquiz:
    print("퀴즈를 시작합니다! O 또는 X로 답해주세요.")
    print("=" * 40)

    score = 0 #시작스코어초기화
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

    save_score(score, len(quiz_list))  # 점수 저장

#2. 퀴즈 추가
elif menu.addquiz:
    print("새로운 퀴즈를 추가합니다.")
    question = input("퀴즈 질문을 입력하세요: ")
    answer = input("정답을 입력하세요 (O/X): ")

    if answer not in ["O", "X"]:
        print("잘못된 정답 형식입니다. O 또는 X로 입력해주세요.")
    else:
        new_quiz = Quiz(question, answer)
        quiz_list.append(new_quiz)

        # 퀴즈 데이터 저장
        with open(QUIZ_FILE, "w", encoding="utf-8") as file:
            json.dump([{"question": q.question, "answer": q.answer} for q in quiz_list], file, ensure_ascii=False, indent=4)

        print("퀴즈가 성공적으로 추가되었습니다.")

#3. 퀴즈 목록
elif menu.quizlist:
    print("======== 등록 된 퀴즈 목록 =======")
    for i, q in enumerate(quiz_list, 1):
        print(f"{i}. {q.question} (정답: {q.answer})")
    print("===========================")

#4. 점수 확인
elif menu.scorecheck:
    print(f"마지막으로 푼 퀴즈의 점수는 {load_score()}입니다.")

#5. 종료
elif menu.quit:
    print("퀴즈 프로그램을 종료합니다.")