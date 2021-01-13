
class Question {
    constructor(qType, qID){
        //short ans, long ans, multiple choice, checkbox
        //sa, la, mc, cb 
        this._____var__questionType = qType;

        this._____var__questionID = qID;
    }

    get questionType(){
        return this._____var__questionType;
    }
    set questionType(x){
        this._____var__questionType = x;
    }

    get questionTitle(){
        return this._____var__questionTitle;
    }
    set questionTitle(x){
        this._____var__questionTitle = x;
    }

    get isAutoGraded(){
        return this._____var__isAutoGraded;
    }
    set isAutoGraded(x){
        this._____var__isAutoGraded = x;
    }

    get questionOptions(){
        return this._____var__questionOptions;
    }
    set questionOptions(x){
        this._____var__questionOptions = x;
    }

    get correctAnswer(){
        return this._____var__correctAnswer;
    }
    set correctAnswer(x){
        this._____var__correctAnswer = x;
    }

    get checkboxValues(){
        return this._____var__checkboxValues;
    }
    set checkboxValues(x){
        this._____var__checkboxValues = x;
    }

    get studentCheckboxValues(){
        return this._____var__studentCheckboxValues;
    }
    set studentCheckboxValues(x){
        this._____var__studentCheckboxValues = x;
    }

    get marksAwarded(){
        return this._____var__marksAwarded;
    }
    set marksAwarded(x){
        this._____var__marksAwarded = x;
    }

    get questionID(){
        return this._____var__questionID;
    }
    set questionID(x){
        this._____var__questionID = x;
    }

}

var availableQuestionID = 0;


var questions = [];

function createQuestion (qType) {
    availableQuestionID += 1;
    newQuestion = new Question(qType, availableQuestionID);
    questions.push(newQuestion);
    $("#allQuesitonsContainer").append(generateQuesionHTML(newQuestion));
    updateNumberedList();
    initialiseChips(qType, availableQuestionID);
    moduleChanged();
    $('select').formSelect();
    $("#id_passingScore").attr("max", questions.length);
}

function initialiseChips (qType, qID){
    if (qType === "mc" || qType === "cb"){
        $(`.chips-placeholder.chips-identifier-${qID}`).chips({
            placeholder: 'Add options',
            secondaryPlaceholder: '+Option',
            onChipAdd: function(){chipsEdited(qID);},
            onChipDelete: function(){chipsEdited(qID);},
        });
    }
}

function updateNumberedList (){
    for (i = 0; i < questions.length; i++){
        $(`#questionNumberLabel${questions[i].questionID}`).text(`${i + 1}.`);
    }
}

function chipsEdited(qID){
    var instance = M.Chips.getInstance($(`.chips-placeholder.chips-identifier-${qID}`));
    var chipsData = instance.chipsData;

    var parsedChipsData = [];
    for (i = 0; i < chipsData.length; i++){
        parsedChipsData.push(chipsData[i].tag);
    }

    let question = questions.find((o, i) => {
        if (o.questionID === qID) {
            return true; // stop searching
        }
    });

    if (question.questionType === "cb"){
        var checkboxData = question.checkboxValues;
        if (checkboxData === undefined){
            checkboxData = {};
        }
        var newCheckboxData = {};
        var studentCheckboxData = {};
        for (i = 0; i < parsedChipsData.length; i++){
            studentCheckboxData[parsedChipsData[i]] = false;
            if (parsedChipsData[i] in checkboxData){
                newCheckboxData[parsedChipsData[i]] = checkboxData[parsedChipsData[i]];
            }
            else {
                newCheckboxData[parsedChipsData[i]] = false;
            }
        }
        
        question.checkboxValues = newCheckboxData;
        console.log(studentCheckboxData);
        question.studentCheckboxValues = studentCheckboxData;
    }

    question.questionOptions = parsedChipsData;

    autoGradeAdd(qID);
    autoGradeAdd(qID);
}

