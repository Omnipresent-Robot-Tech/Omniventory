if($('.phone-number').length>=1){
var cleavePN = new Cleave('.phone-number', {
  phone: true,
  phoneRegionCode: 'us'
});
}


if($('.currency').length>=1){
var cleaveC = new Cleave('.currency', {
  numeral: true,
  numeralThousandsGroupStyle: 'thousand'
});
}

if($('.purchase-code').length>=1){
var cleavePC = new Cleave('.purchase-code', {
  delimiter: '-',
  blocks: [4, 4, 4, 4],
  uppercase: true
});
}

if($('.invoice-input').length>=1){
var cleaveI = new Cleave('.invoice-input', {
  prefix: 'INV',
  delimiter: '-',
  blocks: [10],
  uppercase: true
});
}

if($('.datemask').length>=1){
var cleaveD = new Cleave('.datemask', {
  date: true,
  datePattern: ['Y', 'm', 'd']
});
}


if($('.creditcard').length>=1){

var cc_last_type;
var cleaveCC = new Cleave('.creditcard', {
  creditCard: true,
  onCreditCardTypeChanged: function(type) {
    if(type !== 'unknown') {
      if(type == 'amex') {
        type = 'americanexpress';
      }else if(type == 'mastercard') {
        type = 'mastercard';
      }else if(type == 'visa') {
        type = 'visa';
      }else if(type == 'diners') {
        type = 'dinersclub';
      }else if(type == 'discover') {
        type = 'discover';
      }else if(type == 'jcb') {
        type = 'jcb';
      }
      $(".creditcard").removeClass(cc_last_type);
      $(".creditcard").addClass(type);
      cc_last_type = type;                        
    }
  }
});
}

if($('.pwstrength').length>=1){
$(".pwstrength").pwstrength();
}

if($('.daterange-cus').length>=1){
$('.daterange-cus').daterangepicker({
  locale: {format: 'YYYY-MM-DD'},
  drops: 'down',
  opens: 'right'
});
}

if($('.daterange-btn').length>=1){
$('.daterange-btn').daterangepicker({
  ranges: {
    'Today'       : [moment(), moment()],
    'Yesterday'   : [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
    'Last 7 Days' : [moment().subtract(6, 'days'), moment()],
    'Last 30 Days': [moment().subtract(29, 'days'), moment()],
    'This Month'  : [moment().startOf('month'), moment().endOf('month')],
    'Last Month'  : [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
  },
  startDate: moment().subtract(29, 'days'),
  endDate  : moment()
}, function (start, end) {
  $('.daterange-btn span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'))
});
}

if($('.colorpickerinput').length>=1){
$(".colorpickerinput").colorpicker({
  format: 'hex',
  component: '.input-group-append',
});
}

if($('.inputtags').length>=1){
$(".inputtags").tagsinput('items');
}
