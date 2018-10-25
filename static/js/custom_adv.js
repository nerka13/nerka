  
function getRGBA(start, end, red,green,blue, interval=0.1){
	text = "";
		if (start > end){
		    for (var i=start; i>=end;i+=-interval){
		      text += ",rgba(" + red + "," + green + "," + blue + "," + i.toFixed(1) + ")"
		    }
		}
		else{
			for (var i=start; i<=end; i+=interval){
		      text += ",rgba(" + red + "," + green + "," + blue + "," + i.toFixed(1) + ")"
		    }
		}
	return text;
	};

function getGradient(rgba,mode="to top"){
	var text = "background: linear-gradient(" + mode + rgba + ")";
	return  text;
}
base = 217;
background = 255;
base_red = base;
base_green = base_red;
base_blue = base_red;
back_red = background;
back_green = back_red;
back_blue = back_red;
//Менее выпуклый
//rgba = getRGBA(start=1,end=0.1,red=base_red, green= base_green,blue=base_blue) + getRGBA(start=1,end=1,red=back_red, green= back_green,blue=back_blue);
//Более выпуклый
rgba = getRGBA(start=1,end=0.1,red=base_red, green= base_green,blue=base_blue) + getRGBA(start=1,end=1,red=back_red, green= back_green,blue=back_blue)+ getRGBA(start=0.1,end=1,red=base_red, green= base_green,blue=base_blue);


function setStyle(row=null,col=null,val=null){

  if (row!=null && col!=null && val!=null){
    row = document.getElementsByClassName("slick-row")[row]
    cell = row.getElementsByClassName("slick-cell")[col]
    if (val == 'y'){
      cell.firstElementChild.innerHTML = "  "
    } else {
      cell.firstElementChild.innerHTML = " "
    }
  }
   //---------------------------------------------------------------------------------------------------------------------------------------------------------------
   rows=document.getElementsByClassName('grid-canvas')[0].children
   for (var i=0; i< rows.length; i++){
      text = rows[i].innerHTML
      if (text.indexOf('grey') != -1){
        cells = rows[i].children
        for (var j=0; j<cells.length; j++){
          cells[j].style = getGradient(rgba, mode="to top");
        }
      }
   }

  //---------------------------------------------------------------------------------------------------------------------------------------------------------------

  var elements = document.getElementsByClassName("slick-cell")
 
  for (var i=0; i<elements.length; i++){
          if (elements[i].firstElementChild != null){

            if (elements[i].firstElementChild.innerHTML.charCodeAt(0) == 32 && elements[i].firstElementChild.innerHTML.charCodeAt(1) == 32 ){
            //elements[i].style = "background: linear-gradient(to right, rgba(232,106,48,1) 0%,rgba(255,145,1,1) 50%, rgba(200,67,0,1) 100%)" //оранжевый: Сб-Вс init
              elements[i].style = "background: linear-gradient(to right, #ffdac8 0%, #c0a395 100%)" //оранжевый: Сб-Вс
            }

            //Дежурство (Д)
            else if (elements[i].firstElementChild.innerHTML == 'Д' ){
            //elements[i].style = "background: linear-gradient(to right, rgba(232,106,48,1) 0%,rgba(255,145,1,1) 50%, rgba(200,67,0,1) 100%)"
            elements[i].style = "background: linear-gradient(to top,  #00BFFF 50%, #4682B4 100%)"; //синий: Дежурство
            elements[i].innerHTML = '';
            } 
            //Б/л (Б)
            else if (elements[i].firstElementChild.innerHTML == 'Б' ){
              elements[i].style = "background: linear-gradient(to top, #ffff99 50%, #ffcc66 100%)";//желтый: Б/л
              elements[i].style.color ="#7a5100";
              elements[i].style.fontWeight = "bold";
    
            }
            //Недомогание (Н)
            else if (elements[i].firstElementChild.innerHTML == 'Н'){
              elements[i].style = "background: linear-gradient(to top, #ffff99 50%, #ffcc66 100%)";//желтый: Недомогание
              elements[i].innerHTML = '';
            }
            //Плановый отпуск (П) 
            else if (elements[i].firstElementChild.innerHTML == 'П'){
              elements[i].style =  "background: linear-gradient(to top, rgb(134,238,248)  50%,  #90d5d5  100%)";  //бирюзовый: Плановый отпуск
              elements[i].innerHTML = '';
            }
            //Согласованный отпуск (О) дельфин
            else if (elements[i].firstElementChild.innerHTML == '🐬'){
              elements[i].style = "background: linear-gradient(to top,#00CED1  50%, #5F9EA0 100%)";//изумрудный: Отпуск
            }
            //серп и молот (Работа в выходной)
            else if (elements[i].firstElementChild.innerHTML.charCodeAt(0) == 9773){
              elements[i].style.fontSize = "large";
            }
          }
  }

  
}



