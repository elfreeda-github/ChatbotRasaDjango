var coll = document.getElementsByClassName("collapsible");

//Collapsible
for(let i=0; i<coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("active");

        var content = document.getElementsByClassName("content")[0];
        
        if(content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }
    })
}


//Current Time
function getTime() {
    let today = new Date();
    hours = today.getHours();
    minutes = today.getMinutes();

    if(hours < 10) {
        hours = "0" + hours;
    }
    if(minutes < 10) {
        minutes = "0" + minutes;
    }
    let time = hours + ":" + minutes;
    return time;
}


function firstBotMessage() {
    let firstMessage = "Hey! How may I assit you?"
    let time = getTime();

    $("#chat-timestamp").append(time);
	let botHtml= `<img class="botAvatar" src="/static/images/bot.png" width="50px" height="50px"/><p class="botText"><span> ${firstMessage}</span></p>`;
    $("#chatbox").append(botHtml);
	document.getElementById("chat-bar-bottom").scrollIntoView(true);
}

firstBotMessage();

function getResponse() {
    let userText = $("#textInput").val();
    if(userText == "") {
        userText = "I love chatbot!";
    }
    $("#textInput").val("");
	setUserResponse(userText);
	send(userText);
}

function buttonSendText(sampleText) {
    $("#textInput").val("");
    setUserResponse(sampleText);
	send(sampleText);
}

function sendButton() {
    getResponse();
}

function heartButton() {
    buttonSendText("It was amazing chatting with you!")
}

//Please Enter to send text
$("#textInput").keypress(function(e) {
    var keyCode = e.keyCode || e.which;
	var text = $("#textInput").val();
	if (keyCode === 13) {
		if (text == "" || $.trim(text) == '') {
			e.preventDefault();
			return false;
		} else {
			$("#textInput").blur();
			setUserResponse(text);
			send(text);
			e.preventDefault();
			return false;
		}
	}
})

// clear function to clear the chat contents of the widget.
  $("#clear").click(() => {
    $(".chatbox").fadeOut("normal", () => {
      $(".chatbox").html("");
      $(".chatbox").fadeIn();
	  setTimeout(function() {
		firstBotMessage();
	  },500); 
    });
  });

// restart function to restart the chat contents of the widget.
$("#restart").click(() => {
    $(".chatbox").fadeOut("normal", () => {
		$(".chatbox").html("");
		$(".chatbox").fadeIn();
		setTimeout(function() {
		  firstBotMessage();
		},500); 
	  });
});

// close function to close the widget.
  $("#close").click(() => {
	var content = document.getElementsByClassName("content")[0];
	if(content.style.maxHeight) {
		content.style.maxHeight = null;
	} else {
		content.style.maxHeight = content.scrollHeight + "px";
	}
});



//-------------Code to work with RASA----------------

//------------------------------------- Set user response------------------------------------
function setUserResponse(val) {
	var UserResponse = `<img class="userAvatar" src="/static/images/user.png" width="50px" height="50px"/><p class="userText"><span> ${val} </span></p>`;
    $("#textInput").val("");
    $("#chatbox").append(UserResponse);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);
}

//-------------------------------------- Send message to Bot --------------------------------
function send(message) {
	console.log("User Message:", message)
	$.ajax({
		url: 'http://localhost:5005/webhooks/rest/webhook',
		type: 'POST',
		data: JSON.stringify({
			"message": message,
			"sender": "username"
		}),
		success: function (data, textStatus) {
			setBotResponse(data);
			console.log("Rasa Response: ", data, "\n Status:", textStatus)
		},
		error: function (errorMessage) {
			setBotResponse("");
			console.log('Error' + errorMessage);

		}
	});
}


