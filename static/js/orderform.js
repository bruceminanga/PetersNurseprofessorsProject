var academicLevel, typeOfService, currency = 'USD', subjectArea, deadline, writerCategory, numberOfPages, powerpoint_slides, numberOfPageswords;
  var totalPrice = 0;
  var discount = 0;
  // This script runs when the window loads
  window.onload = function () {
    // It adds an event listener to a form with the id 'myform'
    // The event listener triggers when any input in the form changes
    document.getElementById('myform').addEventListener('change', function () {
      // Reset the discount
      discount = 0;
      // Clear the discount and final price fields
      document.getElementById('discount').innerText = '';
      document.getElementById('finalPrice').innerText = '';

      // It gets the values of various inputs in the form
      academicLevel = document.getElementsByName('academic_level')[0].value;
      typeOfService = document.getElementsByName('type_of_service')[0].value;
      subjectArea = document.getElementsByName('subject_area')[0].value;
      typeOfPaper = document.getElementsByName('type_of_paper')[0].value;
      writerCategory = document.getElementsByName('writer_category')[0].value;
      deadline = document.getElementsByName('deadline')[0].value;
      numberOfPageswords = document.getElementsByName('number_of_pages')[0].value;
      numberOfPages = document.getElementsByName('number_of_pages_increment')[0].value;
      powerpoint_slides = document.getElementsByName('powerpoint_slides')[0].value;
      currency = document.getElementsByName('currency')[0].value;


      // If the number of pages is zero, set it to a lower value
      if (powerpoint_slides == 0) {
        powerpoint_slides = 0.5;
      }

      // It displays the selected options in a text element with the id 'selectedOptions'
      document.getElementById('selectedOptions').innerText = academicLevel + '\n ' + typeOfService + ' * ' + typeOfPaper + '\n ' + subjectArea + ' * ' + numberOfPages + 'pages * ' + numberOfPageswords + ' \n ' + powerpoint_slides + 'PPT * ' + writerCategory + ' * ' + deadline;

      // It calculates the total price based on the selected options
      totalPrice = calculatePrice(academicLevel, typeOfService, currency, subjectArea, deadline, writerCategory, numberOfPages, powerpoint_slides, numberOfPageswords);
      // It displays the total price in a text element with the id 'totalPrice'
      document.getElementById('totalPrice').innerText = 'Total price:' + currency + ' ' + totalPrice;

      // Remove the old PayPal script tag if it exists
      var oldScript = document.getElementById('paypal-js');
      if (oldScript) {
        oldScript.remove();
      }

      // Create a new script tag for the PayPal SDK
      var script = document.createElement('script');
      script.id = 'paypal-js';
      script.src = 'https://www.paypal.com/sdk/js?client-id=AR8UiQdUlh_S3WrWA3JEBM6PRJ5JHYLP_GNUtNVFX-Af6jdnzOtUd8bCEXEntohHdq81rFKf7yUKD5MR&currency=' + currency;
      // When the script loads, initialize the PayPal buttons
      script.onload = function () {
        paypal.Buttons({
          createOrder: function (data, actions) {
            // Calculate the total price based on the selected options
            totalPrice = calculatePrice(academicLevel, typeOfService, currency, subjectArea, deadline, writerCategory, numberOfPages, powerpoint_slides, numberOfPageswords) ;
            // This function sets up the details of the transaction, including the amount and line item details.
            return actions.order.create({
              purchase_units: [{
                amount: {
                  value: totalPrice,
                  currency_code: currency
                }
              }]
            }).catch(error => console.error('Error creating order:', error));
          },
          onApprove: function (data, actions) {
            // This function captures the funds from the transaction.
            return actions.order.capture().then(function (details) {
              // This function shows a transaction success message to your buyer.
              alert('Transaction completed by ' + details.payer.name.given_name);
            });
          }
        }).render('#paypal-button-container');  // Add an HTML element with this id to your page
      };
      // Add the new script tag to the body of the document
      document.body.appendChild(script);
    });
    // Add an event listener to the coupon code field that triggers when it changes
    document.getElementsByName('coupon_code')[0].addEventListener('change', applyCoupon);
  }

  // This function calculates the price based on various parameters
  function calculatePrice(academicLevel, typeOfService, currency, subjectArea, deadline, writerCategory, numberOfPages, powerpoint_slides, numberOfPageswords) {
    // It defines various pricing parameters
    var basePrices = { 'High School': 10, 'Undergraduate': 11, 'Masters': 12, 'Doctoral': 13, 'TEAS 7': 204, 'HESI': 15 };
    var serviceMultipliers = { 'Writing from scratch': 1, 'Editing': 0.8, 'Problem solving': 0.6, 'Paraphrasing/Rewriting': 0.7, 'TEAS 7': 1.2, 'HESI': 1.3 };
    var subjectAreaMultipliers = { 'Any': 1, 'Archaeology': 2.1, 'Architecture': 2.2, 'Arts': 2.3, 'Astronomy': 2.4, 'Biology': 2.5, 'Business': 2.6, 'Chemistry': 2.7, 'Childcare': 2.8, 'Computers': 2.9, 'Counseling': 3, 'Criminology': 3.1, 'Economics': 3.2, 'Education': 3.3, 'Engineering': 3.4, 'Environmental-Studies': 3.5, 'Ethics': 3.6, 'Ethnic-Studies': 3.7, 'Finance': 3.8, 'Food-Nutrition': 3.9, 'Geography': 4, 'Healthcare': 4.1, 'HESI Test': 4.2, 'History': 4.3, 'Law': 4.4, 'Linguistics': 4.5, 'Literature': 4.6, 'Management': 4.7, 'Mathematics': 4.8, 'Medicine': 4.9, 'Music': 5, 'NACE': 5.1, 'NCLEX-RN': 5.2, 'Nursing': 5.3, 'Philosophy': 5.4, 'Physical-Education': 5.5, 'Physics': 5.6, 'Political-Science': 5.7, 'Programming': 5.8, 'Psychology': 5.9, 'Religion': 6, 'Sociology': 6.1, 'Statistics': 6.2, 'TEAS 7 Test': 6.3 };
    var deadlineMultipliers = { '6hrs': 2.8, '12hrs': 2.6, '24hrs': 2.4, '48hrs': 2.2, '5days': 2, '10days': 1.8, '14days': 1.6, '30days': 1.4 };
    var numberOfPageswordsMultipliers = { 'Double Spaced': 2, 'Single Spaced': 1.3 };
    var writerCategoryMultipliers = { 'Standard': 2, 'Premium': 2.5, 'Platinum': 3 };
    var currencyRates = { 'USD': 1, 'EUR': 0.85, 'GBP': 0.75, 'KES': 110.15 };

    // It calculates the price based on the pricing parameters and the selected options
    var basePrice = basePrices[academicLevel];
    var serviceMultiplier = serviceMultipliers[typeOfService];
    var currencyRate = currencyRates[currency];
    var subjectAreaMultipliers = subjectAreaMultipliers[subjectArea];
    var deadlineMultiplier = deadlineMultipliers[deadline];
    var numberOfPageswordsMultipliers = numberOfPageswordsMultipliers[numberOfPageswords];
    var writerCategoryMultipliers = writerCategoryMultipliers[writerCategory]
    var price = basePrice * serviceMultiplier * currencyRate * subjectAreaMultipliers * deadlineMultiplier * numberOfPageswordsMultipliers * writerCategoryMultipliers * numberOfPages * powerpoint_slides;
    return (price - price * discount).toFixed(2);
  }

  // Function to apply a coupon
  function applyCoupon() {
    // Get the coupon code from the form
    var couponCode = document.getElementsByName('coupon_code')[0].value;
    // Validate the coupon code and get the discount value
    validateCoupon(couponCode).then(discountValue => {
      if (discountValue) {
        // If the coupon code is valid, update the global discount variable
        discount = discountValue;
        // Display the discount
        document.getElementById('discount').innerText = 'Discount: ' + discount;
        // Calculate the total price
        var totalPrice = calculatePrice(academicLevel, typeOfService, currency, subjectArea, deadline, writerCategory, numberOfPages, powerpoint_slides, numberOfPageswords);
        // Display the final price
        document.getElementById('finalPrice').innerText = 'Final Price: ' + currency + ' ' + totalPrice;
      } else {
        // If the coupon code is invalid, display an error message
        document.getElementById('discount').innerText = 'Invalid coupon code';
        document.getElementById('finalPrice').innerText = '';
      }
    });
  }

  // Function to validate a coupon code
  function validateCoupon(couponCode) {
    // If the coupon code is undefined, log an error and return null
    if (!couponCode) {
      console.error('Coupon code is undefined');
      return Promise.resolve(null);
    }

    // Fetch the coupon from the API
    return fetch('http://127.0.0.1:8000/api/coupons/' + couponCode)
      .then(response => {
        // If the response is not ok, throw an error
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        // Parse the response as JSON
        return response.json();
      })
      .then(coupon => {
        // If the coupon is active, return the discount value as a decimal
        if (coupon.active) {
          return coupon.discount / 100;
        } else {
          // If the coupon is not active, return null
          return null;
        }
      })
      .catch(error => {
        // If an error occurred, log the error and return null
        console.error('There has been a problem with your fetch operation:', error);
        return null;
      });
  }

  // Function to pay now
  function payNow(event) {
    // Prevent the form from submitting
    event.preventDefault();
    // Calculate the total price
    var totalPrice = calculatePrice(academicLevel, typeOfService, currency, subjectArea, deadline, writerCategory, numberOfPages, powerpoint_slides, numberOfPageswords);
  }