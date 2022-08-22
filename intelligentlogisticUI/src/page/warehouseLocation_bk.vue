<template>
    <div class="mixin-components-container">
        <uyhj class="content-container">
            <!-- 图片上传控件-->
            <el-row  :gutter="20">
                <el-col span="16" style="background-color: white">
                    <div class="home">
                        <div class="echarts_map" ref="charts"></div>
                    </div>
                </el-col>
<!--                <el-col span="12" style="background-color:blue">-->
                <el-col span="8" style="background-color: #E9EEF3" >
                    <el-form :model="formData1">
                            <el-tag>分仓选址</el-tag>
                            <el-divider content-position="right"></el-divider>
                            <el-tag>导入需求点：</el-tag>
                            <el-button>导入文件</el-button>
                            <el-button>下载模板</el-button>
                            <el-button>需求点.xlsx</el-button>
                            <el-button>删除文件</el-button>
                            <el-form-item label="新建仓数量" prop="newWarehouseLocationNumber">
                                <el-input v-model="formData1.name"></el-input>
                            </el-form-item>
                            <el-button>高级配置</el-button>
                            <el-button>开始计算</el-button>
                    </el-form>
                    <el-form :model="formData2">
                        <el-tag>获取时限</el-tag>
                        <el-divider content-position="right"></el-divider>
                        <el-button>获取时限</el-button>
                    </el-form>
                </el-col>
            </el-row>

        </uyhj>

    </div>
</template>

