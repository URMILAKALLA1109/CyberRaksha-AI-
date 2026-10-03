// ================= LANGUAGE =================

const languageSelector =
    document.getElementById("language");

if (languageSelector) {

    const savedLanguage =
        localStorage.getItem("cyberraksha_language");

    if (savedLanguage) {
        languageSelector.value = savedLanguage;
    }

    languageSelector.addEventListener(
        "change",
        function () {

            localStorage.setItem(
                "cyberraksha_language",
                this.value
            );

        }
    );
}


// ================= VOICE INPUT =================

function startVoice() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        alert(
            "Voice recognition is not supported. Please use Google Chrome."
        );

        return;
    }


    const recognition =
        new SpeechRecognition();


    // Selected language
    recognition.lang =
        languageSelector
            ? languageSelector.value
            : "en-IN";


    // Keep listening
    recognition.continuous = true;

    // Show partial speech also
    recognition.interimResults = true;


    let finalText = "";

    let silenceTimer = null;

    let manuallyStopped = false;


    // ================= START =================

    recognition.onstart = function () {

        const status =
            document.getElementById("voiceStatus");

        if (status) {

            status.textContent =
                "🎙️ Listening... Tell us what happened.";

        }

    };


    // ================= SPEECH RESULT =================

    recognition.onresult = function (event) {

        let interimText = "";


        for (
            let i = event.resultIndex;
            i < event.results.length;
            i++
        ) {

            const transcript =
                event.results[i][0].transcript;


            if (event.results[i].isFinal) {

                finalText +=
                    transcript + " ";

            } else {

                interimText +=
                    transcript;

            }

        }


        // Show speech inside textbox

        const input =
            document.getElementById("incidentInput");


        if (input) {

            input.value =
                finalText + interimText;

        }


        // Every time user speaks,
        // restart silence timer

        clearTimeout(silenceTimer);


        silenceTimer =
            setTimeout(function () {

                const text =
                    finalText.trim();


                if (!text) {
                    return;
                }


                const status =
                    document.getElementById("voiceStatus");


                if (status) {

                    status.textContent =
                        "🔍 Understanding your incident...";

                }


                manuallyStopped = true;


                recognition.stop();


                analyzeIncident(text);


            }, 2500);

    };


    // ================= ERROR =================

    recognition.onerror =
        function (event) {

            console.error(
                "Voice recognition error:",
                event.error
            );


            clearTimeout(silenceTimer);


            const status =
                document.getElementById("voiceStatus");


            if (status) {

                status.textContent =
                    "❌ Voice recognition failed. Please try again.";

            }

        };


    // ================= END =================

    recognition.onend =
        function () {

            console.log(
                "Voice recognition ended."
            );


            /*
             If Chrome stops recognition automatically
             while the user is still speaking,
             start it again.
            */

            if (!manuallyStopped && finalText.trim()) {

                try {

                    recognition.start();

                } catch (error) {

                    console.log(
                        "Recognition restart skipped."
                    );

                }

            }

        };


    // ================= START LISTENING =================

    try {

        recognition.start();

    } catch (error) {

        console.error(
            "Unable to start voice recognition:",
            error
        );

    }

}



// ================= TYPED INCIDENT =================

function analyzeTypedIncident() {

    const input =
        document.getElementById("incidentInput");


    if (!input) {

        alert(
            "Incident input box was not found."
        );

        return;

    }


    const text =
        input.value.trim();


    if (!text) {

        alert(
            "Please type or speak what happened."
        );

        return;

    }


    analyzeIncident(text);

}



// ================= SEND INCIDENT TO BACKEND =================

function analyzeIncident(text) {

    const status =
        document.getElementById("voiceStatus");


    if (status) {

        status.textContent =
            "🔍 Analyzing your incident...";

    }


    fetch("/analyze", {

        method: "POST",

        headers: {

            "Content-Type":
                "application/json"

        },

        body: JSON.stringify({

            text: text

        })

    })


    .then(function (response) {

        if (!response.ok) {

            throw new Error(
                "Server error: " +
                response.status
            );

        }

        return response.json();

    })


    .then(function (data) {

        if (!data.success) {

            alert(
                data.message ||
                "Unable to analyze the incident."
            );

            return;

        }


        if (status) {

            status.textContent =
                "✅ Incident identified. Opening guidance...";

        }


        // Open related crime page

        setTimeout(function () {

            window.location.href =
                "/crime/" +
                data.crime_type;

        }, 500);

    })


    .catch(function (error) {

        console.error(
            "Analysis error:",
            error
        );


        alert(
            "Something went wrong while analyzing the incident. Please try again."
        );


        if (status) {

            status.textContent =
                "❌ Unable to analyze the incident.";

        }

    });

}



// ================= POLICE-READY SUMMARY =================

function createSummary(crimeType) {

    const incident =
        prompt(
            "Describe what happened in your own words:"
        );


    if (!incident) {

        return;

    }


    const name =
        prompt(
            "Enter your name (optional):"
        ) || "";


    const phone =
        prompt(
            "Enter your phone number (optional):"
        ) || "";


    fetch("/generate-summary", {

        method: "POST",

        headers: {

            "Content-Type":
                "application/json"

        },

        body: JSON.stringify({

            incident: incident,

            name: name,

            phone: phone

        })

    })


    .then(function (response) {

        if (!response.ok) {

            throw new Error(
                "Server error: " +
                response.status
            );

        }

        return response.json();

    })


    .then(function (data) {

        if (!data.success) {

            alert(
                data.message
            );

            return;

        }


        const box =
            document.getElementById(
                "summaryBox"
            );


        const textarea =
            document.getElementById(
                "summaryText"
            );


        if (textarea) {

            textarea.value =
                data.summary;

        }


        if (box) {

            box.style.display =
                "block";


            box.scrollIntoView({

                behavior: "smooth"

            });

        }

    })


    .catch(function (error) {

        console.error(
            "Summary error:",
            error
        );


        alert(
            "Unable to generate summary."
        );

    });

}