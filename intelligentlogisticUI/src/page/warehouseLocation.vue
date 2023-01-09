<template>
    <div class="mixin-components-container">
        <div class="content-container">
            <!-- 图片上传控件-->
            <el-row  :gutter="20">
                <el-col span=16 style="background-color: white">
                    <div class="home">
<!--                        <div class="echarts_map" ref="charts"></div>-->
                        <div id="container"></div>
                    </div>
                </el-col>

<!--                <el-col span="12" style="background-color:blue">-->
<!--                :file-list="fileList"-->
                <el-col span=8 style="background-color: #E9EEF3" >
                    <el-form :model="formData1">
<!--                            <el-tag >分仓选址</el-tag>-->
                            <el-divider content-position="center">分仓选址</el-divider>
                            <el-tag>导入需求点和指定仓：</el-tag>
                            <el-upload
                                class="upload-demo"
                                ref="uploadWarehouseData"
                                action="http://127.0.0.1:5000/upload/warehouseData"
                                :auto-upload="false">
                                <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
                                <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
                                <div slot="tip" class="el-upload__tip">请根据模板填写输入信息上</div>
                            </el-upload>
                            <el-button @click="getInputTemplate">下载模板</el-button>
<!--                            <el-button>删除文件</el-button>-->
                            <el-form-item label="新建仓数量" prop="newWarehouseLocationNumber">
                                <el-input v-model="formData1.warehouseLocationNumber" type="number" :min="1" ></el-input>
                            </el-form-item>
                            <el-form-item label="是否指定仓">
                                <el-radio-group v-model="formData1.specWarehouse">
                                    <el-radio label="指定仓"></el-radio>
                                    <el-radio label="不指定仓"></el-radio>
                                </el-radio-group>
                            </el-form-item>
                            <el-dialog
                                title="提示"
                                :visible.sync="dialog1Visible"
                                width="30%"
                                :before-close="handleClose">
<!--                                <span>这是一段信息</span>-->
                                <span slot="footer" class="dialog-footer">
                                    <el-form-item label="分仓选址算法">
                                        <el-radio-group v-model="formData1.algori">
                                            <el-radio label="综合最优"></el-radio>
                                            <el-radio label="运算最快"></el-radio>
                                            <el-radio label="效果最优"></el-radio>
                                        </el-radio-group>
                                    </el-form-item>
                                    <el-form-item label="是否需要获取经纬度">
                                        <el-radio-group v-model="formData1.needgetJingWeiDu">
                                            <el-radio label="需要"></el-radio>
                                            <el-radio label="不需要"></el-radio>
                                        </el-radio-group>
                                    </el-form-item>
                                <el-button @click="cancleHighLevelConfig">取 消</el-button>
                                <el-button type="primary" @click="dialog1Visible = false">确 定</el-button>
                                </span>
                            </el-dialog>
                            <el-button @click="dialog1Visible = true">高级配置</el-button>
                            <el-dialog
                                title="提示"
                                :visible.sync="dialog2Visible"
                                width="30%"
                                :before-close="handleClose"
                            >
                                <span>模型计算中，请等待</span>
                            </el-dialog>
                            <el-button @click="submitForm('formData1')">开始计算</el-button>
                    </el-form>
                    <el-form :model="formData2">
<!--                        <el-tag>获取时限</el-tag>-->
                        <el-divider content-position="center">获取时限</el-divider>
                        <el-button @click="submitgetTimeLimit">开始获取时限</el-button>
                    </el-form>
                </el-col>
            </el-row>

        </div>

    </div>
</template>

