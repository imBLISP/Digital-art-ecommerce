var ownedselect = document.querySelector("#ownedselect")
var createdselect = document.querySelector("#createdselect")
var ownedtab = document.querySelector("#ownedtab")
var createdtab = document.querySelector("#createdtab")


// AUTHENTICATION EMAIL POST
var authenticationemailbutton = document.querySelector('#authenticationemailform');
var authenticatetext = document.querySelector('#authenticatetext');
if (authenticationemailbutton) {
    authenticationemailbutton.addEventListener('click', () => {
        authenticatetext.textContent = 'Sent'
        authenticationemailbutton.classList.add('emailsentbutton')
        fetch('/sendauthenticationemail')
            .then(() => {

            })
    })
}

ownedselect.addEventListener('click', () => {
    createdselect.querySelector('.hrlike').classList.remove('profilepage-selectorline-selected');
    ownedselect.querySelector('.hrlike').classList.add('profilepage-selectorline-selected');

    createdtab.classList.add('d-none')
    ownedtab.classList.remove('d-none')
})

createdselect.addEventListener('click', () => {
    ownedselect.querySelector('.hrlike').classList.remove('profilepage-selectorline-selected');
    createdselect.querySelector('.hrlike').classList.add('profilepage-selectorline-selected');

    ownedtab.classList.add('d-none')
    createdtab.classList.remove('d-none')
})

imgInp = document.querySelector("#uploadfile")
changingimage = document.querySelector("#changingimage")

imgInp.onchange = evt => {
    const [file] = imgInp.files
    if (file) {
        changingimage.src = URL.createObjectURL(file)
        changingimage.classList.remove('d-none')
    }
}

displaynameinput = document.querySelector("#uploaddisplayname")
displaynametarget = document.querySelector("#displaynametarget")

displaynameinput.addEventListener('keyup', () => {
    displaynametarget.innerHTML = displaynameinput.value;
})

priceinput = document.querySelector("#uploadprice")
pricechangetarget = document.querySelector("#pricechangetarget")

priceinput.addEventListener('keyup', () => {
    pricechangetarget.innerHTML = '$' + priceinput.value;
})

$(document).ready(function () {
    var downloadbuttonhover = document.querySelectorAll(".downloadbutton")
    var downloadform = document.querySelector("#downloadimageform")

    downloadbuttonhover.forEach(function (button) {
        button.addEventListener('click', () => {
            downloadform.action = "/download/" + button.getAttribute("name");
            downloadform.submit();
        })
    })
})

