var enableTrivia = true;

var questionTimeLimit = 35;
var intervalTimeLimit = 10;

var currentQuestion = {};

$(document).ready(function () {
    if (enableTrivia) {
        cleanUpData();
        setTimer(questionTimeLimit);
        GetQuestion();
    }
});

function GetQuestion() {
    setTimerText("Answer in ", questionTimeLimit);
    currentQuestion = {};
    $.ajax({
        url: "https://opentdb.com/api.php?amount=1&category=15",
        method: "GET",
        success: RenderQuestion
    });
}

function RenderQuestion(response) {
    log(response);
    if (response && response.response_code === 0) {
        var questionObject = response.results[0];

        var $questionContainer = $(".triviaQuestion");
        var $answersContainer = $(".triviaAnswers");

        $questionContainer.empty();
        $answersContainer.empty();

        $questionContainer.html(questionObject.question);
        currentQuestion.Question = questionObject.question;
        currentQuestion.Answers = [];

        if (questionObject.type === "multiple") {

            var questionCount = questionObject.incorrect_answers.length + 1;
            log("There are " + questionCount + " questions");

            var correctAnswerSlot = Math.floor(Math.random() * questionCount);
            log("Inserting correct answer into slot " + correctAnswerSlot);

            for (var i = 0; i < questionCount; i++) {
                var letter = String.fromCharCode(65 + i);
                var correctAnswer = (i === correctAnswerSlot);
                var answerText = (correctAnswer ? questionObject.correct_answer : questionObject.incorrect_answers.pop());

                currentQuestion.Answers.push({
                    "AnswerText": answerText,
                    "AnswerValue": letter,
                    "Index": i,
                    "Correct": correctAnswer
                });

                $answersContainer.append("<div class='triviaAnswer triviaAnswer" + i + "'><h3>" + letter + "</h3>" + answerText + "</div>");
            }

            log("Correct answer is in slot " + correctAnswerSlot);
            revealAnswer(correctAnswerSlot);

        } else if (questionObject.type === "boolean") {
            $answersContainer.append("<div class='triviaAnswer triviaAnswer1'>True</div>");
            $answersContainer.append("<div class='triviaAnswer triviaAnswer0'>False</div>");

            var answerIsTrue = (questionObject.correct_answer === "True");

            currentQuestion.Answers.push({
                "AnswerText": "True",
                "AnswerValue": "TRUE",
                "Index": 0,
                "Correct": answerIsTrue,
                "Answerers": []
            });
            currentQuestion.Answers.push({
                "AnswerText": "False",
                "AnswerValue": "FALSE",
                "Index": 1,
                "Correct": !answerIsTrue,
                "Answerers": []
            });

            if (answerIsTrue) {
                log("Correct answer is True");
                revealAnswer(1);
            } else {
                log("Correct answer is False");
                revealAnswer(0);
            }
        }
        else {
            log("fuck knows what to do now");
        }
    }
}

function revealAnswer(index) {
    $correctAnswerContainer = $(".triviaAnswer" + index);

    var questionCountdown = startCountdown();

    setTimeout(function () {
        clearInterval(questionCountdown);
        var $answersContainer = $(".triviaAnswers");
        $answersContainer.children().addClass("triviaIncorrect");
        $correctAnswerContainer.removeClass("triviaIncorrect").addClass("triviaCorrect");

        awardPoints(index);

        //Start the countdown to the next question
        setTimerText("Next question in ", intervalTimeLimit);
        var intervalCountdown = startCountdown(0);
        setTimeout(function () {
            clearInterval(intervalCountdown);
            GetQuestion();
        }, intervalTimeLimit * 1000);

    }, questionTimeLimit * 1000);
}

function setTimerText(text, time) {
    var $timer = $(".triviaTimer");
    var $counter = $(".triviaTimer > span");

    $timer.html(text + " <span>" + time + "</span> seconds");
}

function startCountdown() {
    return setInterval(function () {
        setTimer(getTimer() - 1);
    }, 1000);
}

function setTimer(time) {
    var $counter = $(".triviaTimer > span");
    $counter.html(time);
}

function getTimer() {
    var $counter = $(".triviaTimer > span");
    return parseInt($counter.html());
}

function awardPoints(index) {
    var rewardValue = currentQuestion.Answers[index].AnswerValue;
    $.getJSON("data.json", function(json){
        json.forEach((player) => {
            var addRemove;
            if (player.Choice === rewardValue) {                
                addRemove = "addpoints";
            }
            else {
                addRemove = "removepoints";
            }
            var command = "!" + addRemove + " " + player.Username + " " + player.Points;
            log(command);
            $.ajax({
                url: "http://localhost:8911/api/v2/chat/message",
                method: "POST",
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                data: JSON.stringify({Message: command})
            });
        });
        cleanUpData();
    });
}

function cleanUpData() {
    $.ajax({
        url: "http://localhost:8911/api/v2/commands",
        success: function(commandsResponse) {
            var command = commandsResponse.Commands.find((c) => c.Name === "Start New Question");
            $.ajax({
                url: "http://localhost:8911/api/v2/commands/"+command.ID,
                method: "POST",
                success: function() {
                    log("Cleaned up successfully");
                },
                error: function(error) {
                    log("Failed to run function");
                    log(error);
                }                
            });
        }
    });
}
//sybilkitsune_ and rafgaming333 were here when I wrote this
