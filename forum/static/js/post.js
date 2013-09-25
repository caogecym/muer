/*
Scripts for voting post
Project Name: Elephant
All Rights Resevred 2013. 
*/

var imgIdPrefixLike = 'post-';
var postId;

// For adding csrf token within internal url calls
var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(function () {
    $('.featurette-image').click(function (event) {
        object = $(event.target.parentElement)
        postId = object.attr("id").substring(imgIdPrefixLike.length);
        submit(object);
    })
})

var submit = function(object, callback) {
    $.ajax({
        type: "POST",
        cache: false,
        dataType: "json",
        url: "/posts/" + postId + "/like/",
        data: { "postId": postId},
        error: handleFail,
        success: function(data){
            updateVoteImage(object, data)
        }});
};

var updateVoteImage = function(object, data) {
    if (data.not_authenticated == 1) {
        $('#login_modal').modal('show'); 
        return;
    }
    if (data.status == 1) {
        object[0].children[2].style.background = "url('static/images/like.png') no-repeat";
        //object[0].children[0].src = "static/images/like.png"
    } 
    else {
        object[0].children[2].style.background = "url('static/images/liked.png') no-repeat";
        //object[0].children[0].src = "static/images/liked.png"
    }
};

var handleFail = function(xhr, msg){
    alert("Callback invoke error: " + msg)
};
