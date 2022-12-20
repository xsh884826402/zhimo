<template>
    <div>
        <my-in-content>
            <!-- 高德地图 -->
            <div id="container"></div>
            <el-button @click="startAnimation">开始动画</el-button>
<!--            <div id="details">-->
<!--                <Card style="width:340px;height:280px">-->
<!--                    <div style="text-align:lef;">-->
<!--                        <p>经纬度：{{this.lnglat}}</p><br/>-->
<!--                        <p>地址：{{this.address}}</p><br/>-->
<!--                        <p>最近的路口：{{this.nearestJunction}}</p><br/>-->
<!--                        <p>最近的路：{{this.nearestRoad}}</p><br/>-->
<!--                        <p>最近的POI：{{this.nearestPOI}}</p><br/>-->
<!--                    </div>-->
<!--                </Card>-->
<!--            </div>-->
<!--            &lt;!&ndash; 搜索 &ndash;&gt;-->
<!--            <div id="search">-->
<!--                <Input v-model="searchValue" placeholder="请输入要搜索的位置" style="width: 300px" />-->
<!--                <Button type="primary" @click="seachAddress">搜索</Button>-->
<!--                <Button style="margin-left:5px;" type="primary" @click="reporAddress">上报位置</Button>-->
<!--            </div>-->
        </my-in-content>
    </div>
