<template>
    <div class="home_div">
        <div class="map_title">
            <h3>JSAPI Vue2地图组件示例</h3>
        </div>
        <div>
            <div id="container"></div>
            <div class="input-item">
                <input type="button" class="btn" value="开始动画" id="start" onclick="startAnimation()"/>
                <input type="button" class="btn" value="暂停动画" id="pause" onclick="pauseAnimation()"/>
            </div>
            <div class="input-item">
                <input type="button" class="btn" value="继续动画" id="resume" onclick="resumeAnimation()"/>
                <input type="button" class="btn" value="停止动画" id="stop" onclick="stopAnimation()"/>
            </div>
            <el-button @click="startAnimation">开始动画</el-button>
            <el-button @click="pauseAnimation">暂停动画</el-button>
            <el-button @click="resumeAnimation">继续动画</el-button>
            <el-button @click="stopAnimation">停止动画</el-button>
        </div>


    </div>
</template>
<script>
    import AMapLoader from '@amap/amap-jsapi-loader';

    export default {
        name: "Mapview",
        data() {
            return {
                //map:null,
            }
        },
        created() {

        },
        mounted() {
            this.initAMap();
        },
        methods: {

            initAMap() {
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
                        zoom:12,
                        center: countyInfo['centerGeoCoord']
                    })

                    AMap.plugin(['AMap.DistrictSearch', 'AMap.Driving', 'AMap.MoveAnimation'], function () {
                        var district = new AMap.DistrictSearch(opts)
                        district.search(countyInfo['name'], function (status, result) {
                            if (status='complete'){
                                var bounds = result.districtList[0].boundaries
                                var mask = []
                                for (var i = 0; i < bounds.length; i += 1) {
                                    mask.push([bounds[i]])
                                }
                                for (var i = 0; i < bounds.length; i += 1) {
                                    new AMap.Polyline({
                                        path: bounds[i],
                                        strokeColor: '#4B0082',
                                        strokeWeight: 4,
                                        strokeStyle: 'dashed',
                                        map: map
                                    })
                                }
                            }
                            var townCenterIconAddr = 'assets/img/star.png'
                            var townCenterIcon = new AMap.Icon({image: townCenterIconAddr,
                                size: new AMap.Size(22, 22), // 设置icon的大小
                                imageSize: new AMap.Size(22, 22)})

                            var villageIconAddr = 'https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png'
                            var villageIcon = new AMap.Icon({image: villageIconAddr,
                                size: new AMap.Size(12, 12), // 设置icon的大小
                                imageSize: new AMap.Size(12, 12)})

                            var postalTruckIconAddr = 'assets/img/postalTruck.png'
                            var postalTruckIcon = new AMap.Icon({image: postalTruckIconAddr,
                                size: new AMap.Size(12.23, 24), // 设置icon的大小
                                imageSize: new AMap.Size(12.23, 24)})


                            var str = '经'

                            var cumulatedIndices = 0

                            var driving = new AMap.Driving({
                                map: map,
                                hideMarkers: true,
                                autoFitView: true,
                                isOutline: false,
                                policy: AMap.DrivingPolicy.LEAST_TIME,
                                // policy: AMap.DrivingPolicy.LEAST_TIME,
                                showTraffic: false
                            })

                            AMap.plugin('AMap.MoveAnimation', function () {
                                var carMarkers = []
                                var lineArrs = []
                                var routeColorDict = {}
                                var routeLineArrsDict = {}
                                var routeCarMarkerIndexDict = {}

                                for (var townCenter in routes) {
                                    var townRoutes = routes[townCenter]

                                    for (var j = 0; j < townRoutes.length; j++) {
                                        var route = townRoutes[j]
                                        var color = colorList[cumulatedIndices % colorList.length]
                                        cumulatedIndices++
                                        for (var k = 0; k < route.length; k++) {
                                            if (k != route.length - 1) {
                                                routeColorDict[route[k].geoCoord[0] + ', ' + route[k].geoCoord[1] + '_' + route[k + 1].geoCoord[0] + ', ' + route[k + 1].geoCoord[1]] = color
                                                routeCarMarkerIndexDict[route[k].geoCoord[0] + ', ' + route[k].geoCoord[1] + '_' + route[k + 1].geoCoord[0] + ', ' + route[k + 1].geoCoord[1]] = carMarkers.length


                                                driving.search(new AMap.LngLat(route[k].geoCoord[0], route[k].geoCoord[1]),
                                                	new AMap.LngLat(route[k + 1].geoCoord[0], route[k + 1].geoCoord[1]),
                                                	function (status, result) {
                                                		if (status === 'complete') {
                                                			var lineArr = []
                                                			var driveRoutes = result.routes
                                                			for (var l = 0; l < driveRoutes.length; l++) {
                                                				var steps = driveRoutes[l].steps
                                                				for (var m = 0; m < steps.length; m++) {
                                                					if (l == 0 && m == 0) {
                                                						var stepStartPosition = steps[m].start_location
                                                						lineArr.push([stepStartPosition.lng, stepStartPosition.lat])
                                                					}

                                                					var stepPath = steps[m].path
                                                					for (var n = 1; n < stepPath.length; n++) {
                                                						var pathPosition = stepPath[n]
                                                						lineArr.push([pathPosition.lng, pathPosition.lat])
                                                					}
                                                				}
                                                			}

                                                			routeLineArrsDict[result.origin.lng + ', ' + result.origin.lat + '_' + result.destination.lng + ', ' + result.destination.lat] = lineArr
                                                			color = routeColorDict[result.origin.lng + ', ' + result.origin.lat + '_' + result.destination.lng + ', ' + result.destination.lat]
                                                            var polyline = new AMap.Polyline({
                                                				map: map,
                                                				path: lineArr,
                                                				showDir: true,
                                                				strokeColor: color, // 线颜色
                                                				strokeWeight: 10 // 线宽
                                                			})
                                                		} else {
                                                			log.error('获取驾车数据失败：' + result)
                                                		}
                                                	})

                                                var labelStr = k == 0 ? townCenter : str.concat(k)
                                                var labelClass = k == 0 ? 'townCenterInfo' : 'villageInfo'
                                                var icon = k == 0 ? townCenterIcon : villageIcon
                                                var zIndex = k == 0 ? 9999 : 12

                                                // 绘制轨迹

                                                // console.info("step in route", route[k].geoCoord[0] + ', ' + route[k].geoCoord[1] + '_' + route[k + 1].geoCoord[0] + ', ' + route[k + 1].geoCoord[1])
                                                // 构造点标记
                                                var marker = new AMap.Marker({
                                                    icon: icon,
                                                    position: route[k].geoCoord,
                                                    anchor: 'bottom-center',
                                                    zIndex: zIndex
                                                })

                                                marker.setMap(map)

                                                var contentStr = "<div class='".concat(labelClass).concat("' style='color:").concat(color).concat("'>").concat(labelStr).concat('</div>')

                                                // 设置label标签
                                                // 样式className为：amap-marker-label
                                                marker.setLabel({
                                                    direction: 'right',
                                                    offset: new AMap.Pixel(0, 0), // 设置文本标注偏移量
                                                    content: contentStr // 设置文本标注内容
                                                })
                                            }
                                        }

                                        var carMarker = new AMap.Marker({
                                            map: map,
                                            position: route[0].geoCoord,
                                            icon: postalTruckIcon,
                                            offset: new AMap.Pixel(-7, -13)
                                        })

                                        map.setFitView()

                                        carMarkers.push(carMarker)
                                        lineArrs.push([])
                                    }
                                }

                                var isLineArrsReady = false;

                                window.startAnimation = function startAnimation () {
                                    if(!isLineArrsReady){
                                        for (var townCenter in routes) {
                                            var townRoutes = routes[townCenter];
                                            for(var j = 0; j < townRoutes.length; j++){
                                                route = townRoutes[j];
                                                for (var k = 0; k < route.length; k++) {
                                                    if (k != route.length - 1){
                                                        key = route[k].geoCoord[0] + ', ' + route[k].geoCoord[1] + '_' + route[k + 1].geoCoord[0] + ', ' + route[k + 1].geoCoord[1];
                                                        var lineArrsIndex = routeCarMarkerIndexDict[key];
                                                        var lineArr = routeLineArrsDict[key];
                                                        lineArrs[lineArrsIndex] = lineArrs[lineArrsIndex].concat(lineArr);
                                                    }
                                                }
                                            }
                                        }
                                        isLineArrsReady = true;
                                    }
                                    console.info("dict", routeLineArrsDict)


                                    for (var i = 0; i < carMarkers.length; i++) {
                                        carMarkers[i].moveAlong(lineArrs[i], {
                                            duration: 1,//可根据实际采集时间间隔设置
                                            // JSAPI2.0 是否延道路自动设置角度在 moveAlong 里设置
                                            autoRotation: true,
                                            circlable: true,
                                        });
                                    }
                                };

                                window.pauseAnimation = function () {
                                    for (var i = 0; i < carMarkers.length; i++) {
                                        carMarker = carMarkers[i];
                                        carMarker.pauseMove();
                                    }
                                };

                                window.resumeAnimation = function () {
                                    for (var i = 0; i < carMarkers.length; i++) {
                                        carMarker = carMarkers[i];
                                        carMarker.resumeMove();
                                    }
                                };

                                window.stopAnimation = function () {
                                    for (var i = 0; i < carMarkers.length; i++) {
                                        carMarker = carMarkers[i];
                                        carMarker.stopMove();
                                    }
                                };
                            })
                        })

                            } )
                    // DistrictSearch可用
                    // var district = new AMap.DistrictSearch(opts)
                    // var countyInfo = {'name': '济南市', 'centerGeoCoord': [117.000923, 36.675807]}
                    // district.search(countyInfo['name'], function (status, result) {
                    //     console.info('in district', status, result)
                    // })
                    //
                    // var driving = new AMap.Driving({
                    //     map: map,
                    //     // panel: 'panel'
                    // })
                    // console.info('driving', driving)
                    // // Driving不可用
                    // driving.search(new AMap.LngLat(116.379028, 39.865042), new AMap.LngLat(116.427281, 39.903719), function(status, result) {
                    //     console.info('status here', status)
                    //     if (status=== 'complete'){
                    //         console.info('status', status)
                    //     }
                    //
                    // })
                    this.map = map

                }).catch(e => {
                    console.log(e);
                })
            },
        }


    }
</script>
<style  scoped>
    .home_div {
        padding: 0px;
        margin: 0px;
        width: 100%;
        height: 100%;
        position: relative;
    }

    #container {
        padding: 0px;
        margin: 0px;
        width: 100%;
        height: 100%;
        position: absolute;
    }

    .map_title {
        position: absolute;
        z-index: 1;
        width: 100%;
        height: 50px;
        background-color: rgba(27, 25, 27, 0.884);

    }

    h3 {
        position: absolute;
        left: 10px;
        z-index: 2;
        color: white;
    }
</style>
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
        .amap-wrapper{
            width: 1000rem;
            height: 50rem;
            border: 1px solid red;
        }
    }
    /*.amap-wrapper {*/
    /*    width: 500px;*/
    /*    height: 500px;*/
    /*}*/
</style>
