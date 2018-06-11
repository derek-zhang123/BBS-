
$(function(){
    $('.highlight-btn').on('click',function(){
       var $this=$(this);
       var tr=$this.parent().parent();
       var post_id=tr.attr('data-id');
       var highlight=parseInt(tr.attr('data-highlight'));
       var url='';
        if(highlight){
           url='/cms/uhpost/'
        }else{
            url='/cms/hpost/'
        }
        zlajax.post({
            'url':url,
            'data':{
                'post_id':post_id
            },
            'success':function(data){
                if(data['code']==200){
                    zlalert.alertSuccessToast('操作成功');
                    setTimeout(function(){
                        window.location.reload();
                    },500);
                }else{
                    zlalert.alertInfo(data['message']);
                }
            }
        })
    });
});