</template>
<script>
export default {
	name: 'gdmap',
	data () {
		return {
			mask: [],
			countyInfo: {'name': '济南市', 'centerGeoCoord': [117.000923, 36.675807]},
			searchValue: '',
			gdmap: null,
            map: null,
            carMarkers: [],
            lineArrs: [],
            routeColorDict: {},
            routeLineArrsDict: {},
            routeCarMarkerIndexDict: {},
            isLineArrsReady: false,
            colorList: [
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

		}
	},

	created () {
	},
	mounted () {
		// 地图初始化

		// this.gdmap = new AMap.Map('container', {
		//     resizeEnable: true,//是否监控地图容器尺寸变化
		//     zoom: 15,//地图显示的缩放级别
		//     zooms: [3, 18],//地图显示的缩放级别范围在PC上，默认为[3,18]，取值范围[3-18]；
		//     viewMode: '2D',//默认为‘2D’，可选’3D’，选择‘3D’会显示 3D 地图效果
		//
		// })
		// this.map = new AMap.Map('container', {
		// 	resizeEnable: false,
		// 	zoom: 12,
		// 	center: this.countyInfo['centerGeoCoord'],
		// 	mask: this.mask
		// })
		// //加载工具条
		// this.addTool();
		// //获取当前位置
		// this.thisLocation();
        this.init();
        this.line();
	},
	methods: {
		// 工具条
		init () {
            console.info('map debug1', this.map)

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
			// console.info("debug0")
            // AMap.plugin('AMap.MoveAnimation', function(){
            //     const animationMarker = new AMap.Marker({
            //         position: new AMap.LngLat(116.397389,39.909466),
            //     });
            //     animationMarker.moveTo([116.397389, 39.909466], {
            //         duration: 1000,
            //         delay: 500,
            //     });
            // });
            const that = this
            console.info('that', that)
			AMap.plugin(['AMap.DistrictSearch', 'AMap.Driving', 'AMap.MoveAnimation'], function () {
				var district = new AMap.DistrictSearch(opts)
				district.search(countyInfo['name'], function (status, result) {
					var bounds = result.districtList[0].boundaries
					var mask = []
					for (var i = 0; i < bounds.length; i += 1) {
						mask.push([bounds[i]])
					}

					var map = new AMap.Map('container', {
						resizeEnable: false,
						zoom: 12,
						center: countyInfo['centerGeoCoord'],
						mask: mask
					})
                    console.info("- debug map", map)
                    // console.info("this map", that.map)
					// 添加描边
					for (var i = 0; i < bounds.length; i += 1) {
						new AMap.Polyline({
							path: bounds[i],
							strokeColor: '#4B0082',
							strokeWeight: 4,
							strokeStyle: 'dashed',
							map: map
						})
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
					console.info('debug1 ')

					var driving = new AMap.Driving({
						map: that.map,
						panel: 'panel',
						hideMarkers: true,
						autoFitView: false,
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
						console.info('debug3 ')
                        var driving = new AMap.Driving({
                            map: map,
                            panel: 'panel',
                            hideMarkers: true,
                            autoFitView: false,
                            isOutline: false,
                            policy: AMap.DrivingPolicy.LEAST_TIME,
                            // policy: AMap.DrivingPolicy.LEAST_TIME,
                            showTraffic: false
                        })
						for (var townCenter in routes) {
							var townRoutes = routes[townCenter]
							console.log('routes', townRoutes)

							for (var j = 0; j < townRoutes.length; j++) {
								var route = townRoutes[j]
                                var color = colorList[cumulatedIndices % colorList.length]
								cumulatedIndices++
								console.log('route : ', j, route)
								for (var k = 0; k < route.length; k++) {
									if (k != route.length - 1) {
										routeColorDict[route[k].geoCoord[0] + ', ' + route[k].geoCoord[1] + '_' + route[k + 1].geoCoord[0] + ', ' + route[k + 1].geoCoord[1]] = color
										routeCarMarkerIndexDict[route[k].geoCoord[0] + ', ' + route[k].geoCoord[1] + '_' + route[k + 1].geoCoord[0] + ', ' + route[k + 1].geoCoord[1]] = carMarkers.length
                                        console.info("source ", new AMap.LngLat(route[k].geoCoord[0], route[k].geoCoord[1]),)

                                        // driving.search(new AMap.LngLat(route[k].geoCoord[0], route[k].geoCoord[1]),
                                        //     new AMap.LngLat(route[k + 1].geoCoord[0], route[k + 1].geoCoord[1]),
                                        //     function (status, result) {
                                        //         console.info("processing ")
                                        //         if (status=== 'complete'){
                                        //             console.info('result', result)
                                        //         }
                                        //
                                        //     }
                                        // )
                                        // driving.search(new AMap.LngLat(route[k].geoCoord[0], route[k].geoCoord[1]),
										// 	new AMap.LngLat(route[k + 1].geoCoord[0], route[k + 1].geoCoord[1]),
										// 	function (status, result) {
										//         console.info('search start ')
										// 		if (status === 'complete') {
										// 		    console.info("debug1 complete")
										// 			this.lineArr = []
										// 			this.driveRoutes = result.routes
										// 			for (var l = 0; l < driveRoutes.length; l++) {
										// 				this.steps = driveRoutes[l].steps
										// 				for (var m = 0; m < steps.length; m++) {
										// 					if (l == 0 && m == 0) {
										// 						var stepStartPosition = steps[m].start_location
										// 						lineArr.push([stepStartPosition.lng, stepStartPosition.lat])
										// 					}
                                        //
										// 					this.stepPath = steps[m].path
										// 					for (var n = 1; n < stepPath.length; n++) {
										// 						var pathPosition = stepPath[n]
										// 						lineArr.push([pathPosition.lng, pathPosition.lat])
										// 					}
										// 				}
										// 			}
                                        //
										// 			routeLineArrsDict[result.origin.lng + ', ' + result.origin.lat + '_' + result.destination.lng + ', ' + result.destination.lat] = lineArr
										// 			color = routeColorDict[result.origin.lng + ', ' + result.origin.lat + '_' + result.destination.lng + ', ' + result.destination.lat]
										// 			console.info('debug1 color', color)
                                        //             var polyline = new AMap.Polyline({
										// 				map: map,
										// 				path: lineArr,
										// 				showDir: true,
										// 				strokeColor: color, // 线颜色
										// 				strokeWeight: 10 // 线宽
										// 			})
										// 		} else {
										// 			log.error('获取驾车数据失败：' + result)
										// 		}
										// 	})
                                        console.info('driving search end')

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
                        console.info(lineArrs)
						var isLineArrsReady = false


						// window.startAnimation = function startAnimation () {
						// 	if (!isLineArrsReady) {
						// 		for (var townCenter in routes) {
						// 			var townRoutes = routes[townCenter]
						// 			for (var j = 0; j < townRoutes.length; j++) {
						// 				var route = townRoutes[j]
						// 				for (var k = 0; k < route.length; k++) {
						// 					if (k != route.length - 1) {
						// 						key = route[k].geoCoord[0] + ', ' + route[k].geoCoord[1] + '_' + route[k + 1].geoCoord[0] + ', ' + route[k + 1].geoCoord[1]
						// 						var lineArrsIndex = routeCarMarkerIndexDict[key]
						// 						var lineArr = routeLineArrsDict[key]
						// 						lineArrs[lineArrsIndex] = lineArrs[lineArrsIndex].concat(lineArr)
						// 					}
						// 				}
						// 			}
						// 		}
						// 		isLineArrsReady = true
						// 	}
						// 	console.info('dict', routeLineArrsDict)
                        //
						// 	for (var i = 0; i < carMarkers.length; i++) {
						// 		carMarkers[i].moveAlong(lineArrs[i], {
						// 			duration: 1, // 可根据实际采集时间间隔设置
						// 			// JSAPI2.0 是否延道路自动设置角度在 moveAlong 里设置
						// 			autoRotation: true,
						// 			circlable: true
						// 		})
						// 	}
						// }
                        //
						// window.pauseAnimation = function () {
						// 	for (var i = 0; i < carMarkers.length; i++) {
						// 		carMarker = carMarkers[i]
						// 		carMarker.pauseMove()
						// 	}
						// }
                        //
						// window.resumeAnimation = function () {
						// 	for (var i = 0; i < carMarkers.length; i++) {
						// 		carMarker = carMarkers[i]
						// 		carMarker.resumeMove()
						// 	}
						// }
                        //
						// window.stopAnimation = function () {
						// 	for (var i = 0; i < carMarkers.length; i++) {
						// 		carMarker = carMarkers[i]
						// 		carMarker.stopMove()
						// 	}
						// }
					})
                    that.map = map
                    console.info('that 1111', that)
				})
			})
		},
        line(){
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
            const that = this
            console.info(' in line')
            AMap.plugin('AMap.MoveAnimation', function () {
                var carMarkers = []
                var lineArrs = []
                var routeColorDict = {}
                var routeLineArrsDict = {}
                var routeCarMarkerIndexDict = {}
                var cumulatedIndices = 0

                var driving = new AMap.Driving({
                    map: that.map,
                    panel: 'panel',
                    hideMarkers: true,
                    autoFitView: false,
                    isOutline: false,
                    policy: AMap.DrivingPolicy.LEAST_TIME,
                    // policy: AMap.DrivingPolicy.LEAST_TIME,
                    showTraffic: false
                })
                console.info("hahaha")
                    driving.search([{keyword:'方恒国际',city:'北京'},{keyword:'壶口瀑布'}], function(status, result){
                        console.log("hahahah", result)});
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
                                console.info("source ", new AMap.LngLat(route[k].geoCoord[0], route[k].geoCoord[1]),)

                                driving.search(new AMap.LngLat(route[k].geoCoord[0], route[k].geoCoord[1]),
                                    new AMap.LngLat(route[k + 1].geoCoord[0], route[k + 1].geoCoord[1]),
                                    function (status, result) {
                                        console.info("processing ")
                                        if (status=== 'complete'){
                                            console.info('result', result)
                                        }

                                    }
                                )
                                // driving.search(new AMap.LngLat(route[k].geoCoord[0], route[k].geoCoord[1]),
                                // 	new AMap.LngLat(route[k + 1].geoCoord[0], route[k + 1].geoCoord[1]),
                                // 	function (status, result) {
                                //         console.info('search start ')
                                // 		if (status === 'complete') {
                                // 		    console.info("debug1 complete")
                                // 			this.lineArr = []
                                // 			this.driveRoutes = result.routes
                                // 			for (var l = 0; l < driveRoutes.length; l++) {
                                // 				this.steps = driveRoutes[l].steps
                                // 				for (var m = 0; m < steps.length; m++) {
                                // 					if (l == 0 && m == 0) {
                                // 						var stepStartPosition = steps[m].start_location
                                // 						lineArr.push([stepStartPosition.lng, stepStartPosition.lat])
                                // 					}
                                //
                                // 					this.stepPath = steps[m].path
                                // 					for (var n = 1; n < stepPath.length; n++) {
                                // 						var pathPosition = stepPath[n]
                                // 						lineArr.push([pathPosition.lng, pathPosition.lat])
                                // 					}
                                // 				}
                                // 			}
                                //
                                // 			routeLineArrsDict[result.origin.lng + ', ' + result.origin.lat + '_' + result.destination.lng + ', ' + result.destination.lat] = lineArr
                                // 			color = routeColorDict[result.origin.lng + ', ' + result.origin.lat + '_' + result.destination.lng + ', ' + result.destination.lat]
                                // 			console.info('debug1 color', color)
                                //             var polyline = new AMap.Polyline({
                                // 				map: map,
                                // 				path: lineArr,
                                // 				showDir: true,
                                // 				strokeColor: color, // 线颜色
                                // 				strokeWeight: 10 // 线宽
                                // 			})
                                // 		} else {
                                // 			log.error('获取驾车数据失败：' + result)
                                // 		}
                                // 	})
                                console.info('driving search end')

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
                console.info(lineArrs)
                var isLineArrsReady = false


                // window.startAnimation = function startAnimation () {
                // 	if (!isLineArrsReady) {
                // 		for (var townCenter in routes) {
                // 			var townRoutes = routes[townCenter]
                // 			for (var j = 0; j < townRoutes.length; j++) {
                // 				var route = townRoutes[j]
                // 				for (var k = 0; k < route.length; k++) {
                // 					if (k != route.length - 1) {
                // 						key = route[k].geoCoord[0] + ', ' + route[k].geoCoord[1] + '_' + route[k + 1].geoCoord[0] + ', ' + route[k + 1].geoCoord[1]
                // 						var lineArrsIndex = routeCarMarkerIndexDict[key]
                // 						var lineArr = routeLineArrsDict[key]
                // 						lineArrs[lineArrsIndex] = lineArrs[lineArrsIndex].concat(lineArr)
                // 					}
                // 				}
                // 			}
                // 		}
                // 		isLineArrsReady = true
                // 	}
                // 	console.info('dict', routeLineArrsDict)
                //
                // 	for (var i = 0; i < carMarkers.length; i++) {
                // 		carMarkers[i].moveAlong(lineArrs[i], {
                // 			duration: 1, // 可根据实际采集时间间隔设置
                // 			// JSAPI2.0 是否延道路自动设置角度在 moveAlong 里设置
                // 			autoRotation: true,
                // 			circlable: true
                // 		})
                // 	}
                // }
                //
                // window.pauseAnimation = function () {
                // 	for (var i = 0; i < carMarkers.length; i++) {
                // 		carMarker = carMarkers[i]
                // 		carMarker.pauseMove()
                // 	}
                // }
                //
                // window.resumeAnimation = function () {
                // 	for (var i = 0; i < carMarkers.length; i++) {
                // 		carMarker = carMarkers[i]
                // 		carMarker.resumeMove()
                // 	}
                // }
                //
                // window.stopAnimation = function () {
                // 	for (var i = 0; i < carMarkers.length; i++) {
                // 		carMarker = carMarkers[i]
                // 		carMarker.stopMove()
                // 	}
                // }
            })
        },
		addTool () {
			AMap.plugin(['AMap.ToolBar'], () => {
				let toolbar = new AMap.ToolBar()
				this.gdmap.addControl(toolbar)
			})
		},
        startAnimation(){
		    this.init()
            console.info('success')

        },
		// 定位
		thisLocation () {
			this.gdmap.plugin('AMap.Geolocation', () => {
				let geolocation = new AMap.Geolocation({
					enableHighAccuracy: true, // 是否使用高精度定位，默认:true
					timeout: 100, // 超过10秒后停止定位，默认：无穷大
					maximumAge: 0, // 定位结果缓存0毫秒，默认：0
					convert: true, // 自动偏移坐标，偏移后的坐标为高德坐标，默认：true
					showButton: true, // 显示定位按钮，默认：true
					buttonPosition: 'RB', // 定位按钮停靠位置，默认：'LB'，左下角
					buttonOffset: new AMap.Pixel(10, 20),
					showMarker: true, // 定位成功后在定位到的位置显示点标记，默认：true
					showCircle: true, // 定位成功后用圆圈表示定位精度范围，默认：true
					panToLocation: true, // 定位成功后将定位到的位置作为地图中心点，默认：true
					zoomToAccuracy: true // 定位成功后调整地图视野范围使定位位置及精度范围视野内可见，默认：false
				})
				this.gdmap.addControl(geolocation)
				geolocation.getCurrentPosition()
				AMap.event.addListener(geolocation, 'complete', (data) => {
					console.log(data)
					// 当前城市编码
					this.citycode = data.addressComponent.cityCode
					// 经纬度
					this.thisPosition = data.position
					// 地址
					this.formattedAddress = data.formattedAddress
					this.chosePosition = this.thisPosition
					/* 画圆 */
					this.cancelLocation()
					this.addCircle()
					/* 拖拽选址 */
					this.positionPicker()
				})
				AMap.event.addListener(geolocation, 'error', function (data) {
					alert('定位失败')
				})
			})
		},
		/* 拖拽选址 */
		positionPicker () {
			AMapUI.loadUI(['misc/PositionPicker'], (PositionPicker) => {
				this.positionPickerObj = new PositionPicker({
					mode: 'dragMarker', // 设定为拖拽地图模式，可选'dragMap'、'dragMarker'，默认为'dragMap'
					map: this.gdmap // 依赖地图对象
				})
				this.positionPickerObj.on('success', (positionResult) => {
					console.log(positionResult, 'positionResult')
					this.chosePosition = positionResult.position
					// 经纬度
					console.log('经纬度:' + positionResult.position)
					this.lnglat = positionResult.position
					// 地址
					console.log('地址:' + positionResult.address)
					this.address = positionResult.address
					// 最近的路口
					console.log('最近的路口:' + positionResult.nearestJunction)
					this.nearestJunction = positionResult.nearestJunction
					// 最近的路
					console.log('最近的路:' + positionResult.nearestRoad)
					this.nearestRoad = positionResult.nearestRoad
					// 最近的POI
					console.log('最近的POI:' + positionResult.nearestPOI)
					this.nearestPOI = positionResult.nearestPOI

					/* 画圆 */
					this.cancelLocation()
					this.addCircle()
				})
				this.positionPickerObj.start([this.chosePosition.lng, this.chosePosition.lat])
			})
		},
		/* 取消圆 */
		cancelLocation () {
			this.gdmap.remove(this.circle)
			if (this.circleEditor) {
				this.circleEditor.close()
			}
		},
		/* 画图 */
		addCircle () {
			this.myCircle = {
				center: [this.chosePosition.lng, this.chosePosition.lat], // 圆心位置
				radius: 50, // 半径
				strokeColor: '#FFFF00', // 线颜色
				strokeOpacity: 0.2, // 线透明度
				strokeWeight: 1, // 线粗细度
				fillColor: '#222222', // 填充颜色
				fillOpacity: 0.2 // 填充透明度
			}
			this.circle = new AMap.Circle(this.myCircle)
			this.circle.setMap(this.gdmap)
			// 引入多边形编辑器插件
			this.gdmap.plugin(['AMap.CircleEditor'], () => {
				// 实例化多边形编辑器，传入地图实例和要进行编辑的多边形实例
				this.circleEditor = new AMap.CircleEditor(this.gdmap, this.circle)
				// 开启编辑模式
				this.circleEditor.open()
				// this.myCircle.radius = this.circle.Mg.radius
				this.circleEditor.on('adjust', (data) => {
					this.myCircle.radius = data.radius
				})
				this.circleEditor.on('move', (data) => {
					console.log('移动')
					this.chosePosition.lng = data.lnglat.lng
					this.chosePosition.lat = data.lnglat.lat
				})
			})
		},
		// 搜索
		seachAddress () {
			console.info('search')
			if (this.searchValue != '') {
				// 清楚地图上的覆盖物
				this.gdmap.clearMap()
				console.log('搜索')
				this.gdmap.plugin('AMap.PlaceSearch', () => {
					let placeSearch = new AMap.PlaceSearch({
						// city 指定搜索所在城市，支持传入格式有：城市名、citycode和adcode
						city: '0797',
						map: this.gdmap
					})
					let that = this
					placeSearch.search(this.searchValue, function (status, result) {
						// 查询成功时，result即对应匹配的POI信息
						console.log(result)
						var pois = result.poiList.pois
						for (var i = 0; i < pois.length; i++) {
							var poi = pois[i]
							var marker = []
							marker[i] = new AMap.Marker({
								position: poi.location, // 经纬度对象，也可以是经纬度构成的一维数组[116.39, 39.9]
								title: poi.name
							})
							// 将创建的点标记添加到已有的地图实例：
							that.gdmap.add(marker[i])
						}
						that.gdmap.setFitView()
						AMap.event.addListener(placeSearch, 'markerClick', function (data) {
							console.log(data)
							let result = data
							// 经纬度
							let lng = result.event.lnglat.lng
							let lat = result.event.lnglat.lat
							that.lnglat = lng + ',' + lat
							// 地址
							that.address = result.data.address
							// 最近路口
							that.nearestJunction = ''
							// 最近的路
							that.nearestRoad = ''
							// 最近的POI
							that.nearestPOI = ''
						})
					})
				})
			}
		},
		// 位置上报
		reporAddress () {

		}
	}
}
</script>
<style>
    #container {
        width:100%;
        height: 600px;
    }
    #search{
        z-index:999;
        position:absolute;
        left:100px;
        top:30px;
        opacity:0.8;
    }
    #details{
        z-index:999;
        position:absolute;
        right:0px;
        top:0px;
        opacity:0.8;
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
