var seleccionar=false;
var seleccion2=false; //detectara si la seleccion es del selector de la pagina siguiente
function habilitarseleccion(){
    seleccionar=!seleccionar;
    if(seleccionar==true){
        document.getElementById("pintartag").textContent="Deshabilitar"
    }else{
        document.getElementById("pintartag").textContent="Seleccionar"
    }
}
function habilitarseleccion2(){
    seleccionar=!seleccionar;
    if(seleccionar==true){
        seleccion2=true;
        document.getElementById("pintartag2").textContent="Deshabilitar"
    }else{
        seleccion2=false;
        document.getElementById("pintartag2").textContent="Seleccionar"
    }
}
var anterior
var coloranterior
var bordeanterior
var listaelemhref=new Array()
var elements
//desactivando enlaces
//desactivando los botones 
const botones=document.querySelectorAll("[onclick]");
for( boton of botones){
    console.log(boton);
    if(boton.getAttribute("marcar")!="nopintar"){
        boton.setAttribute("clickenfuncion",boton.getAttribute("onclick"));
        boton.setAttribute("onclick","return false")
    }
}
//Al momento de hacer click en un enlace no se redireccionara a la pagina web de la noticia
const enlaces=document.getElementsByTagName("a");
for( enlace of enlaces){
    enlace.setAttribute("onclick","return false");
}
//..................................................
//Generar XPaths Multiples algoritmos
//Algoritmo 1 de Xpath
function getPathTo(element) {
        if (element.id !== '')
            return "//*[@id='" + element.id + "']";
        if (element === document.body)
            return "/";
        var ix = 0;
        var siblings = element.parentNode.childNodes;
        for (var i = 0; i < siblings.length; i++) {
            var sibling = siblings[i];
            if (sibling === element)
                return getPathTo(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
            if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                ix++;
            }
        }
    }
//Algoritmo 2 de Xpath
    function createXPathFromElement(elm) { 
        var allNodes = document.getElementsByTagName('*'); 
        contador=0;
        for (var segs = []; elm && elm.nodeType == 1; elm = elm.parentNode) 
        { 
            contador++;
            if (elm.hasAttribute('id')) { 
                
                    var uniqueIdCount = 0; 
                    for (var n=0;n < allNodes.length;n++) { 
                        if (allNodes[n].hasAttribute('id') && allNodes[n].id == elm.id) uniqueIdCount++; 
                        if (uniqueIdCount > 1) break; 
                    }; 
                    if ( uniqueIdCount == 1) { 
                        segs.unshift('id("' + elm.getAttribute('id') + '")'); 
                        return segs.join('/'); 
                    } else { 
                        segs.unshift(elm.localName.toLowerCase() + '[@id="' + elm.getAttribute('id') + '"]'); 
                    } 
            } else if (elm.hasAttribute('class')) { 
                segs.unshift(elm.localName.toLowerCase() + '[@class="' + elm.getAttribute('class') + '"]'); 
            } else { 
                for (i = 1, sib = elm.previousSibling; sib; sib = sib.previousSibling) { 
                    if (sib.localName == elm.localName)  i++; }; 
                    segs.unshift(elm.localName.toLowerCase() + '[' + i + ']'); 
            }; 
            if (contador==37){
                break;
            }
        }; 

        let xpath=segs.length ? '/' + segs.join('/') : null
        if(contador==37){
            xpath='/'+xpath;
        }
        return xpath; 
    }; 

    function lookupElementByXPath(path) { 
        var evaluator = new XPathEvaluator(); 
        var result = evaluator.evaluate(path, document.documentElement, null,XPathResult.FIRST_ORDERED_NODE_TYPE, null); 
        return  result.singleNodeValue; 
    } 
    
