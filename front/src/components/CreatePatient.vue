<script setup>
import axios from 'axios'

import {ref} from 'vue'
import {useRouter} from 'vue-router'

const phone = ref()
const code = ref()

const showCode = ref(false)
const showForm = ref(false)


const form = ref({
  full_name: '',
  birth: '',
  passport_type: 'ID CARD',
  passport: 'asdas'
})

const diagnosis = ref([])

async function sendPhone() {
  const response = await axios.post('https://api.dorilarim.uz/sendcode/', {
    phone: phone.value
  }, {
    headers: {
      'Authorization': 'Token ' + localStorage.getItem('token')
    }
  })
  showCode.value = true
}

async function sendCode() {
  const response = await axios.post('https://api.dorilarim.uz/verifyphone/', {
    phone: phone.value,
    code: code.value.toString()
  }, {
    headers: {
      'Authorization': 'Token ' + localStorage.getItem('token')
    }
  })

  showForm.value = true
}

async function sendForm() {
  form.value.phone_number = phone.value
  const response = await axios.post('https://api.dorilarim.uz/patient/', form.value, {
    headers: {
      'Authorization': 'Token ' + localStorage.getItem('token')
    }
  })
}
</script>

<template>
  <div class="container">
    <form class="form" @submit.prevent="">
      <div class="form-inner">
        <h1 class="create_title">Создания пациента</h1><label for="tel">Тел. номeр:</label>
        <input type="tel" id="tel" name="tel" v-model="phone" placeholder="998941234567"> <input type="submit" value="Получить код"
                                                                      @click="sendPhone"><br><br>
        <div v-if="showCode">
        <label for="code">Код проверки:</label>
        <input type="number" id="code" name="code" v-model="code" placeholder="123456"> <input type="submit" value="Проверить"
                                                                          @click="sendCode"><br><br>
        </div>
        <div v-if="showForm">
        <label for="fname">Ф.И.О.:</label>
        <input type="text" id="fname" name="fname" v-model="form.full_name" placeholder="Иванов Иван Иванович"><br><br>
        <label for="birth">Год рождения:</label>
        <input type="text" id="birth" name="birth" v-model="form.birth" placeholder="2001"><br><br>
        <input type="submit" value="Добавить" @click="sendForm">
          </div>
      </div>
    </form>
  </div>
</template>

<style scoped>

</style>
