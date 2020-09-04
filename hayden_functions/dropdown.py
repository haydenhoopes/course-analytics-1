def colleges(token):
    from hayden_functions import api
    collegesAtUSU = api.subaccounts(token, optional_base_params={'per_page': '200', 'recursive': 'True'})
    colleges = []
    for entry in collegesAtUSU:
        if entry['parent_account_id'] == 15:
            anotherCollege = {}
            anotherCollege['name'] = entry['name']
            anotherCollege['id'] = entry['id']
            anotherCollege['departments'] = []
            colleges.append(anotherCollege)
        else:
            for college in colleges:
                if entry['parent_account_id'] == college['id']:
                    anotherDepartment = {}
                    anotherDepartment['name'] = entry['name']
                    anotherDepartment['id'] = entry['id']
                    college['departments'].append(anotherDepartment)
                else:
                    pass
    return colleges


def terms(token):
    from hayden_functions import api
    enrollment_terms = api.enrollment_terms(token)
    all_terms = {}
    listOfTerms = enrollment_terms['enrollment_terms']
    for term in listOfTerms:
        all_terms[term['name']] = term['id']
    return all_terms


def departmentAndCorrespondingDeptID(colleges):
    depDict = {}
    for college in colleges:
        departments = college['departments']
        for department in departments:
            departmentName = department['name']
            departmentID = department['id']
            depDict[departmentName] = departmentID
    return depDict

def collegeAndCorrespondingCollegeID(colleges):
    collegeIDs = {}
    for college in colleges:
        collegeIDs[college['name']] = college['id']
    return collegeIDs

def departmentIDs(colleges):
    departmentIDs = {}
    for college in colleges:
        for value in college.values():
            if isinstance(value, list):
                for department in value:
                    departmentIDs[department['name']] = department['id']
    return departmentIDs
