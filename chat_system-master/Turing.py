import json
import urllib.request

   elif my_msg[0] == 't' :
      while my_msg != 'q':
        api_url = "http://openapi.tuling123.com/openapi/api/v2"
        text_input = my_msg[0]

        req = {
            "perception":
           {
                "inputText":
                {
                   "text": text_input
                },

                "selfInfo":
                {
                    "location":
                    {
                        "city": "上海",
                        "province": "上海",
                        "street": "文汇路"
                    }
                }
            },

            "userInfo": 
            {
                "apiKey": "0cf352ad917f4e7f9a1f56bc70db712a",
                "userId": "ABC"
            }
        }
      # print(req)
      # 将字典格式的req编码为utf8 
        req = json.dumps(req).encode('utf8')
      # print(req)


        http_post = urllib.request.Request(api_url, data=req, headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(http_post)
        response_str = response.read().decode('utf8')
      # print(response_str)
        response_dic = json.loads(response_str)
      # print(response_dic)

        intent_code = response_dic['intent']['code']
        results_text = response_dic['results'][0]['values']['text']
        print('Turing的回答：')
        print(results_text)




     
