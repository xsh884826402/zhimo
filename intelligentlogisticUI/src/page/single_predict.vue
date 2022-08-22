<template>
    <div>
        <head-top></head-top>
        <el-row style="margin-top: 20px;">
            <el-col :span="12" :offset="4">
                <el-form :model="formData" :rules="rules" ref="formData" label-width="110px" class="demo-formData">

                    <el-form-item label="上传待预测文件">
                        <el-upload
                            class="avatar-uploader"
                            :action="'http://127.0.0.1:5000' + '/write'"
                            :show-file-list="false"
                            :on-success="handleShopAvatarScucess"
                            :before-upload="beforeAvatarUpload">
                            <img v-if="formData.image_path" :src="baseImgPath + formData.image_path" class="avatar">
                            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                        </el-upload>
                    </el-form-item>
                    <el-form-item class="button_submit">
                        <el-button type="primary" @click="submitForm('formData')">请求预测a </el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>

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
      city: {},
      formData: {
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
        catering_service_license_image: '',
        filepath: 'D:/Project/intelligentlogisticsexe/中邮信科测试数据3.xlsx'

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
      baseUrl,
      baseImgPath
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
    handleShopAvatarScucess (res, file) {
      console.log('before handle')
      console.log(res)
      if (res.status === 1) {
        this.formData.image_path = res.image_path
      } else {
        this.$message.error('上传图片失败！')
      }
    },
    beforeAvatarUpload (file) {
      console.log(' prev before upload')
      const isRightType = (file.type === 'image/jpeg') || (file.type === 'image/png')
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isRightType) {
        this.$message.error('上传头像图片只能是 JPG 格式!')
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!')
      }
      console.log(' after  before upload')
      return isRightType && isLt2M
    },
    submitForm (formName) {
      console.log('before submit')
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          Object.assign(this.formData, {activities: this.activities}, {
            category: this.selectedCategory.join('/')
          })
          try {
            let result = await addShop(this.formData)
            if (result.status == 1) {
              this.$message({
                type: 'success',
                message: '添加成功'
              })
              this.formData = {
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
              }
              this.selectedCategory = ['快餐便当', '简餐']
              this.activities = [{
                icon_name: '减',
                name: '满减优惠',
                description: '满30减5，满60减8'
              }]
            } else {
              this.$message({
                type: 'error',
                message: result.message
              })
            }
            console.log(result)
          } catch (err) {
            console.log(err)
          }
        } else {
          this.$notify.error({
            title: '错误',
            message: '请检查输入是否正确',
            offset: 100
          })
          return false
        }
      })
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
</style>
