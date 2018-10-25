
 //if (params['unaltered'].indexOf(columns[i]['field']) ==-1)
//~~Setup GREY style~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
  var text = "linear-gradient(" + mode + rgba + ")";
  return  text;
}
var base = 217;
var background = 255;
var base_red = base_green = base_blue = base;
var back_red = back_green = back_blue = background;
//Менее выпуклый
//rgba = getRGBA(start=1,end=0.1,red=base_red, green= base_green,blue=base_blue) + getRGBA(start=1,end=1,red=back_red, green= back_green,blue=back_blue);
//Более выпуклый
var rgba = getRGBA(start=1,end=0.1,red=base_red, green= base_green,blue=base_blue) + getRGBA(start=1,end=1,red=back_red, green= back_green,blue=back_blue)+ getRGBA(start=0.1,end=1,red=base_red, green= base_green,blue=base_blue);  
var root = document.querySelector(':root');
var color = getGradient(rgba, mode="to top");
root.style.setProperty('--grey-color', color);
//End Setup~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

function HTMLformatter(row, cell, value, columnDef, dataContext) {
  if(value === 'y'){value = String.fromCharCode(32)}         //Сб-Вс_Праздники
  else if(value === 'n'){value = String.fromCharCode(32)}    //Будний день                                          
  else if(value === 'У'){value = String.fromCharCode(9728)}  //Утро                                         
  else if(value === 'В'){value = "\ud83c\udf19"}             //Вечер                                                        
  else if(value === 'Р'){value = String.fromCharCode(9773)}  //Сверхурочные
  else if(value === 'Д'){value = String.fromCharCode(32)}    //Дежурство
  else if(value === 'Н'){value = String.fromCharCode(32)}    //Недуг
  else if(value === 'П'){value = String.fromCharCode(32)}    //Плановый отпуск                                      
  else if(value === 'О'){value = "\ud83d\udc2c"}             //Согласованный отпуск                                                   
  else{value=value} 
  return value
};
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function setClass(columns,data,grid,unaltered,CSSclasses){
  var item;
  var hash = {};
  var colCollect = {};

  for (var key in CSSclasses){//--------------------------------------------------------------->key
    if (key == 'grey'){
      colStart = 0;
    }else{
      colStart = unaltered.length;
    }
    for (var i =0; i<data.length; i++){//-------------------------->i
      for (col=colStart; col<columns.length; col++){ //------------->col
        if (key == 'grey' && data[i]['grey']!='1'){//--->if
           break;
        }else{//-------------------------------------->else
          colId = columns[col].id;
          if (key=='grey'){//--------------~~~
            item = data[i]['grey'];
          } else{//------------------------~~~
            item = data[i][colId];
          }//------------------------------~~~
          if (item === CSSclasses[key][0]){
            colCollect[colId]=CSSclasses[key][1];
          }
        }//---------------------------------------------|if
      }//----------------------------------------------------|col
      if (Object.keys(colCollect).length!=0){
        hash[i] = colCollect;
      }
      colCollect = {};
    }//------------------------------------------------------------|i
    if (Object.keys(hash).length!=0){
      grid.setCellCssStyles(key, hash);
      hash = {};
    }
  }//------------------------------------------------------------------------------------|key
  //hash = { 0: { "id": "myClass","dep":"myClass"},  4: {"dep": "myClass"}}
};//end fun

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function addClass(column,row,item,grid,CSSclasses,oldVal){
  var col = column.id;
  var newVal = item[col];
  var CSSclasses_cut;
  var hash = {};

 //Delete old CSSclass
  CSSclasses_cut = $.extend({},CSSclasses);
  delete CSSclasses_cut.grey;
  var shifter = {};
  for (key in CSSclasses_cut ){
    shifter[CSSclasses_cut[key][0]] = [];
    shifter[CSSclasses_cut[key][0]].push(key);
    shifter[CSSclasses_cut[key][0]].push(CSSclasses_cut[key][1]);////-->{'Б':[sickness_leave:sickness]}
  };
 
  if(shifter[oldVal]){
    hash = grid.getCellCssStyles(shifter[oldVal][0]);//sickness_leave
    delete hash[row][col];
    grid.removeCellCssStyles(shifter[oldVal][0]);
    grid.addCellCssStyles(shifter[oldVal][0], hash)
  };

  hash = {};
  //Add new CSSclass
  if(shifter[newVal]){
    if (grid.getCellCssStyles(shifter[newVal][0])){
      hash = grid.getCellCssStyles(shifter[newVal][0]);
      if (hash[row]){
        hash[row][col] = shifter[newVal][1];
      }else{
        hash[row] = {};
        hash[row][col] = shifter[newVal][1];
      }
    }else{
      hash[row] = {};
      hash[row][col] = shifter[newVal][1]; //created hash={'2'-->row:{'15'-->col:myCSS}}
    }
    grid.removeCellCssStyles(shifter[newVal][0]);
    grid.addCellCssStyles(shifter[newVal][0], hash);
   };

  //grid.invalidate();
  grid.invalidateRow(row);
  grid.render();
  //hash = { 0: { "id": "myClass","dep":"myClass"},  4: {"dep": "myClass"}}
}//end fun

