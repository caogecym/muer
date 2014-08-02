/*
Scripts for voting, deleting post
Project Name: Elephant
All Rights Resevred 2014. 
*/

define(function (require) {
    'use strict';

    var $ = require('jquery');
    var ns = {};

    ns.csrfSafeMethod = function(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    ns.sameOrigin = function(url) {
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
    };

    ns.goToHomePage = function(object, data) {
        window.location.replace("/home/");
    }

    ns.handleFail = function(xhr, msg){
        alert("Callback invoke error: " + msg)
    };

    ns.delete_post = function(object, callback) {
        $.ajax({
            type: "DELETE",
            cache: false,
            dataType: "json",
            url: "/posts/" + postId + "/delete/",
            data: { "postId": postId},
            error: ns.handleFail,
            success: function(data){
                ns.goToHomePage(object, data)
            }});
    }

    ns.submit = function(postId, callback) {
        $.ajax({
            type: "POST",
            cache: false,
            dataType: "json",
            url: "/posts/" + postId + "/like/",
            data: { "postId": postId},
            error: ns.handleFail,
            });
    };

    ns.initKudo = function () {
        // initialize kudos
        $.getScript(STATIC_URL+"kudo/kudos.js", function(){
            $("figure.kudoable").kudoable();
        });
        
        // when kudoing
        $("figure.kudo").bind("kudo:active", function(e)
        {
            console.log("kudoing active");
        });
        
        // when not kudoing
        $("figure.kudo").bind("kudo:inactive", function(e)
        {
            console.log("kudoing inactive");
        });
        
        // after kudo'd
        $("figure.kudo").bind("kudo:added", function(e)
        {
            var element = $(this);
            postId = element.data('id');
            // like
            ns.submit(postId);
        });
        
        // after removing a kudo
        $("figure.kudo").bind("kudo:removed", function(e)
        {
            var element = $(this);
            postId = element.data('id');
            // unlike
            ns.submit(postId);
        });
    };

    ns.initialize = function () {
        // For adding csrf token within internal url calls
        var csrftoken = $.cookie('csrftoken');

        // csrf setup
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!ns.csrfSafeMethod(settings.type) && ns.sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $('.post-delete').click(function (event) {
            object = $(event.target.parentElement)
            postId = object.attr("id").substring(imgIdPrefixLike.length);
            ns.delete_post(object);
        })

        $(document).ready(function() {
            $('.commentarea').keydown(function(event) {
                if (event.keyCode == 13) {
                    this.form.submit()
                    //redirect_url = "/posts/" + postId
                    window.location.replace("/posts/" + postId + "/");
                    return false;
                }
            });
        });

        ns.initKudo();
    }; // initialize //

    return ns;
});
