// Define Components
const home = { template : "<h1> This is Home view </h1>"} // /home
const about = { template : "<h1> This is About view </h1>"}// /about
const profile = { template : "<h1> This is Profile view </h1>"} // /profile

//mapping with Routes
const routes = [
    {path: "/home", component: home},
    {path : "/about", component : about},
    {path : "/profile", component : profile}
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
