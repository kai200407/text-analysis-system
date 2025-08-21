import React, { useState, useEffect } from 'react';
import { Card, Table, Tag, Typography, message } from 'antd';
import { HistoryOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title } = Typography;

const History = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/history', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setHistory(response.data.history);
    } catch (error) {
      message.error('获取历史记录失败');
    } finally {
      setLoading(false);
    }
  };

  const getAnalysisTypeColor = (type) => {
    switch (type) {
      case 'sentiment':
        return 'green';
      case 'keywords':
        return 'blue';
      case 'summary':
        return 'purple';
      case 'similarity':
        return 'orange';
      default:
        return 'default';
    }
  };

  const getAnalysisTypeText = (type) => {
    switch (type) {
      case 'sentiment':
        return '情感分析';
      case 'keywords':
        return '关键词提取';
      case 'summary':
        return '文本摘要';
      case 'similarity':
        return '相似度计算';
      default:
        return type;
    }
  };

  const columns = [
    {
      title: '分析类型',
      dataIndex: 'analysis_type',
      key: 'analysis_type',
      render: (type) => (
        <Tag color={getAnalysisTypeColor(type)}>
          {getAnalysisTypeText(type)}
        </Tag>
      ),
    },
    {
      title: '文本内容',
      dataIndex: 'text',
      key: 'text',
      ellipsis: true,
      width: 300,
    },
    {
      title: '分析结果',
      dataIndex: 'result',
      key: 'result',
      ellipsis: true,
      width: 200,
      render: (result) => {
        try {
          const parsed = JSON.parse(result);
          if (parsed.sentiment) {
            return `情感: ${parsed.sentiment}`;
          } else if (parsed.tfidf_keywords) {
            return `关键词: ${parsed.tfidf_keywords.length}个`;
          } else if (parsed.summary) {
            return `摘要: ${parsed.summary.substring(0, 50)}...`;
          } else if (parsed.similarity_score) {
            return `相似度: ${parsed.similarity_score}`;
          }
          return '查看详情';
        } catch {
          return '查看详情';
        }
      },
    },
    {
      title: '分析时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 150,
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Title level={3}>
          <HistoryOutlined style={{ marginRight: 8 }} />
          分析历史记录
        </Title>
        
        <Table
          columns={columns}
          dataSource={history}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => 
              `第 ${range[0]}-${range[1]} 条，共 ${total} 条记录`,
          }}
          scroll={{ x: 800 }}
        />
      </Card>
    </div>
  );
};

export default History; 