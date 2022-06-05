import {createApp} from 'vue'
import {createRouter, createWebHistory} from 'vue-router'

import App from './App.vue'
import Login from "@/components/Login"
import CreatePatient from "@/components/CreatePatient"
import MainPage from "@/components/MainPage"
import CreateDiagnosis from "@/components/CreateDiagnosis"

const routes = [
    {
        path: '/',
        component: MainPage,
        name: 'Home'
    },
    {
        path: '/create-patient',
        component: CreatePatient,
        name: 'CreatePatient'
    },
    {
        path: '/create-diagnosis',
        component: CreateDiagnosis,
        name: 'CreateDiagnosis'
    },
    {
        path: '/login',
        component: Login,
        name: 'Login'
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach( (to, from, next) => {
    const token = localStorage.getItem('token')
    if(to.name === 'Login') {
        if (token) {
            next({name: 'Home'})
        }
        else
            next()
    }
    else if (!token) {
        next({name: 'Login'})
    }
    else {
        next()
    }
})

const app = createApp(App)

app.use(router)

app.mount('#app')