<script  >
import headTop from '@/components/headTop'
// eslint-disable-next-line no-unused-vars
import {cityGuess, postWarehouseLocation,addShop, searchplace, foodCategory, getTimeLimit} from '@/api/getData'
import {baseUrl, baseImgPath} from '@/config/env'
import * as echarts from "echarts"
// import 'echarts/extension/bmap/bmap'
import {getMap} from "../utils/maputil"
import axios from "axios"
import AMapLoader from '@amap/amap-jsapi-loader'
export default {
  data () {
    return {
      echarts_data: [{'coords': [[117.0274, 36.67486], [116.407526, 39.90403]]}, {'coords': [[116.4134, 39.91092], [116.407526, 39.90403]]}, {'coords': [[114.5366, 38.0432], [116.407526, 39.90403]]}, {'coords': [[123.4888, 41.68465], [116.407526, 39.90403]]}, {'coords': [[112.5694, 37.87983], [116.407526, 39.90403]]}, {'coords': [[126.565, 45.77849], [116.407526, 39.90403]]}, {'coords': [[117.2081, 39.0911], [116.407526, 39.90403]]}, {'coords': [[126.5556, 43.84357], [116.407526, 39.90403]]}, {'coords': [[111.6723, 40.81774], [116.407526, 39.90403]]}, {'coords': [[113.2724, 23.13795], [113.676994, 22.906861]]}, {'coords': [[112.9896, 28.11827], [113.676994, 22.906861]]}, {'coords': [[108.3345, 22.82127], [113.676994, 22.906861]]}, {'coords': [[110.3555, 20.0258], [113.676994, 22.906861]]}, {'coords': [[113.7594, 34.77171], ['118.41597379136614', '31.55455993943438']]}, {'coords': [[118.7696, 32.06678], ['118.41597379136614', '31.55455993943438']]}, {'coords': [[120.1595, 30.27155], ['118.41597379136614', '31.55455993943438']]}, {'coords': [[121.4805, 31.23593], ['118.41597379136614', '31.55455993943438']]}, {'coords': [[119.2701, 26.09064], ['118.41597379136614', '31.55455993943438']]}, {'coords': [[114.3484, 30.5516], ['118.41597379136614', '31.55455993943438']]}, {'coords': [[117.3305, 31.73429], ['118.41597379136614', '31.55455993943438']]}, {'coords': [[115.9154, 28.68169], ['118.41597379136614', '31.55455993943438']]}, {'coords': [[104.0735, 30.57754], ['104.07382049859993', '30.577546681135527']]}, {'coords': [[108.9604, 34.27581], ['104.07382049859993', '30.577546681135527']]}, {'coords': [[102.7164, 25.05156], ['104.07382049859993', '30.577546681135527']]}, {'coords': [[106.5584, 29.569], ['104.07382049859993', '30.577546681135527']]}, {'coords': [[106.6797, 26.62223], ['104.07382049859993', '30.577546681135527']]}, {'coords': [[103.8325, 36.06546], ['104.07382049859993', '30.577546681135527']]}, {'coords': [[87.63347, 43.79924], ['104.07382049859993', '30.577546681135527']]}, {'coords': [[103.8672, 36.02628], ['104.07382049859993', '30.577546681135527']]}, {'coords': [[101.7798, 36.64578], ['104.07382049859993', '30.577546681135527']]}, {'coords': [[91.16703, 29.62534], ['104.07382049859993', '30.577546681135527']]}],
      // echarts_data: [],
        dialog1Visible: false,
        dialog2Visible: false,
      baseUrl,
      baseImgPath,
      isShowUpload: true,
      isShowImgUpload: false,
      localUrl: '',
        formData1: {
            warehouseLocationNumber: 4,
            specWarehouse: '不指定仓',
            algori: "综合最优",
            needgetJingWeiDu: "需要"
        },
        formData2: {
            name: '', // 店铺名称
            address: '', // 地址
            latitude: '',
            longitude: '',
            description: '', // 介绍
            phone: '',
            promotion_info: '',
            float_delivery_fee: 5, // 运费
            float_minimum_order_amount: 20, // 起价
            is_premium: true,
            delivery_mode: true,
            new: true,
            bao: true,
            zhun: true,
            piao: true,
            startTime: '',
            endTime: '',
            image_path: '',
            business_license_image: '',
            catering_service_license_image: ''

        },
        rules: {
            name: [
                { required: true, message: '请输入店铺名称', trigger: 'blur' }
            ],
            address: [
                { required: true, message: '请输入详细地址', trigger: 'blur' }
            ],
            phone: [
                { required: true, message: '请输入联系电话' },
                { type: 'number', message: '电话号码必须是数字' }
            ]
        },
    }
  },
  components: {
    headTop
  },
  mounted () {
    this.initData(),
      // this.initCharts(this.echarts_data)
      this.initAMap1(this.echarts_data)
      console.info('after initAmap, debug xsh',)

  },
  methods: {
      initAMap1(data) {
          const that = this
          console.info('in initMap 分仓选址')
          console.info(data)
          AMapLoader.load({
              key: 'c84f72f82ba9a3d7b0c8f38e22271811',  //设置您的key
              version: "2.0",
              plugins: ['AMap.ToolBar', 'AMap.Driving','AMap.DistrictSearch'],
              AMapUI: {
                  version: "1.1",
                  plugins: [],

              },
              Loca: {
                  version: "2.0"
              },
          }).then((AMap) => {

              var countyInfo = {'name': '济南市', 'centerGeoCoord': [117.000923, 36.675807]}
              const colorList = [
                  '#FF00FF',
                  '#4B0082',
                  '#FF0000',
                  '#0000FF',
                  '#006400',
                  '#A36462',
                  '#C96457',
                  '#00C957',
                  '#A52A2A',
                  '#DC143C',
                  '#082E54',
                  '#D2B48C',
                  '#00FFFF',
                  '#292421',
                  '#FFFF00'
              ]
              var routes = {
                  '济南仓': [
                      [
                          {'name': '济南仓', 'geoCoord': [117.2187, 36.65717] },
                          {'name': 'BB60', 'geoCoord': [116.9677, 36.64082] },
                          {'name': 'BB8A', 'geoCoord': [116.455335, 36.288724] },
                          {'name': 'BB8B', 'geoCoord': [116.447678, 36.273443] },
                          {'name': 'BB04', 'geoCoord': [117.0742, 36.64804] },
                          {'name': 'BB43', 'geoCoord': [117.095027, 36.669696] },
                          // {"name": 'BB43',"geoCoord":[117.0950277, 36.66969639] },
                          {'name': '济南仓', 'geoCoord': [117.2187, 36.65717] }
                      ]
                  ]
              }
              var opts = {
                  subdistrict: 0,
                  extensions: 'all',
                  level: 'city'
              }
              var map = new AMap.Map('container', {
                  resizeEnable: false,
                  zoom:7,
                  center: countyInfo['centerGeoCoord']
              })
              // #[117.0274, 36.67486], [116.407526, 39.90403]
              for (var line in data){
                  // console.log('line', data[line]['coords'])
                  var source = data[line]['coords'][0]
                  var target = data[line]['coords'][1]
                  var path = [new AMap.LngLat(source[0], source[1]), new AMap.LngLat(target[0], target[1])]
                  console.log('line', path)
                  var polyline = new AMap.Polyline({
                      path: path,
                      geodesic: true
                  })
                  map.add(polyline)
              }

              // var path = [new AMap.LngLat(117.0274, 36.67486), new AMap.LngLat(116.407526, 39.90403)]
              // var polyline = new AMap.Polyline({
              //     path: path,
              //     geodesic: true
              // })
              // // polyline.setOption()
              // map.add(polyline)
              that.map = map

              this.map = map

          }).catch(e => {
              console.log(e);
          })
      },

      // initCharts(echarts_data ) {
      //     console.log("进入initCharts")
      //     const charts = echarts.init(this.$refs["charts"]);
      //     const option = {
      //         backgroundColor: "#404a59", // 背景颜色
      //         tooltip: {// 提示浮窗样式
      //             show: true,
      //             trigger: "item",
      //             alwaysShowContent: false,
      //             backgroundColor: "#0C121C",
      //             borderColor: "rgba(0, 0, 0, 0.16);",
      //             hideDelay: 100,
      //             triggerOn: "mousemove",
      //             enterable: true,
      //             textStyle: {
      //                 color: "#DADADA",
      //                 fontSize: "12",
      //                 width: 20,
      //                 height: 30,
      //                 overflow: "break",
      //             },
      //             showDelay: 100,
      //             // formatter(params) {  //series中第二种数据样式时需要加这部分
      //             //     return `地区：${params.name}</br>数值：${params.value[2]}`;
      //             // }
      //         },
      //         // 地图配置
      //         geo: {
      //             zoom: 1,
      //             roam: true,
      //             map: "china",
      //             label: {
      //                 // 通常状态下的样式
      //                 normal: {
      //                     show: true,
      //                     textStyle: {
      //                         color: "#fff",
      //                     },
      //                 },
      //                 // 鼠标放上去的样式
      //                 emphasis: {
      //                     textStyle: {
      //                         color: "#fff",
      //                     },
      //                 },
      //             },
      //             // 地图区域的样式设置
      //             itemStyle: {
      //                 normal: {
      //                     borderColor: "rgba(147, 235, 248, 1)",
      //                     borderWidth: 1,
      //                     areaColor: {
      //                         type: "radial",
      //                         x: 0.5,
      //                         y: 0.5,
      //                         r: 0.8,
      //                         colorStops: [
      //                             {
      //                                 offset: 0,
      //                                 color: "rgba(147, 235, 248, 0)", // 0% 处的颜色
      //                             },
      //                             {
      //                                 offset: 1,
      //                                 color: "rgba(147, 235, 248, .2)", // 100% 处的颜色
      //                             },
      //                         ],
      //                         globalCoord: false, // 缺省为 false
      //                     },
      //                     shadowColor: "rgba(128, 217, 248, 1)",
      //                     shadowOffsetX: -2,
      //                     shadowOffsetY: 2,
      //                     shadowBlur: 10,
      //                 },
      //                 // 鼠标放上去高亮的样式
      //                 emphasis: {
      //                     areaColor: "#389BB7",
      //                     borderWidth: 0,
      //                 },
      //             },
      //         },
      //         graphic: [
      //             {
      //                 type: "text",
      //                 left: "10%",
      //                 top: "10%",
      //                 style: {
      //                     text: "中国",
      //                     font: 'bolder 1.5rem "Microsoft YaHei", sans-serif',
      //                     fill: "#fff",
      //                 },
      //             },
      //         ],
      //         series: [
      //             {
      //                 type: 'lines',
      //                 zlevel: 1,
      //                 symbol: ['none', 'arrow'],
      //
      //                 symbolSize: ['0', '5'],
      //                 linkSymbol: 'arrow',
      //                 effect: {
      //                     show: true,
      //                     period: 6,
      //                     trailLength: 0.7,
      //                     color: '#fff',
      //                     symbolSize: 2
      //                 },
      //                 lineStyle: {
      //                     normal: {
      //                         color: '#F51313',
      //                         width: 0.1,
      //                         curveness: 0.1,
      //                         shadowBlur: 1,
      //                         shadowColor: '#87CFFB'
      //                     }
      //                 },
      //                 data: echarts_data
      //             }
      //
      //         ],
      //
      //     };
      //     // 不传name默认会返回中国地图
      //     const [mapName, mapJson] = getMap();
      //     console.log(mapName, mapJson)
      //
      //     option.geo.map = mapName;
      //     // 地图注册，第一个参数的名字必须和option.geo.map一致
      //     echarts.registerMap(mapName, mapJson);
      //     charts.setOption(option);
      // },
    async initData () {
      try {
        console.log('debug1 \n\n\n\n\n')
      } catch (err) {
        console.log(err)
      }
    },
    imgSaveToUrl (event) {
      // 获取上传图片的本地URL，用于上传前的本地预览
      var URL = null
      if (window.createObjectURL != undefined) {
        // basic
        URL = window.createObjectURL(event.raw)
      } else if (window.URL != undefined) {
        // mozilla(firefox)
        URL = window.URL.createObjectURL(event.raw)
      } else if (window.webkitURL != undefined) {
        // webkit or chrome
        URL = window.webkitURL.createObjectURL(event.raw)
      }
      // 转换后的地址为 blob:http://xxx/7bf54338-74bb-47b9-9a7f-7a7093c716b5
      console.log('url' + URL)
      this.localUrl = URL
      this.isShowImgUpload = true// 呈现本地预览组件
      this.isShowUpload = true// 隐藏上传组件
    },
    processButtonClick () {
      console.log('button click')
      this.$refs.upload.submit()
    },
    handleSuccess (res) {
      console.log('handleSuccess')
      if (res.status === 1) {
        this.message = res.text
      }
    },
    async submitForm (formName) {
        console.log('before submit', formName)
        this.dialog2Visible = true;
        let result =  await postWarehouseLocation(this.formData1)
        if (result.status == 'success') {
            this.dialog2Visible = false;
            this.$message({
                type: 'success',
                message: '计算完成'
            })
        } else {
            this.dialog2Visible = false;
            this.$message({
                type: 'error',
                message: result.message
            })
        }
        this.initCharts(result.map_list)

    },
    submitUpload() {
      this.$refs.uploadWarehouseData.submit();
      this.$refs.uploadWarehouseData.clearFiles();
    },
    async submitgetTimeLimit() {
        const url = 'http://127.0.0.1:5000/getTimeLimit'
        const config = {
            responseType: 'arraybuffer',
            headers: {
            }
        }
        axios.post('http://127.0.0.1:5000/getTimeLimit', {user_id: '1'}, {responseType: 'arraybuffer'}).then(
            res => {
                try {
                    // console.log(res.data)
                    console.log(res.headers.message_dict)
                    var result = JSON.parse(res.headers.message_dict)
                    console.log(result.filename)

                    // let binary = [];
                    // binary.push(res)
                    const blobUrl = window.URL.createObjectURL(new Blob([res.data]))
                    const a = document.createElement('a')
                    a.style.display = 'none'
                    a.download = result.filename
                    a.href = blobUrl
                    a.click()
                    window.URL.revokeObjectURL(blobUrl)
                    // document.body.removeChild(a)
                } catch (e) {
                    console.log(e)
                    alert('保存文件出错')
                }
            }
        )


    },
    async getInputTemplate() {
          // const url = 'http://127.0.0.1:5000/getTimeLimit'
          // const config = {
          //     responseType: 'arraybuffer',
          //     headers: {
          //
          //     }
          // }
          // axios.post(url, config).then(
          //     resp => {
          //         const blob = new Blob([resp.data])
          //     }
          // ).catch(function (error) {
          //     console.log(error)
          // })
          axios.post('http://127.0.0.1:5000/download/inputTemplate', {user_id: '1'}, {responseType: 'arraybuffer'}).then(
              res => {
                  try {
                      // console.log(res.data)
                      console.log(res.headers.message_dict)
                      var result = JSON.parse(res.headers.message_dict)
                      console.log(result.filename)

                      // let binary = [];
                      // binary.push(res)
                      const blobUrl = window.URL.createObjectURL(new Blob([res.data]))
                      const a = document.createElement('a')
                      a.style.display = 'none'
                      a.download = result.filename
                      a.href = blobUrl
                      a.click()
                      window.URL.revokeObjectURL(blobUrl)
                      // document.removeChild(a)
                      // console.log("下载完毕")
                  } catch (e) {
                      console.log("error", e)
                      alert('保存文件出错')
                  }
              }
          )


      },
      cancleHighLevelConfig(){
          this.dialog1Visible = false;
          this.formData1.algori = "综合最优";
          this.formData1.needgetJingWeiDu = "需要";
      }
  }
}
</script>

