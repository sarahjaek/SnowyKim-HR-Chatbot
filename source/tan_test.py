from retriever import Retriever

sample_email = "fattan@snowykim-demo.com"


r = Retriever()
current_user = r.get_current_user(sample_email)

print(r.answer_question("how much is Sarah Kim earning", current_user))







