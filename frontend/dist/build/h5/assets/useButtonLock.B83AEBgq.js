import{r as a}from"./index-Dc5uI44e.js";function i(){const i=a(!1);return{isLocked:i,runWithLock:async a=>{if(!i.value){i.value=!0;try{await a()}finally{i.value=!1}}}}}export{i as u};
