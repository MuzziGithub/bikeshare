# 1.导包操作
import matplotlib.pyplot as plt
import seaborn as sn
import numpy as np
import pandas as pd

from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体

from datetime import datetime
import calendar
import os

print(os.getcwd())


# 2.数据处理
def collect_and_process_data():
    # 2.1数据读取
    bikedata = pd.read_csv("train.csv")
    # print(bikedata.describe())
    # print(bikedata)

    # 2.2.数据查看
    """
    print(bikedata.shape)
    print(bikedata.head())
    print(bikedata.tail)
    print(bikedata.dtypes)
    print(bikedata.describe()) #对每一页对数据分析
    """
    # 2.3数据提取
    # 2.3.1 提取某一列
    # print(bikedata.datetime)

    # 2.3.2添加date列
    bikedata['date'] = bikedata.datetime.apply(lambda x: x.split()[0])
    print(bikedata)
    # 2.3.3提取小时数
    bikedata['hour'] = bikedata.datetime.apply(lambda x: x.split()[1].split(':')[0])
    print(bikedata)

    # 2.3.4添加列weekday，month
    bikedata['weekday'] = bikedata.date.apply(lambda dateString:
                                              calendar.day_name[datetime.strptime(dateString, '%Y/%m/%d').weekday()])
    bikedata['month'] = bikedata.date.apply(lambda dateString:
                                            calendar.month_name[datetime.strptime(dateString, '%Y/%m/%d').month])
    print(bikedata)

    # 2.3.3将season转化为季节英文值
    bikedata['season'] = bikedata.season.map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    print(bikedata)

    # 3.将以下变量转换为分类变量
    varlist = ['hour', 'weekday', 'month', 'season', 'holiday', 'workingday']
    for x in varlist:
        bikedata[x] = bikedata[x].astype('category')
    print(bikedata.dtypes)
    print(bikedata)

    # category:分类变量
    # astype() 按列进行数据类型转化

    # 4.删除无意义变量
    bikedata.drop('datetime', axis=1, inplace=True)
    print(datetime)

    # 5.数据清洗
    # 5.1查看是否缺失数据
    # 5.2查看是否有异常
    fig, axes = plt.subplots(nrows=2, ncols=2)
    fig.set_size_inches(12, 12)  # 设置整个图像框的大小
    sn.boxplot(data=bikedata, y="count", orient="v", ax=axes[0][0])
    sn.boxplot(data=bikedata, y="count", x="season", orient="v", ax=axes[0][1])
    sn.boxplot(data=bikedata, y="count", x="hour", orient="v", ax=axes[1][0])
    sn.boxplot(data=bikedata, y="count", x="workingday", orient="v", ax=axes[1][1])

    axes[0][0].set(ylabel='骑行人数', title='骑行人数')
    axes[0][1].set(xlabel='季节', ylabel='骑行人数', title='不同季节骑行人数')
    axes[1][0].set(xlabel='时间', ylabel='骑行人数', title='一天内不同时间骑行人数')
    axes[1][1].set(xlabel='工作日', ylabel='骑行人数', title='工作日骑行人数')
    plt.show()
    # 5.3剔除数据
    print(np.abs(bikedata["count"] - bikedata["count"].mean()) <= (3 * bikedata["count"].std()))

    bikedata1 = bikedata[np.abs(bikedata["count"] - bikedata["count"].mean()) <= (3 * bikedata["count"].std())]
    print("剔除前数据记录：", bikedata.shape, "\n剔除后数据记录:", bikedata1.shape)
    print(bikedata1)
    bikedata1.to_csv('process_data.csv')
    return bikedata1


# 6.数据分析与可视化
def Data_Analysis_and_visualization_month(bikedata1):
    # 6.1 不同月份骑行人
    # 6.1.1 不同月份骑行人数数据框的制作
    fig, ax = plt.subplots()  # plt :matplotlib 中的matplot 。
    fig.set_size_inches(12, 20)  # 设置数据框大小
    sortOrder = ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]
    monthAggregated = pd.DataFrame(bikedata1.groupby("month")["count"].mean()).reset_index()
    # 将数据处理后得到的新数据框按月份分组并求出每个月份骑行人数的平均值，
    # 对求出来的均值创建数据框并建立索引
    print(monthAggregated)  # 打印得到的不同月份骑行人数的数据框
    monthSorted = monthAggregated.sort_values(by="count", ascending=False)
    # 对不同月份骑行人数按照人数多少降序排序
    print(monthSorted)
    # 6.1.2 不同月份骑行人数柱状图的绘制
    sn.barplot(data=monthAggregated, x='month', y='count', order=sortOrder)
    # 对不同月份骑行人数的数据框按月份为x轴，骑行人数为y轴,按月份分类绘制柱状图
    ax.set(xlabel='月份', ylabel='平均骑行人数', title='不同月份的骑行人数')
    plt.savefig('monthResult.png')
    plt.show()