function questionChanged (qID) {
    let question = questions.find((o, i) => {
        if (o.questionID === qID) {
            questions[i].questionTitle = $(`#QuestionTitle${qID}`).val();
            return true; // stop searching
        }
    });
}

function deleteQuestion (qID) {
    questions.find((o, i) => {
        if (o.questionID === qID) {
            questions.splice(i, 1);
            return true; // stop searching
        }
    });
    $(`.questionWrapper.question-div-identifier-id-${qID}`).remove();
    updateNumberedList();
    $("#id_passingScore").attr("max", questions.length);
}

function generateQuesionHTML (question) {
    
    if (question.questionType === "sa"){
        var questionTypeLabel = "Short Answer"
    } else if (question.questionType === "la"){
        var questionTypeLabel = "Long Answer"
    } else if (question.questionType === "mc"){
        var questionTypeLabel = "Multiple Choice"
    } else if (question.questionType === "cb"){
        var questionTypeLabel = "Checkboxes"
    }


    //actual question
    var generatedHTML = `
    <div class="row questionWrapper z-depth-2 question-div-identifier-id-${question.questionID}">
        <div class="questionContainer">
            <div class="row  noPadding valign-wrapper">
                <div class="input-field col s12 m10 quesionInput">
                    <h1 style="margin: 0px;" id="questionNumberLabel${question.questionID}" class="prefix"></h1>
                    <textarea onfocusout="questionChanged(${question.questionID})" id="QuestionTitle${question.questionID}" class="materialize-textarea"></textarea>
                    <label for="QuestionTitle${question.questionID}">Question</label>
                </div>
                <div class="col s5 m2">
                    <div class="grey darken-2 z-depth-1 questionTypeLabel white-text center-align">${questionTypeLabel}</div>
                </div>
            </div>
            <div class="row right-align noPadding" style="padding-right: 10px;">
                <div class="input-field col s12 m6">
                    <select id="questionTag" class="questionTag">
                    </select>
                    <label>Question Tag</label>
                </div>
                <a class="btn-flat"><i style="font-size: 2rem;" class="material-icons large red-text" onclick="deleteQuestion(${question.questionID})">delete</i></a>
            </div>`;

    if (question.questionType === "mc" || question.questionType === "cb") {
        generatedHTML += `
        <div class="row black-text" style="padding-left: 20px; padding-right: 20px;">
            <p style="margin-bottom: 0px; margin-top: 0px;">Options to choose from</p>
            <div style="margin-top: 0px;" class="chips chips-placeholder chips-identifier-${question.questionID}" ></div>
        </div>`
    }

    //autograde selector
    if (question.questionType != "la"){
        generatedHTML += `
            <div class="row" style="padding-left: 20px;">
                <div class="switch">
                    Auto-grade answer
                    <label >
                        <input onchange="autoGradeAdd(${question.questionID})" type="checkbox">
                        <span class="lever"></span>
                    </label>
                </div>
            </div>`;
    }


    generatedHTML += `
        </div>
    </div>`;
    return generatedHTML;
}

function autoGradeAdd(qID) {
    let question = questions.find((o, i) => {
        if (o.questionID === qID) {
            questions[i].isAutoGraded = !questions[i].isAutoGraded;
            return true; // stop searching
        }
    });
    
    if (question.isAutoGraded) {
        $(`div.question-div-identifier-id-${question.questionID.toString()} > div.questionContainer`).append(generateAutoGrade(question));
    } else {
        $(`div.question-div-identifier-id-${question.questionID.toString()} > div.questionContainer>.autoGradeContainer`).remove();
    }
    $('select').formSelect();
}

