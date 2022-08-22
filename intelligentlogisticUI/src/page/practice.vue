<template>
    <div class="home">
        <div class="echarts_map" ref="charts"></div>
    </div>
</template>

<script>
    import * as echarts from "echarts";
    import {getMap} from "../utils/maputil";
    export default {
        name: 'Home',
        data(){
            return{

            }
        },
        created () {
            this.$nextTick(() => {
                this.initCharts();
            })
        },
        methods: {
            initCharts() {
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
                        formatter(params) {  //series中第二种数据样式时需要加这部分
                            return `地区：${params.name}</br>数值：${params.value[2]}`;
                        }
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
                        }
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
                option.geo.map = mapName;
                // 地图注册，第一个参数的名字必须和option.geo.map一致
                echarts.registerMap(mapName, mapJson);
                charts.setOption(option);
                charts.off() // 防止graph里频繁添加click事件，在添加click事件之前先全部清空掉
                charts.on("click", ({ name }) => {
                    console.log(name);
                    // 如果option.graphic里已经有了城市名称，则不进行任何操作，防止频繁点击
                    const index = option.graphic.findIndex(i => i.style.text === name);
                    if (!name || index !== -1) return
                    // 这里和上面一样，其实还可以再优化一下。为了方便阅读，这里不再封装。
                    const [mapName, mapJson] = getMap(name);
                    option.geo.zoom = 0.8;
                    option.geo.map = mapName;
                    //水印显示
                    // 为了重新定位，这里使用了length
                    const idx = option.graphic.length + 1;
                    option.graphic.push({
                        type: "text",
                        left: `${idx * 10}%`,
                        top: "10%",
                        style: {
                            text: name,
                            font: 'bolder 1.5rem "Microsoft YaHei", sans-serif',
                            fill: "#fff",
                        },
                        onclick: () => {
                            // 利用函数的作用域，可以直接拿上面的name来用
                            const [grahpName, graphJson] = getMap(name);
                            const index = option.graphic.findIndex(i => i.style.text === name);
                            // 点击元素之后的所有元素全部删除
                            option.graphic.splice(index + 1);
                            // 很多操作重复了，你可以将公共部分抽离出来
                            option.geo.map = mapName;
                            echarts.registerMap(grahpName, graphJson);
                            charts.setOption(option, true);
                        },
                    });
                    echarts.registerMap(mapName, mapJson);
                    charts.setOption(option, true);
                });
            },
        },
    }
</script>
<style lang="less">
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
