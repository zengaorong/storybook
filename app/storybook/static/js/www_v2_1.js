function mySubStr(str, len) {
    if(str==undefined)return '';

    str = str.replace(/<br ?\/?>/gi,'');
    // str = str.replace('<br/>','');
    // str = str.replace('<br />','');
    // str = str.replace('<p>','');
    // str = str.replace('</p>','');

    if(str.length>len){
        return str.substr(0,len)+"...";
    }else{
        return str;
    }
}




//设置cookie
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires+"; path=/;";
}
//把高亮诗句添加进cookies
function setHighLightShiju(sj) {
    setCookie(COOKIES_KEY_SHIJU_HIGHLIGHT,sj,1);
}

//获取cookie
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) != -1) return c.substring(name.length, c.length);
    }
    return "";
}

function toRed(kw, word) {

    var arr = kw.split(" ");

    for(var i in arr){
        var k = arr[i];
        if(k=='')continue;
        word =  word.replace(new RegExp(k,"g"),'<em>'+k+'</em>');
    }
    return word;
}

var COOKIES_KEY_KW = 'key_kw';
var COOKIES_KEY_CATE = 'key_cate';
var COOKIES_KEY_SHIJU_HIGHLIGHT = 'key_shiju_highlight';
//鼠标是否进入ajax搜索结果范围
var isEnterSearchResult = false;

