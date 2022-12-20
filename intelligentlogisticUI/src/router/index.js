
import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const login = r => require.ensure([], () => r(require('@/page/login')), 'login')
const manage = r => require.ensure([], () => r(require('@/page/manage')), 'manage')
const home = r => require.ensure([], () => r(require('@/page/home')), 'home')
const addShop = r => require.ensure([], () => r(require('@/page/addShop')), 'addShop')
const addGoods = r => require.ensure([], () => r(require('@/page/addGoods')), 'addGoods')
const userList = r => require.ensure([], () => r(require('@/page/userList')), 'userList')
const shopList = r => require.ensure([], () => r(require('@/page/shopList')), 'shopList')
const foodList = r => require.ensure([], () => r(require('@/page/foodList')), 'foodList')
const orderList = r => require.ensure([], () => r(require('@/page/orderList')), 'orderList')
const adminList = r => require.ensure([], () => r(require('@/page/adminList')), 'adminList')
const visitor = r => require.ensure([], () => r(require('@/page/visitor')), 'visitor')
const newMember = r => require.ensure([], () => r(require('@/page/newMember')), 'newMember')
const uploadImg = r => require.ensure([], () => r(require('@/page/uploadImg')), 'uploadImg')
const vueEdit = r => require.ensure([], () => r(require('@/page/vueEdit')), 'vueEdit')
const adminSet = r => require.ensure([], () => r(require('@/page/adminSet')), 'adminSet')
const sendMessage = r => require.ensure([], () => r(require('@/page/sendMessage')), 'sendMessage')
const explain = r => require.ensure([], () => r(require('@/page/explain')), 'explain')
const dataset_list = r => require.ensure([], () => r(require('@/page/dataset_list')), 'dataset_list_v')
const single_predict = r => require.ensure([], () => r(require('@/page/single_predict')), 'single_predict')
const single_image_predict = r => require.ensure([], () => r(require('@/page/single_image_predict')), 'single_image_predict')
const warehouseLocation = r => require.ensure([], () => r(require('@/page/warehouseLocation')), 'warehouseLocation')
const routePlan = r => require.ensure([], () => r(require('@/page/routePlan')), 'routePlan')
const practice = r=> require.ensure([], () => r(require('@/page/practice')), 'practice')
const practice2 = r=> require.ensure([], () => r(require('@/page/practice2')), 'practice2')
const routes = [
  // {
  //   path: '/',
  //   component: login
  // },
  {
    path: '/',
    component: manage,
    name: '',
    children: [
      {
        path: '',
        component: home,
        meta: []
      },
        {
        path: '/routePlan',
            component: routePlan
      },
      {
        path: '/warehouseLocation',
        component: warehouseLocation
      // meta: ['添加数据', '添加商铺'],
      },
        {
        path: '/practice',
        component: practice
        }
      ,
        {
            path: '/practice2',
            component: practice2
        }
        ,
        {
        path: '/single_image_predict',
        component: single_image_predict
      // meta: ['添加数据', '添加商铺'],
      },
      {
        path: '/addShop',
        component: addShop,
        meta: ['添加数据', '添加商铺']
      }, {
        path: '/addGoods',
        component: addGoods,
        meta: ['添加数据', '添加商品']
      }, {
        path: '/userList',
        component: userList,
        meta: ['数据管理', '用户列表']
      }, {
        path: '/shopList',
        component: shopList,
        meta: ['数据管理', '商家列表']
      }, {
        path: '/foodList',
        component: foodList,
        meta: ['数据管理', '食品列表']
      }, {
        path: '/orderList',
        component: orderList,
        meta: ['数据管理', '订单列表']
      }, {
        path: '/adminList',
        component: adminList,
        meta: ['数据管理', '管理员列表']
      }, {
        path: '/visitor',
        component: visitor,
        meta: ['图表', '用户分布']
      }, {
        path: '/newMember',
        component: newMember,
        meta: ['图表', '用户数据']
      }, {
        path: '/uploadImg',
        component: uploadImg,
        meta: ['文本编辑', 'MarkDown']
      }, {
        path: '/vueEdit',
        component: vueEdit,
        meta: ['编辑', '文本编辑']
      }, {
        path: '/adminSet',
        component: adminSet,
        meta: ['设置', '管理员设置']
      }, {
        path: '/sendMessage',
        component: sendMessage,
        meta: ['设置', '发送通知']
      }, {
        path: '/explain',
        component: explain,
        meta: ['说明', '说明']
      }, {
        path: '/dataset_list',
        component: dataset_list
      }
    ]
  }
]

export default new Router({
  routes,
  strict: process.env.NODE_ENV !== 'production'
})
