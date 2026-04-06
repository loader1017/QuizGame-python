class Quiz:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer


quiz_list = [
    Quiz("고양이는 포유류이다.", "O"),
    Quiz("고양이는 유연하다.", "O"),
    Quiz("고양이는 물을 좋아한다.", "X"),
    Quiz("고양이는 강아지보다 잠을 많이 잔다.", "O"),
    Quiz("고양이는 영역동물이 아니다.", "X")
]

print("퀴즈를 시작합니다! O 또는 X로 답해주세요.")
print("=" * 40)

score = 0


for q in quiz_list:
    print(f"Q: {q.question}")
    user_input = input("A (O/X): ").upper() # 소문자로 입력해도 대문자로 변환
    
    if user_input == q.answer:
        print("✅ 정답")
        score += 1
    else:
        print(f"❌ 오답. 정답은 {q.answer}입니다.")
    
    print("-" * 40)

print(f"퀴즈 종료. 총점: {score}/{len(quiz_list)}")