/*
Scripts for muer platform initialization
Project Name: Elephant
All Rights Resevred 2014. 
*/
/* global define document window alert STATIC_URL require */

define(function (require) {
    'use strict';

    var $ = require('jquery');
    var ns = {
        curUser: $('.user-label').data('userid')
    };

    ns.csrfSafeMethod = function(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    ns.sameOrigin = function(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var srOrigin = '//' + host;
        var origin = protocol + srOrigin;
        // Allow absolute or scheme relative URLs to same origin
        return (url === origin || url.slice(0, origin.length + 1) === origin + '/') ||
            (url === srOrigin || url.slice(0, srOrigin.length + 1) === srOrigin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    };

    ns.goToHomePage = function() {
        window.location.replace('/home');
    }

    ns.handleFail = function(xhr, msg){
        alert(xhr.responseText);
    };

    ns.deletePost = function(postId) {
        $.ajax({
            type: 'DELETE',
            url: '/api/posts/' + postId,
            success: function(data){
                ns.goToHomePage(data);
            },
            error: ns.handleFail,
        });
    };

    ns.like = function(postId) {
        $.ajax({
            type: 'POST',
            url: '/api/posts/' + postId + '/like',
            success: function(){
                console.log('like successful');
            },
            error: ns.handleFail,
        });
    };

    ns.unlike = function(postId) {
        $.ajax({
            type: 'POST',
            url: '/api/posts/' + postId + '/unlike',
            success: function(){
                console.log('unlike successful');
            },
            error: ns.handleFail,
        });
    };

    ns.initKudo = function () {
        // initialize kudos
        $.getScript(STATIC_URL + 'libs/kudo/kudos.js', function() {
            $('figure.kudoable').kudoable();
        });
        
        // like after kudo'd
        $('figure.kudo').bind('kudo:added', function() {
        {
            var postId = $(this).data('id');
            ns.like(postId);
        });
        
        // unlike after removing a kudo
        $('figure.kudo').bind('kudo:removed', function() {
        {
            var postId = $(this).data('id');
            ns.unlike(postId);
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
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });

        $('.post-delete').click(function () {
            // TODO: Add confirm dialog
            var postId = $(this).data('postid');
            ns.delete_post(postId);
        });

        $(document).ready(function () {
            ns.initKudo();
        });
    }; // initialize //

    return ns;
});
