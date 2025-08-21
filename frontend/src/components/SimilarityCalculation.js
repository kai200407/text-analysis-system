import React, { useState } from 'react';
import { Card, Input, Button, Typography, Progress, Tag, message, Row, Col } from 'antd';
import { SwapOutlined } from '@ant-design/icons';
import axios from 'axios';

const { TextArea } = Input;
const { Title, Paragraph } = Typography;

const SimilarityCalculation = () => {
  const [text1, setText1] = useState('');
  const [text2, setText2] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCalculate = async () => {
    if (!text1.trim() || !text2.trim()) {
      message.error('请输入两段要比较的文本');
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('/api/similarity', 
        { text1, text2 },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setResult(response.data);
      message.success('相似度计算完成！');
    } catch (error) {
      message.error('计算失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  const getSimilarityColor = (score) => {
    if (score > 0.8) return '#52c41a';
    if (score > 0.5) return '#faad14';
    return '#ff4d4f';
  };

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Title level={3}>
          <SwapOutlined style={{ marginRight: 8 }} />
          文本相似度计算
        </Title>
        <Paragraph>
          计算两段文本之间的相似度，使用余弦相似度算法进行分析。
        </Paragraph>

        <Row gutter={16} style={{ marginBottom: 16 }}>
          <Col span={12}>
            <TextArea
              rows={6}
              placeholder="请输入第一段文本..."
              value={text1}
              onChange={(e) => setText1(e.target.value)}
            />
          </Col>
          <Col span={12}>
            <TextArea
              rows={6}
              placeholder="请输入第二段文本..."
              value={text2}
              onChange={(e) => setText2(e.target.value)}
            />
          </Col>
        </Row>

        <Button
          type="primary"
          size="large"
          loading={loading}
          onClick={handleCalculate}
          icon={<SwapOutlined />}
          style={{ marginBottom: 16 }}
        >
          计算相似度
        </Button>

        {result && (
          <Card style={{ background: '#fafafa' }}>
            <Title level={4}>相似度结果</Title>
            
            <div style={{ marginBottom: 16 }}>
              <Paragraph>相似度得分：</Paragraph>
              <Progress
                percent={Math.round(result.similarity_percentage)}
                strokeColor={getSimilarityColor(result.similarity_score)}
                format={(percent) => `${percent}%`}
                size="large"
              />
            </div>

            <Row gutter={16}>
              <Col span={8}>
                <Tag color={getSimilarityColor(result.similarity_score)} size="large">
                  相似度：{result.similarity_score}
                </Tag>
              </Col>
              <Col span={8}>
                <Tag color="blue" size="large">
                  百分比：{result.similarity_percentage}%
                </Tag>
              </Col>
              <Col span={8}>
                <Tag color="purple" size="large">
                  评价：{result.interpretation}
                </Tag>
              </Col>
            </Row>

            <div style={{ marginTop: 16 }}>
              <Paragraph>
                <strong>相似度说明：</strong>
              </Paragraph>
              <ul>
                <li>高度相似 (≥80%)：两段文本内容非常相似</li>
                <li>中度相似 (50%-80%)：两段文本有一定相似性</li>
                <li>低度相似 (&lt;50%)：两段文本相似度较低</li>
              </ul>
            </div>
          </Card>
        )}
      </Card>
    </div>
  );
};

export default SimilarityCalculation; 