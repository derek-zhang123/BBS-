$(function () {
    var ue = UE.getEditor('ueditor', {'serverUrl': '/ueditor/upload/'});
    $('#submit-btn').on('click', function (event) {
        event.preventDefault();
        var titleInput = $('input[name=title]');
        var boardSelect = $('select[name=board_id]');

        var title = titleInput.val();
        var board_id = boardSelect.val();
        var content = ue.getContent();
        zlajax.post({
            'url': '/apost/',
            'data': {
                'title': title,
                'board_id': board_id,
                'content': content
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    zlalert.alertConfirm({
                        'msg': '帖子发表成功',
                        'cancelText': '返回首页',
                        'confirmText': '再写一篇',
                        'cancelCallback': function () {
                            window.location = '/';
                        },
                        'confirmCallback': function () {
                            titleInput.val('');
                            ue.setContent('');

                        }
                    });
                } else {
                    zlalert.alertInfo(data['message']);
                }

            }
        })
    });
});