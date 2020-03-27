var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 34.7886447, lng: 32.4056301},
    zoom: 15
  });
  var marker = new google.maps.Marker({
    position: {lat: 34.7886447, lng: 32.4056301},
    map: map,
    title: 'Hello World!'
  });
  var infowindow = new google.maps.InfoWindow({
    content: "<h1>There was an infected person here</h1><br><b>Time:12-03-2020 17:30</b>"
  });
  marker.addListener('click', function() {
    infowindow.open(map, marker);
  });

}