//--MAIN------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~-->CONST
var params = {'unaltered':['id','fio','dep','year','month']};
var CSSclasses = {'grey':['1','grey'],//grey-->keyHash; 1-->valueLogicRule; grey-->CSSclass
                 'holiday':['y','holiday'],
                 'morning':['У','symbol_medium'],
                 'evening':['В','symbol_medium'],
                 'overtime':['Р','symbol_large'],
                 'duty':['Д','duty'],
                 'sickness_leave':['Б','sickness'],
                 'sickness':['Н','sickness'],
                 'vacation_planned':['П','vacation_planned'],
                 'vacation':['О','vacation']
};
var selectOptions = {'У':'Утро', 'В':'Вечер', 'Р':'Работа','Д': 'Дежурство', 'Б':'Б/л', 'Н':'Недуг', 'П':'Плановый отпуск', 'О':'Отпуск', 'd':'delete'} 
var options = {
  enableCellNavigation: true,
  enableColumnReorder: false,
  editable:true,
  autoEdit: true,
  /*dataItemColumnValueExtractor: function(item, columnDef) {
    if(columnDef.editor == Slick.Editors.SelectOption){
      console.log('!!',columnDef.options,item[columnDef.field])
      //return eval(columnDef.options)[item[columnDef.field]];
      return item[columnDef.field]
    }else{
      return item[columnDef.field];
    }
  }*/
};
 

function getColumns(source){  
  //var columns_ini = JSON.parse(document.getElementById("dataServer").dataset.columns);
   var columns =  $.extend([],source);
  var width = 0;
  for (var i=0; i < columns.length; i++){
    
    if (columns[i].id != 'grey'){
      width+=columns[i]['width'];
      columns[i]['formatter'] = HTMLformatter;
      columns[i]['headerCssClass'] = 'header-center';
      //columns[i]['cssClass'] = 'center';
      columns[i]['minWidth'] = columns[i]['width'];
      columns[i]['resizable'] = false;
      if (params['unaltered'].indexOf(columns[i]['id']) ===-1){
        columns[i]['editor'] = Slick.Editors.SelectOption;
        columns[i]['options'] = selectOptions;
        //columns[i]['editor'] = Slick.Editors.Text;
      }
      if (columns[i].id === '1') {
        var select_marker = i
      }
    }else{
       var idx = i;
    }
   };
   columns.splice(idx,1);
   
   margin = 5;
   rectangleWidth = String(margin*2 + width+14) + 'px';
   containerWidth = String(margin*2 + width) + 'px';
   gridWidth = String(width)+'px'
   gridMargin = String(margin) + 'px';
   selectWidth = String(columns[select_marker].width)+'px';
   root.style.setProperty('--rectangle-width', rectangleWidth);
   root.style.setProperty('--container-width', containerWidth);
   root.style.setProperty('--grid-width', gridWidth);
   root.style.setProperty('--grid-margin', gridMargin);
   root.style.setProperty('--select-width', selectWidth); 

   return columns;
}
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~--|CONST
function getIndexes(storage,row,col){
      idx_row = storage['row'].indexOf(row)
      idx_col = storage['col'].indexOf(col)
      if (idx_row ==-1 || idx_col ==-1 ){
        return -1;
      }else{
        for (var i=idx_row;i<storage['row'].length;i++){
          for (var j=idx_row;j<storage['col'].length;j++){
            if (storage['row'][i] === row && storage['col'][j] === col){
              return j;
            }
          }
        }
      }
}
function getGrid(data,columns){
  var dataView = new Slick.Data.DataView();
  dataView.setItems(data);
  grid = new Slick.Grid("#myGrid", dataView, columns, options);
  setClass(columns,data,grid,params['unaltered'],CSSclasses);
  grid.setSelectionModel(new Slick.CellSelectionModel());
  return grid;
}

