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
    def __init__(self, question, options, answer):
        self.question = question
        self.options = options
        self.answer = answer

QUIZ_FILE = "data.json"
LSCORE = "score.json"

#점수 데이터 불러오기 및 저장 함수
def save_score(score, total):
    with open(LSCORE, "w", encoding="utf-8") as file:
        json.dump({"last_score": f"{score}/{total}"}, file)

def load_score():
    with open(LSCORE, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["last_score"]

#퀴즈 데이터가 없을 때 사용할 기본 퀴즈 데이터
SAVE_QUIZ = [
    {
        "question": "고양이의 특징이 아닌것을 고르세요.",
        "options": ["유연하다", "잠이 많다.", "비 영역 동물이다.", "영역 동물이다."],
        "answer": "3"
    },
    {
        "question": "집고양이의 평균 수명을 고르세요.",
        "options": ["1년", "5년", "10년", "15년"],
        "answer": "4"
    },
    {
        "question": "고양이는 몇 개의 발가락을 가지고 있나요?",
        "options": ["4개", "5개", "6개", "7개"],
        "answer": "2"
    },
    {
        "question": "고양이는 하루 평균 몇시간을 잠으로 보내나요?",
        "options": ["1~2시간", "3~4시간", "6~8시간", "12시간~16시간"],
        "answer": "4"
    },
    {
        "question": "고양이는 어떤 동물인가요?",
        "options": ["어류", "포유류", "조류", "파충류"],
        "answer": "2"
    },
]

# 퀴즈 데이터 불러오기 함수 (json 깨졌을때 쓸거)
def load_quizzes():
    if not os.path.exists(QUIZ_FILE):
        print("데이터 파일이 없어 기본 퀴즈 데이터를 사용합니다.")
        return [Quiz(q["question"], q["options"], q["answer"]) for q in SAVE_QUIZ]
    try:
        with open(QUIZ_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        return [Quiz(q["question"], q["options"], q["answer"]) for q in data]
    except json.JSONDecodeError:  # JSON이 깨졌을 때
        print("데이터 파일이 손상되었습니다. 기본 데이터로 초기화합니다.")
        return [Quiz(q["question"], q["options"], q["answer"]) for q in SAVE_QUIZ]

quiz_list = load_quizzes() 

# 퀴즈 프로그램 시작
try:
    while True:
        print("퀴즈 프로그램을 시작합니다. 메뉴를 골라주세요.")
        user_input = input("1. 퀴즈 시작 2. 퀴즈 추가 3. 퀴즈 목록 4. 점수 확인 5. 종료\n선택(숫자입력): ")   

        menu = Menu(
        startquiz=user_input == "1",
        addquiz=user_input == "2",
        quizlist=user_input == "3",
        scorecheck=user_input == "4",
        quit=user_input == "5"
        ) 

        #1. 퀴즈시작
        if menu.startquiz:
            print("퀴즈를 시작합니다! O 또는 X로 답해주세요.")
            print("=" * 40)

            score = 0
            for q in quiz_list:
                print(f"Q: {q.question}")
                for i, option in enumerate(q.options, 1):
                    print(f"  {i}. {option}")  # 선택지 출력

                while True:
                    user_input = input("A (1~4): ").strip()
                    if user_input in ["1", "2", "3", "4"]:
                        break
                    print("1~4 중에서 입력해주세요.")

                if user_input == q.answer:
                    print("✅ 정답")
                    score += 1
                else:
                    print(f"❌ 오답. 정답은 {q.answer}번 {q.options[int(q.answer)-1]}입니다.")
                print("-" * 40)

            print(f"퀴즈 종료. 총점: {score}/{len(quiz_list)}")
            save_score(score, len(quiz_list))

        #2. 퀴즈 추가
        elif menu.addquiz:
            question = input("퀴즈 질문을 입력하세요: ").strip()
            options = []
            for i in range(1, 5):
                option = input(f"{i}번 선택지: ").strip()
                options.append(option)
            
            while True:
                answer = input("정답 번호 (1~4): ").strip()
                if answer in ["1", "2", "3", "4"]:
                    break
                print("1~4 중에서 입력해주세요.")

            quiz_list.append(Quiz(question, options, answer))
            with open(QUIZ_FILE, "w", encoding="utf-8") as file:
                json.dump([{"question": q.question, "options": q.options, "answer": q.answer} for q in quiz_list], file, ensure_ascii=False, indent=4)
            print("퀴즈가 추가되었습니다.")

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
            break

except KeyboardInterrupt:  # 강종할때
    print("\n프로그램을 종료합니다.")

except EOFError:  # 입력끊겼을때
    print("\n입력이 종료되어 프로그램을 종료합니다.")