#retrieves documents from vector and record stores at initialization 
#mock current user
#checks for access based on document type and current user access

from vector_store import VectorStore, RecordStore
from langchain_openai import ChatOpenAI

import re

cal_access = {
    "compensation-records": 
        {"employee": "own_only",
         "manager": "own_only",
         "hr_staff": "own_only",
         "hr_admin": "all",
         "it_admin": "own_only", 
         "executive": "own_only"},
    "employee-benefits":
        {"employee": "all",
         "manager": "all",
         "hr_staff": "all",
         "hr_admin": "all",
         "it_admin": "all",
         "executive": "all"},
    "employee-data": 
        {"employee": "all",
         "manager": "all",
         "hr_staff": "all",
         "hr_admin": "all",
         "it_admin": "all",
         "executive": "all"},
    "california-hr-policies":
        {"employee": "all",
         "manager": "all",
         "hr_staff": "all",
         "hr_admin": "all",
         "it_admin": "all",
         "executive": "all"},
    "newyork-hr-policies":
        {"employee": "all",
         "manager": "all",
         "hr_staff": "all",
         "hr_admin": "all",
         "it_admin": "all",
         "executive": "all"},
    "onboarding-policy":
        {"employee": "none",
         "manager": "none",
         "hr_staff": "all",
         "hr_admin": "all",
         "it_admin": "none",
         "executive": "all"},
    "past-cases":
        {"employee": "none",
         "manager": "none",
         "hr_staff": "all",
         "hr_admin": "all",
         "it_admin": "none",
         "executive": "none"},
    "recruitment-policy":
        {"employee": "none",
         "manager": "none",
         "hr_staff": "all",
         "hr_admin": "all",
         "it_admin": "none",
         "executive": "all"},
    "workplace-investigation":
        {"employee": "none",
         "manager": "none",
         "hr_staff": "none",
         "hr_admin": "all",
         "it_admin": "none",
         "executive": "none"}
}

ny_access = cal_access # new york access is the same as california access, except for the fields below.
ny_access["onboarding-policy"]["executive"] = "none"
ny_access["recruitment-policy"]["executive"] = "none"
ny_access["workplace-investigation"]["executive"] = "all"

class Retriever:

    def __init__(self, router_model = "gpt-5.4-nano", answer_model = "gpt-5.6-luna", k = 4):
        self.policy_store = VectorStore()
        self.employee_store = RecordStore(file_path ="./employee-database.json")
        self.compensation_store = RecordStore(file_path = "./compensation-database.json")
        self.router_llm = ChatOpenAI(model = router_model)
        self.answer_llm = ChatOpenAI(model = answer_model)
        self.k = k
    
    def route_query(self, query) -> str:
        #routes query into type: policy, employee info, or compensation using llm call
        prompt = f"""Classify this HR question into exactly ONE category. Respond with ONLY the category name (out of the three categories listed), nothing else.

            Categories:
            - policy: general company policy, benefits, procedures, onboarding, workplace conduct
            - employee_info: asking about an employee's general info like name, title, department, email, location, position, role.
            - compensation: asking about salary, pay, bonus, equity, or compensation details

            Question: {query}
            Category:"""

        response = self.router_llm.invoke(prompt)
        category = response.content.strip().lower()
        return category

    def target_employee(self, query: str, current_user: dict) -> str:
        '''
        finds employee the question is asking about (if classified into employee or compensation info), returns target employee id
        '''
        #Case 1: Employee is asking about themself
        query_words = query.lower().split()
        self_indicators = {"my", "mine", "i", "myself", "me"}
        if any(word.strip(".,?!") in self_indicators for word in query_words):
            return current_user["employee_id"]
            
        #Case 2: Employee asks using EMP id
        emp_id = re.search(r'EMP-?\d+', query, re.IGNORECASE)
        if emp_id:
            return emp_id.group()

        #Case 3: Employee asks different way
        prompt = f"""
            Extract the full name of the person being asked about in this question. Respond with ONLY the name, nothing else. 
            If no person is named, respond with "NONE". 
            If only a person's first or last name is named, respond exactly with "NEED_FULL_NAME".
            If MORE THAN ONE person is named, respond with "MULTIPLE".

            Question = {query}
            Name:"""
        name_result = self.router_llm.invoke(prompt).content.strip()
        if name_result == "NONE":
            return None
        if name_result == "NEED_FULL_NAME":
            return "NEED_FULL_NAME"
        if name_result == "MULTIPLE":
            return "MULTIPLE"
        name_result_split = name_result.strip().split(" ", 1)
        if len(name_result_split) < 2:
            return None
        first, last = name_result_split[0], name_result_split[1]
        first_record = self.employee_store.get_record_by_field("first_name", first)
        if first_record and first_record.get("last_name", "").lower() == last.lower(): # if first_record none, then doesn't pass
            return first_record["employee_id"]
        return None


    def is_allowed(self, doc_type: str, current_user: dict, target_id: str) -> bool:
        """
        Assuming current_user is valid dictionary in database, return whether the currrent user is allowed to access the specific doc.
        
        If employee_location invalid, returns None. Otherwise, checks access against relevant location access matrix.
        """
        employee_location = current_user["location"]
        employee_access = current_user["access_role"]
        
        if employee_location == "San Francisco":
            access = cal_access[doc_type][employee_access]
        elif employee_location == "New York":
            access = ny_access[doc_type][employee_access]
        else:
            print ("Location invalid.")
            return None
        if access == "all":
            return True
        if access == "own_only":
            if target_id == current_user["employee_id"]:
                return True
            else:
                return False
        return False

    def answer_policy(self, query: str, current_user: dict) -> str:
        """
        Answers policy questions---creates retriever, fetches documents, filters documents by access, then returns response based on context.
        """
        retriever = self.policy_store.get_retriever(k = self.k * 3) # overfetch in case documents access control fails
        documents = retriever.invoke(query)
        valid_docs = []
        
        for doc in documents:
            doc_name = doc.metadata.get("doc_type", "")
            if self.is_allowed(doc_name, current_user, None):
                valid_docs.append(doc)
        if not valid_docs:
            return "I do not have information you are authorized to access to answer this question."
        top_valid = valid_docs[:self.k]
        context = "\n\n".join(doc.page_content for doc in top_valid)
        return self.generate_answer(query, context)

    
    def answer_employee(self, query: str, current_user: dict) -> str:
        """
        Answers employee information questions by accessing target employee, e.g. "What is John Smith's email?"
        """
        query_target = self.target_employee(query, current_user) # returns employee id of relevant target
        target_record = self.employee_store.get_record(query_target)
        if not target_record:
            return "Employee information not found."
        context = str(target_record)
        return self.generate_answer(query, context)
    
    def answer_compensation(self, query: str, current_user: dict) -> str:
        """
        Answers compensation information questions by accessing target employee, e.g. "What is John Smith's salary?"
        Checks for access rules.
        """
        query_target = self.target_employee(query, current_user) # returns employee id of relevant target
        access = self.is_allowed(doc_type = "compsensation-records", current_user = current_user, target_id = query_target)
        if not access:
            return "You do not have access to this information."
        target_record = self.employee_store.get_record(query_target)
        context = str(target_record)
        return self.generate_answer(query, context)

    def generate_answer():
        #TODO
    def answer_question():
        #TODO
    def get_current_user():