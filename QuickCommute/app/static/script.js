// Register
$(document).on('pageinit', '#registerPage', function(){  
    $(document).on('click', '#register-btn', function() {
        if($('#register-name').val().length > 0 && $('#register-password').val().length > 0 
          && $('#register-email').val().length > 0){        
            $.ajax({url: 'http://websys3.stern.nyu.edu:7006/register',
                    data: $('#register-form').serialize(),
                    type: 'POST',                   
                    async: 'true',
		    dataType: 'json',
		   
                    beforeSend: function() {
                        $.mobile.loading('show');
                    },
                
                    complete: function() {
                        $.mobile.loading('hide');
                    },
   
                    success: function (result) {
                        if(result.status && result.status == "success") {
                            $.mobile.changePage("#loginPage");                         
                        } else {
                            alert('Registration unsuccessful!'); 
                        }
                    },
                
                    error: function (request,error) {
                        alert('Network error has occurred please try again!');
                    }
            });                   
    
        } else {
            alert('Please fill all necessary fields');
        }           
        return false; // cancel original event to prevent form submitting
    });    
});

// login
$(document).on('pageinit', '#login', function(){  
    $(document).on('click', '#login-submit', function() { // catch the form's submit event
	    if($('#l-username').val().length > 0 && $('#l-password').val().length > 0){
            $.ajax({url: 'http://websys3.stern.nyu.edu:7002/login',
                	data: $('#l-form').serialize(),
                	type: 'post',                   
                	async: 'true',
                    dataType: 'json',
                	beforeSend: function() {
                    	$.mobile.loading('show'); // This will show ajax spinner
                	},
                
                	complete: function() {
                    	$.mobile.loading('hide'); // This will hide ajax spinner
                	},
                	
                	success: function (result) {
                        if(result.status && result.status == "success") {
                            $.mobile.changePage("#plan");                         
                        } else {
                            alert('Logon unsuccessful!'); 
                        }
                	},
                
                	error: function (request,error) {
                    	alert('Network error has occurred please try again!');
                	}
            });                   
    
    	} else {
        	alert('Please fill all necessary fields');
    	}           
	    return false; // cancel original event to prevent form submitting
	});    
});
