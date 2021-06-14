$(function() {
    var $predictForm = $("#predictForm");
    if ($predictForm.length){
        $predictForm.validate({
    rules:{
        pId : {
            required: true,
            number: true
            
        },
        age : {
            required: true,
            number: true,
            range: [10, 120]

        },
        rbp:{
            required: true,
            number: true,
            range: [10, 400]

        },       
        chol:{
            required: true,
            number: true,
            range: [50, 800]

        },
        thalach :{
            required: true,
            number: true,
            range: [30, 400]

        },
        oldpeak : {
            required: true,
            number: true,
            min: 0,
            max: 20.0
        }
    
    
    
    
    },
    messages:{
        pId:{
            required: "Please enter patient Id",
            number: "Please patient Id as a numerical value",

        },
        age : {
            required: "Please enter your age",
            number: "Please enter numerical values.",
            range: "Please enter a value between 10 and 120."
            },
        rbp : {
            required: "Please enter your resting blood pressure.",
            number: "Please enter numerical values.",
            range: "Please enter a value between 10 and 400."
        },
        chol : {
            required: "Please enter your cholesterol level.",
            number: "Please enter numerical values.",
            range: "Please enter a value between 50 and 800."
        },
        thalach : {
            required: "Please enter your max heart rate.",
            number: "Please enter numerical values.",
            range: "Please enter a value between 30 and 400."
        },
        oldpeak : {
            required: "Please enter your max heart rate.",
            number: "Please enter numerical values.",
            min: "Please enter valid value.",
            max: "Please enter a value below 20."
        }
    }
  });
}});

