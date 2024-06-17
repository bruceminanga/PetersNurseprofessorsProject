let academicLevel, typeOfService, currency = 'USD', subjectArea, deadline, writerCategory, numberOfPages, powerpoint_slides, numberOfPageswords;
let totalPrice = 0;
let discount = 0;

window.onload = () => {
  const form = document.getElementById('myform');
  const discountElem = document.getElementById('discount');
  const finalPriceElem = document.getElementById('finalPrice');
  const selectedOptionsElem = document.getElementById('selectedOptions');
  const totalPriceElem = document.getElementById('totalPrice');
  const couponCodeElem = document.getElementsByName('coupon_code')[0];

  form.addEventListener('change', handleFormChange);
  couponCodeElem.addEventListener('change', applyCoupon);

  function handleFormChange() {
    discount = 0;
    discountElem.innerText = '';
    finalPriceElem.innerText = '';

    academicLevel = form.elements['academic_level'].value;
    typeOfService = form.elements['type_of_service'].value;
    subjectArea = form.elements['subject_area'].value;
    typeOfPaper = form.elements['type_of_paper'].value;
    writerCategory = form.elements['writer_category'].value;
    deadline = form.elements['deadline'].value;
    numberOfPageswords = form.elements['number_of_pages'].value;
    numberOfPages = form.elements['number_of_pages_increment'].value;
    powerpoint_slides = form.elements['powerpoint_slides'].value;
    currency = form.elements['currency'].value;

    if (powerpoint_slides == 0) {
      powerpoint_slides = 0.5;
    }

    selectedOptionsElem.innerText = `${academicLevel}\n ${typeOfService} * ${typeOfPaper}\n ${subjectArea} * ${numberOfPages} pages * ${numberOfPageswords} \n ${powerpoint_slides} PPT * ${writerCategory} * ${deadline}`;

    totalPrice = calculatePrice();
    totalPriceElem.innerText = `Total price: ${currency} ${totalPrice}`;

    updatePayPalScript();
  }

  function calculatePrice() {
    const basePrices = { 'High School': 39.8, 'Undergraduate': 44.1, 'Masters': 50.2, 'Doctoral': 54.9, 'TEAS 7': 39.8, 'HESI': 39.8 };
    const serviceMultipliers = { 'Writing from scratch': 1, 'Editing': 0.75, 'Problem solving': 0.65, 'Paraphrasing/Rewriting': 0.64, 'TEAS 7': 1, 'HESI': 1 };
    const subjectAreaMultipliers = { 'Any': 0.7, 'Archaeology': 0.7, 'Architecture': 1.3, 'Arts': 0.7, 'Astronomy': 0.7, 'Biology': 0.7, 'Business': 0.7, 'Chemistry': 0.8, 'Childcare': 0.7, 'Computers': 0.7, 'Counseling': 0.7, 'Criminology': 0.7, 'Economics': 0.7, 'Education': 0.7, 'Engineering': 0.82, 'Environmental-Studies': 0.7, 'Ethics': 1.8, 'Ethnic-Studies': 0.7, 'Finance': 0.7, 'Food-Nutrition': 0.7, 'Geography': 0.7, 'Healthcare': 0.7, 'History': 0.7, 'Law': 0.7, 'Linguistics': 0.7, 'Literature': 0.7, 'Management': 0.7, 'Mathematics': 0.9, 'Medicine': 0.7, 'Music': 0.7, 'Nursing': 0.7, 'Philosophy': 0.7, 'Physical-Education': 0.7, 'Physics': 0.83, 'Political-Science': 0.7, 'Programming': 0.82, 'Psychology': 0.7, 'Religion': 0.7, 'Sociology': 0.7, 'Statistics': 0.8, 'TEAS 7 Test': 0.7 };
    const deadlineMultipliers = { '6hrs': 2.5, '12hrs': 2.3, '24hrs': 2.1, '48hrs': 1.9, '5days': 1.7, '10days': 1.5, '14days': 1.3, '30days': 1.1 };
    const numberOfPageswordsMultipliers = { 'Double Spaced': 1, 'Single Spaced': 1.9 };
    const writerCategoryMultipliers = { 'Standard': 1, 'Premium': 1.2, 'Platinum': 1.4 };
    const currencyRates = { 'USD': 1, 'EUR': 0.88, 'GBP': 0.78, 'KES': 113 };

    const basePrice = basePrices[academicLevel];
    const serviceMultiplier = serviceMultipliers[typeOfService];
    const currencyRate = currencyRates[currency];
    const subjectAreaMultiplier = subjectAreaMultipliers[subjectArea];
    const deadlineMultiplier = deadlineMultipliers[deadline];
    const numberOfPageswordsMultiplier = numberOfPageswordsMultipliers[numberOfPageswords];
    const writerCategoryMultiplier = writerCategoryMultipliers[writerCategory];
    
    let price = basePrice * serviceMultiplier * currencyRate * subjectAreaMultiplier * deadlineMultiplier * numberOfPageswordsMultiplier * writerCategoryMultiplier * numberOfPages * powerpoint_slides;
    
    return (price - price * discount).toFixed(2);
  }

  function applyCoupon() {
    const couponCode = couponCodeElem.value;

    validateCoupon(couponCode).then(discountValue => {
      if (discountValue) {
        discount = discountValue;
        discountElem.innerText = `Discount: ${discount}`;
        const finalPrice = calculatePrice();
        finalPriceElem.innerText = `Final Price: ${currency} ${finalPrice}`;
      } else {
        discountElem.innerText = 'Invalid coupon code';
        finalPriceElem.innerText = '';
      }
    });
  }

  function validateCoupon(couponCode) {
    if (!couponCode) {
      console.error('Coupon code is undefined');
      return Promise.resolve(null);
    }

    return fetch(`http://127.0.0.1:8000/api/coupons/${couponCode}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(coupon => coupon.active ? coupon.discount / 100 : null)
      .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
        return null;
      });
  }

  function updatePayPalScript() {
    const oldScript = document.getElementById('paypal-js');
    if (oldScript) {
      oldScript.remove();
    }

    const script = document.createElement('script');
    script.id = 'paypal-js';
    script.src = `https://www.paypal.com/sdk/js?client-id=AR8UiQdUlh_S3WrWA3JEBM6PRJ5JHYLP_GNUtNVFX-Af6jdnzOtUd8bCEXEntohHdq81rFKf7yUKD5MR&currency=${currency}`;
    
    script.onload = () => {
      paypal.Buttons({
        createOrder: (data, actions) => {
          totalPrice = calculatePrice();
          return actions.order.create({
            purchase_units: [{
              amount: {
                value: totalPrice,
                currency_code: currency
              }
            }]
          }).catch(error => console.error('Error creating order:', error));
        },
        onApprove: (data, actions) => {
          return actions.order.capture().then(details => {
            alert(`Transaction completed by ${details.payer.name.given_name}`);
          });
        }
      }).render('#paypal-button-container');
    };

    document.body.appendChild(script);
  }
};
