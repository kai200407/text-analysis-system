import React, { useState } from 'react';
import { Card, Input, Button, Typography, Row, Col, Tag, InputNumber, message, Space } from 'antd';
import { KeyOutlined } from '@ant-design/icons';
import axios from 'axios';

const { TextArea } = Input;
const { Title, Paragraph } = Typography;

const KeywordExtraction = () => {
  const [text, setText] = useState('');
  const [topK, setTopK] = useState(10);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleExtract = async () => {
    if (!text.trim()) {
      message.error('请输入要分析的文本');
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('/api/keywords', 
        { text, top_k: topK },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setResult(response.data);
      message.success('关键词提取完成！');
    } catch (error) {
      message.error('提取失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Title level={3}>
          <KeyOutlined style={{ marginRight: 8 }} />
          关键词提取
        </Title>
        <Paragraph>
          使用TF-IDF和TextRank算法自动提取文本中的关键词汇，帮助理解文本主题。
        </Paragraph>

        <div style={{ marginBottom: 16 }}>
          <TextArea
            rows={6}
            placeholder="请输入要提取关键词的文本内容..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            style={{ marginBottom: 16 }}
          />
          
          <Space style={{ marginBottom: 16 }}>
            <span>提取关键词数量：</span>
            <InputNumber
              min={1}
              max={50}
              value={topK}
              onChange={setTopK}
              style={{ width: 100 }}
            />
            <Button
              type="primary"
              size="large"
              loading={loading}
              onClick={handleExtract}
              icon={<KeyOutlined />}
            >
              开始提取
            </Button>
          </Space>
        </div>

        {result && (
          <Row gutter={16}>
            <Col span={12}>
              <Card title="TF-IDF算法结果" size="small">
                <div style={{ maxHeight: 300, overflowY: 'auto' }}>
                  {result.tfidf_keywords?.map((item, index) => (
                    <Tag
                      key={index}
                      color="blue"
                      style={{ margin: '4px', fontSize: '12px' }}
                    >
                      {item.word} ({item.weight})
                    </Tag>
                  ))}
                </div>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="TextRank算法结果" size="small">
                <div style={{ maxHeight: 300, overflowY: 'auto' }}>
                  {result.textrank_keywords?.map((item, index) => (
                    <Tag
                      key={index}
                      color="green"
                      style={{ margin: '4px', fontSize: '12px' }}
                    >
                      {item.word} ({item.weight})
                    </Tag>
                  ))}
                </div>
              </Card>
            </Col>
          </Row>
        )}
      </Card>
    </div>
  );
};

export default KeywordExtraction; 