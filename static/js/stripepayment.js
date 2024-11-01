//STRIPE

var cardimage = document.querySelector(".credit-card-box")
var paymentformcard = document.querySelector("#payment-form-card")
var paymentformaddress = document.querySelector("#payment-form-address")
var artname = window.location.href.split('/').at(-1).split(/[\s,?=]+/).at(0)
var button_next_address = document.querySelector("#submitaddress")
var buybutton = document.querySelector('#buybutton');


buybutton.addEventListener('click', function () {

    var clientsecret = null;

    var mac = /(Mac|iPhone|iPod|iPad)/i.test(navigator.userAgent);
    console.log(mac)

    // BUY BUTTON PRESSED
    if (mac) {

        button_next_address.style.display = "none";

        $.post('/buyartpiece',
            {
                firstname: 'automatic',
                lastname: 'automatic',
                addressline1: 'automatic',
                postalcode: 'automatic',
                state: 'automatic',
                city: 'automatic',
                country: 'US',
                artname: artname,
            },
            function (data, status, jqXHR) {
                clientsecret = data.client_secret;
            }
        )
    }
    else {
        cardimage.classList.add('d-none');
        paymentformcard.classList.add('d-none');
        paymentformaddress.classList.add('d-block');

        // get client secret and make customer
        button_next_address.addEventListener('click', function () {

            var addressforms = document.querySelectorAll("input.nonempty")

            var filled = true

            addressforms.forEach((el) => {
                if (el.value.length == 0) filled = false
            })

            if (filled) {
                paymentformaddress.classList.add('d-none');
                paymentformaddress.classList.remove('d-block');
                cardimage.classList.add('d-block');
                cardimage.classList.remove('d-none');
                paymentformcard.classList.add('d-block');
                paymentformcard.classList.remove('d-none');
                var countryy = document.querySelector("#countryform").value;
                console.log(countryy)

                if (countryy == 'IN') {
                    countryy = 'US'
                }
                console.log(countryy)

                $.post('/buyartpiece',
                    {
                        firstname: $("#firstnameform").val(),
                        lastname: $("#lastnameform").val(),
                        addressline1: $("#addressform").val(),
                        postalcode: $("#postalcodeform").val(),
                        state: $("#stateform").val(),
                        city: $("#cityform").val(),
                        country: countryy,
                        artname: artname,
                    },
                    function (data, status, jqXHR) {
                        clientsecret = data.client_secret;


                    }
                )
            }
        })
    }

    // input your stripe public key here
    var stripe = Stripe('');
    var elements = stripe.elements();

    // stripe elements style and classes
    var elementStyles = {
        base: {
            color: '#161616',
            fontWeight: 500,
            fontSize: '16px',
        },
        invalid: {
            color: '#E25950'
        },
    };
    var elementClasses = {
        base: 'form-control input-cart-number',
        focus: 'focused',
        empty: 'empty',
        invalid: 'invalid',
    };

    // create stripe elements
    var cardNumber = elements.create('cardNumber', { style: elementStyles, classes: elementClasses });
    cardNumber.mount('#cardnumberr');

    var cardExpiry = elements.create('cardExpiry', { style: elementStyles, classes: elementClasses });
    cardExpiry.mount('#cardexpiryy');

    var cardCvc = elements.create('cardCvc', { style: elementStyles, classes: elementClasses });
    cardCvc.mount('#cardcvcc');

    // display error messages
    cardNumber.on('change', function (event) {
        var displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });
    cardExpiry.on('change', function (event) {
        var displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });
    cardCvc.on('change', function (event) {
        var displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });

    // process payment on submit
    var form = document.querySelector('#payment-form-card');
    form.addEventListener('submit', function (ev) {
        ev.preventDefault();
        stripe.confirmCardPayment(clientsecret, {
            payment_method: {
                card: cardNumber
            }
        }).then(function (result) {
            if (result.error) {
                displayError = document.getElementById('card-errors');
                displayError.textContent = result.error.message;
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    window.location.href = "/profile";
                    console.log("succeeded payment yahoo");
                }
            }
        })

    })
})



