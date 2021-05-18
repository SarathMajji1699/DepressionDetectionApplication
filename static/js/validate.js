var myInput = document.getElementById("password");
var letter = document.getElementById("letter");
var capital = document.getElementById("capital");
var number = document.getElementById("number");
var length = document.getElementById("length");
var special = document.getElementById("special");


// When the user clicks on the password field, show the message box
myInput.onfocus = function() {
  document.getElementById("message").style.display = "block";
  document.getElementsByClassName("loginbox")[0].style.height = "940px";
  document.getElementsByClassName("loginbox")[0].style.marginTop = "33%";
}

// When the user clicks outside of the password field, hide the message box
myInput.onblur = function() {
  document.getElementById("message").style.display = "none";
  document.getElementsByClassName("loginbox")[0].style.height = "650px";
  document.getElementsByClassName("loginbox")[0].style.marginTop = "23%";
}


// When the user starts to type something inside the password field
myInput.onkeyup = function() {
  // Validate lowercase letters
  var lowerCaseLetters = /[a-z]/g;
  if(myInput.value.match(lowerCaseLetters)) {
    letter.classList.remove("invalid");
    letter.classList.add("valid");
  } else {
    letter.classList.remove("valid");
    letter.classList.add("invalid");
  }

  // Validate capital letters
  var upperCaseLetters = /[A-Z]/g;
  if(myInput.value.match(upperCaseLetters)) {
    capital.classList.remove("invalid");
    capital.classList.add("valid");
  } else {
    capital.classList.remove("valid");
    capital.classList.add("invalid");
  }

  // Validate numbers
  var numbers = /[0-9]/g;
  if(myInput.value.match(numbers)) {
    number.classList.remove("invalid");
    number.classList.add("valid");
  } else {
    number.classList.remove("valid");
    number.classList.add("invalid");
  }

  var specials = /[#?!@$*-]/g;
  if(myInput.value.match(specials)) {
    special.classList.remove("invalid");
    special.classList.add("valid");
  } else {
    special.classList.remove("valid");
    special.classList.add("invalid");
  }

  // Validate length
  if(myInput.value.length >= 8) {
    length.classList.remove("invalid");
    length.classList.add("valid");
  } else {
    length.classList.remove("valid");
    length.classList.add("invalid");
  }

}

var phno = document.getElementById("phone");
phno.onfocus = function() {
  document.getElementById("pmsg").style.display = "block";
  document.getElementsByClassName("loginbox")[0].style.height = "700px";
  document.getElementsByClassName("loginbox")[0].style.marginTop = "26%";
}

phno.onblur = function() {
  document.getElementById("pmsg").style.display = "none";
  document.getElementsByClassName("loginbox")[0].style.height = "680px";
  document.getElementsByClassName("loginbox")[0].style.marginTop = "23%";
}
