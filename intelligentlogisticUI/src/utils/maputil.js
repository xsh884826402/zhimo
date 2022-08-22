import zhongguo from "@/assets/mapJson/chinaChange.json";
// import henan from "@/assets/mapJson/data-henan.json";
// import kaifeng from "@/assets/mapJson/data-kaifeng.json";
// import tongxu from "@/assets/mapJson/data-tongxu.json";
// import beijing from "@/assets/mapJson/data-beijing.json";
// import shanghai from "@/assets/mapJson/data-shanghai.json";
// import songjiang from "@/assets/mapJson/data-songjiang.json";
// import pudong from "@/assets/mapJson/data-pudong.json";
// import anhui from "@/assets/mapJson/data-anhui.json";
// import anqing from "@/assets/mapJson/data-anqing.json";
// import tongling from "@/assets/mapJson/data-tongling.json";
// import zongyang from "@/assets/mapJson/data-zongyang.json";
//
// const mapDict = {
//     "北京市": "beijing",
//     "河南省": "henan",
//     "开封市": "kaifeng",
//     "通许县": "tongxu",
//     "上海市": "shanghai",
//     "松江区": "songjiang",
//     "浦东新区": "pudong",
//     "安徽省": "anhui",
//     "安庆市": "anqing",
//     "铜陵市": "tongling",
//     "枞阳县": "zongyang",
// }
//
// const mapData = {
//     beijing,
//     henan,
//     kaifeng,
//     tongxu,
//     shanghai,
//     songjiang,
//     pudong,
//     anhui,
//     anqing,
//     tongling,
//     zongyang,
// }

export function getMap(mapName) {
    // const cityName = mapDict[mapName]
    // if(cityName){
    //     return [cityName, mapData[cityName]]
    // }
    return ['china', zhongguo]
}
