## 快速启动小程序
用微信开发者工具打开该文件下的mina文件夹即可

=====================
数据库的搭建
python环境搭建 （可选：创建python3的虚拟环境）
pip install -r requirements.txt 下载python所依赖的库

首先切换到source /root/bin/activate 的python3虚拟环境
关闭防火墙 systemctl stop firewalld（可选）
##启动（首先得在虚拟机上加载配置文件）且得有对应的数据库表
* export ops_config=local python manage.py runserver  本地运行
* export ops_config=production uwsgi --ini uwsgi.ini  线上开发

uwsgi 中配置对应端口 ，nginx进行80端口转发到对应配置中的端口

##flask-sqlacodegen

    ## 记得输入密码
    flask-sqlacodegen 'mysql://root:password@127.0.0.1/food_db' --outfile "common/models/model.py"  --flask
    flask-sqlacodegen 'mysql://root:password@127.0.0.1/food_db' --tables user --outfile "common/models/User.py"  --flask
    flask-sqlacodegen 'mysql://root:password@127.0.0.1/food_db' --tables app_access_log --outfile "common/models/log/AppAccessLog.py"  --flask
    flask-sqlacodegen 'mysql://root:password@127.0.0.1/food_db' --tables app_error_log --outfile "common/models/log/AppErrorLog.py"  --flask

## 所见即所得编辑器ueditor

    <script src="{{ buildStaticUrl('/plugins/ueditor/ueditor.config.js') }}"></script>
    <script src="{{ buildStaticUrl('/plugins/ueditor/ueditor.all.min.js') }}"></script>
    <script src="{{ buildStaticUrl('/plugins/ueditor/lang/zh-cn/zh-cn.js') }}"></script>


    UE.getEditor('editor',{
       toolbars: [
            [ 'undo', 'redo', '|',
                'bold', 'italic', 'underline', 'strikethrough', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall',  '|','rowspacingtop', 'rowspacingbottom', 'lineheight'],
            [ 'customstyle', 'paragraph', 'fontfamily', 'fontsize', '|',
                'directionalityltr', 'directionalityrtl', 'indent', '|',
                'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|', 'touppercase', 'tolowercase', '|',
                'link', 'unlink'],
            [ 'imagenone', 'imageleft', 'imageright', 'imagecenter', '|',
                'insertimage', 'insertvideo', '|',
                'horizontal', 'spechars','|','inserttable', 'deletetable', 'insertparagraphbeforetable', 'insertrow', 'deleterow', 'insertcol', 'deletecol', 'mergecells', 'mergeright', 'mergedown', 'splittocells', 'splittorows', 'splittocols' ]

        ],
        enableAutoSave:true,
        saveInterval:60000,
        elementPathEnabled:false,
        zIndex:4,
        serverUrl:common_ops.buildUrl(  '/upload/ueditor' )
    });



##可参考资料
* [python-Flask（jinja2）语法：过滤器](https://www.jianshu.com/p/3127ac233518)
* [SQLAlchemy 各种查询语句写法](https://wxnacy.com/2017/08/14/python-2017-08-14-sqlalchemy-filter/)

## 启动服务器
1.python manager.py runserver
2.runjob......来启动定时器
