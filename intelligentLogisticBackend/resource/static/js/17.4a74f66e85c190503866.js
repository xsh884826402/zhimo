webpackJsonp([17],{"Y+5+":function(e,t){},dTCu:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s=a("Dd8w"),r=a.n(s),n=a("Xxa5"),l=a.n(n),o=a("exGp"),i=a.n(o),c=a("bBUo"),u=a("uaSg"),p=a("1h8J"),m={data:function(){return{baseUrl:u.b,baseImgPath:u.a,restaurant_id:null,city:{},offset:0,limit:20,count:0,tableData:[],currentPage:1,selectTable:{},dialogFormVisible:!1,menuOptions:[],selectMenu:{},selectIndex:null,specsForm:{specs:"",packing_fee:0,price:20},specsFormrules:{specs:[{required:!0,message:"请输入规格",trigger:"blur"}]},specsFormVisible:!1,expendRow:[]}},created:function(){this.restaurant_id=this.$route.query.restaurant_id,this.initData()},computed:{specs:function(){var e=[];return this.selectTable.specfoods&&this.selectTable.specfoods.forEach(function(t){e.push({specs:t.specs_name,packing_fee:t.packing_fee,price:t.price})}),e}},components:{headTop:c.a},methods:{initData:function(){var e=this;return i()(l.a.mark(function t(){var a;return l.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return t.prev=0,t.next=3,Object(p.o)({restaurant_id:e.restaurant_id});case 3:if(1!=(a=t.sent).status){t.next=8;break}e.count=a.count,t.next=9;break;case 8:throw new Error("获取数据失败");case 9:e.getFoods(),t.next=15;break;case 12:t.prev=12,t.t0=t.catch(0),console.log("获取数据失败",t.t0);case 15:case"end":return t.stop()}},t,e,[[0,12]])}))()},getMenu:function(){var e=this;return i()(l.a.mark(function t(){return l.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return e.menuOptions=[],t.prev=1,t.next=4,Object(p.p)({restaurant_id:e.selectTable.restaurant_id,allMenu:!0});case 4:t.sent.forEach(function(t,a){e.menuOptions.push({label:t.name,value:t.id,index:a})}),t.next=11;break;case 8:t.prev=8,t.t0=t.catch(1),console.log("获取食品种类失败",t.t0);case 11:case"end":return t.stop()}},t,e,[[1,8]])}))()},getFoods:function(){var e=this;return i()(l.a.mark(function t(){var a;return l.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,Object(p.n)({offset:e.offset,limit:e.limit,restaurant_id:e.restaurant_id});case 2:a=t.sent,e.tableData=[],a.forEach(function(t,a){var s={};s.name=t.name,s.item_id=t.item_id,s.description=t.description,s.rating=t.rating,s.month_sales=t.month_sales,s.restaurant_id=t.restaurant_id,s.category_id=t.category_id,s.image_path=t.image_path,s.specfoods=t.specfoods,s.index=a,e.tableData.push(s)});case 5:case"end":return t.stop()}},t,e)}))()},tableRowClassName:function(e,t){return 1===t?"info-row":3===t?"positive-row":""},addspecs:function(){this.specs.push(r()({},this.specsForm)),this.specsForm.specs="",this.specsForm.packing_fee=0,this.specsForm.price=20,this.specsFormVisible=!1},deleteSpecs:function(e){this.specs.splice(e,1)},handleSizeChange:function(e){console.log("每页 "+e+" 条")},handleCurrentChange:function(e){this.currentPage=e,this.offset=(e-1)*this.limit,this.getFoods()},expand:function(e,t){if(t)this.getSelectItemData(e);else{var a=this.expendRow.indexOf(e.index);this.expendRow.splice(a,1)}},handleEdit:function(e){this.getSelectItemData(e,"edit"),this.dialogFormVisible=!0},getSelectItemData:function(e,t){var a=this;return i()(l.a.mark(function s(){var n,o;return l.a.wrap(function(s){for(;;)switch(s.prev=s.next){case 0:return s.next=2,Object(p.t)(e.restaurant_id);case 2:return n=s.sent,s.next=5,Object(p.q)(e.category_id);case 5:o=s.sent,a.selectTable=r()({},e,{restaurant_name:n.name,restaurant_address:n.address,category_name:o.name}),a.selectMenu={label:o.name,value:e.category_id},a.tableData.splice(e.index,1,r()({},a.selectTable)),a.$nextTick(function(){a.expendRow.push(e.index)}),"edit"==t&&a.restaurant_id!=e.restaurant_id&&a.getMenu();case 11:case"end":return s.stop()}},s,a)}))()},handleSelect:function(e){this.selectIndex=e,this.selectMenu=this.menuOptions[e]},handleDelete:function(e,t){var a=this;return i()(l.a.mark(function s(){var r;return l.a.wrap(function(s){for(;;)switch(s.prev=s.next){case 0:return s.prev=0,s.next=3,Object(p.h)(t.item_id);case 3:if(1!=(r=s.sent).status){s.next=9;break}a.$message({type:"success",message:"删除食品成功"}),a.tableData.splice(e,1),s.next=10;break;case 9:throw new Error(r.message);case 10:s.next=16;break;case 12:s.prev=12,s.t0=s.catch(0),a.$message({type:"error",message:s.t0.message}),console.log("删除食品失败");case 16:case"end":return s.stop()}},s,a,[[0,12]])}))()},handleServiceAvatarScucess:function(e,t){1==e.status?this.selectTable.image_path=e.image_path:this.$message.error("上传图片失败！")},beforeAvatarUpload:function(e){var t="image/jpeg"===e.type||"image/png"===e.type,a=e.size/1024/1024<2;return t||this.$message.error("上传头像图片只能是 JPG 格式!"),a||this.$message.error("上传头像图片大小不能超过 2MB!"),t&&a},updateFood:function(){var e=this;return i()(l.a.mark(function t(){var a,s,n;return l.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return e.dialogFormVisible=!1,t.prev=1,a={new_category_id:e.selectMenu.value,specs:e.specs},s=r()({},e.selectTable,a),t.next=6,Object(p.F)(s);case 6:1==(n=t.sent).status?(e.$message({type:"success",message:"更新食品信息成功"}),e.getFoods()):e.$message({type:"error",message:n.message}),t.next=13;break;case 10:t.prev=10,t.t0=t.catch(1),console.log("更新餐馆信息失败",t.t0);case 13:case"end":return t.stop()}},t,e,[[1,10]])}))()}}},d={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"fillcontain"},[a("head-top"),e._v(" "),a("div",{staticClass:"table_container"},[a("el-table",{staticStyle:{width:"100%"},attrs:{data:e.tableData,"expand-row-keys":e.expendRow,"row-key":function(e){return e.index}},on:{expand:e.expand}},[a("el-table-column",{attrs:{type:"expand"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-form",{staticClass:"demo-table-expand",attrs:{"label-position":"left",inline:""}},[a("el-form-item",{attrs:{label:"食品名称"}},[a("span",[e._v(e._s(t.row.name))])]),e._v(" "),a("el-form-item",{attrs:{label:"餐馆名称"}},[a("span",[e._v(e._s(t.row.restaurant_name))])]),e._v(" "),a("el-form-item",{attrs:{label:"食品 ID"}},[a("span",[e._v(e._s(t.row.item_id))])]),e._v(" "),a("el-form-item",{attrs:{label:"餐馆 ID"}},[a("span",[e._v(e._s(t.row.restaurant_id))])]),e._v(" "),a("el-form-item",{attrs:{label:"食品介绍"}},[a("span",[e._v(e._s(t.row.description))])]),e._v(" "),a("el-form-item",{attrs:{label:"餐馆地址"}},[a("span",[e._v(e._s(t.row.restaurant_address))])]),e._v(" "),a("el-form-item",{attrs:{label:"食品评分"}},[a("span",[e._v(e._s(t.row.rating))])]),e._v(" "),a("el-form-item",{attrs:{label:"食品分类"}},[a("span",[e._v(e._s(t.row.category_name))])]),e._v(" "),a("el-form-item",{attrs:{label:"月销量"}},[a("span",[e._v(e._s(t.row.month_sales))])])],1)]}}])}),e._v(" "),a("el-table-column",{attrs:{label:"食品名称",prop:"name"}}),e._v(" "),a("el-table-column",{attrs:{label:"食品介绍",prop:"description"}}),e._v(" "),a("el-table-column",{attrs:{label:"评分",prop:"rating"}}),e._v(" "),a("el-table-column",{attrs:{label:"操作",width:"160"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-button",{attrs:{size:"small"},on:{click:function(a){return e.handleEdit(t.row)}}},[e._v("编辑")]),e._v(" "),a("el-button",{attrs:{size:"small",type:"danger"},on:{click:function(a){return e.handleDelete(t.$index,t.row)}}},[e._v("删除")])]}}])})],1),e._v(" "),a("div",{staticClass:"Pagination"},[a("el-pagination",{attrs:{"current-page":e.currentPage,"page-size":20,layout:"total, prev, pager, next",total:e.count},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}})],1),e._v(" "),a("el-dialog",{attrs:{title:"修改食品信息"},model:{value:e.dialogFormVisible,callback:function(t){e.dialogFormVisible=t},expression:"dialogFormVisible"}},[a("el-form",{attrs:{model:e.selectTable}},[a("el-form-item",{attrs:{label:"食品名称","label-width":"100px"}},[a("el-input",{attrs:{"auto-complete":"off"},model:{value:e.selectTable.name,callback:function(t){e.$set(e.selectTable,"name",t)},expression:"selectTable.name"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"食品介绍","label-width":"100px"}},[a("el-input",{model:{value:e.selectTable.description,callback:function(t){e.$set(e.selectTable,"description",t)},expression:"selectTable.description"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"食品分类","label-width":"100px"}},[a("el-select",{attrs:{placeholder:e.selectMenu.label},on:{change:e.handleSelect},model:{value:e.selectIndex,callback:function(t){e.selectIndex=t},expression:"selectIndex"}},e._l(e.menuOptions,function(e){return a("el-option",{key:e.value,attrs:{label:e.label,value:e.index}})}),1)],1),e._v(" "),a("el-form-item",{attrs:{label:"食品图片","label-width":"100px"}},[a("el-upload",{staticClass:"avatar-uploader",attrs:{action:e.baseUrl+"/v1/addimg/food","show-file-list":!1,"on-success":e.handleServiceAvatarScucess,"before-upload":e.beforeAvatarUpload}},[e.selectTable.image_path?a("img",{staticClass:"avatar",attrs:{src:e.baseImgPath+e.selectTable.image_path}}):a("i",{staticClass:"el-icon-plus avatar-uploader-icon"})])],1)],1),e._v(" "),a("el-row",{staticStyle:{overflow:"auto","text-align":"center"}},[a("el-table",{staticStyle:{"margin-bottom":"20px"},attrs:{data:e.specs,"row-class-name":e.tableRowClassName}},[a("el-table-column",{attrs:{prop:"specs",label:"规格"}}),e._v(" "),a("el-table-column",{attrs:{prop:"packing_fee",label:"包装费"}}),e._v(" "),a("el-table-column",{attrs:{prop:"price",label:"价格"}}),e._v(" "),a("el-table-column",{attrs:{label:"操作"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-button",{attrs:{size:"small",type:"danger"},on:{click:function(a){return e.deleteSpecs(t.$index)}}},[e._v("删除")])]}}])})],1),e._v(" "),a("el-button",{staticStyle:{"margin-bottom":"10px"},attrs:{type:"primary"},on:{click:function(t){e.specsFormVisible=!0}}},[e._v("添加规格")])],1),e._v(" "),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){e.dialogFormVisible=!1}}},[e._v("取 消")]),e._v(" "),a("el-button",{attrs:{type:"primary"},on:{click:e.updateFood}},[e._v("确 定")])],1)],1),e._v(" "),a("el-dialog",{attrs:{title:"添加规格"},model:{value:e.specsFormVisible,callback:function(t){e.specsFormVisible=t},expression:"specsFormVisible"}},[a("el-form",{attrs:{rules:e.specsFormrules,model:e.specsForm}},[a("el-form-item",{attrs:{label:"规格","label-width":"100px",prop:"specs"}},[a("el-input",{attrs:{"auto-complete":"off"},model:{value:e.specsForm.specs,callback:function(t){e.$set(e.specsForm,"specs",t)},expression:"specsForm.specs"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"包装费","label-width":"100px"}},[a("el-input-number",{attrs:{min:0,max:100},model:{value:e.specsForm.packing_fee,callback:function(t){e.$set(e.specsForm,"packing_fee",t)},expression:"specsForm.packing_fee"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"价格","label-width":"100px"}},[a("el-input-number",{attrs:{min:0,max:1e4},model:{value:e.specsForm.price,callback:function(t){e.$set(e.specsForm,"price",t)},expression:"specsForm.price"}})],1)],1),e._v(" "),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){e.specsFormVisible=!1}}},[e._v("取 消")]),e._v(" "),a("el-button",{attrs:{type:"primary"},on:{click:e.addspecs}},[e._v("确 定")])],1)],1)],1)],1)},staticRenderFns:[]};var f=a("VU/8")(m,d,!1,function(e){a("Y+5+")},null,null);t.default=f.exports}});
//# sourceMappingURL=17.4a74f66e85c190503866.js.map