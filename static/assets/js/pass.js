const pass = document.getElementById('signupPassword')
const con_pass = document.getElementById('ConfirmPassword')

pass.addEventListener('keydown',()=>{
    if( pass.value != con_pass.value){
        pass.classList.remove('green_indicate')
        pass.classList.add('red_indicate')
    }
    else{
        pass.classList.remove('red_indicate')
        pass.classList.add('green_indicate')
    }
    console.log('pass change')
})
con_pass.addEventListener('keydown',()=>{
    if( pass.value != con_pass.value){
        con_pass.classList.remove('green_indicate')
        con_pass.classList.add('red_indicate')
    }
    else{
        con_pass.classList.remove('red_indicate')
        con_pass.classList.add('green_indicate')
    }
    console.log('conpass change')
})