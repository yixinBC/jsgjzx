let mySelect = document.getElementById('mySelect');
let myButton = document.getElementById('myButton');
myButton.addEventListener('click', (event)=>{
  window.location.href = `/canteen/export_excel/${mySelect.options[mySelect.selectedIndex].value}`
},false)