var all_data;
$.ajax({
  url: 'get_all_data'+window.location.search,//add date as param
  method: 'get',
  async: false, // notice this line
  success: (data) => {
    all_data = data;
  }
});
