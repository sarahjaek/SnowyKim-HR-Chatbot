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
            If no person is named, respond with "NONE". If only a person's first or last name is named, respond exactly with "NEED_FULL_NAME".

            Question = {query}
            Name:"""
        name_result = self.router_llm.invoke(prompt).content.strip()
        if name_result == "NONE":
            return None
        if name_result == "NEED_FULL_NAME":
            return "NEED_FULL_NAME"
        name_result_split = name_result.strip().split(" ", 1)
        if len(name_result_split) < 2:
            return None
        first, last = name_result_split[0], name_result_split[1]
        first_record = self.employee_store.get_record_by_field("first_name", first)
        if first_record and first_record.get("last_name", "").lower() == last.lower(): # if first_record none, then doesn't pass
            return first_record["employee_id"]
        return None


    def is_allowed(self, doc_type, current_user) -> bool:
        
    def answer_policy:
    
    def answer_employee:
    
    def answer_compensation: