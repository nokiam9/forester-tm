// ==UserScript==
// @name         TM of notice list
// @namespace    www.caogo.cn
// @version      0.5
// @description  scrapy notice info from DOM
// @author       sj0225@icloud.com
// @match        https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=*
// @require      https://b2b.10086.cn/b2b/supplier/b2bStyle/js/jquery.min.js
// @grant        GM_xmlhttpRequest
// @grant        GM_openInTab
// @connect      http://127.0.0.1:3000/*
// ==/UserScript==

(function() {
    'use strict';

    const main = async function() {
        const spider = 'TM'; // TamperMonkey
        const notice_type_id = window.location.search.split('=')[1]; // 取出url的参数值 [1,2,3,7,8,16]
        const active_page_selector = 'a.current';
        const next_page_button_selector = '#pageid2 > table > tbody > tr > td:nth-child(4) > a';
        const post_url = 'http://127.0.0.1:3000/v1/notice';

        do {
            await waitforNode(window, active_page_selector);

            // 提取当前活跃焦点的Page序号
            let page_now = Number(document.querySelector(active_page_selector).textContent);
            console.log('Info(main): page_now=', page_now, '，爬取&发送数据');

            await getNoticeList(document, spider, notice_type_id).then( // 分析页面获得公告列表的数据
                noticeList => postNoticeList(noticeList, post_url) // 通过XHR发送爬取结果数据
            ).then(
                response => console.log(response), // 分析XHR结果，如果全部数据重复，说明页面无更新，需要想办法退出main()
                error => console.error(error)
            );

            if (document.querySelector(next_page_button_selector)) { // 发现‘下一页’按钮
                console.log('Info(main): Pause 5 seconds for next page');
                await sleep(5000);
                $(next_page_button_selector)[0].onclick(); // 模拟click动作
            } else { // 找不到‘下一页’的按钮，说明页面已全部提取
                console.log('Info(main): Scrapy data compeleted !!!');
                return;
            }
        } while(1);
    }
    main();

    // Func: 分析list页面，返回公告列表
    function getNoticeList(listDoc, spider, notice_type_id){
        return new Promise((resolve, reject)=> {
            const first_notice_selector = '#searchResult > table > tbody > tr:nth-child(3)';
            const content_base_url = 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=';

            let now = new Date();
            let notices = [];
            let line = listDoc.querySelector(first_notice_selector); // 提取第一行notice
            while (line) {
                notices.push({
                    spider: spider,
                    type_id: notice_type_id,
                    nid: line.getAttribute('onclick').split("'")[1],
                    source_ch: line.children[0].textContent,
                    notice_type: line.children[1].textContent,
                    title: line.children[2].children[0].textContent,
                    published_date: line.children[3].textContent,
                    timestamp: now.toJSON(),
                }); // 获得公告列表的基础信息
                line = line.nextElementSibling; // 循环提取下一行
            };

            // 采用异步模式新开窗口提取公告内容文本等数据
            (async function getContentFromList(){
                let ctw = window.open(); // 打开一个临时窗口，用于提取内容文本，循环使用以节约资源

                for (let i in notices) {
                    let url = content_base_url + notices[i].nid;
                    await getNoticeContent(ctw, url).then(function(content){
                        //console.log('Debug(getContentFromList): Result: nid=', notices[i].nid, ',length=', result.length);
                        //debugger;
                        Object.assign(notices[i], {notice_content : content}); // 追加公告内容，后续增加附件下载功能
                    });
                };
                ctw.close();
                resolve(notices);
            })(); //定义函数并立即执行
        })
    }

    function getNoticeContent(handle, url) {
        return new Promise((resolve,reject)=>{
            console.log('Debug(getContent): Start! url=', url);
            const selector_id = '#tableWrap';
            const retry_delay = 500;
            const retry_limits = 5;

            let retry_cnt = 0;
            handle.location.assign(url); // 打开内容网页，设置计数器等待指定内容出现
            let myVar2 = setInterval(function(){myTimer2()}, retry_delay);

            function myTimer2(){
                //console.log('Debug(getContent->myTimer): Start...');
                if (handle.document.querySelector(selector_id)) {
                    //console.log('Debug(getContent->myTimer): scrapy content successful! title=', handle.document.querySelector('#title').innerText);
                    clearInterval(myVar2);
                    resolve(handle.document.body.innerText.trim());
                } else if (retry_cnt >= retry_limits) {
                    clearInterval(myVar2);
                    reject('Warn(getContent->myTimer): scrapy content html timeout! url=', url);
                } else retry_cnt++;
            };
        })
    }

    // Func: 向XHR发送公告数据
    function postNoticeList(noticeList, url){
        return new Promise((resolve, reject)=>{
            console.log('Debug(postNoticeList): Start...');
            //console.log('cnt=', noticeList.length, ', ex=', noticeList[0].notice_content);
            //debugger;

            // 成批post公告数据
            /*
            GM_xmlhttpRequest ({
                method:     "POST",
                url:        url,
                data:       noticeList,
                onload:     function (response){
                    console.log('XHR onload:', response.responseText);
                    resolve(response); // 如果全部数据重复，要想办法自动退出
                },
                onerror: function(error){
                    reject('XHR onerror: network error!'); // POST网络故障时退出
                }
            });
            */
            resolve('Test: post records=' + noticeList.length); //Debug
        });
    }

    function waitforNode(handle, selector_id){
        return new Promise((resolve, reject)=> {
            const retry_delay = 500;
            const retry_limits = 5;

            console.log('Debug(waitforNode): start looking for node with ', selector_id);
            let retry_cnt = 0;
            let myVar = setInterval(function(){myTimer()}, retry_delay);

            function myTimer() {
                if (handle.document.querySelector(selector_id)) {
                    clearInterval(myVar);
                    resolve(handle.document);
                } else if (retry_cnt >= retry_limits) {
                    clearInterval(myVar);
                    reject('Error(waitforNode->myTimer): Failed searching for node=', selector_id);
                } else retry_cnt++;
            }
        })
    }

    function sleep(ms) {
        return new Promise((resolve) => {
            setTimeout(resolve, ms);
        });
    }
})();