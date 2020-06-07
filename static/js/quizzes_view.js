
function renderQuizQuestions(quizJSON) {
    
    var questionsData = JSON.parse(quizJSON);

    var finalHTML = "";
    for (k=0; k < questionsData.length; k++) {
        finalHTML += generateQuesionHTML(questionsData[k], k);
    }



    function generateQuesionHTML (question, index) {
        //actual question
        var generatedHTML = `
        <div class="row questionWrapper z-depth-2 question-div-identifier-id-${question.questionID}">
            <div class="questionContainer">
                <div class="row  noPadding valign-wrapper">
                    <div class="input-field col s12 quesionInput">
                        <h4 style="margin: 0px;" id="questionNumberLabel${question.questionID}">${index + 1}. ${question.questionTitle}</h4>
                    </div>
                </div>`;

        if (question.questionType === "mc") {
            generatedHTML += `
            <div class="row answerInputContainer">
                <div class="input-field col s12 m6">
                    <select id="mcAnswer${question.questionID}">
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

        if (question.questionType === "cb") {
            generatedHTML += `
            <div class="row answerInputContainer">
                <div style="margin-top: 10px; margin-bottom: 0px;" class="input-field col s12 m6">
                    <p style="margin-top: 0px;">Select Correct Options</p>`;
            question.questionOptions.forEach(function (option, index) {
                generatedHTML += `
                    <p>
                        <label>
                            <input type="checkbox" id="checkbox-question${question.questionID}-index${index}" oninput="cbValidationChanged(${question.questionID}, ${index})"/>
                            <span>${option}</span>
                        </label>
                    </p>`;
            });
            generatedHTML += `
                </div>
            </div>`;
        }

        if (question.questionType === "sa") {
            generatedHTML += `
            <div class="row answerInputContainer">
                <div class="input-field col s12 m6">
                    <input id="validationAnswer${question.questionID}"  type="text" class="validate">
                    <label for="validationAnswer${question.questionID}">Your answer</label>
                </div>
            </div>`;
        }

        if (question.questionType === "la") {
            generatedHTML += `
            <div class="row answerInputContainer">
                <div class="input-field col s12">
                    <textarea  id="validationAnswer${question.questionID}"  type="text" class="materialize-textarea"></textarea>
                    <label for="validationAnswer${question.questionID}">Your answer</label>
                </div>
            </div>`;
        }


        generatedHTML += `
            </div>
        </div>`;

        return generatedHTML;
    }

    return finalHTML;
}