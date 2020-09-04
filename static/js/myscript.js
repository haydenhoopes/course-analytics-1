function getDepartments(raw_data) {
//    Separates departments by college in order to filter department based on user selection of college
    var rawData, unformatted_data, colleges_departments, selected, option_list, college, department;
    colleges_departments = raw_data;
    college = document.getElementById("college");
    selected = college.options[college.selectedIndex].text;
    option_list = "";
    college;
    department;
    for (college of colleges_departments) {
        if (college.name === selected) {
            var departments = college.departments;
            for (department in departments) {
                option_list += "<option>" + departments[department].name + "</option>";
            }
        }
    }
    if (option_list === "") {
        option_list += "<option selected disabled>No departments available</option>";
    }
    document.getElementById("department").innerHTML = option_list;
}


function allowSubmit() {
//    Disables or enables button clickability to prevent against errors
    var college, collegeTag, departmentTag, department, selectedTerm, button1, button2;
    college = document.getElementById("college").value;
    department = document.getElementById("department").value;
    collegeTag = document.getElementById("college");
    departmentTag = document.getElementById("department");
    button1 = document.getElementById("button1");
    button2 = document.getElementById("button2");
    if (college !== "" && department !== "No departments available") {
        button1.disabled = false;
        button2.disabled = false;
    } else {
        button1.disabled = true;
        button2.disabled = true;
    }
}


function next_page() {
//    Increases invisible page input attribute by one, which will be returned to courses.py to go to next page
    var page = document.getElementById("new_page").value;
    variable = Number(page);
    variable += 1;
    document.getElementById("new_page").value = variable
}


function prev_page() {
//    Decreases invisible page input attribute by one, which will be returned to courses.py to go to previous page

    var page = document.getElementById("new_page").value;
    variable = Number(page);
    variable -= 1;
    document.getElementById("new_page").value = variable
}


function openAssignmentPanel(id) {
//    Opens the assignment panel and calls function to get assignments from /_assignments endpoint
    const panel = document.getElementById(id);
    if (panel.style.height === "300px") {
        panel.style.height = "0px";
        panel.style.display = "none";
    } else {
        panel.style.display = "block";
        panel.style.height = "300px";
        panel.innerHTML = "Loading..."
        runAssignmentsAPI(id);
    }
}


function runAssignmentsAPI(id) {
//    Gets assignment data from /_assignments endpoint, then changes assignment panel to a table with relevant information
    let panel;
    panel = document.getElementById(id);
    $.getJSON('/_assignments', {id: id}, function(result) {
        assignmentDiv = makeAssignmentDiv(result);
        panel.innerHTML = assignmentDiv;
    });
}


function makeAssignmentDiv(data) {
//    Creates a table using divs and assignment data
    let discussion_topic, online_quiz, on_paper, count_none, external_tool, online_text_entry;
    let online_url, online_upload, media_recording, total_assignments;
    let div1, div2, div3, div4, div5, div6, div7, div8, div9, div10;

    discussion_topic = data.discussion_topic;
    online_quiz = data.online_quiz;
    on_paper = data.on_paper;
    external_tool = data.external_tool;
    online_text_entry = data.online_text_entry;
    online_url = data.online_url;
    online_upload = data.online_upload;
    media_recording = data.media_recording;
    none = data.none;
    total_assignments = data.total_assignments;

    div1 = '<div class="divTableCell">' + discussion_topic + '</div>';
    div2 = '<div class="divTableCell">' + online_quiz + '</div>';
    div3 = '<div class="divTableCell">' + on_paper + '</div>';
    div4 = '<div class="divTableCell">' + external_tool + '</div>';
    div5 = '<div class="divTableCell">' + online_text_entry + '</div>';
    div6 = '<div class="divTableCell">' + online_url + '</div>';
    div7 = '<div class="divTableCell">' + online_upload + '</div>';
    div8 = '<div class="divTableCell">' + media_recording + '</div>';
    div9 = '<div class="divTableCell">' + none + '</div>';
    div10 = '<div class="divTableCell">' + total_assignments + '</div>';

    divToReturn =
        '<div class="divTable">' +
        '<div class="divTableBody">' +

        '<div class="divTableHeading">' +
        '<div class="divTableHead">Assignment</div>' +
        '<div class="divTableHead">Count</div>' +
        '</div>' +

        '<div class="divTableRow">' +
        '<div class="divTableCell">Discussion Topic</div>' +
        div1 +
        '</div>' +

        '<div class="divTableRow">' +
        '<div class="divTableCell">Online Quiz</div>' +
        div2 +
        '</div>' +

        '<div class="divTableRow">' +
        '<div class="divTableCell">On Paper</div>' +
        div3 +
        '</div>' +

        '<div class="divTableRow">' +
        '<div class="divTableCell">External Tool</div>' +
        div4 +
        '</div>' +

        '<div class="divTableRow">' +
        '<div class="divTableCell">Online Text Entry</div>' +
        div5 +
        '</div>' +

        '<div class="divTableRow">' +
        '<div class="divTableCell">Online URL</div>' +
        div6 +
        '</div>' +

        '<div class="divTableRow">' +
        '<div class="divTableCell">Online Upload</div>' +
        div7 +
        '</div>' +

        '<div class="divTableRow">' +
        '<div class="divTableCell">Media Recording</div>' +
        div8 +
        '</div>' +

        '<div class="divTableRow">' +
        '<div class="divTableCell">None</div>' +
        div9 +
        '</div>' +

        '<div class="divTableRow">' +
        '<div class="divTableCell">Total Assignments</div>' +
        div10 +
        '</div>' +
        '</div>' +
        '</div>';

    return divToReturn

}

function pleaseWait() {
//    Makes loader box visible
    var loader;
    loader = document.getElementById("loaderbox");
    loader.style.visibility = 'visible';
}
