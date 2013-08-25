/*
Scripts for voting post
Project Name: Elephant
All Rights Resevred 2013. 
*/

var imgIdPrefixLike = 'post-img-like-';
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
    $('.post-img-like-wrapper').click(function (event) {
        object = $(event.target)
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
        data: { "postId": postId },
        error: handleFail,
        success: function(data){
            changeVoteImage(object, data)
        }});
        //success: function(data){callback(object, data)}});
};

var changeVoteImage = function(object, data) {
    // TODO: add cancel, after user model is created
    object[0].style.backgroundImage="url('/static/images/liked.png')"
};

var handleFail = function(xhr, msg){
    alert("Callback invoke error: " + msg)
};
