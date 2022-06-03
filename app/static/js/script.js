$(document).ready(function () {
    $("select").select2();
 });
var obj 
function GetContent(){
 var xr = new XMLHttpRequest()
 xr.open("GET","http://127.0.0.1:5000/listAircraft",false)
  xr.send()
  let content=`<option value="">Выберите самолет...</option>`
 let resp= xr.response
 obj = JSON.parse(resp);
 
 obj.airbus.forEach(el => {
     content+=`<option value="${el.ssj}">${el.ssj}</option>`
 });

 document.getElementById("airbus").innerHTML=content
}
function SettingsList(){
 var xr = new XMLHttpRequest()
 xr.open("GET","http://127.0.0.1:5000/boardSystems?settings="+document.getElementById("airbus").value,false)
  xr.send()
  let resp= xr.response
 obj = JSON.parse(resp);
 document.getElementById("sys").style.display="block"
 let content=`<option value="">Выберите sys...</option>`
 obj.sys.forEach(el => {  
    content+=`<option value="${el.set}">${el.set}</option>`
     
 }); 
document.getElementById("sys").innerHTML=content
 content=`<option value="">Выберите fly...</option>`
 obj.fly.forEach(el => {  
    content+=`<option value="${el.set}">${el.set}</option>`
     
 }); 
 document.getElementById("sysdiv").style.display="block"
 document.getElementById("flydiv").style.display="block"
document.getElementById("fly").innerHTML=content  
}



function ParList(){
  var xr = new XMLHttpRequest()
  xr.open("GET","http://127.0.0.1:5000/listParam?sys="+document.getElementById("sys").value,false)
   xr.send()
   let resp= xr.response
  obj = JSON.parse(resp);
  // console.log(xr.responseText)
  const obj1 = JSON.parse(resp);
  let d = document.createElement('div');
  d.className="scroll-table"
  document.body.append(d);
  let t = document.createElement('table');
  t.innerHTML =`<thead>
  <tr>
  <th>Параметр</th>
  <th>Выбрать</th>
  </tr>
  </thead>`
  const ddd = document.querySelector('.scroll-table');
  let dd = document.createElement('div');
  dd.className='scroll-table-body'
  ddd.appendChild(t)
  ddd.appendChild(dd)
  const dddd = document.querySelector('.scroll-table-body');
  let tt = document.createElement('table');
  var tr =``
  obj1.params.forEach(el => {
  console.log(el)
  tr+='<tr>'
  + `<td>${el.set}</td>`
  + `<td><input type="checkbox" class="status" value="${el.set}"/></td>`
  + '</tr>';
  })
  tr+= '</tbody>'
  tt.innerHTML=tr
  dddd.appendChild(tt)
  // document.getElementById("table").innerHTML=tr;
  // document.getElementById("table").style.display='block';
  //document.getElementById("Res").style.display='block';
  
let b = document.createElement('input');
b.type="button"
b.value="Отправить"
b.className="but btn btn-secondary"
b.setAttribute('onclick',"GetResault()")
document.body.append(b)
}
  


function GetResault(){
document.getElementById("spinner").style.display='block';
let spin = document.getElementById("spinner")
console.log(spin, "Смотри сюда");

 param= getCheckBoxes()
 var json = JSON.stringify({
     airbus:document.getElementById("airbus").value,
     sys:document.getElementById("sys").value,
     fly:document.getElementById("fly").value,
     param: param,
   });
  //  console.log(json);
 var xr = new XMLHttpRequest()
 xr.open("POST","http://127.0.0.1:5000/forecast",false)
  xr.send(json)
  if (xr.status != 200) {
   // обработать ошибку
   alert( xr.status + ': ' + xr.statusText ); // пример вывода: 404: Not Found
 } else {
   // вывести результат
   let bro = document.getElementById('Bro')
   let pardiv = document.createElement('div')
   
   document.getElementById("spinner").style.display='none';
   pardiv.className = 'Val'
   document.body.append(pardiv)
   const PD = document.querySelector('.Val')
   
   
   //  console.log(xr.responseText)
   let Val2 = JSON.parse(xr.responseText)
   
   
   //  console.log(Val2)

   // PD.appendChild(newVal)
   
   
   const myImage = document.createElement('img')
   myImage.src=Val2.image;
   myImage.classList.add('Img')
   pardiv.innerHTML = `<span class="sp">${Val2.text}</span>`
 console.log(myImage)
 pardiv.appendChild(myImage)
 bro.appendChild(pardiv)

 let w100 = document.createElement('div')
 w100.className = "w-100"
 bro.appendChild(w100)



  //pardiv.innerHTML(myImage)
//pardiv.innerHTML=myImage


 }}
 

function getCheckBoxes() {
 var checkboxes = document.getElementsByClassName('status');
 var active = []
 for (var index = 0; index < checkboxes.length; index++) {
    if (checkboxes[index].checked) {
     active.push(checkboxes[index].value); 
    } 
 }
 return active
}


$(function() {
   $('#upload-file-btn').click(function() {
       var form_data = new FormData($('#upload-file')[0]);
       var response = ''
       $.ajax({
           type: 'POST',
           url: 'http://127.0.0.1:5000/uploadFiles',
           data: form_data,
           contentType: false,
           cache: false,
           processData: false,
           success: function(data) {
              response = data
              console.log(response)
              alert(JSON.stringify(data))
           }

       });
   });
});
