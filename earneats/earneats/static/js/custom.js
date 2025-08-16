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

$(function () {
  $(".add_to_cart").on("click", function (event) {
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

$(function () {
  $(".remove_from_cart").on("click", function (event) {
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

$(function () {
  $(".delete_cart").on("click", function (event) {
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

function setLocation(latitude, longitude) {
  sessionStorage.setItem("lat", latitude);
  sessionStorage.setItem("lng", longitude);
}

function updateUrlWithCoordinates(latitude, longitude) {
  const url = new URL(window.location);
  url.searchParams.set("lat", latitude);
  url.searchParams.set("lng", longitude);
  history.pushState({}, "", url);
}

function getLocation() {
  const x = document.getElementById("id_location");

  // Check if URL already has lat/lng params
  const urlParams = new URLSearchParams(window.location.search);
  const lat = urlParams.get("lat");
  const lng = urlParams.get("lng");

  if (lat && lng) {
    // URL already has coordinates, use them
    const location = sessionStorage.getItem("location");
    if (location) {
      x.value = location;
    } else {
      x.value = `${lat}, ${lng}`;
    }
    return;
  }

  // Check sessionStorage only if URL doesn't have params
  const location = sessionStorage.getItem("location");
  if (location) {
    x.value = location;
    return;
  }

  if (!x) {
    console.error("Location input element not found");
    return;
  }

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => success(position, x),
      (error) => handleError(error, x)
    );
  } else {
    x.value = "Geolocation is not supported by this browser.";
  }
}

function success(position, element) {
  const { latitude, longitude } = position.coords;
  element.value = `${latitude}, ${longitude}`;

  // Get the address from the latitude and longitude
  if (typeof google !== "undefined" && google.maps) {
    const geocoder = new google.maps.Geocoder();
    const latlng = { lat: parseFloat(latitude), lng: parseFloat(longitude) };

    geocoder.geocode({ location: latlng }, (results, status) => {
      if (status === "OK" && results[0]) {
        element.value = results[0].formatted_address;
        sessionStorage.setItem("location", results[0].formatted_address);
        setLocation(latitude, longitude);
        updateUrlWithCoordinates(latitude, longitude);
      } else {
        element.value = `${latitude}, ${longitude}`;
        setLocation(latitude, longitude);
        updateUrlWithCoordinates(latitude, longitude);
      }
    });
  } else {
    // Fallback if Google Maps is not available
    element.value = `${latitude}, ${longitude}`;
    updateUrlWithCoordinates(latitude, longitude);
  }
}

function handleError(error, element) {
  element.value = "Location unavailable";
}

// Password Toggle Functionality
$(document).ready(function() {
  // Handle password toggle buttons
  $('.password-toggle').on('click', function(e) {
    e.preventDefault();
    
    const targetId = $(this).data('target');
    const passwordField = $('#' + targetId);
    const icon = $(this).find('i');
    
    if (passwordField.length === 0) {
      // If field doesn't have an ID, try to find it as a sibling
      const passwordInput = $(this).siblings('input[type="password"], input[type="text"]').first();
      
      if (passwordInput.attr('type') === 'password') {
        passwordInput.attr('type', 'text');
        icon.removeClass('fa-eye').addClass('fa-eye-slash');
      } else {
        passwordInput.attr('type', 'password');
        icon.removeClass('fa-eye-slash').addClass('fa-eye');
      }
    } else {
      // Field has an ID, use it directly
      if (passwordField.attr('type') === 'password') {
        passwordField.attr('type', 'text');
        icon.removeClass('fa-eye').addClass('fa-eye-slash');
      } else {
        passwordField.attr('type', 'password');
        icon.removeClass('fa-eye-slash').addClass('fa-eye');
      }
    }
  });
  
  // Ensure password fields generated by Django forms get proper IDs
  $('input[name="password"]').each(function() {
    if (!$(this).attr('id')) {
      $(this).attr('id', 'id_password');
    }
  });
  
  $('input[name="confirm_password"]').each(function() {
    if (!$(this).attr('id')) {
      $(this).attr('id', 'id_confirm_password');
    }
  });
});
