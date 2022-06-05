<script setup>
import {onBeforeMount, ref, defineProps} from 'vue'
import {useRoute, useRouter} from 'vue-router';

import axios from "axios";

const route = useRoute()
const router = useRouter()
const history = ref([])

const props = defineProps(['fio', 'tel'])

const form = ref({
  family: 'Myself',
  recept: [{
    m_name: '',
    description: '',
  }]
})

onBeforeMount(async () => {
  const response = await axios.get('https://api.dorilarim.uz/detail/', {
    headers: {
      'Authorization': 'Token ' + localStorage.getItem('token')
    }
  })

  const response1 = await axios.get('https://api.dorilarim.uz/medbook/?p_id=' + route.params.id, {
    headers: {
      'Authorization': 'Token ' + localStorage.getItem('token')
    }
  })


  history.value = response1.data

  form.value.doctor_id = response.data.id
  form.value.patient_id = route.params.id
})

const dorilar = ref(1)

function addMed() {
  dorilar.value++
  form.value.recept[dorilar.value - 1] = {
    m_name: '',
    description: ''
  }
}

async function sendForm() {
  const response = await axios.post('https://api.dorilarim.uz/medbook/', form.value, {
    headers: {
      'Authorization': 'Token ' + localStorage.getItem('token')
    }
  })
  router.push({name: 'Home'})

}

</script>

<template>
  <nav id="nav3">
    <div class="container">
      <div class="navbar">
        <div class="header__nav">
          <div class="header__logo"><a href="./index.html"> <img src="../../public/assets/images/site-logo-text.png"
                                                                 alt="site-logotip"/></a></div>
        </div>
        <div class="nav__list">
          <form action="">
            <input class="create_petiant" type="submit" id="create_petiant" value="Создать"
                   @click="router.push({name: 'CreatePatient'})"/>
            <input type="search" id="search" name="search" placeholder="Поиск" @input="search"/>
          </form>
        </div>
      </div>
    </div>
  </nav>
  <form action="" @submit.prevent>
    <label for="fio">Ф.И.О</label>
    <input type="text" name="fio" id="fio" :value="route.params.fio" disabled>
    <label for="tel">Тел.</label>
    <input type="text" id="tel" :value="route.params.tel" disabled>
    <div v-for="(h, id) in history" :key="id">
      <p style="text-align: center">{{ h.diagnoz }}</p>
      <div v-for="(r, id) in h.recept" :key="id">
        <label>Лекарства</label>
        <input type="text" :value="r.m_name" disabled>
        <label>Примечание</label>
        <input type="text" :value="r.description" disabled>
      </div>
    </div>
    <label for="diagnosis">Диагноз</label>
    <input type="text" id="diagnosis" v-model="form.diagnoz">
    <div v-for="id in dorilar" :key="id">
      <label>Лекарства</label>
      <input type="text" v-model="form.recept[id - 1].m_name">
      <label>Примечание</label>
      <input type="text" v-model="form.recept[id - 1].description">
    </div>
    <button @click="addMed">Добавить лекарство</button>
    <button @click="sendForm">Сохранить</button>
  </form>
</template>


<style scoped lang="css" src="../assets/css/main.css">
</style>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  margin-top: 50px;
}

form > input {
  height: 20px;
}
</style>
