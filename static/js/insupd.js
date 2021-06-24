    $(document).ready(function(){
      var date_input=$('input[name="dob"]'); //our date input has the name "date"
      var container=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
      var options={
        format: 'yyyy/mm/dd',
        container: container,
        todayHighlight: true,
        autoclose: true,
/*		onSelect: function(value, ui) {
			var today = new Date();
			age = today.getFullYear() - ui.selectedYear;
			$('#age').val(age);			
			},
		*/      };
      date_input.datepicker(options);
	  date_input.datepicker().on("hide", function(ev){
		var yearSelect = $('#dob').val().split("/")[0];
		var yearDate = new Date().getFullYear();
		age = yearDate - yearSelect;
		$("#age").val(age);
      });


	  $.validator.addMethod(
			"regex",
			function(value, element, regexp) 
			{
//				var check = false;
				var re = RegExp(regexp);
				return this.optional(element) || re.test(value);
    		},
		    ""
		);

	  /* Functions for checking validation */
	  	$("form[name='formInsUpdPatient']").validate({
			rules:{
				name: "required",
				address: "required",
				gender: {
					required: true,
					regex: /^(?:m|M|male|Male|f|F|female|Female)$/
				},
				nricno:  {
					required: true,
					minlength: 9,
					maxlength: 9,
					regex: /^[STFG]\d{7}[A-Z]$/
				},
				email: {
					required: true,
					email: true
				},
				age:  {
					required: true,
					digits: true,
					range: [1, 150]
				},
				contactno: {
					required: true,
					digits: true,
					minlength: 8,
					maxlength: 20
				},
				postcode : {
					required: true,
					digits: true,
					minlength: 6,
					maxlength: 6
				},
				dob: {
					required: true,
					date: true
				}
			},
			messages: {
				name: "Plesae enter your name.",
				gender: "Please choose your gender.",
				nricno: "Please enter a valid NRIC No.",
				email : "Please enter a valid email address.",
				address: "Please enter your address",
				contactno: "Please enter your contact number (Max:20 digits).",
				postcode: "Pleae enter a valid postcode.",
				dob: "Please enter a valid date.",
				age: "Please enter a valid age (1-150)"
			},

	  });
	});

	function selectElement(id, valueToSelect) {    
    	let element = document.getElementById(id);
    	element.value = valueToSelect;
	};

