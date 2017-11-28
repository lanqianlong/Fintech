
$(document).ready(function(){
 var count =0;
  $( "#calculate" ).click(function() {
   count=0;
    if($("#Firstname").val()==""){
      alert("Please fill the required feilds");
    }else{
      count++;
      
    }
    if($("#LastName").val()!=""){
      count=count+1;
    }else{
      count=count;
    }
    if($("#Email").val()!=""){
      count=count+1;
    }else{
      count=count;
    }
    if($("#PhoneNumber").val()!=""){
      count=count+1;
    }else{
      count=count;
    }
    if($("#StreetName").val()!=""){
      count=count+1;
    }else{
      count=count;
    }
    if($("#HouseNumber").val()!=""){
      count=count+1;
    }else{
      count=count;
    }
    if($("#Apartment").val()!=""){
      count=count+1;
    }else{
      count=count;
    }
    if($("#City").val()!=""){
      count=count+1;
    }else{
      count=count;
    }
    if($("#Zipcode").val()!=""){
      count=count+1;
    }else{
      count=count;
    }
    if($("#Country").val()!=""){
      count=count+1;
    }else{
      count=count;
    }
    $("#result").html("Your Score:"+count+"/10");

  });

});
