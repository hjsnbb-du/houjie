import React, { useEffect, useRef } from 'react';
import { Card } from 'antd';
import ReactECharts from 'echarts-for-react';
import { theme } from 'antd';
import * as echarts from 'echarts';

interface DataPoint {
  date: string;
  value: number;
  category?: string;
}

interface TrendChartProps {
  title: string;
  data: DataPoint[];
  loading?: boolean;
  height?: number;
}

const TrendChart: React.FC<TrendChartProps> = ({
  title,
  data,
  loading = false,
  height = 300,
}) => {
  const { token } = theme.useToken();
  const chartRef = useRef<ReactECharts>(null);

  useEffect(() => {
    console.log('TrendChart data:', { title, data }); // Debug log
    if (chartRef.current) {
      const chart = chartRef.current.getEchartsInstance();
      console.log('ECharts instance:', chart); // Debug log
      chart.resize();
    }
  }, [data]);

  const option: echarts.EChartsOption = {
    grid: {
      top: 40,
      right: 20,
      bottom: 40,
      left: 60,
      containLabel: true
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: {
          backgroundColor: token.colorPrimary
        }
      }
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.date),
      boundaryGap: false,
      axisLine: {
        lineStyle: {
          color: token.colorBorder
        }
      },
      axisTick: {
        alignWithLabel: true
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: token.colorBorder
        }
      },
      splitLine: {
        lineStyle: {
          color: token.colorBorderSecondary
        }
      }
    },
    series: [{
      name: title,
      type: 'line',
      data: data.map(item => item.value),
      smooth: true,
      showSymbol: true,
      symbol: 'circle',
      symbolSize: 8,
      itemStyle: {
        color: token.colorPrimary
      },
      lineStyle: {
        width: 3,
        color: token.colorPrimary
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: token.colorPrimaryBg
          },
          {
            offset: 1,
            color: token.colorBgContainer
          }
        ])
      }
    }]
  };

  return (
    <Card title={title} loading={loading} bordered={false}>
      <ReactECharts
        ref={chartRef}
        option={option}
        style={{ height }}
        notMerge={true}
        lazyUpdate={true}
        onChartReady={() => {
          if (chartRef.current) {
            chartRef.current.getEchartsInstance().resize();
          }
        }}
        onEvents={{
          resize: () => {
            if (chartRef.current) {
              chartRef.current.getEchartsInstance().resize();
            }
          }
        }}
      />
    </Card>
  );
};

export default TrendChart;
