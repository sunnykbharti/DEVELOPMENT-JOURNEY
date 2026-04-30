// Define Components
const home = { template : "<h1> This is Home view </h1>"} // /home
const about = { template : "<h1> This is About view </h1>"}// /about
const profile = { 
    template : `
    <div>
        <h1> This is Profile view </h1>
        Username : <input type="text" v-model="username">
        Role : <input type="text" v-model="role">
        <button @click="naviGate">GO</button>
    </div>`,

    data : function(){
        return {
            username : "",
            role : ""
        }
    },
    
    methods : {
        naviGate : function(){
            this.$router.push({name : "userName", params : { username : this.username }, query : { role : this.role }})
        }
    }
    } // /profile
const user = { 
    template : `
    <div>
        <h1> Hello, {{ $route.params.username }}. Welcome to VUE Lessons</h1>
        <h1> Accessing as {{ $route.query.role }} ......</h1>
    </div>`,
    method : function(){
        console.log(this.$route.params.username)
    }
}
const users = {
    template : `
        <div>
            <router-link to="users/dashboard">Dashboard</router-link>
            <router-link to="users/activities">Activities</router-link>
            <h1>This is Users View</h1>
            <router-view></router-view>
        </div>
    `
}
const dashboard = { template : "<h3> This is Dasboard View </h3>" }
const activities = { 
    template : `
    <div>
        <h2> This is Activity View </h2>
        <button @click="goHome">Home</button>
    </div>
    `,

    methods : {
        goHome : function(){
            this.$router.push("/home")
        }
    }
}

//mapping with Routes
const routes = [
    {path: "/home", component: home},
    {path : "/about", component : about},
    {path : "/profile", component : profile},
    {path : "/user/:username", name : "userName", component : user},
    {
        path : "/users",
        component : users,
        children : [
            { path : "dashboard", component : dashboard},
            { path : "activities", component : activities}
        ]
    }
]

// create router object
const router = new VueRouter({
    // routes : routes
    routes
})



const app = new Vue({
    el: "#app",
    // router : router
    router
})
