<script setup>
import {onBeforeMount, ref} from "vue";
import {useRouter} from "vue-router";
import axios from "axios";


const router = useRouter();
const cards = ref({})

let timer;

function search(e) {
  let response
  if (timer !== null)
    clearTimeout(timer)

  timer = setTimeout(async () => {
    try {
      response = await axios.get('http://api.dorilarim.uz/patient/?search=' + e.target.value, {
        headers: {
          'Authorization': 'Token ' + localStorage.getItem('token')
        }
      })
      cards.value = response.data
    } catch (e) {
      console.log('error')
    }
  }, 1000)
}

onBeforeMount(async () => {
  try {
    const request = await axios.get('https://api.dorilarim.uz/patient/', {
      headers: {
        'Authorization': 'Token ' + localStorage.getItem('token')
      }
    })
    cards.value = request.data
  } catch (e) {
    console.log('error')
  }

})
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
  <div class="body__content">
    <section id="profile">
      <div class="container">
        <div class="profile"><br/>
          <br/>

          <div class="profile__title">
            <h2>Профиль</h2>
            <br/>
          </div>
          <div class="profile__content">
            <ul>
              <li><b>Имя:</b><span>Bobur</span></li>
              <li><b>Специализация:</b><span>LOR</span></li>
            </ul>
            <input type="submit" value="Сохранить">
          </div>
        </div>
      </div>
    </section>
    <section id="medHistory">
      <div class="container">
        <div class="medHistory">
          <div class="medHistory__card" v-for="(card, id) in cards" :key="id" @click="router.push({name: 'CreateDiagnosis', params: {fio: card.full_name, tel: card.phone_number, id: id + 1}})">
            <div class="medHistory__counter"><span>{{ id + 1 }}</span></div>
            <div class="medHistory__content">
              <ul class="medHistoryTreatment">
                <li class="name"><b>И.Ф.О:</b><span>{{ card.full_name }}</span></li>
                <li class="tel_number"><b>Номер тел:</b><span>{{ card.phone_number }}</span></li>
                <li class="treatment"><b>Диагноз:</b><span>здоров</span></li>
                <li class="date"><b>Дата приема:</b><span>{{ card.birth }}</span></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped lang="css" src="../assets/css/main.css">
</style>
