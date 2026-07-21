from retriever import Retriever

sample_email = "fattan@snowykim-demo.com"

r = Retriever()

# Test routing
print(r.route_query("How much am I earning currently?"))
print(r.route_query("What type of insurance do we get?"))
print(r.route_query("What is Maya Patel's email?"))

# Test current user from email
print(r.get_current_user(sample_email))

curr_user = r.get_current_user(sample_email)

# Test target employee
print(r.target_employee("What location is Marcus Johnson at?", curr_user))

# Test access control
print(r.answer_question("What have we done in the past when employees have had a conflict due to a romantic relationship?", curr_user)) # should be not allowed


# Test full flow
print(r.answer_question("What is my salary?", curr_user))
print(r.answer_question("Tell me one thing about executive strategy", curr_user))