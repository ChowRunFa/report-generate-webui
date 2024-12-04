import request from '@/apis/client/request'
import * as url from 'url'


export function set_llm(form){
    return request.post('/set_llm',form)
}

export function paper_report(form) {
    return request.post('/paper_report', form)
}

export function related_work(form) {
    return request.post('/related_work', form)

}


export function text_evaluate(form){
return request.post('/text_evaluate',form)

}

export function auto_kg(form){
return request.post('/autokg',form)

}

export function update_kg(form){
return request.get('/update_kg',form)
}

export function get_mermaid(form){
return request.post('/generate_mermaid',form)

}


export function get_response_data(form){
return request.post('/instagraph/get_response_data',form)

}

export function graphviz_kg(form){
return request.post('/instagraph/graphviz',form)

}
export function get_graph_data(form){
return request.post('/instagraph/get_graph_data',form)

}


export function get_graph_history(form){
return request.get('/instagraph/get_graph_history',form)

}

export function framework_report(form){
return request.post('/framework_report',form)

}

export function document_list(){
return request.get('/document_list')

}

export function save_prompt(form){
return request.post('/save_prompt',form)

}

export function load_prompts(){
return request.get('/load_prompts')

}

export function load_json_prompts(){
return request.get('/load_json_prompts')

}
export function load_framework_reports(){
return request.get('/load_framework')

}

export function generate_framework(form){
return request.post('/generate_framework',form)

}

