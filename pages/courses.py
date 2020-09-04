# Last edit: November 14, 2019 by Hayden Hoopes, hayden.hoopes@usu.edu


def courses(collegeAndCorrespondingCollegeID, terms, departmentAndCorrespondingDeptID, colleges):
    from flask import render_template, request, session
    from hayden_functions import api, make_table
    from pages import stats_page

    token = session['TOKEN']

    if request.method == 'POST':

        #  Are we going to a new page?
        if request.form.get('new_page', None) is not None:
            new_page = int(request.form['new_page'])
            page_before = int(session['PAGE'])

            #  Are we going to the next page?
            if new_page > page_before:
                session['PAGE'] += 1
                more_pages_URI = session['NEXT_PAGE']
                session['NOW_URI'] = more_pages_URI

                #  Are we going to the previous page?
            elif new_page < page_before:
                session['PAGE'] -= 1
                more_pages_URI = session['PREVIOUS_PAGE']
                session['NOW_URI'] = more_pages_URI

                #  If not, we must be staying on the same page.
            else:
                more_pages_URI = session['NOW_URI']

            term = session['TERM']
            deleted = session['DELETED']
            department = session['DEPARTMENT']
            departmentID = departmentAndCorrespondingDeptID[department]
            college = session['COLLEGE']
            deleted_checked = session['DELETED']
            data, more_pages_URI, first, last, per_page = api.courses(token, id=departmentID,
                                                                      more_pages_URI=more_pages_URI,
                                                                      deleted=deleted)
            data = make_table.make(data)
            return render_template('courses.html', departments=departmentAndCorrespondingDeptID, token=token,
                                   colleges=collegeAndCorrespondingCollegeID, terms=terms, data=data,
                                   department=department, more_pages=more_pages_URI, term=term,
                                   new_page=new_page, first=first, last=last, colleges_departments=colleges,
                                   college=college, deleted_checked=deleted_checked, with_dropdown=True)

        # If not getting assignments and not going to a new page, we must be trying to get new data for a course or
        # department
        else:

            #  Page 1
            session['PAGE'] = 1
            new_page = 1

            #  Do we want to see only deleted courses?
            if request.form.getlist('deleted') == ["Show Deleted"]:
                deleted = True
            else:
                deleted = False
            session['DELETED'] = deleted

            #  Let's get the college
            if request.form.get('college',
                                None) is None:  # If a college has not been selected, tell the user to select one
                return 'Please select a college / department<br><a href="/courses">Go back</a>'
            session['COLLEGE'] = request.form['college']  # Otherwise, get the college
            college = session['COLLEGE']

            #  Let's get the department
            if request.form.get('department', None) is None:
                return 'Please select a college / department<br><a href="/courses">Go back</a>'
            session['DEPARTMENT'] = request.form['department']
            department = session['DEPARTMENT']  # Get the department
            departmentID = departmentAndCorrespondingDeptID[department]

            #  Let's get the term
            if request.form.get('term',
                                None) != 'All Terms':  # If the user didn't select "All Terms" then get the term.
                if request.form.get('term', None) is not None:
                    session['TERM'] = request.form['term']
                term = session['TERM']  # Store the term in the session for getting next and prev pages later
                termID = terms[term]
            else:
                session['TERM'] = None  # Otherwise, set the term equal to none so that we get all terms.
                term = session['TERM']
                termID = None

            # Now we ask: Are we getting courses or summary data for a department?
            if request.form.get('summary') == 'getDepartmentSummary':
                return stats_page.summary_statistics(colleges, collegeAndCorrespondingCollegeID, terms, college,
                                                     departmentAndCorrespondingDeptID, department, term, termID)

            else:
                data, more_pages_URI, first, last, per_page = api.courses(token, id=departmentID, term=termID,
                                                                          deleted=deleted)

            data = make_table.make(data)
            deleted_checked = session['DELETED']

            return render_template('courses.html', departments=departmentAndCorrespondingDeptID,
                                   colleges=collegeAndCorrespondingCollegeID, terms=terms, data=data,
                                   department=department, more_pages=more_pages_URI, term=term, token=token,
                                   new_page=new_page, first=first, last=last, colleges_departments=colleges,
                                   college=college, deleted_checked=deleted_checked, with_dropdown=True)

    # If a POST request has not been made (redirected to this page without submitting anything), just pull up the
    # dropdown menu
    return render_template('courses.html', departments=departmentAndCorrespondingDeptID, homepage=True,
                           colleges=collegeAndCorrespondingCollegeID, terms=terms, colleges_departments=colleges,
                           with_dropdown=True)
