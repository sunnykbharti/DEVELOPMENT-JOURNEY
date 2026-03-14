const obj = {
    name: 'Sunny',
    greet: function() {
        console.log(this.name)  // this = whoever called it
    }
}

obj.greet()          // ✅ 'Sunny'  — obj called it

const fn = obj.greet
name='Sunny';
fn()                 // ❌ undefined — window called it, no name on window