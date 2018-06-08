/**
 * Created by derek on 2018/6/8.
 */
$(function () {
   $('#captcha-img').click(function (event) {
       var self= $(this);
       var src = self.attr('src');
       var newsrc = zlparam.setParam(src,'xx',Math.random());
       self.attr('src',newsrc);
   });
});