//------------------------------Set bot response ----------------------------
function setBotResponse(val) {
	setTimeout(function () {
		if (val.length < 1) {
			//if there is no response from Rasa
			msg = 'I couldn\'t get that. Let\' try something else!';

            let botHtml = `<img class="botAvatar" src="/static/images/bot.png" width="50px" height="50px"/><p class="botText"><span> ${msg} </span></p>`;
            $("#chatbox").append(botHtml);

		} else {
			//if we get response from Rasa
			for (i = 0; i < val.length; i++) {
				//check if there is text message
				if (val[i].hasOwnProperty("text")) {
					let txt = urlify(val[i].text);
					txt = txt.replace(/(?:\r\n|\r|\n)/g, '<br>')
					console.log("The txt is : "+txt)
					let botHtml = `<img class="botAvatar" src="/static/images/bot.png" width="50px" height="50px"/><p class="botText"><span> ${txt}</span></p>`;
					$("#chatbox").append(botHtml);
				}

				//check if there is image
				if (val[i].hasOwnProperty("image")) {
					var BotResponse = '<div class="singleCard">' +
						'<img class="imgcard" src="' + val[i].image + '">' +
						'</div><div class="clearfix"></div><br/>'
                        $("#chatbox").append(BotResponse);
				}

				// check if the response contains "buttons"
                if (Object.hasOwnProperty.call(val[i], "buttons")) {
                    if (val[i].buttons.length > 0) {
                        addSuggestion(val[i].buttons);
                    }
                }

				//link
				if (Object.hasOwnProperty.call(val[i], "link")) {
                    if (val[i].buttons.length > 0) {
                        checkInlineURL(val[i].link);
                    }
                }


			}
            document.getElementById("chat-bar-bottom").scrollIntoView(true);
		}

	}, 500);
}

//Local functions to change few texts
// [(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)

function urlify(text) {
	var urlRegex = /[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g;
	var inlineRegex = /]\(/g;
	subStr = text.substring(text.indexOf("[")+1,text.indexOf("]\("));
	if(subStr !== "") {
		text = text.replace(subStr,"");
		text = text.replace("["," ");
		text = text.replace("]"," ");
		text = text.replace(")"," ");
		text = text.replace("("," ");
	}	
	return text.replace(urlRegex, function(url) {
		if(subStr !== "") 
			return '<a href="' + url + '">' + subStr + '</a>';
		else 
			return '<a href="' + url + '">' + url + '</a>';
	})
}

// Function to check if there is any inline words to be added
// text: "Please click link to continue: [ALM Home](put your link in here)"
function checkInlineURL(inlineLinks) {
	let urlVal = '<a href="' + inlineLinks[0].url + '">' + inlineLinks[0].inline + '</a>'
	let botHtml = `<img class="botAvatar" src="/static/images/bot.png" width="50px" height="50px"/><p class="botText"><span> ${urlVal}</span></p>`;
	$("#chatbox").append(botHtml);
}


// For adding suggestion buttons
/**
 *  adds vertically stacked buttons as a bot response
 * @param {Array} suggestions buttons json array
 */
 function addSuggestion(suggestions) {
    setTimeout(() => {
        const suggLength = suggestions.length;
        $(
            ' <div class="singleCard"> <div class="suggestions"><div class="menu"></div></div></diV>',
        )
            .appendTo("#chatbox")
            .hide()
            .fadeIn(1000);
        // Loop through suggestions
        for (let i = 0; i < suggLength; i += 1) {
            $(
                `<div class="menuChips" data-payload='${suggestions[i].payload}'>${suggestions[i].title}</div>`,
            ).appendTo(".menu");
        }
		document.getElementById("chat-bar-bottom").scrollIntoView(true);
    }, 1000);
}


// on click of suggestion's button, get the title value and send it to rasa
$(document).on("click", ".menu .menuChips", function () {
    const text = this.innerText;
    const payload = this.getAttribute("data-payload");
    console.log("payload: ", this.getAttribute("data-payload"));
    setUserResponse(text);
    send(payload);

    // delete the suggestions once user click on it.
    $(".suggestions").remove();
});