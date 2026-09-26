from retriever import Retriever

sample_email = "ilovemeowth@snowykim-demo.com"


r = Retriever()
current_user = r.get_current_user(sample_email)

queries = [
    "What is Grace Liu's location?",
    "What was a past HR violation related to assault?",
    "Summarize the process for onboarding a new employee"
]

for query in queries: # formatting cleanly
    answer = r.answer_question(query, current_user)

    print("\n" + "=" * 60)
    print(f"\033[1mQuestion: {query}\033[0m")
    print()
    print(f"\033[1mHR Assistant:\033[0m")
    print(answer)
    print("=" * 60)









