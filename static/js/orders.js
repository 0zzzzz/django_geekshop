window.onload = function () {
    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    let quantity_arr = [];
    let price_arr = [];

    let TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());

    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;

    for (let i = 0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }


    // console.log(quantity_arr)


    $('.order_form').on('click', 'input[type=number]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        console.log(price_arr[orderitem_num])
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            // console.log(delta_quantity)
            quantity_arr[orderitem_num] = orderitem_quantity;
            order_summary_update(price_arr[orderitem_num], delta_quantity)
        }
        console.log(price_arr)
        console.log(quantity_arr)
    });

    $('.order_form').on('click', 'input[type=checkbox]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
        } else {
            delta_quantity = quantity_arr[orderitem_num];
        }
        order_summary_update(price_arr[orderitem_num], delta_quantity)
    });

    function order_summary_update(orderitem_price, delta_quantity) {
        // console.log(orderitem_price)
        // console.log(delta_quantity)
        delta_cost = orderitem_price * delta_quantity;
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;

        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(order_total_cost.toString());
    }


    $('.order_form').on('click', 'select', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
        _price = parseFloat($('.orderitems-' + orderitem_num + '-price').text().replace(',', '.'));
        _quantity = parseInt($('input[name="orderitems-' + orderitem_num + '-quantity"]').val());
        if (isNaN(_quantity)) {
            _quantity = 0
        }
        let ajax_price = target.value
        $('.orderitems-' + orderitem_num + '-price').text(ajax_price.toString());
        let order_total = Number(order_total_cost - _price * _quantity + ajax_price * _quantity).toFixed(2);
        order_total_cost = parseFloat(order_total);
        $('.order_total_cost').html(order_total_cost.toString());
        _price = parseFloat($('.orderitems-' + orderitem_num + '-price').text().replace(',', '.'));
        price_arr[orderitem_num] = _price
        // console.log(price_arr)
        // $(document).ready(function() {
        //     $('#id').change(function() {
        //         let query = $(this).val();
        //         console.log(query);
        //         $.ajax({
        //             url: "/update/",
        //             type: "POST",
        //             dataType: "json",
        //             data: {
        //                 client_response: query
        //             },
        //             success: function (json) {
        //                 console.log(document.getElementById('id_amount').value = json.amount)
        //                 document.getElementById('id_amount').value = json.amount;
        //             },
        //             failure: function (json) {
        //                 alert('Got an error dude');
        //             }
        //         });
        //     })
        // })
        // console.log('asdfgsdfgsdfgsdfgdsfg')
    });


    $('.formset_row').formset({
        addText: 'Добавить товар',
        deleteText: 'Удалить товар',
        prefix: 'orderitems',
        removed: delete_order_item,
        added: add_order_item,
    })

    function delete_order_item(row) {
        let target_name = row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        quantity_arr.splice(orderitem_num, 1)
        console.log(orderitem_num)
        // console.log(quantity_arr)
        // console.log(quantity_arr[orderitem_num])
        price_arr.splice(orderitem_num, 1)
        console.log(price_arr[orderitem_num])
        console.log(price_arr)
        order_summary_update(price_arr[orderitem_num], delta_quantity);
    }

    function add_order_item(row) {
        let arr_length = quantity_arr.length
        quantity_arr.push(0)
        price_arr.push(0)
        delta_quantity = quantity_arr[arr_length];
        let selector = document.getElementsByClassName('td3')[arr_length+1]
        selector = selector.getElementsByTagName('span')
        selector[0].setAttribute('class', 'orderitems-' + (arr_length) + '-price')
        selector = document.getElementsByClassName('td2')[arr_length+1]
        selector = selector.getElementsByTagName('input')
        selector[0].setAttribute('name', 'orderitems-' + (arr_length) + '-quantity')
        selector[0].setAttribute('id', 'orderitems-' + (arr_length) + '-quantity')
        order_summary_update(0, 0);
    }
}
