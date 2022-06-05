<script setup>
import axios from 'axios'
import {ref} from 'vue'
import {useRouter} from 'vue-router'

const router = useRouter()

let form = ref({
  username: '',
  password: ''
})

async function login() {
  let response = {}
  console.log(router)
  try {
    response = await axios.post('https://api.dorilarim.uz/login/', form.value, {
      headers: {
        'Content-type': 'application/json',
        'Accept': 'application/json',
      }
    })
  } catch (e) {
    if (e.response.data.non_field_errors) {
      alert('response.data.non_field_errors')
    }
    return
  }
  localStorage.setItem('token', response.data.token)
  router.push({name: 'Home'})
}

</script>

<template>
  <div class="container">
    <div class="sing_bg">
    </div>
    <form class="form" @submit.prevent="onSubmit">
      <div class="form-inner">
        <h3>Вход</h3>
        <input type="tel" placeholder="tel number" class="form_input" v-model="form.username">
        <input type="password" placeholder="Пароль" class="form_input" v-model="form.password">
        <input type="submit" class="form_submit" value="Отправить" @click="login">
      </div>
    </form>
  </div>

</template>

<style lang="css">
@import "../assets/css/sign_in.css";
@import "../assets/css/bootstrap-grid.min.css";
</style>
