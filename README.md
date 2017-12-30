# Rem Lang

## 简介

Rem是一门简便的, 具有高可读性的, 面向非计算机专业人群的现代编程语言。 


```
print 'rem'  // => rem

f 1 := 10
f n := f(n-1) * 10
f 10  // =>  10!
```

## 方便使用目标后端的现有库

Rem将会是一个多后端的语言。考虑实现方便和调用优化库的便利, 初期后端使用Python。
```
link `python` with {
    math::sqrt
    math::log10
    os
}
sqrt 9   # => 3
log10 10   # => 10
os#system "echo **"  # => **
```

## 语言配置和EDSL

它从关键字层面支持各种字符集的编程, 能够自定义中缀操作符以轻易实现EDSL。

```

use 中文编程

<中缀> 相关于 甲 乙 
    当 
        甲 之 为向量, 
        乙 之 为向量 
    := {
        
        甲 笛卡尔积 乙 
            然后 
                从 甲元 乙元 到 (甲元 减 甲之平均) * (乙元 减 乙之平均)  
            然后
                从 其 到 其 之 平均
            然后
                除以 (甲 之 标准差 * 乙 之 标准差)
        其中
            甲之平均 = 甲 之 平均,
            乙之平均 = 乙 之 平均,
            标准差 序列 := 
                ((序列 各 自乘) 之 平均 - 序列 之 平均 自乘) 之 开方


}   

[1, 2, 3] 相关于 [2, 3, 5]  # => 0.98198050606196585

```

非中文

```
<infix> correlate xs ys 
    when xs . is_vector,
         ys . is_vector
    :={
    xs cartesian_product ys 
        then (x, y) => (x - mean_xs) * (y - mean_ys)
        then it => it . mean
        then div_by (xs.std * ys.std)
    
    where
        mean_xs = xs . mean,
        mean_ys = ys . mean,
        std seq := ((seq . map x=>x*x) . mean - seq . mean . x => x*x) . sqrt
}

[1, 2, 3] correlate [2, 3, 5]  # => 0.98198050606196585
```

## 为什么需要Rem

因为简单。可以让原先对程序设计有畏惧心理的人轻松掌握。

- 写文件

```
打开文件 '我的文件'
    然后
        写入 "你好, Rem"

open 'my file'    
    then write "hello, rem"

```

- 查询

```
打开文件 '论文集.txt'
    然后
        读取
    然后
        选取 
        从 一行话 到 一行话 之 小写 包含 'reinforcement learning'
    然后
        换行符 之 拼接
        其中
            换行符 = '\n'
    然后
        打印

open 'papers.txt'
    then 
        read
    then
        select line => line . low contains 'reinforcement'
    then
        '\n' . join
    then 
        print
```

以上













