webpackJsonp([2],{"8hXn":function(t,n,s){"use strict";Object.defineProperty(n,"__esModule",{value:!0});var i=s("lhjU"),a=s("MfVK"),e={name:"index",data:function(){return{match_list:[],ranking_list:[],info:{name:"",coins:0}}},methods:{setMatch:function(t,n){var s=this,e=t.pay_for;if(e.toString().indexOf(".")>-1||e.toString().indexOf("-")>-1||e<10||e>500)a.Toast.fail({message:"请输入正整数的押金，且范围为10-500",duration:2e3});else{var o={schedule_id:t.schedule_id,country_name:n,condition_id:t.condition_id,pay_for:e};a.Toast.loading("laoding"),i.a.httpApi.set_cup(o).then(function(t){200===t.code?(a.Toast.success(t.msg),s.getMatch()):a.Toast.fail(t.msg)})}},getInfo:function(){var t=this;i.a.httpApi.userinfo().then(function(n){200===n.code?(t.info.name=n.data.user_name,t.info.coins=n.data.coins):a.Toast.fail(n.msg)})},getMatch:function(){var t=this;i.a.httpApi.get_info().then(function(n){200===n.code?t.match_list=n.data.schedules:a.Toast.fail(n.msg)})},getRanking:function(){var t=this;i.a.httpApi.get_ranking().then(function(n){200===n.code?t.ranking_list=n.data.ranking:a.Toast.fail(n.msg)})},loginout:function(){var t=this;i.a.httpApi.logout().then(function(n){t.$router.push("/login")})}},created:function(){a.Toast.loading("laoding"),this.getInfo(),this.getMatch(),this.getRanking()}},o={render:function(){var t=this,n=t.$createElement,s=t._self._c||n;return s("div",{staticClass:"body"},[s("wv-header",{attrs:{title:"世界杯猜胜负"}},[s("div",{staticClass:"btn-back",attrs:{slot:"right"},slot:"right"},[s("span",{staticClass:"iconfont icon-back",on:{click:t.loginout}},[t._v("退出")])])]),t._v(" "),s("p",{staticClass:"infoBox"},[t._v(t._s(t.info.name)+"，您的金币："),s("span",{staticStyle:{color:"red"},domProps:{textContent:t._s(t.info.coins)}},[t._v("500")]),t._v("。查看"),s("router-link",{staticStyle:{color:"#ffe70b","text-decoration":"underline"},attrs:{to:"/history"}},[t._v("往期竞猜")])],1),t._v(" "),s("div",{staticClass:"matchBox"},[s("header",[t._v("本期竞猜")]),t._v(" "),0===t.match_list.length?s("div",[t._v("没有比赛可以竞猜")]):t._e(),t._v(" "),t._l(t.match_list,function(n,i){return s("div",{staticClass:"matchDiv"},[s("p",[t._v("竞猜截止："+t._s(n.guess_end_time))]),t._v(" "),s("wv-flex",{staticClass:"col-1"},[s("wv-flex-item",{attrs:{flex:"4"}},[t._v(t._s(n.country_a_cn))]),t._v(" "),s("wv-flex-item",{staticStyle:{color:"#fff"}},[t._v("VS")]),t._v(" "),s("wv-flex-item",{attrs:{flex:"4"}},[t._v(t._s(n.country_b_cn))])],1),t._v(" "),s("wv-flex",{staticClass:"col-2"},[s("wv-flex-item",[s("div",[t._v(t._s(n.handicap_disc))])]),t._v(" "),s("wv-flex-item",["unjoined"===n.flag?s("div",[t._v("押 "),s("wv-input",{staticClass:"moneyInput",attrs:{type:"number"},model:{value:n.pay_for,callback:function(s){t.$set(n,"pay_for",s)},expression:"m.pay_for"}}),t._v(" 金币")],1):t._e(),t._v(" "),"unjoined"!==n.flag?s("div",[t._v("押 "),s("span",{domProps:{textContent:t._s(n.pay_for)}},[t._v("0")]),t._v(" 金币")]):t._e()])],1),t._v(" "),"unjoined"===n.flag?s("wv-flex",{staticClass:"col-3",attrs:{gutter:5}},[s("wv-flex-item",[s("button",{staticClass:"matchBtn",on:{click:function(s){t.setMatch(n,n.country_a)}}},[t._v("支持"+t._s(n.country_a_cn)),s("span",{staticStyle:{"font-size":"10px"}},[t._v(t._s("("+n.odds_a+")"))])])]),t._v(" "),s("wv-flex-item",[s("button",{staticClass:"matchBtn",on:{click:function(s){t.setMatch(n,n.country_b)}}},[t._v("支持"+t._s(n.country_b_cn)),s("span",{staticStyle:{"font-size":"10px"}},[t._v(t._s("("+n.odds_b+")"))])])])],1):t._e(),t._v(" "),"cannot_join"===n.flag?s("div",{staticClass:"col-3"},[t._v("您未参加此场比赛竞猜")]):t._e(),t._v(" "),"joined"===n.flag?s("div",{staticClass:"col-3"},[t._v("您支持"+t._s(n.support_country_cn)+"胜，赔率为"+t._s(n.support_odds))]):t._e()],1)})],2),t._v(" "),t._m(0),t._v(" "),s("div",{staticClass:"conBox"},[s("header",{staticClass:"head-title2"},[t._v("--财富排行榜--")]),t._v(" "),s("ol",{},t._l(t.ranking_list,function(n){return s("li",[s("span",{staticStyle:{float:"right"},domProps:{textContent:t._s(n.coins)}},[t._v("10000")]),s("span",{domProps:{textContent:t._s(n.user_name)}},[t._v("张三")])])}))])],1)},staticRenderFns:[function(){var t=this,n=t.$createElement,s=t._self._c||n;return s("div",{staticClass:"conBox"},[s("header",{staticClass:"head-title"},[t._v(" --活动规则--")]),t._v(" "),s("ol",[s("li",[t._v("此活动参照的比分是90分钟内的比分，加时赛、点球的比分不计入。")]),t._v(" "),s("li",[t._v("初始金币为0，按照正负算值。")]),t._v(" "),s("li",[t._v("规则参照国际惯例（澳盘），每场比赛前1小时，关闭该场比赛的竞猜。")]),t._v(" "),s("li",[t._v("当天上午10点至次日上午10点为一个比赛日。上午10点之后公布昨日结算结果，上午10点当天比赛竞猜开始。")])])])}]};var c=s("VU/8")(e,o,!1,function(t){s("KYZC")},null,null);n.default=c.exports},KYZC:function(t,n){}});
//# sourceMappingURL=2.894a03669a624073735a.js.map