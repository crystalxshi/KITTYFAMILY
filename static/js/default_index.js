// This is the js for the default/index.html view.
var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    // Enumerates an array.
    var enumerate = function(v) { var k=0; return v.map(function(e) {e._idx = k++;});};
    self.show_form=function(){
          self.vue.form_show=true;
    };
    self.show_hide=function(){
          self.vue.form_show=false;
    };
    self.add_post = function () {
        // We disable the button, to prevent double submission.
        $.web2py.disableElement($("#add-post"));
        var sent_title = self.vue.form_title; // Makes a copy
        var sent_content = self.vue.form_content; //
        $.post(add_post_url,
            // Data we are sending.
            {
                post_title: self.vue.form_title,
                post_content: self.vue.form_content
            },
            // What do we do when the post succeeds?
            function (data) {
                // Re-enable the button.
                $.web2py.enableElement($("#add-post"));
                // Clears the form.
                self.vue.form_title = "";
                self.vue.form_content = "";
                self.vue.form_show = false;
                // Adds the post to the list of posts.
                var new_post = {
                    id: data.post_id,
                    post_title: sent_title,
                    post_content: sent_content,
                    like_num: 0,
                    unlike_num:0
                };
                self.vue.post_list.unshift(new_post);
                // We re-enumerate the array.
                self.process_posts();
            });
        // If you put code here, it is run BEFORE the call comes back.
    };

    self.get_posts = function() {
        $.getJSON(get_post_list_url,
            function(data) {
                // I am assuming here that the server gives me a nice list
                // of posts, all ready for display.
                self.vue.post_list = data.post_list;
                // Post-processing.
                self.process_posts();
                console.log("I got my list");
            }
        );
        console.log("I fired the get");
    };

    self.process_posts = function() {
        // This function is used to post-process posts, after the list has been modified
        // or after we have gotten new posts.
        // We add the _idx attribute to the posts.
        enumerate(self.vue.post_list);
        // We initialize the smile status to match the like.
        self.vue.post_list.map(function (e) {
            // I need to use Vue.set here, because I am adding a new watched attribute
            // to an object.  See https://vuejs.org/v2/guide/list.html#Object-Change-Detection-Caveats
            // The code below is commented out, as we don't have smiles any more.
            // Replace it with the appropriate code for thumbs.
            // // Did I like it?
            // // If I do e._smile = e.like, then Vue won't see the changes to e._smile .
            // Vue.set(e, '_smile', e.like);
            Vue.set(e, 'editing', false);
        });
    };

    self.editPost = function(post_idx) {
        var p = self.vue.post_list[post_idx];
        p.editing = true;
        editing = p.editing;
    };
    self.deletePost = function(post_idx) {
        var p = self.vue.post_list[post_idx];
        $.post(delete_post_url,
            {
                post_id: p.id,
            });
        p.editing = false;
    };
    self.submitEditPost = function(post_idx) {
        var p = self.vue.post_list[post_idx];
        var newText = document.getElementById("edittext").value;
        p.post_content = newText;
        $.post(edit_post_url,
            {
                post_id: p.id,
                post_content: newText
            });
        p.editing = false;
    };

    self.changethumbs=function(type,id){
        $.get(set_like_url,
            // Data we are sending.
            {
                post_id: id,
                thumb_state: type
            },
            // What do we do when the post succeeds?
            function (data) {
                console.log(typeof data);
                   if(data.code==-1){
                       alert("Please login first!")
                   }else{
                      self.get_posts();
                   }

            });

    };

    self.thumbTrans=function(type,val,index){
        this.type=type;
        if(val==1){
           this.current=index;
        }else{
           this.current=-1;
        }
    };
    
    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            form_title: "",
            form_content: "",
            post_list: [],
            form_show:false,
            current:-1,
            type:0,
			login:is_logged_in
        },
        methods: {
            add_post: self.add_post,
            show_form:self.show_form,
            show_hide:self.show_hide,
            changethumbs:self.changethumbs,
            thumbTrans:self.thumbTrans,
            editPost: self.editPost,
            submitEditPost: self.submitEditPost,
            deletePost:self.deletePost
        }
    });

    // If we are logged in, shows the form to add posts.
    if (is_logged_in) {
        $("#add_post").show();
    }

    // Gets the posts.
    self.get_posts();

    return self;
};

var APP = null;

// No, this would evaluate it too soon.
// var APP = app();

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
