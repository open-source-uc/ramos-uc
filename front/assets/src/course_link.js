import {getCookie} from './cookies';

// make link to buscacursos
const link = () => {

    var saved = getCookie('ramos');
    saved = saved ? saved.split(',') : [];

    var initials = '';
    var fst = 1;

    for (let i in saved) {

        let id = saved[i];
        let tb = $(`[name=ramo_${id}]`);
        
        let initial = tb.find('td').eq(3).text();
        
        if(fst == 0){
            initials += ',';
        } else
            fst = 0;

        initials += initial;
        console.log(fst.toString());
    }
    return 'https://buscacursos.uc.cl/?cursos=' + initials;

};


export {link};