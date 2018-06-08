/**
 * Created by derekon 2018/6/4.
 */

$(function () {
    $("#captcha-btn").click(function (event) {
        event.preventDefault();
        var email = $("input[name='email']").val();
        if (!email) {
            zlalert.alertInfoToast('请输入邮箱');
        }
        zlajax.get({
            'url': '/cms/email_captcha/',
            'data': {'email': email},
            'success': function (data) {
                if (data['code'] == 200) {
                    zlalert.alertSuccessToast('邮件已发送成功！请注意查收！');
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });
    });
});


$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var emailE = $("input[name='email']");
        var captcheE = $("input[name='captcha']");

        var email = emailE.val();
        var captcha = captcheE.val();

        zlajax.post({
            'url': '/cms/resetemail/',
            'data': {'email': email, 'captcha': captcha},
            'success': function (data) {
                if (data['code'] == 200) {
                    emailE.val("");
                    captcheE.val("");
                    zlalert.alertSuccessToast('恭喜！邮箱修改成功');
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });
    });
});



