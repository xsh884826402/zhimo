webpackJsonp([20],{Ai5B:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=a("Xxa5"),r=a.n(n),i=a("exGp"),s=a.n(i),c=a("bBUo"),o=a("1h8J"),l={data:function(){return{tableData:[{registe_time:"2016-05-02",username:"王小虎",city:"上海市普陀区金沙江路 1518 弄"},{registe_time:"2016-05-04",username:"王小虎",city:"上海市普陀区金沙江路 1517 弄"},{registe_time:"2016-05-01",username:"王小虎",city:"上海市普陀区金沙江路 1519 弄"},{registe_time:"2016-05-03",username:"王小虎",city:"上海市普陀区金沙江路 1516 弄"}],currentRow:null,offset:0,limit:20,count:0,currentPage:1}},components:{headTop:c.a},created:function(){this.initData()},methods:{initData:function(){var t=this;return s()(r.a.mark(function e(){var a;return r.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.x)();case 3:if(1!=(a=e.sent).status){e.next=8;break}t.count=a.count,e.next=9;break;case 8:throw new Error("获取数据失败");case 9:t.getUsers(),e.next=15;break;case 12:e.prev=12,e.t0=e.catch(0),console.log("获取数据失败",e.t0);case 15:case"end":return e.stop()}},e,t,[[0,12]])}))()},handleSizeChange:function(t){console.log("每页 "+t+" 条")},handleCurrentChange:function(t){this.currentPage=t,this.offset=(t-1)*this.limit,this.getUsers()},getUsers:function(){var t=this;return s()(r.a.mark(function e(){var a;return r.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,Object(o.z)({offset:t.offset,limit:t.limit});case 2:a=e.sent,t.tableData=[],a.forEach(function(e){var a={};a.username=e.username,a.registe_time=e.registe_time,a.city=e.city,t.tableData.push(a)});case 5:case"end":return e.stop()}},e,t)}))()}}},u={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"fillcontain"},[a("head-top"),t._v(" "),a("div",{staticClass:"table_container"},[a("el-table",{staticStyle:{width:"100%"},attrs:{data:t.tableData,"highlight-current-row":""}},[a("el-table-column",{attrs:{type:"index",width:"100"}}),t._v(" "),a("el-table-column",{attrs:{property:"registe_time",label:"注册日期",width:"220"}}),t._v(" "),a("el-table-column",{attrs:{property:"username",label:"用户姓名",width:"220"}}),t._v(" "),a("el-table-column",{attrs:{property:"city",label:"注册地址"}})],1),t._v(" "),a("div",{staticClass:"Pagination",staticStyle:{"text-align":"left","margin-top":"10px"}},[a("el-pagination",{attrs:{"current-page":t.currentPage,"page-size":20,layout:"total, prev, pager, next",total:t.count},on:{"size-change":t.handleSizeChange,"current-change":t.handleCurrentChange}})],1)],1)],1)},staticRenderFns:[]};var h=a("VU/8")(l,u,!1,function(t){a("wsmL")},null,null);e.default=h.exports},wsmL:function(t,e){}});
//# sourceMappingURL=20.2afe200158ed23321fbe.js.map