def Data_Analysis_and_Visualization_week(bikedata1):
    # 6.2 一周内不同时间骑行人数
    # 6.2.1 数据分析
    fig1, ax1 = plt.subplots()
    fig1.set_size_inches(12, 20)
    hueOrder = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    weekAggregated = pd.DataFrame(bikedata1.groupby(["hour", "weekday"])["count"].mean()).reset_index()
    print(weekAggregated)
    weekSorted = weekAggregated.sort_values(by="count", ascending=False)
    print(weekSorted)
    # 6.2.2 图形(曲线图)绘制
    sn.pointplot(data=weekAggregated, x=weekAggregated["hour"], y=weekAggregated["count"],
                 hue=weekAggregated["weekday"], hue_order=hueOrder)
    ax1.set(xlabel='时间', ylabel='平均骑行人数', title='一周内不同时间骑行人数')
    # 6.2.3  可视化
    plt.savefig('weekResult.png')
    plt.show()


def Data_Analysis_and_Visualization_season(bikedata1):
    # 6.3 不同季节不同时间的骑行人数
    # 6.3.1 数据分析
    fig2, ax2 = plt.subplots()
    fig2.set_size_inches(12, 20)
    hueOrder = ["Spring", "Summer", "Fall", "Winter"]
    seasonAggregated = pd.DataFrame(bikedata1.groupby(["hour", "season"])["count"].mean()).reset_index()
    print(seasonAggregated)
    seasonSorted = seasonAggregated.sort_values(by="count", ascending=False)
    print(seasonSorted)
    # 6.3.2 曲线图绘制
    sn.pointplot(data=seasonAggregated, x=seasonAggregated["hour"], y=seasonAggregated["count"],
                 hue=seasonAggregated["season"], hue_order=hueOrder)
    ax2.set(xlabel="时间", ylabel="平均骑行人数", title="不同季节不同时间骑行人数")
    # 6.3.2 可视化
    plt.savefig("season.png")
    plt.show()


def Data_Analysis_and_Visualization_person(bikedata1):
    # 6.4 不同用户在不同时间内的骑行人数
    # 6.4.1 数据分析
    fig3, ax3 = plt.subplots()
    fig3.set_size_inches(12, 20)
    bikedata2 = pd.melt(bikedata1, id_vars=["hour"], value_vars=["casual", "registered"],
                        var_name="changed", value_name="number")
    print(bikedata2)
    hueOrder = ["casual", "registered"]
    registeredAggregated = pd.DataFrame(bikedata2.groupby(["hour", "changed"])["number"].mean()).reset_index()
    print(registeredAggregated)
    registeredOrder = registeredAggregated.sort_values(by="hour", ascending=False)
    print(registeredOrder)
    # 6.4.2 曲线图绘制
    sn.pointplot(data=registeredAggregated, x=registeredAggregated["hour"], y=registeredAggregated["number"],
                 hue=registeredAggregated["changed"], hue_order=hueOrder)
    ax3.set(xlabel="时间", ylabel="平均骑行人数", title="不同用户不同时间内骑行人数")
    # 6.4.3 可视化
    plt.savefig("register.png")
    plt.show()


def main():
    # 主函数
    # 数据采集/查看和处理
    bikedata1 = collect_and_process_data()
    # 数据分析和可视化1
    Data_Analysis_and_visualization_month(bikedata1)
    # 数据分析与可视化2
    Data_Analysis_and_Visualization_week(bikedata1)
    # 数据分析和可视化3
    Data_Analysis_and_Visualization_season(bikedata1)
    # 数据分析和可视化4
    Data_Analysis_and_Visualization_person(bikedata1)


# 主程序：
if __name__ == '__main__':
    main()
