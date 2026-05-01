import{e as a}from"./index-D5ShsG8J.js";function e(){const e=a(!1);return{isLocked:e,runWithLock:async a=>{if(!e.value){e.value=!0;try{await a()}finally{e.value=!1}}}}}export{e as u};
