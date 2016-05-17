var userObject = {
    email : "",
    fromStation : ""
    toStation : ""
    service : ""
}


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
$(document).on('pageinit', '#loginPage', function(){  
    $(document).on('click', '#login-btn', function() { // catch the form's submit event
	    if($('#login-email').val().length > 0 && $('#login-password').val().length > 0){
            $.ajax({url: 'http://websys3.stern.nyu.edu:7006/login',
                	data: $('#login-form').serialize(),
                	type: 'POST',                   
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
                            userObject.email = email
                            userObject.fromStation = fromStation
                            userObject.toStation = toStation
                            userObject.service = service
                            $.mobile.changePage("#page1");                         
                        } else {
                            alert('Login unsuccessful!'); 
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

// Update Profile
$(document).on('pageinit', '#page3', function(){  
    $(document).on('click', '#update-btn', function() {
        if($('#profile-name').val().length > 0){        
            $.ajax({url: 'http://websys3.stern.nyu.edu:7006/profile',
                    data: $('#profile-form').serialize(),
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
                            $.mobile.changePage("#page3");                         
                        } else {
                            alert('Update unsuccessful! - Try again Later'); 
                        }
                    },
                
                    error: function (request,error) {
                        alert('Network error has occurred please try again!');
                    }
            });                   
    
        } else {
            alert('Please fill all necessary fields');
        }           
        return false;
    });    
});