<script>
import headTop from '@/components/headTop'
// eslint-disable-next-line no-unused-vars
import {cityGuess, addShop, searchplace, foodCategory} from '@/api/getData'
import {baseUrl, baseImgPath} from '@/config/env'
import * as echarts from "echarts"
import {getMap} from "../utils/maputil"
export default {
  data () {
    return {
      baseUrl,
      baseImgPath,
      isShowUpload: true,
      isShowImgUpload: false,
      localUrl: '',
        formData1: {
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
      this.initCharts()
  },
  methods: {
      initCharts() {
          console.log("进入initCharts")
          const charts = echarts.init(this.$refs["charts"]);
          const option = {
              backgroundColor: "#404a59", // 背景颜色
              tooltip: {// 提示浮窗样式
                  show: true,
                  trigger: "item",
                  alwaysShowContent: false,
                  backgroundColor: "#0C121C",
                  borderColor: "rgba(0, 0, 0, 0.16);",
                  hideDelay: 100,
                  triggerOn: "mousemove",
                  enterable: true,
                  textStyle: {
                      color: "#DADADA",
                      fontSize: "12",
                      width: 20,
                      height: 30,
                      overflow: "break",
                  },
                  showDelay: 100,
                  // formatter(params) {  //series中第二种数据样式时需要加这部分
                  //     return `地区：${params.name}</br>数值：${params.value[2]}`;
                  // }
              },
              // 地图配置
              geo: {
                  map: "china",
                  label: {
                      // 通常状态下的样式
                      normal: {
                          show: true,
                          textStyle: {
                              color: "#fff",
                          },
                      },
                      // 鼠标放上去的样式
                      emphasis: {
                          textStyle: {
                              color: "#fff",
                          },
                      },
                  },
                  // 地图区域的样式设置
                  itemStyle: {
                      normal: {
                          borderColor: "rgba(147, 235, 248, 1)",
                          borderWidth: 1,
                          areaColor: {
                              type: "radial",
                              x: 0.5,
                              y: 0.5,
                              r: 0.8,
                              colorStops: [
                                  {
                                      offset: 0,
                                      color: "rgba(147, 235, 248, 0)", // 0% 处的颜色
                                  },
                                  {
                                      offset: 1,
                                      color: "rgba(147, 235, 248, .2)", // 100% 处的颜色
                                  },
                              ],
                              globalCoord: false, // 缺省为 false
                          },
                          shadowColor: "rgba(128, 217, 248, 1)",
                          shadowOffsetX: -2,
                          shadowOffsetY: 2,
                          shadowBlur: 10,
                      },
                      // 鼠标放上去高亮的样式
                      emphasis: {
                          areaColor: "#389BB7",
                          borderWidth: 0,
                      },
                  },
              },
              graphic: [
                  {
                      type: "text",
                      left: "10%",
                      top: "10%",
                      style: {
                          text: "中国",
                          font: 'bolder 1.5rem "Microsoft YaHei", sans-serif',
                          fill: "#fff",
                      },
                  },
              ],
              series: [
                  // { //第一种数据展示样式
                  //   type: "scatter",
                  //   coordinateSystem: "geo",
                  //   symbol: "pin",
                  //   legendHoverLink: true,
                  //   symbolSize: [60, 60],
                  //   // 这里渲染标志里的内容以及样式
                  //   label: {
                  //     show: true,
                  //     formatter(value) {
                  //       return value.data.value[2];
                  //     },
                  //     color: "#fff",
                  //   },
                  //   // 标志的样式
                  //   itemStyle: {
                  //     normal: {
                  //       color: "rgba(255,0,0,.7)",
                  //       shadowBlur: 2,
                  //       shadowColor: "D8BC37",
                  //     },
                  //   },
                  //   // 数据格式，其中name,value是必要的，value的前两个值是数据点的经纬度，其他的数据格式可以自定义
                  //   // 至于如何展示，完全是靠上面的formatter来自己定义的
                  //   data: [
                  //     { name: "西藏", value: [91.23, 29.5, 2333] },
                  //     { name: "黑龙江", value: [128.03, 47.01, 1007] },
                  //   ],
                  //   showEffectOn: "render",
                  //   rippleEffect: {
                  //     brushType: "stroke",
                  //   },
                  //   hoverAnimation: true,
                  //   zlevel: 1,
                  // },
                  { //第二种数据展示样式
                      type: "effectScatter",
                      coordinateSystem: "geo",
                      effectType: "ripple",
                      showEffectOn: "render",
                      rippleEffect: {
                          period: 10,
                          scale: 10,
                          brushType: "fill",
                      },

                      hoverAnimation: true,
                      itemStyle: {
                          normal: {
                              // color: "rgba(255, 235, 59, .7)",
                              color: "rgba(255,0,0,.7)",
                              shadowBlur: 10,
                              shadowColor: "#333",
                          },
                      },
                      zlevel: 1,
                      data: [
                          {name: "西藏", value: [91.23, 29.5, 2333]},
                          {name: "黑龙江", value: [128.03, 47.01, 1007]},
                      ],
                  },
                  
              ],
              // visualMap: {
              //   // 是否展示左下角，即是是false，也仅是不显示，不影响数据的映射
              //   show: true,
              //   // 上下端文字
              //   text: ["高", "低"],
              //   // 最小值和最大值，必须指定
              //   min: 0,
              //   max: 6000,
              //   // 位置
              //   left: "10%",
              //   bottom: "10%",
              //   // 是否展示滑块
              //   calculable: true,
              //   // 指定映射的数据，对应的是option.series，这里根据自己的实际需要进行配置
              //   seriesIndex: [0],
              //   // 从下到上的颜色
              //   inRange: {
              //     color: ['#00467F', '#A5CC82'],
              //   },
              //   //字体颜色
              //   textStyle: {
              //     color: "#fff",
              //     map: "china",
              //   },
              // },

          };
          // 不传name默认会返回中国地图
          const [mapName, mapJson] = getMap();
          console.log(mapName, mapJson)

          option.geo.map = mapName;
          // 地图注册，第一个参数的名字必须和option.geo.map一致
          echarts.registerMap(mapName, mapJson);
          charts.setOption(option);
          charts.off() // 防止graph里频繁添加click事件，在添加click事件之前先全部清空掉
          // charts.on("click", ({ name }) => {
          //     console.log(name);
          //     // 如果option.graphic里已经有了城市名称，则不进行任何操作，防止频繁点击
          //     const index = option.graphic.findIndex(i => i.style.text === name);
          //     if (!name || index !== -1) return
          //     // 这里和上面一样，其实还可以再优化一下。为了方便阅读，这里不再封装。
          //     const [mapName, mapJson] = getMap(name);
          //     option.geo.zoom = 0.8;
          //     option.geo.map = mapName;
          //     //水印显示
          //     // 为了重新定位，这里使用了length
          //     const idx = option.graphic.length + 1;
          //     option.graphic.push({
          //         type: "text",
          //         left: `${idx * 10}%`,
          //         top: "10%",
          //         style: {
          //             text: name,
          //             font: 'bolder 1.5rem "Microsoft YaHei", sans-serif',
          //             fill: "#fff",
          //         },
          //         onclick: () => {
          //             // 利用函数的作用域，可以直接拿上面的name来用
          //             const [grahpName, graphJson] = getMap(name);
          //             const index = option.graphic.findIndex(i => i.style.text === name);
          //             // 点击元素之后的所有元素全部删除
          //             option.graphic.splice(index + 1);
          //             // 很多操作重复了，你可以将公共部分抽离出来
          //             option.geo.map = mapName;
          //             echarts.registerMap(grahpName, graphJson);
          //             charts.setOption(option, true);
          //         },
          //     });
          //     echarts.registerMap(mapName, mapJson);
          //     charts.setOption(option, true);
          // });
      },
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
        .echarts_map{
            width: 1000px;
            height: 800px;
            border: 1px solid red;
        }
    }
</style>
