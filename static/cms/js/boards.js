$(function () {
    $('#add_board_btn').on('click', function () {
        event.preventDefault();
        zlalert.alertOneInput({
            'title':'添加板块',
            'text': '请输入板块名称',
            'placeholder': '版块名称',
            'confirmCallback': function (inputValue) {
                zlajax.post({
                    'url': '/cms/aboards/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            zlalert.alertInfo(data['message']);
                        }
                    }
                });

            }
        })
    });

});