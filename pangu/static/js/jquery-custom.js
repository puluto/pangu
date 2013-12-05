/* $('#level1_seleclist_id').flushSelectList('level2_selectlist_id', 'http://...'); */

(function($){
    $.fn.flushSelectList = function(d, url) {
        $.ajax({
            url: url,
            type: 'post',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            data: { 
                current_id: $(this).val()
            },
            success: function(msg) {
                var tmp = eval(msg);
                var str = '';
                for (var i = 0; i < tmp.length; i++) {
                    var c = tmp[i];
                    str += '<option value=' + c + '>' + c + '</option>';
                }
                $('#' + d).html(str);
            }
        });
        
        console.log(data)
    }
}(jQuery));