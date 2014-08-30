/*
Scripts for voting, deleting post
Project Name: Elephant
All Rights Resevred 2014. 
*/

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
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    };

    ns.goToHomePage = function(data) {
        window.location.replace("/home/");
    }

    ns.handleFail = function(xhr, msg){
        alert(xhr.responseText);
    };

    ns.delete_post = function(postId) {
        $.ajax({
            type: "DELETE",
            url: "/api/posts/" + postId,
            success: function(data){
                ns.goToHomePage(data)
            },
            error: ns.handleFail,
        });
    }

    ns.like = function(postId) {
        $.ajax({
            type: "POST",
            url: "/api/posts/" + postId + "/like/",
            success: function(){
                console.log('like successful');
            },
            error: ns.handleFail,
        });
    };

    ns.unlike = function(postId) {
        $.ajax({
            type: "POST",
            url: "/api/posts/" + postId + "/unlike/",
            success: function(){
                console.log('unlike successful');
            },
            error: ns.handleFail,
        });
    };

    ns.initKudo = function () {
        // initialize kudos
        $.getScript(STATIC_URL+"libs/kudo/kudos.js", function(){
            $("figure.kudoable").kudoable();
        });
        
        // like after kudo'd
        $("figure.kudo").bind("kudo:added", function(e)
        {
            var postId = $(this).data('id');
            ns.like(postId);
        });
        
        // unlike after removing a kudo
        $("figure.kudo").bind("kudo:removed", function(e)
        {
            var postId = $(this).data('id');
            ns.unlike(postId);
        });
    };

    ns.onCommentLikeSuccess = function (response) {
        var commentId = response.id;
        $('.comment-upvote[data-commentid=' + commentId + ']').addClass('up');
        $('.comment-upvote[data-commentid=' + commentId + ']').text('unlike');
        var $commentCount = $('.comment-like-count[data-commentid=' + commentId + ']');
        var likeCount = parseInt($commentCount.text());
        $commentCount.text(likeCount + 1);
    };

    ns.onCommentUnlikeSuccess = function (response) {
        var commentId = response.id;
        $('.comment-upvote[data-commentid=' + commentId + ']').removeClass('up');
        $('.comment-upvote[data-commentid=' + commentId + ']').text('like');
        var $commentCount = $('.comment-like-count[data-commentid=' + commentId + ']');
        var likeCount = parseInt($commentCount.text());
        $commentCount.text(likeCount - 1);
    };

    ns.onCommentSuccess = function (response) {
        // TODO: refresh comment list
        $('.post-comments').append('<li class="inner-pre">' + response.content + '</li>');
        $('.commentarea').val('');
        $('.alert-success').text('Comment added!');
        $('.alert-success').show(0).delay(1000).hide(0);
    };

    ns.onCommentFail = function (response) {
        $('.alert-warning').text(response.responseJSON.detail);
        $('.alert-warning').show(0).delay(1000).hide(0);
    }


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

        $('.post-delete').click(function () {
            var postId = $(this).data('postid');
            ns.delete_post(postId);
        });

        $('.comment-upvote').click(function () {
            var commentId = $(this).closest('li').data('commentid');
            if (!$(this).hasClass('up')) {
                $.ajax({
                    type: 'POST',
                    url: '/api/comments/' + commentId + '/like/',
                    success: ns.onCommentLikeSuccess,
                });
            }
            else {
                $.ajax({
                    type: 'POST',
                    url: '/api/comments/' + commentId + '/unlike/',
                    success: ns.onCommentUnlikeSuccess,
                });
            }
        });

        $(document).ready(function() {
            // TODO: add post button
            $('.commentarea').keydown(function(event) {
                if (event.keyCode == 13) {
                    var postId = $('.post-content').data('postid');
                    $.ajax({
                        type: 'POST',
                        data: {
                            content: $(this).val(),
                            post: postId,
                            author: ns.curUser,
                        },
                        url: '/api/comments/',
                        success: ns.onCommentSuccess,
                        error: ns.onCommentFail,
                    });
                }
            });
        });

        ns.initKudo();
    }; // initialize //

    return ns;
});
