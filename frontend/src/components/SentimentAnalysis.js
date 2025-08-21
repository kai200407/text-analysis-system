import React, { useState } from 'react';
import { Card, Input, Button, Result, Progress, Tag, Typography, Space, message } from 'antd';
import { HeartOutlined, SmileOutlined, MehOutlined, FrownOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import api from '../utils/axios';

const { TextArea } = Input;
const { Title, Paragraph } = Typography;

const SentimentAnalysis = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleAnalyze = async () => {
    if (!text.trim()) {
      message.error('请输入要分析的文本');
      return;
    }

    setLoading(true);
    try {
      const response = await api.post('/api/sentiment', { text });
      setResult(response.data);
      message.success('分析完成！');
    } catch (error) {
      message.error('分析失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  const getSentimentIcon = (sentiment) => {
    switch (sentiment) {
      case '积极':
        return <SmileOutlined style={{ color: '#52c41a', fontSize: '24px' }} />;
      case '消极':
        return <FrownOutlined style={{ color: '#ff4d4f', fontSize: '24px' }} />;
      default:
        return <MehOutlined style={{ color: '#faad14', fontSize: '24px' }} />;
    }
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case '积极':
        return '#52c41a';
      case '消极':
        return '#ff4d4f';
      default:
        return '#faad14';
    }
  };

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Title level={3}>
          <HeartOutlined style={{ marginRight: 8 }} />
          情感分析
        </Title>
        <Paragraph>
          输入文本内容，系统将自动分析文本的情感倾向，判断为积极、消极或中性。
        </Paragraph>

        <div style={{ marginBottom: 16 }}>
          <TextArea
            rows={6}
            placeholder="请输入要分析的文本内容..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            style={{ marginBottom: 16 }}
          />
          <Button
            type="primary"
            size="large"
            loading={loading}
            onClick={handleAnalyze}
            icon={<HeartOutlined />}
          >
            开始分析
          </Button>
        </div>

        {result && (
          <Card style={{ marginTop: 16, background: '#fafafa' }}>
            <Result
              icon={getSentimentIcon(result.sentiment)}
              title={`情感倾向：${result.sentiment}`}
              subTitle={`置信度：${result.confidence}`}
              extra={
                <Space direction="vertical" size="large" style={{ width: '100%' }}>
                  <div>
                    <Paragraph>情感得分：</Paragraph>
                    <Progress
                      percent={Math.round(result.score * 100)}
                      strokeColor={getSentimentColor(result.sentiment)}
                      format={(percent) => `${percent}%`}
                    />
                  </div>
                  <div>
                    <Tag color={getSentimentColor(result.sentiment)} size="large">
                      得分：{result.score}
                    </Tag>
                    <Tag color="blue" size="large">
                      置信度：{result.confidence}
                    </Tag>
                  </div>
                </Space>
              }
            />
          </Card>
        )}
      </Card>
    </div>
  );
};

export default SentimentAnalysis; 