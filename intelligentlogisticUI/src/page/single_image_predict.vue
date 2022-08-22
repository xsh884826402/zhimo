<template>
    <div class="mixin-components-container">
        <div class="content-container">
            <!-- 图片上传控件-->
            <el-row style="padding-left:100px;padding-right:100px;background:#">
                <el-upload
                    v-if="isShowUpload"
                    class="upload-demo"
                    drag
                    list-type="picture"
                    ref="upload"
                    action="http://127.0.0.1:5000/write?filepath=D:\Project\intelligentlogisticsexe\中邮信科测试数据3.xlsx"
                    :show-file-list="true"
                    :auto-upload="false"
                    :on-success="handleSuccess"
                    :on-change="imgSaveToUrl"
                    :accept="'image/*'"
                >
                    <i class="el-icon-upload" style="color:#409EFF"></i>
                    <div class="el-upload__text text">
                        将图片拖到此处，或
                        <em>点击上传</em>
                    </div>
                    <div
                        class="el-upload__tip text"
                        slot="tip"
                    >提示：可支持PNG、JPG、BMP，图片大小不超过2M</div>
                </el-upload>
            </el-row>
            <!-- 本地预览需要上传处理的图片-->
            <el-row v-if="isShowImgUpload" style="padding-left:100px;padding-right:100px;">
                <el-col :span="4" style="color:white">1</el-col>
                <el-col :span="16">
                    <div style="position:relative;background-color: #f0f3fa;">
                        <el-image
                            :src="localUrl"
                            :preview-src-list="[localUrl]"
                            style="width:100%;height:600px;"
                            fit="scale-down"
                        ></el-image>
                    </div>

                </el-col>
                <el-col :span="4" style="color:white">1</el-col>
            </el-row>
            <el-row  style="padding-left:100px;padding-right:100px;">
                <el-col :span="2" style="color:white">1</el-col>
                <el-col :span="13" offset="6">
                    <div style="padding: 5px;">
                        <el-button type="primary" :loading="false" size="small" @click="processButtonClick">开始预测</el-button>
                    </div>

                </el-col>
                <el-col :span="4" style="color:white">1</el-col>
            </el-row>
            <el-row  style="padding-left:100px;padding-right:100px;">
                <textarea v-model="message" placeholder="模型预测结果" class="text-area"></textarea>
            </el-row>

        </div>
    </div>
</template>
<script>
import headTop from '@/components/headTop'
// eslint-disable-next-line no-unused-vars
import {cityGuess, addShop, searchplace, foodCategory} from '@/api/getData'
import {baseUrl, baseImgPath} from '@/config/env'
export default {
  data () {
    return {
      baseUrl,
      baseImgPath,
      isShowUpload: true,
      isShowImgUpload: false,
      localUrl: ''
    }
  },
  components: {
    headTop
  },
  mounted () {
    this.initData()
  },
  methods: {
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
</style>
