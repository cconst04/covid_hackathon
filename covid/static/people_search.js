$("#people_search").on("click",function(){
  $(this).html("");
  $(this).append('<span class="spinner-border spinner-border-sm"></span>Loading..');
  var btn = $(this);
  $.ajax({
    method:"GET",
    url:$("#people_url").attr("url"),
    data:{'ssn':$("#people_input").val()},
    success:function(response){
      $("#search_results").not("#search_header").html("");
      btn.html("Search");
      console.log(response);
      $("#search_results").show();
      $("#search_header").html("Results for:"+$("#people_input").val());
      var res='<ul class="list-group">';
      console.log(response.data.length);
      for(var i=0;i<response.data.length;i++){
        res+='<li class="list-group-item">['+new Date(response.data[i].date)+
             '][Postal Code:'+response.data[i].postal_code__postal_code+'][Reason:'+response.data[i].reason+']</li>';
      }
      res+="</ul>"
      console.log(res);
      $("#search_results").append(res);
    }
  });
});
