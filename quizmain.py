import json
import os
import signal

class QUIZ:
    def __init__(self, question, options, answer):
        self.question = question
        self.options = options
        self.answer = answer

    def display(self):  # 퀴즈 출력 메서드
        print(f"Q: {self.question}")
        for i, option in enumerate(self.options, 1):
            print(f"  {i}. {option}")

    def check_answer(self, user_input):  # 정답 확인 메서드
        return user_input == self.answer

QUIZ_FILE = "state.json"  # 퀴즈 데이터 파일

#퀴즈 데이터가 없을 때 사용할 기본 퀴즈 데이터
SAVE_QUIZ = [
    {
        "question": "고양이의 특징이 아닌것을 고르세요.",
        "options": ["유연하다", "잠이 많다", "비 영역 동물이다", "영역 동물이다"],
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

class QuizGame:
    def __init__(self):
        self.quiz_list = self.load_quizzes()  # 퀴즈 목록
        self.high_score = 0                   # 최고 점수
        if hasattr(signal, 'SIGTSTP'):
            signal.signal(signal.SIGTSTP, signal.SIG_IGN)  # Ctrl+Z 무시
    
    def load_state(self):
        if not os.path.exists(QUIZ_FILE):
            return {}
        try:
            with open(QUIZ_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}

    def save_state(self, state):
        with open(QUIZ_FILE, "w", encoding="utf-8") as file:
            json.dump(state, file, ensure_ascii=False, indent=4)

    # 파일 불러오기
    def load_quizzes(self):
        if not os.path.exists(QUIZ_FILE):
            print("데이터 파일이 없어 기본 퀴즈 데이터를 사용합니다.")
            return [QUIZ(q["question"], q["options"], q["answer"]) for q in SAVE_QUIZ]
        try:
            with open(QUIZ_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            return [QUIZ(q["question"], q["options"], q["answer"]) for q in data["quizzes"]]
        except (json.JSONDecodeError, KeyError):
            print("데이터 파일이 손상되었습니다. 기본 데이터로 초기화합니다.")
            return [QUIZ(q["question"], q["options"], q["answer"]) for q in SAVE_QUIZ]

    # 파일 저장
    def save_score(self, score, total):
        if score > self.high_score:
            self.high_score = score
        state = self.load_state()
        state["last_score"] = f"{score}/{total}"
        state["high_score"] = self.high_score
        self.save_state(state)


    def load_score(self):
        state = self.load_state()
        return state if "last_score" in state else None

    # 메뉴 표시
    def show_menu(self):
        while True:
            user_input = input("1. 퀴즈 시작 2. 퀴즈 추가 3. 퀴즈 목록 4. 점수 확인 5. 종료\n선택(숫자입력): ").strip()
            if user_input == "":
                print("올바른 번호를 입력해주세요. (1~5)")
            elif user_input not in ["1", "2", "3", "4", "5"]:
                print("올바른 번호를 입력해주세요. (1~5)")
            else:
                return user_input
    
    # 퀴즈 풀기
    def start_quiz(self):
        if not self.quiz_list:
            print("등록된 퀴즈가 없습니다.")
            return
        score = 0
        for q in self.quiz_list:
            q.display()
            while True:
                user_input = input("A (1~4): ").strip()
                if user_input in ["1", "2", "3", "4"]:
                    break
                print("1~4 중에서 입력해주세요.")
            if q.check_answer(user_input):
                print("✅ 정답")
                score += 1
            else:
                print(f"❌ 오답. 정답은 {q.answer}번 {q.options[int(q.answer)-1]}입니다.")
        print(f"퀴즈 종료. 총점: {score}/{len(self.quiz_list)}")
        self.save_score(score, len(self.quiz_list))

    # 퀴즈 추가
    def add_quiz(self):
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
        self.quiz_list.append(QUIZ(question, options, answer))
        state = self.load_state()
        state["quizzes"] = [{"question": q.question, "options": q.options, "answer": q.answer} for q in self.quiz_list]
        self.save_state(state)
        print("퀴즈가 추가되었습니다.") 

    # 퀴즈 목록
    def show_quiz_list(self):
        print("======== 등록 된 퀴즈 목록 =======")
        for i, q in enumerate(self.quiz_list, 1):
            print(f"{i}. {q.question} (정답: {q.answer})")
        print("===========================")

    # 점수 확인
    def show_score(self):
        data = self.load_score()
        if data:
            print(f"마지막 점수: {data['last_score']}, 최고 점수: {data.get('high_score', 0)}")
        else:
            print("저장된 점수가 없습니다.")
    
    def run(self):
        try:
            while True:
                user_input = self.show_menu()
                if user_input == "1":
                    self.start_quiz()
                elif user_input == "2":
                    self.add_quiz()
                elif user_input == "3":
                    self.show_quiz_list()
                elif user_input == "4":
                    self.show_score()
                elif user_input == "5":
                    print("퀴즈 프로그램을 종료합니다.")
                    break
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
        except EOFError:
            print("\n입력이 종료되어 프로그램을 종료합니다.")
        finally:
            self.save_state()

game = QuizGame()
game.run()  