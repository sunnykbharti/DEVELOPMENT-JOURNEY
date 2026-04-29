// Define Components
const home = { template : "<h1> This is Home view </h1>"} // /home
const about = { template : "<h1> This is About view </h1>"}// /about
const profile = { template : "<h1> This is Profile view </h1>"} // /profile
const user = { 
    template : "<h1> Hello, {{ $route.params.username }}. Welcome to VUE Lessons</h1>",
    method : function(){
        console.log(this.$route.params.username)
    }
}


//mapping with Routes
const routes = [
    {path: "/home", component: home},
    {path : "/about", component : about},
    {path : "/profile", component : profile},
    {path : "/user/:username", component : user}
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
