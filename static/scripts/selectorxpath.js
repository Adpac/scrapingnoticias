var posicion="arriba";
var seleccionar=false;
var colormouseover="rgba(255,255,0, 0.5)";
var colorclick="rgba(241, 220, 0, 0.5)";
var campoinput="";
var seleccion=0;
var numerodeinputs=8;
var seleccionmultiple=[1,2,3,4,5,6]

  const botones=document.querySelectorAll("[onclick]");
for( boton of botones){
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
//..
var listacolores=["rgba(0,143,76,0.5)","rgba(128,0,128,0.5)","rgba(234,193,2,0.5)","rgba(0,113,188,0.5)","rgba(141,0,54,0.5)","rgba(175,110,55,0.5)","rgba(255,102,0,0.5)","rgba(252,209,198,0.5)","rgba(81,209,246,0.5)","rgba(128,128,128,0.5)","rgba(204,0,0,0.5)","rgba(255,90,54,0.5)","rgba(255,186,0,0.5)","rgba(255,126,0,0.5)","rgba(0,66,37,0.5)","rgba(27,65,37,0.5)","rgba(0,97,169,0.5)","rgba(209,235,247,0.5)","rgba(150,200,162,0.5)","rgba(129,216,208,0.5)","rgba(0,26,87,0.5)","rgba(65,125,193,0.5)","rgba(83,104,149,0.5)","rgba(145,163,176,0.5)","rgba(245,245,220,0.5)","rgba(62,174,177,0.5)","rgba(206,70,118,0.5)","rgba(151,127,115,0.5)","rgba(201,174,93,0.5)","rgba(243,229,171,0.5)","rgba(80,64,77,0.5)","rgba(103,49,71,0.5)","rgba(84,61,63,0.5)","rgba(145,163,176,0.5)","rgba(129,135,139,0.5)","rgba(196,30,58,0.5)","rgba(193,154,107,0.5)","rgba(86,57,112,0.5)","rgba(228,155,15,0.5)","rgba(252,247,94,0.5)","rgba(248,222,126,0.5)","rgba(238,223,160,0.5)","rgba(184,41,40,0.5)","rgba(34,34,34,0.5)","rgba(72,60,50,0.5)","rgba(59,49,33,0.5)","rgba(103,76,71,0.5)","rgba(172,92,181,0.5)","rgba(217,144,88,0.5)","rgba(255,153,102,0.5)","rgba(178,27,28,0.5)","rgba(237,135,45,0.5)","rgba(217,144,88,0.5)","rgba(135,0,116,0.5)","rgba(96,47,107,0.5)","rgba(96,78,151,0.5)","rgba(250,214,165,0.5)","rgba(138,154,91,0.5)","rgba(147,197,146,0.5)","rgba(126,159,46,0.5)","rgba(143,151,121,0.5)","rgba(174,32,41,0.5)","rgba(114,47,55,0.5)"];
document.body.addEventListener("mouseover",(e)=>{
    if(seleccionar==true){
        console.log("llegue aqui");
        try {
            //Con el if evitamos la deseleccion de un elemento click
            anterior.style.backgroundColor=coloranterior;   
        }catch (error){
        }
        let selector = document.querySelector(".selector");
        // selector output
        anterior=e.target;
        coloranterior=e.target.style.backgroundColor;
        if(e.target.getAttribute("marcar")!="nopintar"){
            let output = getPathTo(e.target);
            e.target.style.backgroundColor=colormouseover;
            console.log(e.target);
            selector.innerHTML = `<strong>Selector:</strong> ${output}`;
        
        }
        pintarelementos(1);
        pintarelementos(2);
        pintarelementos(3);
        pintarelementos(4);
        pintarelementos(5);
        pintarelementos(6);
    }

});
function recortarxpath(xpath, simbolo){
    //El simbolo es un elemento xpath que si o si queremos conservar
    arrayxp=xpath.split("/")
    devolver=""
    encontrosimbolo=false
    for(var i=1; i<arrayxp.length; i++){
        devolver=devolver+"/"+arrayxp[i];
        seccionxp=arrayxp[i];
        seccionxp=seccionxp.replaceAll(/ *\[[^)]*\] */g, "");
        seccionxp=seccionxp.replaceAll(/[0-9]/g, '');
        console.log("seccion: "+seccionxp)
        if(seccionxp==simbolo){
            encontrosimbolo=true
            break;
        }
    
    }
    return devolver;
}
document.body.addEventListener("click",(e)=>{
    if(seleccionar==true){
        if(e.target.getAttribute("marcar")!="nopintar"){
            enlaceel=e.target.getElementsByTagName("a")
            console.log("enlace.....")
            xpathelemento=getPathTo(e.target);

            xpathoptim=(xpathelemento);
            if(seleccion==1){
                xpathoptim=recortarxpath(xpathoptim,"a")
            }
            if(seleccion==4){
                xpathoptim=recortarxpath(xpathoptim,"img")
            }
            var elementohtml=new Object();
            elementohtml.xpath=xpathoptim;
            elementohtml.elemento=e.target;
            var seguirseleccionando=true;
            document.getElementById("input"+seleccion).value=xpathoptim
            if(seleccionmultiple.includes(seleccion)){
                
                var elem = document.getElementById('myDropdown'+seleccion);
                elem.insertAdjacentHTML('beforeend', '<p class="delete" marcar="nopintar" xp="'+elementohtml.xpath+'">'+elementohtml.elemento.innerText+'<br> url=('+elementohtml.elemento.href+')<br><button marcar="nopintar" type="button">Eliminar</button></p>');
                var listaelems=elem.getElementsByClassName("delete")
                var numelementos=listaelems.length
                if(numelementos>=2){
                    listaxpath=[]
                    for(var i=0; i<numelementos; i++){
                        xpelement=listaelems[i].getAttribute("xp")
                        listaxpath.push(xpelement);
                        console.log(xpelement)
                    }
                    xpathvalido=generarxpathmultiple2(listaxpath)
                    document.getElementById("input"+seleccion).value=xpathvalido
                    seguirseleccionando=false
                }

            }
           
            //FIn eliminar
            pintarelementos(seleccion);
            if(!seguirseleccionando){
                seleccionarcampo(seleccion);
            }
            
        }
         //En caso de hacer click en el boton eliminar 
        elements = document.getElementsByClassName("delete");
        $(".delete").on("click", "button", function(e) {
            e.preventDefault();
            xpathelim=$(this).parent().attr("xp");
            
            $(this).parent().remove();
        });
    }

});
function seleccionarcampo(campo){
        console.log("Seleccion: "+campo)
        colormouseover=listacolores[campo-1];
        colorclick=listacolores[campo-1];
        if(seleccion==campo){
            seleccionar=false
            seleccion=0;
            document.getElementById("pintartag"+campo).innerText="Seleccionar";
        }else{
            seleccionar=true;
            seleccion=campo;
            for(var i=1; i<= numerodeinputs; i++){
                //Cambiamos los valores de los botones
                idboton="pintartag"+i;
                boton=document.getElementById(idboton);
                
                if(i==campo){
                    console.log(idboton);
                    boton.innerText="Deshabilitar";
                }else{
                    boton.innerText="Seleccionar";
                }
            }
        }
    
    }
    function stringContainsNumber(_input){
        let string1 = String(_input);
        for( let i = 0; i < string1.length; i++){
            if(!isNaN(string1.charAt(i)) && !(string1.charAt(i) === " ") ){
              return true;
            }
        }
        return false;
      }
    function getPathTo(element) {
    if (element.id !== '' && !stringContainsNumber(String(element.id)))
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
function pintarelementos(numinput){
var entrada=document.getElementById("input"+numinput)
var xpathentrada=entrada.value;


try {
        //dejamos de pintar los anteriores elementos con el color del input numinput
    var elementospintados=document.querySelectorAll('[seleccion="seleccion'+numinput+'"]');
    for(elemento of elementospintados){
                if(elemento.getAttribute("estado")!="seleccionado"){
                   elemento.style.backgroundColor="";
                   elemento.style.border="";
                }
            }
    console.log(xpathentrada);
    textoxpath=""
    try{
        listapint=getElementsByXPath(xpathentrada);
        entrada.setCustomValidity("");
        for(var i=0; i<listapint.length; i++){
            element=listapint[i];
            element.style.backgroundColor=listacolores[numinput-1];
            element.setAttribute("seleccion","seleccion"+numinput);
            element.style.border="thick solid "+listacolores[numinput-1];
            textoxpath=textoxpath+element.innerText+" ";
            if(numinput==1){
                textoxpath=textoxpath+element.href+" ";
            }
            if(numinput==4){
                textoxpath=textoxpath+element.src+" ";
            }
        }
    }catch(Exception){
        console.log("Error: "+xpathentrada)
        listapint=null;
        $('#datos'+numinput).empty();
        if(xpathentrada!=""){
            entrada.setCustomValidity("Xpath no valido");
        }
    }
   

    $('#datos'+numinput).empty();
    $('#datos'+numinput).append(String(textoxpath));
    textoxpath=""

} catch (error) {
    console.error(error);
}





}
//
function getElementsByXPath(xpath, parent){
    let results = [];
    let query = document.evaluate(xpath, parent || document,null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
    for (let i = 0, length = query.snapshotLength; i < length; ++i) {
        results.push(query.snapshotItem(i));
    }
    return results;
}
function optimizarxpath(xpathentrada){
xpathsalida=xpathentrada;
elementosxpth=xpathentrada.split("/");
for(var i=0; i<elementosxpth.length; i++){
    elemento=elementosxpth[i];
    
    nombrenodo=elemento.replaceAll(/ *\[[^)]*\] */g, "");
    remplazar="/"+elemento;
    if(elemento!="" || elemento!=" " || !nombrenodo!="a"){
        console.log("remplazar: ",remplazar);
        aux=xpathsalida.replace(remplazar,"");
        var consultaaux=getElementsByXPath(aux);
        var consultaactual=getElementsByXPath(xpathsalida);
        console.log("Xpactual="+xpathsalida);
        console.log("xpaux: "+aux);
        console.log(consultaactual)
        console.log(consultaaux)
        if(compararelementosxp(consultaactual,consultaaux)){
            xpathsalida=aux;
        }else{
            aux=xpathsalida.replace(remplazar,"/"+nombrenodo);
             consultaaux=getElementsByXPath(aux);
             consultaactual=getElementsByXPath(xpathsalida);
            if(compararelementosxp(consultaactual,consultaaux)){
                xpathsalida=aux;
            }
        }

    }
    console.log("Xpahsalida: ..."+xpathsalida)
}
return xpathsalida;
}

function compararelementosxp(elema, elemb){
    retornar=false
    if(elema.length==elemb.length){
        for(var i=0; i<elema.length; i++){
            if(elema[i].isSameNode(elemb[i])){
                retornar=true
            }else{
                retornar=false
                break
            }
        }
    }
    return retornar
}
function cambiarposicion(){
    if(posicion=="arriba"){
        document.getElementById("xpathmenu").setAttribute("class","xpathmenuabajo")
        posicion="abajo";
        document.getElementById("btncambiarposicion").innerText="Cambiar Arriba";
    }else{
        document.getElementById("xpathmenu").setAttribute("class","xpathmenu")
        posicion="arriba";
        document.getElementById("btncambiarposicion").innerText="Cambiar Abajo";
    }
}


 function mostrarlista(numlista){
    document.getElementById("myDropdown"+String(numlista)).classList.toggle("show");    
 }        
 
 function eliminardelista(xpath){
    var listaaux=new Array();
    console.log("xp............");
    console.log(xpath);
    console.log(xpath);
    var elem=getElementByXpath(xpath);
    elem.setAttribute("color", "none");
  

}
function getElementByXpath(path) {
    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

function generarxpathmultiple(lista){
    //Dado ciertos Xpaths generamos un xpath generico
    var xp=""
    var arrayaux=new Array();
    for(let i=0; i<lista.length; i++){
        var arrayelemento=lista[i].split("/");
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
    //xp=optimizarxpath2(xp);
    return xp;
    }
function generarxpathmultiple2(lista){
    devolver=""
    listaelementos=[]
    numcolumnas=Number.MAX_VALUE;
    for(var i=0; i<lista.length; i++){
        //EL primer for seleccionara los xpaths
        xparray=lista[i].split("/");
        listaelementos.push(xparray.reverse())
        if(numcolumnas<xparray.length){
            numcolumnas=xparray.length
        }

    }
    numfilas=listaelementos.length;
    iterar:
    for(i=0; i<numcolumnas; i++){
        nombrenodoaux=""
        corchetenotoaux=""
        for(j=0; j<numfilas; j++){
            nodo=listaelementos[j][i]
            nombrenodo=nodo.replaceAll(/ *\[[^)]*\] */g, "");
            corchetenodo=nodo.replace(nombrenodo,"");
            console.log(nombrenodo)
            console.log(corchetenodo);
            console.log("Nodo: "+nodo)
            if(j==0){
                nombrenodoaux=nombrenodo;
                corchetenotoaux=corchetenodo;
            }else{
                if(nombrenodo==nombrenodoaux && nodo!=""){
                    if(corchetenotoaux!=corchetenodo){
                        corchetenotoaux=""
                    }
                }else{
                    break iterar;
                }
            }
        }
        console.log("////////////////////")
        if(devolver!=""){
            devolver=nombrenodoaux+corchetenotoaux+"/"+devolver
        }else{
            devolver=nombrenodoaux+corchetenotoaux
        }

        
    }
    devolver="//"+devolver
    devolver=optimizarxpath2(devolver)
    return devolver
}
    function optimizarxpath2(xpath){
        xparray=xpath.split("/")
        xpdevolver="/"+xparray[xparray.length-1]
        consultaoriginal=getElementsByXPath(xpath);
        añadirguion=false;
        for(var i=xparray.length-2; i>1; i--){
            nodo=xparray[i]
            nombrenodo=nodo.replaceAll(/ *\[[^)]*\] */g, "");
            xpincompleto=""
            for(var j=1; j<i; j++){
                if(!(xparray[j]=="" && j==i-1)){
                    xpincompleto=xpincompleto+"/"+xparray[j]

                }
                
            }
            if(xpincompleto!="/"){
                xpincompleto=xpincompleto+"/"
            }
            
            console.log("xpi: "+xpincompleto)
            console.log("xpd: "+xpdevolver)
            xpathprueba=xpincompleto+xpdevolver
            console.log("xpprueba: "+xpathprueba)
            consultaaux=getElementsByXPath(xpathprueba);
            if(nodo!=""){
                if(!compararelementosxp(consultaoriginal,consultaaux)){
                    if(añadirguion){
                        nombrenodo=nombrenodo+"/"
                        nodo=nodo+"/"
                        añadirguion=false
                    }
    
                    xpdevolveraux="/"+nombrenodo+xpdevolver
                    xpathprueba=xpincompleto+xpdevolveraux
                    consultaaux=getElementsByXPath(xpathprueba);
                    console.log()
                    if(!compararelementosxp(consultaoriginal,consultaaux)){
                        xpdevolver="/"+nodo+xpdevolver
                        console.log("xpdevolveraux "+xpdevolveraux)
                        console.log("detencion3"+xpathprueba)
                    }else{
                        xpdevolver=xpdevolveraux
                        console.log("detencion2"+xpathprueba)
                    }
                }else{
                    console.log("detencion1")
                    //xpdevolver="/"+xpdevolver
                    añadirguion=true;
                }   
            }

                
        }
        xpdevolver="/"+xpdevolver
        return xpdevolver
    }