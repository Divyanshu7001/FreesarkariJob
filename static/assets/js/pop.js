function pop_box(){
    let box_content = '<div style="width:300px;background:"rgba(205, 205, 255, .8)"; height:fit-content;"><form class="popup_form" action="/login" action="get"><h3>Get Update With Notification for Leatest Jobs First !<h3><label>Enter Your Gmail</lable><input style="width:100%; padding:5px;border-radius:5px" type="email" required placeholder="Something@gmail.com" ><br><span><input type="submit" value="Subscribe"><input type="button" onclick="remove_div()" value="cancel"></span></form><div>'
    let body = document.getElementsByTagName("body")[0]
    let box = document.createElement("div")
    box.id="popup"
    box.style.position='absolute'
    box.style.top=20+'px'
    box.style.margin='auto'
    box.style.width='100vw'
    box.style.display='flex'
    box.style.textAlign='center'
    box.style.alignItems ="center"
    box.style.justifyContent ="center"
    box.style.height='fit-content'
    box.style.background='rgba(205, 205, 255, .8)'
    box.style.zIndex=9999
    box.innerHTML=box_content
    body.appendChild(box)
}
function remove_div(){
    var div = document.getElementById('popup');
    div.style.display = "none"
}
document.addEventListener("DOMContentLoaded", () => {
    pop_box()
});