//.......................................
  // mouse over, encima de elemento
    document.body.addEventListener("mouseover", (e) => {
        if(seleccionar==true){
            try {
                if(anterior.getAttribute("color")!="verde"){

                    anterior.setAttribute("color",coloranterior)
                }
                
            }catch (error){
            
            }
            let selector = document.querySelector(".selector");
            // selector output
            anterior=e.target;
            coloranterior=e.target.getAttribute("color");
            
            if(e.target.getAttribute("marcar")!="nopintar" && e.target.getAttribute("color")!="verde"  ){
                if(seleccion2){
                    e.target.setAttribute("color","amarillo");
                }else{
                    e.target.setAttribute("color","naranja");
                }
                
                let output = getPathTo(e.target);
                console.log(output)
                selector.innerHTML = `<strong>Selector:</strong> ${output}`;
            }
        }
    
  });

  
  document.body.addEventListener("click", (e) => {
      
        if(seleccionar==true){
            
            try {
                //Con el if evitamos la deseleccion de un elemento click
                if (anterior.getAttribute("color")!="verde"){
                    anterior.setAttribute("color",coloranterior);
                    
                }
                
            }catch (error){
            
            }
            let selector = document.querySelector(".selector");
            // selector output
            anterior=e.target;
            coloranterior=e.target.getAttribute("color");
            
            if(e.target.getAttribute("marcar")!="nopintar"){
                var elementohtml=new Object();
                let output = getPathTo(e.target);
      
                if(!seleccion2){
                    e.target.setAttribute("color","verde")
            
                    elementohtml.xpath=output;
                    elementohtml.elemento=e.target;
                    listaelemhref.push(elementohtml);
                    var elem = document.getElementById('myDropdown');
                    elem.insertAdjacentHTML('beforeend', '<p class="delete" marcar="nopintar" xp="'+elementohtml.xpath+'">'+elementohtml.elemento.innerText+'<br> url=('+elementohtml.elemento.href+')<br><button marcar="nopintar">Eliminar</button></p>');
                    elements = document.getElementsByClassName("delete");
                    $(".delete").on("click", "button", function(e) {
                        e.preventDefault();
                        xpathelim=$(this).parent().attr("xp");
                        eliminardelista(xpathelim);
                        $(this).parent().remove();
                    });
                    cambiarcolorlista();
                   
                    if(listaelemhref.length>=2){
                        xpgen=generarxpathmultiple(listaelemhref);
                        document.getElementById("inputxpenlace").value=optimizarxpath(xpgen);
                        habilitarseleccion();
                        pintarxp();
                        
                    }

                }else{
                    
                    document.getElementById("xpinputsig").value=optimizarxpath(output);
                    habilitarseleccion2();
                    pintarplomo();
                    enlacesig=getElementByXpath(output).href;
                    
                    if(enlacesig=== undefined){
                        enlacesig=getElementByXpath(output).getAttribute("clickenfuncion");
                        if(enlacesig==undefined){
                            document.getElementById("datosinputsig").innerText="No se selecciono una paginacion";
                        }else{
                            document.getElementById("datosinputsig").innerText="Página Web Dinamica";
                            document.getElementById("tipopagina").value="dinamica"
                        }
                    }else{
                        if(enlacesig==""){
                            document.getElementById("tipopagina").value="dinamica"
                            document.getElementById("datosinputsig").innerText="url vacia se tomara a la pagina como dinamica";
                        }else{
                            document.getElementById("tipopagina").value="nodinamica"
                            document.getElementById("datosinputsig").innerText="URL="+enlacesig;
                        }
                        
                    }
                    
                    
                }
            

           
                selector.innerHTML = `<strong>Selector:</strong> ${output}`;
            
            }
        }
    
  });


function generarxpathmultiple(lista){
//Dado ciertos Xpaths generamos un xpath generico
var xp=""
var arrayaux=new Array();
for(let i=0; i<lista.length; i++){
    var arrayelemento=lista[i].xpath.split("/");
    for (let j=0;j < arrayelemento.length; j++){
        if(arrayaux.length==j){
            arrayaux.push(arrayelemento[j]);
        }else{
            if(arrayaux[j]!= arrayelemento[j] && arrayelemento[j]!=""){
                arrayaux[j]=arrayaux[j].replace("[","");
                arrayaux[j]=arrayaux[j].replace(/[0-9]/g,"");
                arrayaux[j]=arrayaux[j].replace("]","")
            }
        }
    }
}
for(let i=0; i<arrayaux.length; i++){
    xp=xp+"/"+arrayaux[i];
}

contbarra=0;
for(let i=0; i<xp.length-1; i++){
    if(xp.substring(i,i+1)=="/"){
        contbarra++;
    }else{
        break
    }
}
if(contbarra==1){
    xp="/"+xp
}
if(contbarra>2){
    xp=xp.substring(contbarra-2);
}
xp=optimizarxpath(xp);
return xp;
}
/*
function bindIFrameMousemove(iframe){
    iframe.contentWindow.addEventListener('mousemove', function(event) {
        var clRect = iframe.getBoundingClientRect();
        var evt = new CustomEvent('mousemove', {bubbles: true, cancelable: false});

        evt.clientX = event.clientX + clRect.left;
        evt.clientY = event.clientY + clRect.top;
        console.log
        iframe.dispatchEvent(evt);
    });
};

bindIFrameMousemove(document.getElementById('iFrameId'));
*/

