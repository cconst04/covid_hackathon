var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 34.7886447, lng: 32.4056301},
    zoom: 12
  });
  for(var i=0;i<all_data.count_per_coordinate.length;i++){
    var marker = new google.maps.Marker({
      position: {lat: all_data.count_per_coordinate[i].lat, lng: all_data.count_per_coordinate[i].lon},
      map: map,
      title: "Total sms:"+all_data.count_per_coordinate[i].value
    });
    var infowindow = new google.maps.InfoWindow({
      content: "Total sms:"+all_data.count_per_coordinate[i].value
    });
    marker.addListener('click', function() {
      infowindow.open(map, marker);
    });
  }

}
