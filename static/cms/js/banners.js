$(function () {
    $('#save_banner_btn').click(function (event) {
        event.preventDefault();
        var dialog = $('#banner-dialog');
        var nameInput = $("input[name='name']");
        var imgInput = $("input[name='img_url']");
        var linkInput = $("input[name='link_url']");
        var priorityInput = $("input[name='priority']");

        var name = nameInput.val();
        var img_url = imgInput.val();
        var link_url = linkInput.val();
        var priority = priorityInput.val();

        if (!name || !img_url || !link_url || !priority) {
            zlalert.alertInfo('请输入完整的轮播图数据');
            return;
        }

        zlajax.post({
            'url': '/cms/abanner/',
            'data': {
                'name': name,
                'img_url': img_url,
                'link_url': link_url,
                'priority': priority
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    dialog.modal('hide');
                    window.location.reload()
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError()
            }
        });
    });

});