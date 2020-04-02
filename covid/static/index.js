var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 34.7886447, lng: 32.4056301},
    zoom: 12
  });

  for(var i=0;i<all_data.count_per_coordinate.length;i++){
    var cityCircle = new google.maps.Circle({
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: map,
        title:"Total sms:"+all_data.count_per_coordinate[i].value,
        center: {lat: all_data.count_per_coordinate[i].lat, lng: all_data.count_per_coordinate[i].lon},
        radius: Math.sqrt(all_data.count_per_coordinate[i].value) * 100
      });

    // var marker = new google.maps.Marker({
    //   position: {lat: all_data.count_per_coordinate[i].lat, lng: all_data.count_per_coordinate[i].lon},
    //   map: map,
    //   title: "Total sms:"+all_data.count_per_coordinate[i].value
    // });
    var infoWindow = new google.maps.InfoWindow();
    google.maps.event.addListener(cityCircle, 'click', function(ev){
      infoWindow.setContent(this.title);
      infoWindow.setPosition(ev.latLng);
      infoWindow.open(map);
    });
    // cityCircle.addListener('click', function() {
    //   infowindow.open(map, cityCircle);
    // });
  }

  for(var i=0;i<all_data.fines.length;i++){
    var cityCircle = new google.maps.Circle({
        strokeColor: '#329DA8',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#329DA8',
        fillOpacity: 0.35,
        map: map,
        title:"Total fines:"+all_data.fines[i].count+" "+(new Date(all_data.fines[i].date)),
        center: {lat: all_data.fines[i].lat, lng: all_data.fines[i].lon},
        radius: Math.sqrt(all_data.fines[i].count) * 100
      });

    // var marker = new google.maps.Marker({
    //   position: {lat: all_data.count_per_coordinate[i].lat, lng: all_data.count_per_coordinate[i].lon},
    //   map: map,
    //   title: "Total sms:"+all_data.count_per_coordinate[i].value
    // });
    var infoWindow = new google.maps.InfoWindow();
    google.maps.event.addListener(cityCircle, 'click', function(ev){
      infoWindow.setContent(this.title);
      infoWindow.setPosition(ev.latLng);
      infoWindow.open(map);
    });
  }

  var defaultBounds = new google.maps.LatLngBounds(
    new google.maps.LatLng(35.0290183, 33.3258966),
    new google.maps.LatLng(35.3634419, 33.8971857)
  );
  map.fitBounds(defaultBounds);

// Create the search box and link it to the UI element.
  var input = /** @type {HTMLInputElement} */(
    document.getElementById('place_search')
  );
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  var searchBox = new google.maps.places.SearchBox(
  /** @type {HTMLInputElement} */(input)
  );

// [START region_getplaces]
// Listen for the event fired when the user selects an item from the
// pick list. Retrieve the matching places for that item.
  google.maps.event.addListener(searchBox, 'places_changed', function() {
    var places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }
    // for (var i = 0, marker; marker = markers[i]; i++) {
    //   marker.setMap(null);
    // }

    // For each place, get the icon, place name, and location.
    var bounds = new google.maps.LatLngBounds();
    for (var i = 0, place; place = places[i]; i++) {
      var image = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25)
      };

      // Create a marker for each place.
      var marker = new google.maps.Marker({
        map: map,
        icon: image,
        title: place.name,
        position: place.geometry.location
      });

      bounds.extend(place.geometry.location);
    }

    map.fitBounds(bounds);
  });
  // [END region_getplaces]

  // Bias the SearchBox results towards places that are within the bounds of the
  // current map's viewport.
  google.maps.event.addListener(map, 'bounds_changed', function() {
    var bounds = map.getBounds();
    searchBox.setBounds(bounds);
  });

  // google.maps.event.addDomListener(window, 'load', initialize);



}
