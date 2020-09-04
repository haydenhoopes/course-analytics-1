from flask import session, jsonify
from hayden_functions import api


def assignments(id):
    token = session['TOKEN']
    id = str(id)
    assignmentsDict = {
        'discussion_topic': 0,
        'online_quiz': 0,
        'on_paper': 0,
        'count_none': 0,
        'external_tool': 0,
        'online_text_entry': 0,
        'online_url': 0,
        'online_upload': 0,
        'media_recording': 0,
        'none': 0,
        'total_assignments': 0
    }
    data = api.get_assignments(token, id)

    for assignment in data:
        for i in range(len(assignment['submission_types'])):
            if assignment['submission_types'][i - 1] == 'discussion_topic':
                assignmentsDict['discussion_topic'] += 1
            if assignment['submission_types'][i - 1] == 'online_quiz':
                assignmentsDict['online_quiz'] += 1
            if assignment['submission_types'][i - 1] == 'on_paper':
                assignmentsDict['on_paper'] += 1
            if assignment['submission_types'][i - 1] == 'count_none':
                assignmentsDict['count_none'] += 1
            if assignment['submission_types'][i - 1] == 'external_tool':
                assignmentsDict['external_tool'] += 1
            if assignment['submission_types'][i - 1] == 'online_text_entry':
                assignmentsDict['online_text_entry'] += 1
            if assignment['submission_types'][i - 1] == 'online_url':
                assignmentsDict['online_url'] += 1
            if assignment['submission_types'][i - 1] == 'online_upload':
                assignmentsDict['online_upload'] += 1
            if assignment['submission_types'][i - 1] == 'none':
                assignmentsDict['none'] += 1
            if assignment['submission_types'][i - 1] == 'media_recording':
                assignmentsDict['media_recording'] += 1
            assignmentsDict['total_assignments'] += 1
    return jsonify(assignmentsDict)
