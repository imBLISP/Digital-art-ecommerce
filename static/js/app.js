

$(document).ready(function () {

  // LOGIN SIGNUP
  var login = document.querySelector('#login');
  var signup = document.querySelector('#signup');
  var loginform = document.querySelector('#loginform');
  var signupform = document.querySelector('#signupform');

  login.addEventListener('click', function () {
    loginform.classList.remove('d-none');
    signupform.classList.add('d-none');
  });

  signup.addEventListener('click', function () {
    loginform.classList.add('d-none');
    signupform.classList.remove('d-none');
  });


  // CLICKABLE CARDS
  var cards = document.querySelectorAll('.clickablecard');

  cards.forEach(function (card) {
    card.addEventListener('click', function () {
      filename = card.getAttribute('id');
      location.href = "/artworks/" + card.getAttribute('id').slice(3);
    })
  })

  // CREDIT CARD ANIMATIONS
  $('.__PrivateStripeElement-input').on('keyup change', function () {
    $t = $(this);

    var card_number = '';
    $('.__PrivateStripeElement-input').each(function () {
      card_number += $(this).val() + ' ';

    })

    $('.credit-card-box .number').html(card_number);
  });

  $('#card-holder').on('keyup change', function () {
    $t = $(this);
    $('.credit-card-box .card-holder div').html($t.val());
  });

  $('#card-holder').on('keyup change', function () {
    $t = $(this);
    $('.credit-card-box .card-holder div').html($t.val());
  });

  $('#card-expiration-month, #card-expiration-year').change(function () {
    m = $('#card-expiration-month option').index($('#card-expiration-month option:selected'));
    m = (m < 10) ? '0' + m : m;
    y = $('#card-expiration-year').val().substr(2, 2);
    $('.card-expiration-date div').html(m + '/' + y);
  })

  $(".hoverflip").hover(function () {
    $('.credit-card-box').addClass('hover');
  }, function () {
    $('.credit-card-box').removeClass('hover');
  })



  // $('.input-cart-number').on('keyup change', function () {
  //     $t = $(this);

  //     if ($t.val().length > 3) {
  //         $t.next().focus();
  //     }

  //     var card_number = '';
  //     $('.input-cart-number').each(function () {
  //         card_number += $(this).val() + ' ';
  //         if ($(this).val().length == 4) {
  //             $(this).next().focus();
  //         }
  //     })

  //     $('.credit-card-box .number').html(card_number);
  // });

  // $('#card-holder').on('keyup change', function () {
  //     $t = $(this);
  //     $('.credit-card-box .card-holder div').html($t.val());
  // });

  // $('#card-holder').on('keyup change', function () {
  //     $t = $(this);
  //     $('.credit-card-box .card-holder div').html($t.val());
  // });

  // $('#card-expiration-month, #card-expiration-year').change(function () {
  //     m = $('#card-expiration-month option').index($('#card-expiration-month option:selected'));
  //     m = (m < 10) ? '0' + m : m;
  //     y = $('#card-expiration-year').val().substr(2, 2);
  //     $('.card-expiration-date div').html(m + '/' + y);
  // })

  // $('#card-ccv').on('focus', function () {
  //     $('.credit-card-box').addClass('hover');
  // }).on('blur', function () {
  //     $('.credit-card-box').removeClass('hover');
  // }).on('keyup change', function () {
  //     $('.ccv div').html($(this).val());
  // });





  // $('submit').off('click').click(function (clickevent) {
  //     alert('hello');
  //     clickevent.preventDefault();
  // })


  /*--------------------
  CodePen Tile Preview
  --------------------*/
  //   setTimeout(function(){
  //     $('#card-ccv').focus().delay(1000).queue(function(){
  //       $(this).blur().dequeue();
  //     });
  //   }, 500);

  /*function getCreditCardType(accountNumber) {
    if (/^5[1-5]/.test(accountNumber)) {
      result = 'mastercard';
    } else if (/^4/.test(accountNumber)) {
      result = 'visa';
    } else if ( /^(5018|5020|5038|6304|6759|676[1-3])/.test(accountNumber)) {
      result = 'maestro';
    } else {
      result = 'unknown'
    }
    return result;
  }
  
  $('#card-number').change(function(){
    console.log(getCreditCardType($(this).val()));
  })*/
})

