qq会对asar内的文件进行加密,用原版asar提取以后可以使用本工具进行解密

以下为示例命令
python3 decrypt_qq_asar.py input output 0051C42C0C8D2C929CEBFECA3B0492F7157739C7401D45545D2BDD4A15458CF735 

其中0051C42C0C8D2C929CEBFECA3B0492F7157739C7401D45545D2BDD4A15458CF735为密钥 可以从qq二进制中获取,以下为linux-x64版qq定位方式

ida打开/opt/QQ/qq后使用alt+b搜索以下特征码定位到解密函数
55 48 89 E5 41 57 41 56 41 55 41 54 53 48 83 EC 58 89 4D 88 49 89 D5 48 89 F3 49 89 FC 64 48 8B 04 25 28 00 00 00 48 89 45 D0 E8 ?? ?? ?? ?? 49 89 C6 48 89 C7 E8 ?? ?? ?? ?? 89 C0 4D 89 EF 49 29 C7 73 ??
![alt text](image.png)
ymmword_2222780即为密钥内容 第二行的35也是密钥的一部分
![alt text](image-1.png)