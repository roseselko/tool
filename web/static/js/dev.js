$("#sendMail").on("submit", function(e){
    e.preventDefault();
    var formData = new FormData(this);

    $.ajax({
        url: window.location.href,
        type: 'POST',
        data: formData,
        beforeSend: function(){
            $("#btnSend").attr("disabled")
            $("#btnSend").text("Sending")
        },
        success: function (res) {
            $("#btnSend").removeAttr("disabled")
            $("#btnSend").text("Send")
            if(!alert("Mail sent successfully.")){
                window.location.reload();
            }
        },
        error: function(){
            $("#btnSend").removeAttr("disabled")
            $("#btnSend").text("Send")
            alert("Error")
        },
        cache: false,
        contentType: false,
        processData: false
    });
});

$("select#gen_sender_name").on("change", function(){
    const status = this.value;
    if (status == "no"){
        $("#send_name").show();
    } else{
        $("#send_name").hide();
    }
});

$("select#gen_email_name").on("change", function(){
    const status = this.value;
    if (status == "no"){
        $("#mail_name").show();
    } else{
        $("#mail_name").hide();
    }
});

$("#validateLicense").on("submit", function(e){
    e.preventDefault();
    const pattern = "^[0]\d{10}$)|(^[\+]?[234]\d{12}$";
    var formData = new FormData(this);
    
    $.ajax({
        url: window.location.href,
        method: "POST",
        data: formData,
        beforeSend: function(){},
        success: function(res){
            if (res.success) {
                Swal.fire({position:"top-end",icon:"success",title:"Validated Successful.",showConfirmButton:!1,timer:1500})
                window.location.replace("/upload/")
            }
            else{
                Swal.fire({position:"top-end",icon:"error",title: res.error,showConfirmButton:!1,timer:1500})
            }
        },
        error: function(error){},
        cache: false,
        contentType: false,
        processData: false
    });
    
});
