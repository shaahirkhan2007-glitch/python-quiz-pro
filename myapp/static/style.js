let time = 30;

let timer = setInterval(function(){

time--;

let t = document.getElementById("timer");

if(t){
t.innerHTML=time;
}

if(time==0){

clearInterval(timer);

document.forms[0].submit();

}


},1000);

<script>
const progress = document.querySelector(".progress-fill");

let total = {{ total_questions }};
let current = {{ current_question }};

let percent = (current / total) * 100;

progress.style.width = percent + "%";
</script>