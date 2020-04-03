$(document).ready(function(){
  console.log($("#form-date"));
  $("#form-date").on("submit",function(e){
    // $(this).attr("")
    e.preventDefault();
    var selected_date=$("#date-input").val();
    url = $(this).attr("action")+"?date="+selected_date;
    console.log(url);
    window.location.replace(url);
  });
});
