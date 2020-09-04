def summary_statistics(colleges, collegeAndCorrespondingCollegeID, terms, college, departmentAndCorrespondingDeptID,
                       department, term, termID):
    from flask import render_template, session
    from hayden_functions import summary

    token = session['TOKEN']

    departmentID = departmentAndCorrespondingDeptID[department]

    data = summary.departmentSummary(token, departmentID, termID)

    if data['stats']:
        has_syllabus = data['stats']['has_syllabus']
        feed = data['stats']['feed']
        modules = data['stats']['modules']
        syllabus = data['stats']['syllabus']
        wiki = data['stats']['wiki']
        assignments = data['stats']['assignments']
        total = data['stats']['total']
        published_courses_with_syllabus = data['stats']['published_course_and_has_syllabus']
    else:
            has_syllabus = None
            feed = None
            modules = None
            syllabus = None
            wiki = None
            assignments = None
            total = None
            published_courses_with_syllabus = None

    return render_template('courses.html', colleges=collegeAndCorrespondingCollegeID, terms=terms,
                           departments=departmentAndCorrespondingDeptID, department=department, has_syllabus=has_syllabus,
                           feed=feed, modules=modules,syllabus=syllabus,wiki=wiki, assignments=assignments,
                           total=total,term=term, college=college, colleges_departments=colleges, with_dropdown=True,
                           published_courses_with_syllabus=published_courses_with_syllabus)
