from src.llm_module import LLMModule

if __name__ == '__main__':
    # 加载文件内容到变量中
    with open('./Test_spin/yh.log', 'r', encoding='utf-8') as f:
        log_data = f.read()

    with open('./template_test.txt', 'r', encoding='utf-8') as f:
        template = f.read()

    print("==== log_data ====")
    print(log_data)
    print("")
    print("==== template ====")
    print(template)

    test = LLMModule()
    test.set_url('http://172.16.31.129:11434/api/chat')
    test.set_model('deepseek-r1-m:671b')

    test.test_run(log_data, template, 'Test', 'None')