function getCellEvents(grid,columns,data){
  var index;
  var oldValCell;
  var storage ={'row':[],'col':[],'oldVal':[]} ;

  grid.onBeforeEditCell.subscribe(function (e, args) {
    oldVal = args.item[args.column.id]
    index = getIndexes(storage,args.row,args.cell);
    if (index > -1){
      storage['row'].splice(index,1,args.row);
      storage['col'].splice(index,1,args.cell);
      storage['oldVal'].splice(index,1,oldVal);
     }else{
      storage['row'].push(args.row);
      storage['col'].push(args.cell);
      storage['oldVal'].push(oldVal);
    }
  });

  grid.onCellChange.subscribe(function (e, args) {
    data_changed = data[args.row];
    column_changed = columns[args.cell];
    keyCol = column_changed.id;
    newVal = data_changed[keyCol];
    index = getIndexes(storage,args.row,args.cell);
    oldValCell = storage['oldVal'][index];
    dict = {};
    dict['id'] = data_changed.id;
    dict['key'] = keyCol;
    dict['newVal'] = newVal;
    if($(".editor-select").children('option:selected').index() >=0){
      jQuery.ajax({
                    type: 'POST',
                    url: '/data',
                    dataType: 'json',
                    data: dict,
                    success: function (response) {
                      data[args.row][keyCol] = response;
                      data_changed = data[args.row];
                      column_changed = columns[args.cell];
                      row_changed = args.row;
                      old = oldValCell
                      addClass(column_changed,row_changed,data_changed,grid,CSSclasses,oldValCell);
                    },
                    error: function() {
                      alert("An error occured!");
                    }
      });
    }

  });

  // Make the grid respond to DataView change events.
  /*
  dataView.onRowCountChanged.subscribe(function (e, args) {
    grid.updateRowCount();
    grid.render();
  });

  dataView.onRowsChanged.subscribe(function (e, args) {
    grid.invalidateRows(args.rows);
    grid.render();
  });
  */

} 

function getChecker1(){
  radioValueOld = $("input:checked");
  $(".checker").click(function(){
    //cnt+=1;
    //radioValueOld.removeAttr('checked');
    //console.log('WAS_'+cnt,radioValueOld.val());
    curr = $(this).val();
    var radioValue = $("input:checked").val();
    //$("input:checked").attr( 'checked', 'checked');
    //console.log('NOW_'+cnt,$("input:checked").val());
    //a=$("input")
    
    inp = $("input");
    for(var i=0; i<inp.length;i++){
      //if (inp[i].val() <> curr){

      //}
      console.log('here',inp[i]);

    }
    //$("input:checked").each(function () {
    //                var name = $(this).val()
    //                //Checking whether radio button is selected and based on selection setting variable to true or false
    //                console.log('!!!!',name);
     //           });

    
    jQuery.ajax({
                  type: 'POST',
                  url: '/table',
                  dataType: 'json',
                  data:{month:radioValue},
                  success: function (response) {
                    $("#dataServer").removeAttr('data-columns');
                    $("#dataServer").removeAttr('data-source');
                    $("#dataServer").attr('data-columns',response.columns);
                    $("#dataServer").attr('data-source',response.data);
                    colSource = JSON.parse(document.getElementById("dataServer").dataset.columns);
                    columns = getColumns(colSource);
                    data = JSON.parse(document.getElementById("dataServer").dataset.source);
                    grid = getGrid(data,columns);
                    grid.render();
                    getEvents(grid,columns,data);
                  },
                  error: function() {
                    alert("An error occured!");
                  }
    });
  });
}



