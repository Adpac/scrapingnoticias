//desactivando los botones 
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
var listacolores=["rgba(0,113,188,0.5)","rgba(0,143,76,0.5)","rgba(128,0,128,0.5)","rgba(234,193,2,0.5)","rgba(141,0,54,0.5)","rgba(170,0,0,0.5)","rgba(175,110,55,0.5)","rgba(255,102,0,0.5)","rgba(252,209,198,0.5)","rgba(81,209,246,0.5)","rgba(128,128,128,0.5)","rgba(204,0,0,0.5)","rgba(255,90,54,0.5)","rgba(255,186,0,0.5)","rgba(255,126,0,0.5)","rgba(0,66,37,0.5)","rgba(27,65,37,0.5)","rgba(0,97,169,0.5)","rgba(209,235,247,0.5)","rgba(150,200,162,0.5)","rgba(129,216,208,0.5)","rgba(0,26,87,0.5)","rgba(65,125,193,0.5)","rgba(83,104,149,0.5)","rgba(145,163,176,0.5)","rgba(245,245,220,0.5)","rgba(62,174,177,0.5)","rgba(206,70,118,0.5)","rgba(151,127,115,0.5)","rgba(201,174,93,0.5)","rgba(243,229,171,0.5)","rgba(80,64,77,0.5)","rgba(103,49,71,0.5)","rgba(84,61,63,0.5)","rgba(145,163,176,0.5)","rgba(129,135,139,0.5)","rgba(196,30,58,0.5)","rgba(193,154,107,0.5)","rgba(86,57,112,0.5)","rgba(228,155,15,0.5)","rgba(252,247,94,0.5)","rgba(248,222,126,0.5)","rgba(238,223,160,0.5)","rgba(184,41,40,0.5)","rgba(34,34,34,0.5)","rgba(72,60,50,0.5)","rgba(59,49,33,0.5)","rgba(103,76,71,0.5)","rgba(172,92,181,0.5)","rgba(217,144,88,0.5)","rgba(255,153,102,0.5)","rgba(178,27,28,0.5)","rgba(237,135,45,0.5)","rgba(217,144,88,0.5)","rgba(135,0,116,0.5)","rgba(96,47,107,0.5)","rgba(96,78,151,0.5)","rgba(250,214,165,0.5)","rgba(138,154,91,0.5)","rgba(147,197,146,0.5)","rgba(126,159,46,0.5)","rgba(143,151,121,0.5)","rgba(174,32,41,0.5)","rgba(114,47,55,0.5)"];

var seleccionar=false;
var colormouseover="rgba(255,255,0, 0.5)";
var colorclick="rgba(241, 220, 0, 0.5)";
var campoinput="";
var seleccion=0;
var numerodeinputs=8;


document.body.addEventListener("mouseover",(e)=>{
    
    if(seleccionar==true){
        console.log("llegue aqui");
        try {
            //Con el if evitamos la deseleccion de un elemento click
            anterior.style.backgroundColor=coloranterior; 
            anterior.style.border=bordeanterior;
        }catch (error){
        }
        let selector = document.querySelector(".selector");
        // selector output
        anterior=e.target;
        coloranterior=e.target.style.backgroundColor;
        bordeanterior=e.target.style.border;
        if(e.target.getAttribute("marcar")!="nopintar"){
            let output = getPathTo(e.target);
            e.target.style.backgroundColor=colormouseover;
            e.target.style.border="thick solid "+colormouseover;
            console.log(e.target);
            selector.innerHTML = `<strong>Selector:</strong> ${output}`;
        
        }
    }
});

document.body.addEventListener("click",(e)=>{

    if(seleccionar==true){
        try {
            //Con el if evitamos la deseleccion de un elemento click
            anterior.style.border=bordeanterior;
            anterior.style.backgroundColor=coloranterior;   
        }catch (error){
        }
        let selector = document.querySelector(".selector");
        // selector output
        anterior=e.target;
        coloranterior=e.target.style.backgroundColor;
        bordeanterior=e.target.style.border;
        if(e.target.getAttribute("marcar")!="nopintar"){
            let output = getPathTo(e.target);
            document.getElementById("input"+seleccion).value=optimizarxpath(output);
            for(var i=0; i<=8; i++){
                try {
                    pintarelemento(i);
                } catch (error) {
                    
                }
                
            }
            
            seleccionarcampo(seleccion);
            
            console.log(e.target);
            selector.innerHTML = `<strong>Selector:</strong> ${output}`;
        
        }
        for(var i=0; i<=10; i++){
            try {
                pintarelemento(i);
            } catch (error) {
                
            }
            
        }
    }
});



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

function seleccionarcampo(campo){
        
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

function xpathinput(numinput){
    try{
        
        $("#inputxpenlace").on('keyup', function(){
            //dejamos de pintar los anteriores elementos seleccionados
            var elementospintados=document.querySelectorAll('[color="rojo"]');
            for(elemento of elementospintados){
                if(elemento.getAttribute("estado")!="seleccionado"){
                    color=listacolores[numinput-1];
                    color=color.replace("0.5","1");
                    elemento.style.backgroundColor=listacolores[numinput-1];

                }
            }
            //pintamos los valores actuales
            var value = $(this).val();
            lista=getElementsByXPath(value);
            
           
        }).keyup();
    }catch(e){
     
    }
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
            if(consultaaux.length==consultaactual.length && !elemento.includes("@id")){
                xpathsalida=aux;
            }else{
                console.log("no son iguakes");
                console.log(consultaactual);
                console.log(consultaaux);
                break;
            }
    
        }
    
    }
    return xpathsalida;
    }

function pintarelemento(numinput){
        var xpathentrada=document.getElementById("input"+numinput).value;
        
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
            listapint=getElementsByXPath2(xpathentrada);
            for(var i=0; i<listapint.length; i++){
                element=listapint[i];
                element.style.backgroundColor=listacolores[numinput-1];
                element.style.border="thick solid "+listacolores[numinput-1];
                element.setAttribute("seleccion","seleccion"+numinput);
            }
        } catch (error) {
            console.error(error);
        }
        
                
}