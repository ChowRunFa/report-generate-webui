import request from '@/apis/client/request'


export function set_llm(form){
    return request.post('/set_llm',form)
}

export function paper_report(form){
    return request.post('/paper_report',form)
}

