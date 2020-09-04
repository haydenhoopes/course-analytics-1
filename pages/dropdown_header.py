from hayden_functions import dropdown
from flask import session


def dropdown_header():
    """   PLEASE DON'T DELETE THIS FUNCTION --- IT CACHES ALL THE DATA FOR FASTER LOADS   """
    token = session.get('TOKEN')
    colleges = dropdown.colleges(token)
    # collegesList = dropdown.collegesList(colleges)
    collegeAndCorrespondingCollegeID = dropdown.collegeAndCorrespondingCollegeID(colleges)
    departmentAndCorrespondingDeptID = dropdown.departmentAndCorrespondingDeptID(colleges)
    # departmentIDs = dropdown.departmentIDs(colleges)
    terms = dropdown.terms(token)
    return colleges, collegeAndCorrespondingCollegeID, terms, departmentAndCorrespondingDeptID
