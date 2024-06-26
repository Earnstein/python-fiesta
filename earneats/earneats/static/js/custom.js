let autocomplete;

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
      document.getElementById("id_latitude").value = results[0].geometry.location.lat();
      document.getElementById("id_longitude").value = results[0].geometry.location.lng();
      document.getElementById("id_address").value = results[0].formatted_address;
    }
  });

  for (var i = 0; i < place.address_components.length; i++) {
   for (var j = 0; j < place.address_components[i].types.length; j++) {
     if (place.address_components[i].types[j] == "country") {
       document.getElementById("id_country").value = place.address_components[i].long_name;
     };
     if (place.address_components[i].types[j] == "administrative_area_level_1") {
       document.getElementById("id_state").value = place.address_components[i].long_name;
     };
     if (place.address_components[i].types[j] == "locality") {
       document.getElementById("id_city").value = place.address_components[i].long_name;
     };
     if (place.address_components[i].types[j] == "postal_code") {
       document.getElementById("id_pin_code").value = place.address_components[i].long_name;
     }else {
       document.getElementById("id_pin_code").value = "";
     }
   };
  };
}
