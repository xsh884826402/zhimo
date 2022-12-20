import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store/'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// import VueAMap from 'vue-amap'
// import {lazyAMapApiLoaderInstance} from 'vue-amap'
//
// Vue.config.productionTip = false
Vue.use(ElementUI)
// Vue.use(VueAMap)
// VueAMap.initAMapApiLoader({
//     key: '6cb06f76509c53d2afa3f320d924ec30',
//     plugin: ['AMap.Autocomplete', 'AMap.PlaceSearch', 'AMap.Scale', 'AMap.OverView', 'AMap.ToolBar', 'AMap.MapType', 'AMap.PolyEditor', 'AMap.CircleEditor', 'AMap.Driving'],
//     v: '1.4.4'
//
// })
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})
