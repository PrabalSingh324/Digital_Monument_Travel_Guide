const faqQuestions = document.querySelectorAll(".faq-question");

faqQuestions.forEach(question => {

    question.addEventListener("click", () => {

        const currentAnswer = question.nextElementSibling;
        const currentIcon = question.querySelector("span");

        faqQuestions.forEach(item => {

            if(item !== question){

                item.nextElementSibling.style.maxHeight = null;
                item.querySelector("span").textContent = "+";

            }

        });

        if(currentAnswer.style.maxHeight){

            currentAnswer.style.maxHeight = null;
            currentIcon.textContent = "+";

        }else{

            currentAnswer.style.maxHeight =
            currentAnswer.scrollHeight + "px";

            currentIcon.textContent = "−";

        }

    });

});