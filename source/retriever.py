#retrieves documents and generates
#checks for access
#checks for record info vs document info (compensation, employee data vs policy)

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