<style lang="less">
    @import '../style/mixin';
    .button_submit{
        text-align: center;
    }
    .avatar-uploader .el-upload {
        border: 1px dashed #d9d9d9;
        border-radius: 6px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    .avatar-uploader .el-upload:hover {
        border-color: #20a0ff;
    }
    .avatar-uploader-icon {
        font-size: 28px;
        color: #8c939d;
        width: 120px;
        height: 120px;
        line-height: 120px;
        text-align: center;
    }
    .avatar {
        width: 120px;
        height: 120px;
        display: block;
    }
    .el-table .info-row {
        background: #c9e5f5;
    }
    .el-table .positive-row {
        background: #e2f0e4;
    }
    .text-area{
        width: 400px;
        height: 400px;
        overflow: scroll;
    }
    .left-bar {
        float: left;
        width: 20%;
        height: 100%;
        position: absolute;
        overflow: auto;
    }
    .right-bar {
        margin-top: -190px;
        float: right;
        right: 0px;
        width: 50%;
        height: 100%;
        position: absolute;
        overflow: auto;
    }
    .el-aside {
        background-color: #D3DCE6;
        color: #333;
        text-align: center;
        line-height: 200px;
    }

    .el-main {
        background-color: #E9EEF3;
        color: #333;
        text-align: center;
        line-height: 160px;
    }
    .el-row {
        margin-bottom: 20px;
        display: flex;
        flex-wrap: wrap;
        height: 800px;
    }
    .el-divider {
        background-color: #333333;
    }
    .home{
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid yellowgreen;
        #container{
            width: 1000rem;
            height: 50rem;
            border: 1px solid red;
        }
        /*#container {*/
        /*    padding: 0px;*/
        /*    margin: 0px;*/
        /*    width: 100%;*/
        /*    height: 100%;*/
        /*    !*position: absolute;*!*/
        /*}*/
    }
</style>
