let autocomplete;

function clearCart(qty, cart_id) {
  if (qty <= 0) {
    document.getElementById(`qty-${cart_id}`).remove();
  }
}
function initAutoComplete() {
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById("id_address"),
    {
      types: ["geocode", "establishment"],
      componentRestrictions: { country: ["ng"] },
    }
  );
  autocomplete.addListener("place_changed", onPlaceChanged);
}

function onPlaceChanged() {
  var place = autocomplete.getPlace();
  if (!place.geometry) {
    document.getElementById("id_address").placeholder = "Start typying...";
  } else {
  }

  var geocoder = new google.maps.Geocoder();
  var address = document.getElementById("id_address").value;

  geocoder.geocode({ address: address }, (results, status) => {
    if (status == google.maps.GeocoderStatus.OK) {
      document.getElementById("id_latitude").value =
        results[0].geometry.location.lat();
      document.getElementById("id_longitude").value =
        results[0].geometry.location.lng();
      document.getElementById("id_address").value =
        results[0].formatted_address;
    }
  });

  for (var i = 0; i < place.address_components.length; i++) {
    for (var j = 0; j < place.address_components[i].types.length; j++) {
      if (place.address_components[i].types[j] == "country") {
        document.getElementById("id_country").value =
          place.address_components[i].long_name;
      }
      if (
        place.address_components[i].types[j] == "administrative_area_level_1"
      ) {
        document.getElementById("id_state").value =
          place.address_components[i].long_name;
      }
      if (place.address_components[i].types[j] == "locality") {
        document.getElementById("id_city").value =
          place.address_components[i].long_name;
      }
      if (place.address_components[i].types[j] == "postal_code") {
        document.getElementById("id_pin_code").value =
          place.address_components[i].long_name;
      } else {
        document.getElementById("id_pin_code").value = "";
      }
    }
  }
}

$(document).ready(function () {
  $(".add_to_cart").click(function (event) {
    event.preventDefault();
    food_id = $(this).data("id");
    data = { food_id: food_id };
    url = $(this).data("url");
    $.ajax({
      type: "GET",
      url: url,
      data: data,
      success: function (response) {
        const {
          status,
          message,
          total_quantity: totalQuantity,
          qty: foodQuantity,
          subtotal,
          tax,
          total,
        } = response;
        if (status === "failed") {
          swal({
            text: message,
            icon: "info",
            timer: 2000,
          }).then(() => {
            window.location = "/login";
          });
        } else {
          $("#cart_counter").text(totalQuantity);
          $(`#qty-${food_id}`).text(foodQuantity);
          $("#subtotal").text(`$ ${subtotal}`);
          $("#tax").text(`$ ${tax}`);
          $("#total").text(`$ ${total}`);
          swal({
            text: message,
            icon: "success",
            timer: 1000,
          });
        }
      },
      error: function () {
        swal({
          text: "Something went wrong, try again.",
          icon: "error",
          timer: 2000,
        });
      },
    });
  });
});

$(document).ready(function () {
  $(".remove_from_cart").click(function (event) {
    event.preventDefault();
    food_id = $(this).data("id");
    data = { food_id: food_id };
    url = $(this).data("url");
    $.ajax({
      type: "GET",
      url: url,
      data: data,
      success: function (response) {
        const {
          status,
          message,
          total_quantity: totalQuantity,
          qty: foodQuantity,
          subtotal,
          tax,
          total,
        } = response;
        if (status === "success") {
          $("#cart_counter").text(totalQuantity);
          $(`#qty-${food_id}`).text(foodQuantity);
          $("#subtotal").text(`$ ${subtotal}`);
          $("#tax").text(`$ ${tax}`);
          $("#total").text(`$ ${total}`);
          swal({
            text: message,
            icon: "success",
            timer: 1000,
          });
        } else {
          swal({
            text: message,
            icon: "info",
            timer: 2000,
          }).then(() => {
            window.location = "/login";
          });
        }
      },
      error: function () {
        swal({
          text: "Something went wrong, try again.",
          icon: "error",
          timer: 2000,
        });
      },
    });
  });
});

$(document).ready(function () {
  $(".delete_cart").click(function (event) {
    event.preventDefault();
    cart_id = $(this).data("id");
    data = { cart_id: cart_id };
    url = $(this).data("url");
    $.ajax({
      type: "GET",
      url: url,
      data: data,
      success: function (response) {
        const {
          status,
          message,
          total_quantity: totalQuantity,
          subtotal,
          tax,
          total,
        } = response;
        if (status === "success") {
          $("#cart_counter").text(totalQuantity);
          $("#subtotal").text(`$ ${subtotal}`);
          $("#tax").text(`$ ${tax}`);
          $("#total").text(`$ ${total}`);
          swal({
            text: message,
            icon: "success",
            timer: 1000,
          }).then(() => {
            clearCart(0, cart_id);
          });
        } else {
          swal({
            text: message,
            icon: "info",
            timer: 2000,
          });
        }
      },
      error: function () {
        swal({
          text: "Something went wrong, try again.",
          icon: "error",
          timer: 2000,
        });
      },
    });
  });
});