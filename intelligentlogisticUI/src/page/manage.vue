
<template>
    <div class="manage_page fillcontain">
        <el-row style="height: 100%;">
            <el-col :span="4"  style="min-height: 100%; background-color: #324057;">
                <el-menu :default-active="defaultActive" style="min-height: 100%;" theme="dark" router>
                    <el-menu-item index="/"><i class="el-icon-menu"></i>首页</el-menu-item>
<!--                        <el-submenu index="2">-->
<!--                            <template slot="title"><i class="el-icon-document"></i>数据管理</template>-->
<!--                            <el-menu-item index="userList">用户列表</el-menu-item>-->
<!--                            <el-menu-item index="shopList">商家列表</el-menu-item>-->
<!--                            <el-menu-item index="foodList">食品列表</el-menu-item>-->
<!--                            <el-menu-item index="orderList">订单列表</el-menu-item>-->
<!--                            <el-menu-item index="adminList">管理员列表</el-menu-item>-->
<!--                        </el-submenu>-->
<!--                        <el-submenu index="3">-->
<!--                            <template slot="title"><i class="el-icon-plus"></i>添加数据</template>-->
<!--                            <el-menu-item index="addShop">添加商铺</el-menu-item>-->
<!--                            <el-menu-item index="addGoods">添加商品</el-menu-item>-->
<!--                        </el-submenu>-->
<!--                        <el-submenu index = "8">-->
<!--                            <template slot="title"><i class ="el-icon-arrow-up">数据集模块</i></template>-->
<!--                            <el-menu-item index="dataset_list">数据集列表</el-menu-item>-->
<!--                            <el-menu-item index="dataset_add">新增数据集</el-menu-item>-->
<!--                            <el-menu-item index="dataset_delete">删除数据集</el-menu-item>-->
<!--                        </el-submenu>-->
<!--                        <el-submenu index="9">-->
<!--                            <template slot="title"><i class ="el-icon-arrow-up">模型中心模块</i></template>-->
<!--                            <el-menu-item index="result">模型列表</el-menu-item>-->
<!--                        </el-submenu>-->
<!--                        <el-submenu index = "10">-->
<!--                            <template slot="title"><i class ="el-icon-arrow-up">预测模块</i></template>-->
<!--                            <el-menu-item index="single_image_predict">提交OCR预测任务</el-menu-item>-->
<!--                            <el-menu-item index="batch_predict">提交批量OCR预测任务</el-menu-item>-->
<!--                            <el-menu-item index="result">查看批量OCR预测结果</el-menu-item>-->
<!--                        </el-submenu>-->
                        <el-submenu index = "11">
                            <template slot="title"><i class ="el-icon-arrow-up">分仓选址</i></template>
                            <el-menu-item index="warehouseLocation">智能仓预测</el-menu-item>
                            <el-menu-item index="routePlan">线路规划</el-menu-item>
                        </el-submenu>
                </el-menu>
            </el-col>
            <el-col :span="20" style="height: 100%;overflow: auto;">
                <keep-alive>
                    <router-view></router-view>
                </keep-alive>
            </el-col>
        </el-row>
    </div>
</template>

<script>
export default {
  computed: {
    defaultActive: function () {
      return this.$route.path.replace('/', '')
    }
  }
}
</script>

<style lang="less" scoped>
	@import '../style/mixin';
    .manage_page{

    }
</style>
