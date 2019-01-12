

var pagesize = 0;
var num_entries = 0;
var totalnum = 0;
var page_index = 0;
var chaterid = $("#mh_data").attr("chapterid");
post_data = null







function deleteDraft(the){
    $.confirm({
        escapeKey: 'buttonName',
        buttons: {
            删除: {
                btnClass: 'btn-red',
                action: function(){
                    $.ajax({
                        type : "post",
                        url:'/chaptercontrol' + '/operate',
                        async:true,
                        data : post_data,
                        layerIndex:-1,
                        dataType:"json",

                        beforeSend:function () {
                            this.layerIndex = layer.load(0,{
                                shade: [0.5, '#393D49']
                            });
                        },

                        complete: function(){
                            layer.close(this.layerIndex);
                        },

                        success : function(data) {
                            if(data.picslist != "") {
                                $.alert(
                                    '图片已经删除'
                                );

                                console.log(data)
                                picslist = data.picslist
                                totalnum = data.totalnum
                                pagesize = data.pagesize

                                obj_picslist = []
                                for(var i=0;i<picslist.length;i++){
                                    var obj_pics = new Object();
                                    obj_pics.urls = picslist[i]
                                    obj_pics.num = i + 1
                                    obj_picslist.push(obj_pics)
                                }
                                console.log(obj_picslist)

                                html_str = Mustache.render(_template, {prop: obj_picslist})
                                //
                                $("#chapter_pics").html(html_str)


                                if(Math.ceil(totalnum/pagesize) != num_entries){
                                    num_entries =  Math.ceil(totalnum/pagesize)
                                    $("#Pagination1").pagination(num_entries, {
                                        maxentries:20,
                                        prev_text:'上一页',
                                        next_text:'下一页',
                                        num_edge_entries: 1, //边缘页数
                                        num_display_entries: 4, //主体页数
                                        items_per_page:1 //每页显示1项
                                    });
                                }

                            }
                            else {
                                location.reload([true])
                            }
                        },

                        error:function(){
                            layer.alert('部分数据加载失败，可能会导致页面显示异常，请刷新后重试', {
                                skin: 'layui-layer-molv'
                                , closeBtn: 0
                                , shift: 4 //动画类型
                            });
                        }

                    });


                }
            },
            取消:  {
                btnClass: 'btn-blue',

            },
        },
        content: '是否删除该图片!',
        title: '删除图片',
    });
}

function insertDraft(the,pic_url){
    layer.open({
        type: 2,
        area: ['700px', '450px'],
        fixed: false, //不固定
        maxmin: true,
        content: '/chaptercontrol/upload?chapterid=' + chaterid + '&pic_url=' + pic_url
    });
}

function operatepics(type,pic_url){
    console.log(type)
    post_data = {"chapterid":chaterid,"manhuaid":"manhuaid456","operatetype":type,"pic_url":pic_url,"page":page_index}
    if(type===3){
        // 删除操作提示框
        deleteDraft(this)
    }else if(type==4){
        insertDraft(this,pic_url)
    }else{
        $.ajax({
            method:"post",
            url:'/chaptercontrol' + '/operate',
            async:true,
            data : post_data,
            dataType:"json",

            success:function(data){
                console.log(data)
                picslist = data.picslist
                totalnum = data.totalnum
                pagesize = data.pagesize

                obj_picslist = []
                for(var i=0;i<picslist.length;i++){
                    var obj_pics = new Object();
                    obj_pics.urls = picslist[i]
                    obj_pics.num = i + 1
                    obj_picslist.push(obj_pics)
                }
                console.log(obj_picslist)

                html_str = Mustache.render(_template, {prop: obj_picslist})
                //
                $("#chapter_pics").html(html_str)
            },
            error:function(){
                alert("请求失败！");
            }
        });
    }


}


function pageselectCallback(page_index, jq){
    // ajax
    // console.log(111111);
    // console.log(page_index);
    Mustache.parse(_template);
    pagenum = page_index+1;
    // rating_data = {"page":page,"pagesize":pagesize,"goodsid":rating_goodsid,"businessid":rating_businessid};
    rating_data = {"chapterid":chaterid,"page":page_index};
    $.ajax({
        method:"get",
        url:'/chaptercontrol' + '/getpicslist',
        async:true,
        data : rating_data,
        dataType:"json",
        success:function(data){
            picslist = data.picslist
            totalnum = data.totalnum
            pagesize = data.pagesize

            obj_picslist = []
            for(var i=0;i<picslist.length;i++){
                var obj_pics = new Object();
                obj_pics.urls = picslist[i]
                obj_pics.num = i + 1
                obj_picslist.push(obj_pics)
            }
            console.log(obj_picslist)

            html_str = Mustache.render(_template, {prop: obj_picslist})
            //
            $("#chapter_pics").html(html_str)

        },
        error:function(){
            alert("请求失败！");
        }
    });
    return false;
}



var _template = [
    '                            <tr>',
    '                                <th>序号</th>',
    '                                <th>图片名称</th>',
    '                                <th>操作</th>',
    '                            </tr>',
    '{{#prop}}',
    '                           <tr>',
    '                                                                <td>{{num}}</td>',
    '                                <td>{{urls}}</td>',
    '                                <td class="last">',
    '                                    <a onclick="operatepics(type=1,pic_url = \'{{urls}}\')" > 上移 </a>',
    '                                    <a onclick="operatepics(type=2,pic_url = \'{{urls}}\')" >下移</a>',
    '                                    <a onclick="operatepics(type=3,pic_url =\'{{urls}}\')">删除</a>',
    '                                    <a onclick="operatepics(type=4,pic_url =\'{{urls}}\')">插入</a>',
    '                                </td>',
    '                            </tr>',
    '{{/prop}}',
].join('');


$(function(){
    // 创建分页
    var initPagination = function() {
        rating_data = {"chapterid":chaterid,"page":page_index};
        // 发送ajax请求，获取配置信息
        $.ajax({
            method: "get",
            url: '/chaptercontrol' + '/getpicslist',
            async: true,
            data: rating_data,
            dataType: "json",
            success: function (data) {
                console.log(data)
                totalnum = data.totalnum
                page = data.page
                pagesize = data.pagesize

                num_entries =  Math.ceil(totalnum/pagesize) ;
                // 创建分页
                $("#PageNum").pagination(num_entries, {
                    maxentries:20,
                    prev_text:'上一页',
                    next_text:'下一页',
                    num_edge_entries: 1, //边缘页数
                    num_display_entries: 4, //主体页数
                    callback: pageselectCallback,
                    items_per_page:1 //每页显示1项
                });
            },
        });

    }();

    $(".i_kfi_sub .i_zoom a").click(function(event) {
        var index = $(this).index();
        switch(index){
            case 0: $(".i_sub_con").css("fontSize","12px");break;
            case 1: $(".i_sub_con").css("fontSize","14px");break;
            case 2: $(".i_sub_con").css("fontSize","18px");break;
            case 3: $(".i_sub_con").css("fontSize","16px");break;
            default:$(".i_sub_con").css("fontSize","16px");break;
        }
    });
})