function getChecker(){
  radioValueOld = $("input:checked");

  $(".checker").click(function(){
    //cnt+=1;
    //radioValueOld.removeAttr('checked');
    //console.log('WAS_'+cnt,radioValueOld.val());
    curr = $(this).val();
    var radioValue = $("input:checked").val();
    //$("input:checked").attr( 'checked', 'checked');
    //console.log('NOW_'+cnt,$("input:checked").val());
    //a=$("input")
    
    inp = $("input");
    for(var i=0; i<inp.length;i++){
      //if (inp[i].val() <> curr){

      //}
      console.log('here',inp[i]);

    }
    //$("input:checked").each(function () {
    //                var name = $(this).val()
    //                //Checking whether radio button is selected and based on selection setting variable to true or false
    //                console.log('!!!!',name);
     //           });

    
   
  });
}

function getEvents(grid,columns,data){
  getCellEvents(grid,columns,data);
  //getChecker();

}
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~--|FUNCTIONS
$(function () {

  var colSource = JSON.parse(document.getElementById("dataServer").dataset.columns);
  var columns = getColumns(colSource);
  var data = JSON.parse(document.getElementById("dataServer").dataset.source);
  var grid = getGrid(data,columns);
  grid.render();
  //------------------------------------------------------------------------------------------------------------------------------------------------------------------------->EVENTS
  getEvents(grid,columns,data);
  radioValueOld = $("input:checked");
  //-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|EVENTS
  
  //$(".checker").blur(function(){
  //  radioValueOld = $(this);
  //});

  $(".checker").click(function(){
    radioValueOld.removeAttr('checked');
    console.log('OLD',radioValueOld.val());
    var radioValue = $("input:checked").val();
    $("input:checked").attr( 'checked', 'checked');
    radioValueOld = $("input:checked");
    inp = $("input");
    for(var i=0; i<inp.length;i++){
        console.log('here',inp[i]);

    }

    jQuery.ajax({
                  type: 'POST',
                  url: '/table',
                  dataType: 'json',
                  data:{month:radioValue},
                  success: function (response) {
                    $("#dataServer").removeAttr('data-columns');
                    $("#dataServer").removeAttr('data-source');
                    $("#dataServer").attr('data-columns',response.columns);
                    $("#dataServer").attr('data-source',response.data);
                    colSource = JSON.parse(document.getElementById("dataServer").dataset.columns);
                    columns = getColumns(colSource);
                    data = JSON.parse(document.getElementById("dataServer").dataset.source);
                    grid = getGrid(data,columns);
                    grid.render();
                    getEvents(grid,columns,data);
                  },
                  error: function() {
                    alert("An error occured!");
                  }
    });
  });




  $('ul.tabs li').click(function(){
      console.log('VVVVVV');
      var tab_id = $(this).attr('data-tab');
      $('ul.tabs li').removeClass('current');
      $('.tab-content').removeClass('current');
      $(this).addClass('current');
      $("#"+tab_id).addClass('current');
      radioValueOld.removeAttr('checked');
      radioValue = $("input[value='current']");
      radioValue.attr('checked','checked');
      console.log('XXX',radioValue.attr('id'));
           
      //radioValue.css();
      radioValueOld = radioValue;
      //var n = tab_id.indexOf("-");
      //idx = tab_id.substring(n+1,tab_id.length);
      colSource = JSON.parse(document.getElementById("dataServer").dataset.columns);
      columns = getColumns(colSource);
      data = JSON.parse(document.getElementById("dataServer").dataset.source);
      grid = getGrid(data,columns);
      getEvents(grid,columns,data);

  });

})


//https://github.com/6pac/SlickGrid/wiki/Examples
//http://6pac.github.io/SlickGrid/examples/example-dynamic-with-jquery-tabs.html
//https://github.com/6pac/SlickGrid/blob/master/examples/example-dynamic-with-jquery-tabs.html