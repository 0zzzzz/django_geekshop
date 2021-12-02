$(function(){
    $.ajax({                                      
      url: 'api.php',                       
      data: "",                                                      
      dataType: 'json',                
      success: function(data)          
      {
        //var obj=JSON.parse(data);
        var obj=data;
        for (var x in obj)
          {
          alert(obj[x].id + " AND " + obj[x].desc);
          }         
      } 
   });   
});