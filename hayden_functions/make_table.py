import re
from hayden_functions import api
from flask import session
from time import time

currentTime = time()

syllabus_pattern = re.compile(
    r'href="https://usu.instructure.com/courses/\d+/files/\d+/download\?verifier=\S*"')

def make(data):
    data = keep(data)
    # assignments = getAssignments(data)
    if not data:
        data = None

    return data


def keep(data):
    valuesToKeep = ['id', 'name', 'default_view', 'term']
    newData = []
    for course in data:
        courseDict = {}
        for k in valuesToKeep:
            courseDict[k] = course[k]

        if course['syllabus_body']:
            courseDict['has_syllabus'] = 'Yes'
        else:
            courseDict['has_syllabus'] = 'No'

        if course['workflow_state'] == 'available':
            courseDict['published'] = 'Yes'
        else:
            courseDict['published'] = 'No'

        if course['teachers']:
            teacherList = []
            for teacher in course['teachers']:
                teacherList.append(teacher['display_name'])
            courseDict['teachers'] = ', '.join(teacherList)

        newData.append(courseDict)

    return newData


def parse_syllabus_with_download_link(x): # Unused function, use instead of parse_syllabus() to get download links for syllabi
    if x:
        match = syllabus_pattern.search(x)
        if match:
            return '<a ' + match.group(0) + '>Yes</a>'
        else:
            return 'Yes'
    else:
        return 'No'


def getAssignments(data):
    token = session['TOKEN']
    assignmentsList = []

    for course in data:

        courseDict = {}

        discussion_topic = 0
        online_quiz = 0
        on_paper = 0
        count_none = 0
        external_tool = 0
        online_text_entry = 0
        online_url = 0
        online_upload = 0
        media_recording = 0
        total_assignments = 0

        assignmentData = api.get_assignments(token, str(course['id']))
        if isinstance(assignmentData, str):
            pass
        else:
            for assignment in assignmentData:
                for i in range(len(assignment['submission_types'])):
                    if assignment['submission_types'][i-1] == 'discussion_topic':
                        discussion_topic += 1
                    if assignment['submission_types'][i-1] == 'online_quiz':
                        online_quiz += 1
                    if assignment['submission_types'][i-1] == 'on_paper':
                        on_paper += 1
                    if assignment['submission_types'][i-1] == 'none':
                        count_none += 1
                    if assignment['submission_types'][i-1] == 'external_tool':
                        external_tool += 1
                    if assignment['submission_types'][i-1] == 'online_text_entry':
                        online_text_entry += 1
                    if assignment['submission_types'][i-1] == 'online_url':
                        online_url += 1
                    if assignment['submission_types'][i-1] == 'online_upload':
                        online_upload += 1
                    if assignment['submission_types'][i-1] == 'media_recording':
                        media_recording += 1
                    total_assignments += 1

        courseDict['id'] = course['id']
        courseDict['assignments'] = {
            'discussion_topic': str(discussion_topic),
            'online_quiz': str(online_quiz),
            'on_paper': str(on_paper),
            'count_none': str(count_none),
            'external_tool': str(external_tool),
            'online_text_entry': str(online_text_entry),
            'online_url': str(online_url),
            'online_upload': str(online_upload),
            'media_recording': str(media_recording),
            'total_assignments': str(total_assignments)
        }

        # {'id': 547672, 'assignments': [{'discussion_topic': '6'}, {'online_quiz': '13'}, {'on_paper': '0'}, {'count_none': '3'}, {'external_tool': '0'}, {'online_text_entry': '7'}, {'online_url': '0'}, {'online_upload': '19'}, {'media_recording': '0'}, {'total_assignments': '48'}]}
        assignmentsList.append(courseDict)
    return assignmentsList


