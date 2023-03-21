prompt_message='''\
#命令
後述の条件を必ず守った上で、入力された文章に改行を入れて出力して下さい。

#条件(優先順)
1位：文章が読みやすい。
2位：1行あたりの文字数が必ず16文字以下である。
3位：品詞と品詞の間で改行する。
4位：1行あたりの文字数が10文字以上である。

#入力
{event_message}
'''.format(event_message="hello")

# print(prompt_message)

event_message='''\
ウクライナ情勢をめぐって中国が対話と停戦を呼びかける文書を発表するなか、

アメリカと対立する両国の首脳がどのような方針を打ち出すのかが焦点です。
'''
line_event_message=event_message.replace("\n","")
# line_event_message=line_event_message.replace(" ","")

print(line_event_message)