var searchResultSelectedIndex = 0;//搜索结果选中index
var searchMaxResult = 0;//搜索结果数量
var cate = 'all';
var subAjaxScid = 0;
layui.use(['form','jquery','carousel'],function () {
    var form = layui.form;
    var $ = layui.$;
    var carousel = layui.carousel;
    var search_input_container = $("#search_input_container");

    //搜索框
    var INPUT = $("#search_input");
    //搜索框清除按钮
    var clearBtn = $("#clear_input");

    //搜索框获取焦点事件
    var picDomain = 'http://pics.mathfunc.com/';
    //搜索结果tab
    var topNav = $("#top_nav");
    //搜索框内容改变事件
    search_input_container.hover(function () {
        isEnterSearchResult = true;
    },function () {
        isEnterSearchResult = false;
    });

    INPUT.blur(function () {
        if(!isEnterSearchResult){
            hideResult();
        }

    });
    var lastKw = getCookie(COOKIES_KEY_KW);

    if(lastKw!=undefined){
        INPUT.val(lastKw);
    }



    function setItem(k, v) {
        try{
            sessionStorage.setItem(k,v);
        }catch(oException){
            if(oException.name == 'QuotaExceededError'){
                //如果历史信息不重要了，可清空后再设置
                sessionStorage.clear();
                sessionStorage.setItem(k,v);
            }
        }
    }

    function getItem(k) {
        return sessionStorage.getItem(k);
    }

    //主ajax
    function ajaxCallBack(res,kw) {
        if(INPUT.val()!=kw){
            return;
        }
        var shicis,shijus;
        var zuozhes = res.zuozhes;
        if(res.titles!=undefined)shicis = res.titles.shicis;
        if(res.shijus!=undefined)shijus = res.shijus.shijus;

        var books = res.books;
        var chengyus = res.chengyus;
        var result = '';
        var kw_url = encodeURI(kw);
        var total = 0;
        searchMaxResult = 0;
        searchResultSelectedIndex = 0;
        if(zuozhes!=undefined && zuozhes.zuozhes.length>0){
            total = zuozhes.total;
            var zzs = zuozhes.zuozhes;
            for(var i in zzs){
                var item = zzs[i];
                var img = '';
                if(item.pic !="" && item.pic!=null){
                    img = '<img src="'+picDomain+item.pic+'">';
                }

                var zz = toRed(kw,item.zuozhe);
                result +='<li><a href="/poetry/actorlist/'+item.id+'">['+item.niandai+'] <strong>'+zz+'</strong><span>作者</span></a></li>';
                searchMaxResult++;
            }
        }

        if(shicis!=undefined && shicis.length>0){
            for(var i in shicis){
                var item = shicis[i];
                var title = toRed(kw,item.title);
                result +='<li><a href="/poetry/chaptershow/'+item.scid+'" data-scid="'+item.scid+'"><strong>《'+title+'》</strong>['+item.niandai+'] '+item.zuozhe+'<span>标题</span></a></li>';
                searchMaxResult++;
            }
            total = res.titles.total;
        }

        if(shijus!=undefined && shijus.length>0){
            for(var i in shijus){
                var item = shijus[i];

                var shiju = toRed(kw,item.shiju);

                result += '<li><a href="/poetry/chaptershow/'+item.scid+'" data-scid="'+item.scid+'" data-shiju="'+item.shiju+'" class="highlight-link2"><strong>'+shiju+'</strong>'+item.zuozhe+' 《'+item.title+'》'+'<span>诗句</span></a></li>';

                searchMaxResult++;
            }
            total = res.shijus.total;
        }

        if(books!=undefined && books.length>0){
            for(var i in books){
                var item = books[i];

                var title = toRed(kw,item.title);
                if(item.cate == 'book_name'){
                    result += '<li><a href="/book/'+item.urlname+'.html" data-urlname="'+item.urlname+'"><strong>《'+title+'》</strong>'+item.info+'<span>古籍</span></a></li>';

                }else{

                    result += '<li><a href="/book/chaxun/?kw='+kw_url+'&book_id='+item.id+'"><strong>《'+title+'》</strong>'+item.info+'<span>古籍</span></a></li>';
                }
                searchMaxResult++;
            }
        }

        if(chengyus!=undefined && chengyus.length>0){
            chengyusCache = chengyus;
            total = chengyus[0].total;
            for(var i in chengyus){
                var item = chengyus[i];
                var name = toRed(kw,item.name);
                result += '<li><a href="/chengyu/'+item.py+'-'+item.id+'.html" data-jieshi="'+item.jieshi+'"><strong>'+name+'</strong>['+item.pinyin+']<span>成语</span></a></li>';
                searchMaxResult++;
            }
        }


        if(result == ''){
            $(".result-card").html(result);
            search_input_container.removeClass('search-status');
            $(".result-card").hide();
            $(".sub-result-card").hide();
        }else{
            if(cate!='all'){
                var u = '';
                if(cate == 'book'){
                    u = "/book/chaxun/?kw="+kw_url;
                    result+='<li><a href="'+u+'" style="text-align: center;vertical-align: middle;font-size: 16px;font-weight: bold"><i class="iconfont icon-search" style="font-size: 14px"></i>古籍全文检索</a></li>';
                }else if(cate == 'chengyu'){
                    u = "/chengyu/chaxun/?kw="+kw_url;
                    result+='<li><a href="'+u+'" style="text-align: center;vertical-align: middle;font-size: 16px;font-weight: bold"><i class="iconfont icon-search" style="font-size: 14px"></i>更多成语('+total+')</a></li>';
                }else{

                    if(cate == 'first' || cate == 'end'){
                        u = '/chaxun/shiju/'+cate+'/'+kw_url;
                    }else if(cate == 'title'){
                        u = '/chaxun/shici/'+kw_url;
                    }else if(cate =='zz_list'){
                        u = '/chaxun/zuozhe_list/'+kw_url;
                    }else{
                        u = '/chaxun/'+cate+'/'+kw_url;
                    }
                    result+='<li><a href="'+u+'" style="text-align: center;vertical-align: middle;font-size: 16px;font-weight: bold"><i class="iconfont icon-search" style="font-size: 14px"></i> 查看全部查询结果('+total+')</a></li>';
                }

                searchMaxResult++;
            }

            result = '<ul>'+result+'</ul>';

            $(".result-card").html(result);
            search_input_container.addClass('search-status');
            $(".result-card").show();

            $(".highlight-link2").on('click',function () {
                var sj = $(this).attr('data-shiju');
                setHighLightShiju(sj);
            });


            listen();
        }
    }
    //内容改变和获得焦点事件
    INPUT.on('input focus',function(e){
        var kw = $(this).val();
        if(kw==undefined)kw = '';

        setCookie(COOKIES_KEY_KW,kw,3);

        $(".result-card").hide();
        $(".sub-result-card").hide();
        if(kw.length ==0){
            clearBtn.addClass('www-visibility-hidden');
            search_input_container.removeClass('search-status');
        }else{
            // clearBtn.css('opacity',1);
            clearBtn.removeClass('www-visibility-hidden');
            var postCate = cate;
            var position = 0;
            if(cate == 'shiju'){
                position = 1;
            }else if(cate == 'first'){
                postCate = 'shiju';
                position = 0;
            }else if(cate =='end'){
                postCate = 'shiju';
                position = 2;
            }else if(cate =='title'){
                position = 1;
            }


            var k = cate+':v2:'+kw;

            // var r = getItem(k);
            var r;
            if(r != undefined){
                var res = JSON.parse(r);
                ajaxCallBack(res,kw);
            }else{
                $.ajax({
                    method:'POST',
                    data:{
                        kw:kw,
                        cate:cate,
                        position:position
                    },
                    url:'/storybook/story/api/ajaxSearch',
                    success:function (res) {
                        setItem(k,JSON.stringify(res));
                        ajaxCallBack(res,kw);
                    }
                });
            }


        }
    });


    if(INPUT.val().length>0){
        clearBtn.removeClass('www-visibility-hidden');
    }
    INPUT.hover(function () {
        searchResultSelectedIndex = 0;
        refreshSearchIndex();
    },function () {

    });
    $('.search-tab-top ul li a').on('click',function () {
        $('.search-tab-top ul li a').removeClass('search-tab-current');
        $(this).addClass('search-tab-current');
        cate = $(this).attr('data-cate');

        setCookie(COOKIES_KEY_CATE,cate,100);
    });

    var lastCate = getCookie(COOKIES_KEY_CATE);

    if(lastCate){
        cate = lastCate;
    }else{
        cate = 'all';
    }
    refreshCate();
    function refreshCate() {
        $('.search-tab-top ul li a').each(function () {
            if($(this).attr('data-cate') == cate){
                $(this).addClass('search-tab-current')
            }else{
                $(this).removeClass('search-tab-current')
            }
        })
    }

    function listen() {
        $('.result-card ul li a').hover(function () {
            var me = this;
            $('.result-card ul li a').each(function (index,e) {
                if(e == me){
                    if(searchResultSelectedIndex == index+1){
                        return;
                    }
                    searchResultSelectedIndex = index+1;
                    refreshSearchIndex();
                    return;
                }
            });
        },function () {

        });
    }
    //搜索结果指示加一
    function searchIndexAdd() {
        searchResultSelectedIndex ++;
        if(searchResultSelectedIndex>searchMaxResult){
            searchResultSelectedIndex = 1;
        }
        refreshSearchIndex()
    }
//搜索结果指示减一
    function searchIndexMinus() {
        searchResultSelectedIndex--;
        if(searchResultSelectedIndex<=0){
            searchResultSelectedIndex = searchMaxResult;
        }
        refreshSearchIndex()
    }

    function hideResult() {
        search_input_container.removeClass('search-status');
        $(".result-card").hide();
        $('.sub-result-card').hide();
    }
    //刷新指示
    function refreshSearchIndex() {
        isEnterSearchResult = true;
        var hh ;
        $('.result-card ul li a').each(function (index,e) {
            if(index+1 == searchResultSelectedIndex){
                $(this).addClass('selected');
                hh = this;
                var top = $(this).position().top;

                var ctop = $('.result-card').css('top');
                ctop = ctop.replace('px','');

                top = top+Number(ctop)+1;
                $('.sub-result-card').css('top',top+"px");
            }else{
                $(this).removeClass('selected');
            }
        });


        if(cate == 'chengyu'){
            var jieshi = $(hh).attr('data-jieshi');

            if(jieshi!=undefined){
                $('.sub-result-card').show();
                $('.sub-result-card').html("【释义】"+jieshi);
            }else{
                $('.sub-result-card').hide();
            }


        }else{
            var scid = $(hh).attr('data-scid');
            subAjaxScid = scid;
            if(scid!=undefined){
                $('.sub-result-card').show();
                $('.sub-result-card').html('加载中...');

                var k = 'scid:v2:'+scid;

                var r = getItem(k);
                if(r!=undefined){
                    var res = JSON.parse(r);
                    subAjaxCallBack(res);

                }else{
                    $.ajax({
                        method:'GET',
                        url:'/poetry/api/itemContent?scid='+scid,
                        cache:true,
                        success:function (res){
                            if(subAjaxScid != scid)return;
                            if(res!=undefined && res!=''){
                                subAjaxCallBack(res);
                                setItem(k,JSON.stringify(res));
                            }
                        }
                    });
                }


            }else{
                $('.sub-result-card').html("");
                $('.sub-result-card').hide();
            }
        }

    }

    function subAjaxCallBack(res) {
        $('.sub-result-card').html(res.content);
    }






    $('#search_form').submit(function (e) {
        if(searchResultSelectedIndex !=0){
            e.preventDefault();
            $('.result-card ul li a').each(function (index, e) {
                if(index+1 == searchResultSelectedIndex){
                    var url = $(this).attr('href');

                    window.location = url;
                    var sj = $(this).attr('data-shiju');
                    setHighLightShiju(sj);
                    return;
                }
            })
        }else{
            if(cate !='all'){
                e.preventDefault();
                var kw_url = encodeURI(INPUT.val());

                var u = '';
                if(cate == 'book'){
                    u = '/book/chaxun/?kw='+kw_url;
                }else if(cate == 'chengyu'){
                    u = '/chengyu/chaxun?kw='+kw_url;
                }else{
                    if(cate == 'first' || cate == 'end'){
                        u = '/chaxun/shiju/'+cate+'/'+kw_url;
                    }else if(cate == 'title'){
                        u = '/chaxun/shici/'+kw_url;
                    }else if(cate =='zz_list'){
                        u = '/chaxun/zuozhe_list/'+kw_url;
                    }else{
                        u = '/chaxun/'+cate+'/'+kw_url;
                    }
                }

                window.location = u;
            }
        }


    });

    INPUT.keydown(function (e) {
        if(e.keyCode == 38){
            searchIndexMinus();
        }else if(e.keyCode == 40){
            searchIndexAdd();
        }else if(e.keyCode == 27){
            hideResult();
        }
    });


    //清除按钮点击事件
    clearBtn.on('click',function () {
        INPUT.val('');
        INPUT.focus();
        clearBtn.addClass('www-visibility-hidden');
        topNav.show();
    });

    //设置搜索结果的长度
    $(".result-card").width(search_input_container.width());
    $('.sub-result-card').width(search_input_container.width()*0.5);
    $('.sub-result-card').css('left',search_input_container.width()+'px');

    $(".www-search-nav-ul li a").on('click',function () {
        $(".card_item").hide();
        $(".www-search-nav-ul li a").removeClass('www-selected');
        $(this).addClass('www-selected');
        var id = $(this).attr('id');
        if(id!=undefined){
            id = id.replace('_nav','');
            $("#"+id).show();
            $('html').animate({
                scrollTop: 0
            }, 300);
        }

    });



    //侧边栏作者简介
    var asideZuozheSummary = $(".aside-zuozhe-summary .summary");
    $("#aside_zuozhe_more").on('click',function () {
        var px = asideZuozheSummary.css('max-height');
        if(px =='200px'){
            asideZuozheSummary.css('max-height','2000px');
            setTimeout(function () {
                $(".more-info img").addClass('rotate-180');
            },300)

        }else{
            asideZuozheSummary.css('max-height','200px');

            setTimeout(function () {
                $(".more-info img").removeClass('rotate-180');
            },300)
        }
    });
    if(asideZuozheSummary!=undefined){
        $(document).ready(function () {
            var h = asideZuozheSummary.height();
            if(h>200){
                asideZuozheSummary.css('max-height','200px');
            }else{
                $("#aside_zuozhe_more .more-info").hide();
            }
        })
    }

    var toTopPx = 0;
    var HEADER = $("#header");
    var MAIN_ADJUST = $(".main-adjust");

    $(window).scroll(function () {
        var top = $(window).scrollTop();


        if(top>toTopPx &&top>100){//隐藏导航栏
            HEADER.css('top','-100px');
            // MAIN_ADJUST.css('margin-top','0px');
            toTopPx = top;
        }else if(top<toTopPx){//显示导航栏
            HEADER.css('top','0px');
            // MAIN_ADJUST.css('margin-top','100px');
            toTopPx = top;
        }
    });



    //新窗~

    var newWindow = $("#newWindow");
    var COOKIES_KEY_NEW_WINDOW = "link_new_window";
    var isNewWindow = getCookie(COOKIES_KEY_NEW_WINDOW)=="yes";
    newWindow.attr('checked',isNewWindow);
    if(isNewWindow){
        $(".www-main-container h3 a").attr("target","_blank");
    }
    newWindow.change(function () {
        if(newWindow.is(":checked")){
            $(".www-main-container h3 a").attr("target","_blank");
            setCookie(COOKIES_KEY_NEW_WINDOW,"yes",10000);
        }else {
            $(".www-main-container h3 a").attr("target","_self");
            setCookie(COOKIES_KEY_NEW_WINDOW,"no",10000);
        }
    });



    //歇后语显示答案

    $(".xiehouyu .answer a").on('click',function () {

        $(this).hide();
        $(this).next().show();
    });

    //渲染ddd
    if($("#ddd_aside")!=undefined){
        carousel.render({
            elem: '#ddd_aside'
            ,width: '100%' //设置容器宽度
            ,arrow: 'always' //始终显示箭头
            //,anim: 'updown' //切换动画方式
        });
    }

    $(".nav-xiala-father").hover(function () {
        $(this).children(".nav-xiala").show();
    },function () {
        $(this).children(".nav-xiala").hide();
    });

    //滚动到顶部
    $("#totop").on('click',function () {
        $('html,body').animate({scrollTop:0}, 300);
    });

    //展开更多搜索结果
    $(".more-chaxun-result").on('click',function () {
        if($(this).parent().next().css('max-height') == '0px'){
            $(this).parent().next().addClass("sub-item-show");
            $(this).parent().next().removeClass("sub-item-hide");
            $(this).children('i').removeClass("rotate-180");
        }else{
            $(this).parent().next().removeClass("sub-item-show");
            $(this).parent().next().addClass("sub-item-hide");
            $(this).children('i').addClass("rotate-180");

        }
    });



    $(".book-chaxun-more").on('click',function () {
        if($(this).parent().next().css('display') == 'none'){
            $(this).parent().next().show();
            $(this).children('img').addClass('rotate-180');

        }else{
            $(this).children('img').removeClass('rotate-180');
            $(this).parent().next().hide();
        }


    });

    //章节页面高亮

    if(/\/book\/[a-zA-Z0-9]+\/[0-9]+\.html/.test(location.pathname)){
        if(/^\?kw=[^&]+$/.test(location.search)){
            var kw = decodeURI(location.search).replace('?kw=','');

            var kwArr = kw.split(" ");

            var content = $(".chapter_content").html();
            if(kw.length>0){

                for(var i in kwArr){
                    var reg = new RegExp(kwArr[i],'g');
                    content = content.replace(reg,'<span class="highlight">'+kwArr[i]+'</span>');
                }
                $(".chapter_content").html(content);

                var first = $('.highlight:first');
                if(first.length){


                    var ch = $(first).position().top;
                    $('html,body').animate({scrollTop:ch}, 300);
                }
            }
        }
    }


    $('.highlight-link').on('click',function () {
        var sj = $(this).html();
        sj = sj.replace('<em>','');
        sj = sj.replace('</em>','');
        setHighLightShiju(sj);
    });
    //诗句高亮

    if(/\/chaxun\/list\/[0-9]+\.html/.test(location.pathname)){
        var sj = getCookie(COOKIES_KEY_SHIJU_HIGHLIGHT);
        if(sj!=undefined && sj.length>0){

            var content = $('.shici-content').html();
            var reg = new RegExp(sj,'g');
            content = content.replace(reg,'<span class="highlight">'+sj+'</span>');
            $('.shici-content').html(content);
            setCookie(COOKIES_KEY_SHIJU_HIGHLIGHT,'',0);
        }
    }


});