//actualizar input enlaces
function pintarplomo(){//pintamos el elemento del input2
            //dejamos de pintar los anteriores elementos seleccionados
        try{
            var elementospintados=document.querySelectorAll('[color="plomo"]');
            for(elemento of elementospintados){
                if(elemento.getAttribute("estado")!="seleccionado"){
                    elemento.setAttribute("color","none");
                   
                }
            }
            //íntamos los valores actuales
            var valuexp=document.getElementById("xpinputsig").value;
            pintar=getElementsByXPath(valuexp,"plomo");
        }catch(e){
            pintarxp();
        }

            
            
}
function pintarxp(){
    try{
        
        $("#inputxpenlace").on('keyup', function(){
            //dejamos de pintar los anteriores elementos seleccionados
            var elementospintados=document.querySelectorAll('[color="rojo"]');
            for(elemento of elementospintados){
                if(elemento.getAttribute("estado")!="seleccionado"){
                    elemento.setAttribute("color","none");
                }
            }
            //pintamos los valores actuales
            var value = $(this).val();
            lista=getElementsByXPath(value);
            
           
        }).keyup();
    }catch(e){
     
    }
}
window.onload = (function(){

    pintarxp();
});
//Obtener un elemento mediante xpath
function getElementByXpath(path) {
    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}
//obtener varios elementos mediante xpath
function getElementsByXPath(xpath, colorp,parent)
{
let results = [];
let query = document.evaluate(xpath, parent || document,
    null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
for (let i = 0, length = query.snapshotLength; i < length; ++i) {
    if(query.snapshotItem(i).getAttribute("estado")!="seleccionado"){
  
        query.snapshotItem(i).setAttribute("color",colorp || "rojo");
        pintarlista();
    }else{
        color=query.snapshotItem(i).getAttribute("color")+colorp|| "rojo";
        query.snapshotItem(i).setAttribute("color",color);
    }
    
    results.push(query.snapshotItem(i));
}
return results;
}
function getElementsByXPath2(xpath, parent){
    let results = [];
let query = document.evaluate(xpath, parent || document,
    null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
for (let i = 0, length = query.snapshotLength; i < length; ++i) {
    results.push(query.snapshotItem(i));
}
return results;
}

//eliminar selecionados


//Lista elementos seleccionados
function mostrarlista() {
    document.getElementById("myDropdown").classList.toggle("show");
}
  
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }

  //Eliminar de la lista


//Seleccionar elemento de una lista
/*
function pintarelemento(xpa, color){
var elemento=getElementByXpath(xpa);
elemento.setAttribute("color",color);
}

for (var i = 0; i < elements.length; i++) {
    console.log
    console.log("llegue aqui");
    elements[i].addEventListener('mouseover', pintarelemento(elements[i].getAttribute('xp'), "naranja"));
}*/

function pintarlista(){
    for (var i=0; i<listaelemhref.length; i++){
        var xp=listaelemhref[i].xpath;
        var elem=getElementByXpath(xp);
        console.log("Xpath cod...")
        console.log(xp);
        elem.setAttribute("color", "verde");
    }
}

function eliminardelista(xpath){
    var listaaux=new Array();
    for (var i=0; i<listaelemhref.length; i++){
        var xp=listaelemhref[i].xpath;
        if(xp!=xpath){
            listaaux.push(listaelemhref[i]);
        }
    }
    listaelemhref=listaaux;
    console.log("xp............");
    console.log(xpath);
    console.log(xpath);
    var elem=getElementByXpath(xpath);
    elem.setAttribute("color", "none");
    pintarxp();

}

function cambiarcolorlista(){
    document.getElementById("btnlista").setAttribute("color","plomo");
    setTimeout(function() {document.getElementById("btnlista").setAttribute("color","none")}, 200);
    
}

//Optimizaremos el xpath, de forma que el mismo funcione la mayor cantidad de veces
function optimizarxpath(xpathentrada){
xpathsalida=xpathentrada;
elementosxpth=xpathentrada.split("/");
for(var i=0; i<elementosxpth.length; i++){
    elemento=elementosxpth[i];
    remplazar="/"+elemento;
    if(elemento!="" || elemento!=" "){
        console.log("remplazar: ",remplazar);
        aux=xpathsalida.replace(remplazar,"");
        var consultaaux=getElementsByXPath2(aux);
        var consultaactual=getElementsByXPath2(xpathsalida);
        console.log("Xpactual="+xpathsalida);
        console.log("xpaux: "+aux);
        if(consultaaux.length==consultaactual.length){
            xpathsalida=aux;
        }else{
            console.log("no son iguales");
            break;
        }

    }

}
return xpathsalida;
}