function saValidationChanged(qID) {
    let question = questions.find((o, i) => {
        if (o.questionID === qID) {
            questions[i].correctAnswer = $(`#validationAnswer${qID}`).val();
            return true; // stop searching
        }
    });
}
function mcValidationChanged(qID) {
    let question = questions.find((o, i) => {
        if (o.questionID === qID) {
            questions[i].correctAnswer = questions[i].questionOptions[parseInt($(`#validationAnswer${qID}`).val())];
            return true; // stop searching
        }
    });
}
function cbValidationChanged(qID, checkboxIndex) {
    let question = questions.find((o, i) => {
        if (o.questionID === qID) {
            var currentCheckboxValues = questions[i].checkboxValues;
            var optionChanged = questions[i].questionOptions[checkboxIndex];
            currentCheckboxValues[optionChanged] = !currentCheckboxValues[optionChanged];
            questions[i].checkboxValues = currentCheckboxValues;
            var correctAnswers = [];
            for (j = 0; j < currentCheckboxValues.length; j++) {
                if (currentCheckboxValues[j] === true) {
                    correctAnswers.push(Object.keys(currentCheckboxValues)[j]);
                }
            }
            questions[i].correctAnswer = correctAnswers;
            return true; // stop searching
        }
    });
}

function generateAutoGrade(question){
    var generatedHTML = "";
    if (question.questionType === "sa"){
        generatedHTML += `
        <div class="row autoGradeContainer">
            <div class="input-field col s12 m6">
                <input id="validationAnswer${question.questionID}"  type="text" class="validate" onfocusout="saValidationChanged(${question.questionID})">
                <label class="active" for="validationAnswer${question.questionID}">Answer to check against</label>
            </div>
        </div>`;
    } 
    else if (question.questionType === "mc"){
        generatedHTML += `
        <div class="row autoGradeContainer">
            <div class="input-field col s12 m6">
                <select id="validationAnswer${question.questionID}" onChange="mcValidationChanged(${question.questionID})">
                    <option value="" disabled selected>Select correct option</option>
                    `
        question.questionOptions.forEach(function (option, index) {
            generatedHTML += `
                    <option value="${index.toString()}">${option}</option>\n`
        });
        generatedHTML += `
                </select>
                <label>Correct Option</label>
            </div>
        </div>`;
    } 
    else if (question.questionType === "cb"){
        generatedHTML += `
        <div class="row autoGradeContainer">
            <div style="margin-top: 10px;" class="input-field col s12 m6">
            <p style="margin-top: 0px;">Select Correct Options</p>`;
        question.questionOptions.forEach(function (option, index) {
            if (question.checkboxValues[option] === true){
                var isCheckedHTML = 'checked="checked"';
            }
            else {
                var isCheckedHTML = '';
            }
            generatedHTML += `
            <p>
                <label>
                    <input type="checkbox" ${isCheckedHTML} id="checkbox-question${question.questionID}-index${index}" oninput="cbValidationChanged(${question.questionID}, ${index})"/>
                    <span>${option}</span>
                </label>
            </p>`;
        });
    }
        
    return generatedHTML;

}






function convertToJSON() {
    jsonQuestions = JSON.stringify(questions);
    $("#allQuestionsJSON").val(jsonQuestions);
}

function submitForm() {
    if(questions.length > 0){
        convertToJSON();
        $("#quizDataForm").submit();
    }
    else{
        const errorNotification = window.createNotification({
            theme: 'warning',
        });
        // Invoke success notification
        errorNotification({ 
            message: 'Please add at least one question' 
        });
    }
}



var tags = {};

function setTags(retrievedTags) {
    console.log(retrievedTags);
    tags = retrievedTags;

}


function moduleChanged() {
    assignedModule = $(`#moduleSelect${selectedCourseID}`).val();
    console.log(assignedModule);
    console.log(tags[assignedModule]);
    selectOptions = `
    <option value="" disabled selected>Choose question tag</option>
    `;
    if (tags[assignedModule] === undefined){
        selectOptions += `<option value="" selected>this module has no tags</option>`
    }
    else {
        tags[assignedModule].forEach(function (option, index) {
            selectOptions += `
                    <option value="${index.toString()}">${option}</option>\n`
        });
    }
    $('.questionTag').html(selectOptions);
    $('select').formSelect();
}