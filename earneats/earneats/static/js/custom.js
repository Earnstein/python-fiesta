let autocomplete;
// Country code mapping for django_countries
const countryCodeMap = {
  Nigeria: "NG",
  "United States": "US",
  "United Kingdom": "GB",
  Canada: "CA",
  Australia: "AU",
  Germany: "DE",
  France: "FR",
  Spain: "ES",
  Italy: "IT",
  Netherlands: "NL",
  Belgium: "BE",
  Switzerland: "CH",
  Austria: "AT",
  Sweden: "SE",
  Norway: "NO",
  Denmark: "DK",
  Finland: "FI",
  Poland: "PL",
  "Czech Republic": "CZ",
  Hungary: "HU",
  Romania: "RO",
  Bulgaria: "BG",
  Greece: "GR",
  Portugal: "PT",
  Ireland: "IE",
  "New Zealand": "NZ",
  "South Africa": "ZA",
  Kenya: "KE",
  Ghana: "GH",
  Egypt: "EG",
  Morocco: "MA",
  Tunisia: "TN",
  Algeria: "DZ",
  Libya: "LY",
  Sudan: "SD",
  Ethiopia: "ET",
  Uganda: "UG",
  Tanzania: "TZ",
  Zambia: "ZM",
  Zimbabwe: "ZW",
  Botswana: "BW",
  Namibia: "NA",
  Mozambique: "MZ",
  Angola: "AO",
  Congo: "CG",
  "Democratic Republic of the Congo": "CD",
  Cameroon: "CM",
  Chad: "TD",
  Niger: "NE",
  Mali: "ML",
  "Burkina Faso": "BF",
  Senegal: "SN",
  Guinea: "GN",
  "Sierra Leone": "SL",
  Liberia: "LR",
  "Ivory Coast": "CI",
  Togo: "TG",
  Benin: "BJ",
  "Central African Republic": "CF",
  "Equatorial Guinea": "GQ",
  Gabon: "GA",
  "Republic of the Congo": "CG",
  "São Tomé and Príncipe": "ST",
  "Cape Verde": "CV",
  Mauritania: "MR",
  "Western Sahara": "EH",
  Gambia: "GM",
  "Guinea-Bissau": "GW",
  Comoros: "KM",
  Seychelles: "SC",
  Mauritius: "MU",
  Madagascar: "MG",
  Malawi: "MW",
  Lesotho: "LS",
  Eswatini: "SZ",
  Burundi: "BI",
  Rwanda: "RW",
  Djibouti: "DJ",
  Eritrea: "ER",
  Somalia: "SO",
  "South Sudan": "SS",
  India: "IN",
  China: "CN",
  Japan: "JP",
  "South Korea": "KR",
  "North Korea": "KP",
  Vietnam: "VN",
  Thailand: "TH",
  Myanmar: "MM",
  Laos: "LA",
  Cambodia: "KH",
  Malaysia: "MY",
  Singapore: "SG",
  Indonesia: "ID",
  Philippines: "PH",
  Taiwan: "TW",
  "Hong Kong": "HK",
  Macau: "MO",
  Mongolia: "MN",
  Kazakhstan: "KZ",
  Uzbekistan: "UZ",
  Kyrgyzstan: "KG",
  Tajikistan: "TJ",
  Turkmenistan: "TM",
  Afghanistan: "AF",
  Pakistan: "PK",
  Bangladesh: "BD",
  "Sri Lanka": "LK",
  Nepal: "NP",
  Bhutan: "BT",
  Maldives: "MV",
  Iran: "IR",
  Iraq: "IQ",
  Syria: "SY",
  Lebanon: "LB",
  Jordan: "JO",
  Israel: "IL",
  Palestine: "PS",
  "Saudi Arabia": "SA",
  Yemen: "YE",
  Oman: "OM",
  "United Arab Emirates": "AE",
  Qatar: "QA",
  Bahrain: "BH",
  Kuwait: "KW",
  Turkey: "TR",
  Georgia: "GE",
  Armenia: "AM",
  Azerbaijan: "AZ",
  Russia: "RU",
  Ukraine: "UA",
  Belarus: "BY",
  Lithuania: "LT",
  Latvia: "LV",
  Estonia: "EE",
  Moldova: "MD",
  Slovakia: "SK",
  Slovenia: "SI",
  Croatia: "HR",
  "Bosnia and Herzegovina": "BA",
  Serbia: "RS",
  Montenegro: "ME",
  Kosovo: "XK",
  "North Macedonia": "MK",
  Albania: "AL",
  Iceland: "IS",
  Luxembourg: "LU",
  Malta: "MT",
  Cyprus: "CY",
  Brazil: "BR",
  Argentina: "AR",
  Chile: "CL",
  Peru: "PE",
  Colombia: "CO",
  Venezuela: "VE",
  Ecuador: "EC",
  Bolivia: "BO",
  Paraguay: "PY",
  Uruguay: "UY",
  Guyana: "GY",
  Suriname: "SR",
  "French Guiana": "GF",
  Mexico: "MX",
  Guatemala: "GT",
  Belize: "BZ",
  "El Salvador": "SV",
  Honduras: "HN",
  Nicaragua: "NI",
  "Costa Rica": "CR",
  Panama: "PA",
  Cuba: "CU",
  Jamaica: "JM",
  Haiti: "HT",
  "Dominican Republic": "DO",
  "Puerto Rico": "PR",
  "Trinidad and Tobago": "TT",
  Barbados: "BB",
  Grenada: "GD",
  "Saint Vincent and the Grenadines": "VC",
  "Saint Lucia": "LC",
  Dominica: "DM",
  "Antigua and Barbuda": "AG",
  "Saint Kitts and Nevis": "KN",
  Bahamas: "BS",
  "Cayman Islands": "KY",
  "British Virgin Islands": "VG",
  "US Virgin Islands": "VI",
  Aruba: "AW",
  Curaçao: "CW",
  "Sint Maarten": "SX",
  "Bonaire, Sint Eustatius and Saba": "BQ",
  "Falkland Islands": "FK",
  Greenland: "GL",
  "French Polynesia": "PF",
  "New Caledonia": "NC",
  Fiji: "FJ",
  "Papua New Guinea": "PG",
  "Solomon Islands": "SB",
  Vanuatu: "VU",
  "New Caledonia": "NC",
  "French Polynesia": "PF",
  "Wallis and Futuna": "WF",
  Samoa: "WS",
  Tonga: "TO",
  Tuvalu: "TV",
  Kiribati: "KI",
  Nauru: "NR",
  Palau: "PW",
  Micronesia: "FM",
  "Marshall Islands": "MH",
  "Northern Mariana Islands": "MP",
  Guam: "GU",
  "American Samoa": "AS",
  "Cook Islands": "CK",
  Niue: "NU",
  Tokelau: "TK",
  "Pitcairn Islands": "PN",
  "Easter Island": "CL",
  "Galápagos Islands": "EC",
};

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
        const countryName = place.address_components[i].long_name;
        const countryCode = countryCodeMap[countryName] || countryName;
        document.getElementById("id_country").value = countryCode;
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
$(function () {
  // Handle password toggle buttons
  $(".password-toggle").on("click", function (e) {
    e.preventDefault();

    const targetId = $(this).data("target");
    const passwordField = $("#" + targetId);
    const icon = $(this).find("i");

    if (passwordField.length === 0) {
      // If field doesn't have an ID, try to find it as a sibling
      const passwordInput = $(this)
        .siblings('input[type="password"], input[type="text"]')
        .first();

      if (passwordInput.attr("type") === "password") {
        passwordInput.attr("type", "text");
        icon.removeClass("fa-eye").addClass("fa-eye-slash");
      } else {
        passwordInput.attr("type", "password");
        icon.removeClass("fa-eye-slash").addClass("fa-eye");
      }
    } else {
      // Field has an ID, use it directly
      if (passwordField.attr("type") === "password") {
        passwordField.attr("type", "text");
        icon.removeClass("fa-eye").addClass("fa-eye-slash");
      } else {
        passwordField.attr("type", "password");
        icon.removeClass("fa-eye-slash").addClass("fa-eye");
      }
    }
  });

  // Ensure password fields generated by Django forms get proper IDs
  $('input[name="password"]').each(function () {
    if (!$(this).attr("id")) {
      $(this).attr("id", "id_password");
    }
  });

  $('input[name="confirm_password"]').each(function () {
    if (!$(this).attr("id")) {
      $(this).attr("id", "id_confirm_password");
    }
  });
});
