$(function() {
    var $predictForm = $("#predictForm");
    
    if ($predictForm.length){
        $predictForm.validate({
    rules:{
        age : {
            required: true,
            number: true,
            range: [18, 100]

        },
        rbp:{
            required: true,
            number: true,
            range: [50, 400]

        },       
        chol:{
            required: true,
            number: true,
            range: [50, 800]

        },
        thalach :{
            required: true,
            number: true,
            range: [50, 400]

        },
        oldpeak : {
            required: true,
            number: true,
            min: 0,
            max: 20.0
        }
    
    
    
    
    },
    messages:{
        age : {
            required: "Please enter your age",
            number: "Please enter numerical values.",
            range: "Please enter a valid value between 18 and 100."
            },
        rbp : {
            required: "Please enter your resting blood pressure.",
            number: "Please enter numerical values.",
            range: "Please enter a value between 50 and 400."
        },
        chol : {
            required: "Please enter your cholesterol level.",
            number: "Please enter numerical values.",
            range: "Please enter a value between 50 and 800."
        },
        thalach : {
            required: "Please enter your max heart rate.",
            number: "Please enter numerical values.",
            range: "Please enter a value between 50 and 400."
        },
        oldpeak : {
            required: "Please enter your max heart rate.",
            number: "Please enter numerical values.",
            min: "Please enter valid value.",
            max: "Please enter a value between 0 and 20."
        }
    }
  });
}});

