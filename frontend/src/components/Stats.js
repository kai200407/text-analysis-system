import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Typography, message } from 'antd';
import { BarChartOutlined, HeartOutlined, KeyOutlined, FileTextOutlined, SwapOutlined } from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import axios from 'axios';

const { Title } = Typography;

const Stats = () => {
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/stats', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStats(response.data);
    } catch (error) {
      message.error('获取统计数据失败');
    } finally {
      setLoading(false);
    }
  };

  const getPieChartOption = () => ({
    title: {
      text: '分析类型分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '分析类型',
        type: 'pie',
        radius: '50%',
        data: [
          { value: stats.sentiment_count || 0, name: '情感分析' },
          { value: stats.keywords_count || 0, name: '关键词提取' },
          { value: stats.summary_count || 0, name: '文本摘要' },
          { value: stats.similarity_count || 0, name: '相似度计算' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  });

  const getBarChartOption = () => ({
    title: {
      text: '各功能使用次数',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: ['情感分析', '关键词提取', '文本摘要', '相似度计算']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '使用次数',
        type: 'bar',
        data: [
          stats.sentiment_count || 0,
          stats.keywords_count || 0,
          stats.summary_count || 0,
          stats.similarity_count || 0
        ],
        itemStyle: {
          color: function(params) {
            const colors = ['#52c41a', '#1890ff', '#722ed1', '#fa8c16'];
            return colors[params.dataIndex];
          }
        }
      }
    ]
  });

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Title level={3}>
          <BarChartOutlined style={{ marginRight: 8 }} />
          统计分析
        </Title>

        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={6}>
            <Card>
              <Statistic
                title="总分析次数"
                value={stats.total_analyses || 0}
                prefix={<BarChartOutlined />}
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="情感分析"
                value={stats.sentiment_count || 0}
                prefix={<HeartOutlined />}
                valueStyle={{ color: '#52c41a' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="关键词提取"
                value={stats.keywords_count || 0}
                prefix={<KeyOutlined />}
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="文本摘要"
                value={stats.summary_count || 0}
                prefix={<FileTextOutlined />}
                valueStyle={{ color: '#722ed1' }}
              />
            </Card>
          </Col>
        </Row>

        <Row gutter={16}>
          <Col span={12}>
            <Card title="分析类型分布">
              <ReactECharts option={getPieChartOption()} style={{ height: '300px' }} />
            </Card>
          </Col>
          <Col span={12}>
            <Card title="功能使用统计">
              <ReactECharts option={getBarChartOption()} style={{ height: '300px' }} />
            </Card>
          </Col>
        </Row>

        <Row style={{ marginTop: 16 }}>
          <Col span={24}>
            <Card title="使用情况分析">
              <div style={{ lineHeight: 2 }}>
                <p><strong>总体使用情况：</strong></p>
                <ul>
                  <li>您总共进行了 {stats.total_analyses || 0} 次文本分析</li>
                  <li>其中情感分析 {stats.sentiment_count || 0} 次，占比 {stats.total_analyses ? Math.round((stats.sentiment_count || 0) / stats.total_analyses * 100) : 0}%</li>
                  <li>关键词提取 {stats.keywords_count || 0} 次，占比 {stats.total_analyses ? Math.round((stats.keywords_count || 0) / stats.total_analyses * 100) : 0}%</li>
                  <li>文本摘要 {stats.summary_count || 0} 次，占比 {stats.total_analyses ? Math.round((stats.summary_count || 0) / stats.total_analyses * 100) : 0}%</li>
                  <li>相似度计算 {stats.similarity_count || 0} 次，占比 {stats.total_analyses ? Math.round((stats.similarity_count || 0) / stats.total_analyses * 100) : 0}%</li>
                </ul>
              </div>
            </Card>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default Stats; 