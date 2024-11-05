## 如何使用

1.如果是在本地部署，请下载全部源码，然后在 `config/setting.py` 中替换自己的 api_key；如果是在我自己搭建的在线网站使用，可以省略这一步骤。

2.在界面中左上角输入五个要读的单词，用空格或者英文逗号隔开，然后点击“split text”橙色按钮。

3.接下来可以看到“Word_1”到 "Word_5"显示，有每个要读的单词，你就点击对应的“录音”按钮（带录音 icon），让电脑或手机录入你的发音，发音完点“结束”。

4.五个单词都录完自己的发音，最后回到页面最上面，点击右上角“evaluate”，等几秒钟，就能得到评估打分。

5.为了方便保存评分结果，可以最后点击“Generate Markdown”，会在下方进行 5 个单词发音评估结果汇总，方便复制粘贴到本地。

![image-20241105173440114](https://picbox-1313243162.cos.ap-nanjing.myqcloud.com/image-20241105173440114.png)

具体每个细分分数的含义，可以参考这个[微软官方发音评估网站](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-pronunciation-assessment?pivots=programming-language-csharp) 的说明。
