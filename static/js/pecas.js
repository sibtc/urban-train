$(document).ready(function() {
  // Insere classe no primeiro item de produto
  $('#id_itenspecas_set-0-description').addClass('clDescription');
  $('#id_itenspecas_set-0-price').addClass('clPrice');
  $('#id_itenspecas_set-0-quantity').addClass('clQuantity');
  $('#id_itenspecas_set-0-subtotal').addClass('clSubtotal');
  $('#id_itenspecas_set-0-price').mask('000.000.000.000.000,00', {reverse: true});
  $("#id_comercio").select2();
  $('#id_city').select2();
});

$("#add-item").click(function(ev) {
  ev.preventDefault();
  let count = $('#itens-peca').children().length;
  let tmplMarkup = $("#item-peca").html();
  let compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
  $("div#itens-peca").append(compiledTmpl);

  $('#id_itenspecas_set-' + (count) + '-price').mask('000.000.000.000.000,00', {reverse: true});
  $('#id_itenspecas_set-TOTAL_FORMS').attr('value', count + 1);
  $('html, body').animate({
      scrollTop: $("#add-item").position().top-200
  }, 800);
  $('#id_itenspecas_set-' + (count) + '-description').addClass('clDescription');
  $('#id_itenspecas_set-' + (count) + '-price').addClass('clPrice');
  $('#id_itenspecas_set-' + (count) + '-quantity').addClass('clQuantity');
  $('#id_itenspecas_set-' + (count) + '-subtotal').addClass('clSubtotal');
});

$(document).on('focusout', '.clQuantity', function() {
  let quantity = $(this).val();
  let chance_to_price = $(this).attr('id').replace('quantity', 'price');
  mask = $('#'+chance_to_price).mask('000.000.000.000.000,00', {reverse: true});
  let price = $('#'+chance_to_price).val();
  let chance_to_subtotal = $(this).attr('id').replace('quantity', 'subtotal');
  let calculate = price.replace(',','.') * quantity;
  $('#'+chance_to_subtotal).val(calculate);
});

