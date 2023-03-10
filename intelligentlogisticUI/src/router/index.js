
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
      // meta: ['????????????', '????????????'],
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
      // meta: ['????????????', '????????????'],
      },
      {
        path: '/addShop',
        component: addShop,
        meta: ['????????????', '????????????']
      }, {
        path: '/addGoods',
        component: addGoods,
        meta: ['????????????', '????????????']
      }, {
        path: '/userList',
        component: userList,
        meta: ['????????????', '????????????']
      }, {
        path: '/shopList',
        component: shopList,
        meta: ['????????????', '????????????']
      }, {
        path: '/foodList',
        component: foodList,
        meta: ['????????????', '????????????']
      }, {
        path: '/orderList',
        component: orderList,
        meta: ['????????????', '????????????']
      }, {
        path: '/adminList',
        component: adminList,
        meta: ['????????????', '???????????????']
      }, {
        path: '/visitor',
        component: visitor,
        meta: ['??????', '????????????']
      }, {
        path: '/newMember',
        component: newMember,
        meta: ['??????', '????????????']
      }, {
        path: '/uploadImg',
        component: uploadImg,
        meta: ['????????????', 'MarkDown']
      }, {
        path: '/vueEdit',
        component: vueEdit,
        meta: ['??????', '????????????']
      }, {
        path: '/adminSet',
        component: adminSet,
        meta: ['??????', '???????????????']
      }, {
        path: '/sendMessage',
        component: sendMessage,
        meta: ['??????', '????????????']
      }, {
        path: '/explain',
        component: explain,
        meta: ['??????', '??????']
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
