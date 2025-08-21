import React, { useState } from 'react';
import { Card, Input, Button, Typography, InputNumber, message, Space, Divider } from 'antd';
import { FileTextOutlined } from '@ant-design/icons';
import axios from 'axios';

const { TextArea } = Input;
const { Title, Paragraph } = Typography;

const SummaryGeneration = () => {
  const [text, setText] = useState('');
  const [maxLength, setMaxLength] = useState(200);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!text.trim()) {
      message.error('请输入要生成摘要的文本');
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('/api/summary', 
        { text, max_length: maxLength },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setResult(response.data);
      message.success('摘要生成完成！');
    } catch (error) {
      message.error('生成失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Title level={3}>
          <FileTextOutlined style={{ marginRight: 8 }} />
          文本摘要生成
        </Title>
        <Paragraph>
          自动生成文本的摘要信息，帮助快速理解文本的核心内容。
        </Paragraph>

        <div style={{ marginBottom: 16 }}>
          <TextArea
            rows={8}
            placeholder="请输入要生成摘要的文本内容..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            style={{ marginBottom: 16 }}
          />
          
          <Space style={{ marginBottom: 16 }}>
            <span>最大摘要长度：</span>
            <InputNumber
              min={50}
              max={1000}
              value={maxLength}
              onChange={setMaxLength}
              style={{ width: 120 }}
            />
            <span>字符</span>
            <Button
              type="primary"
              size="large"
              loading={loading}
              onClick={handleGenerate}
              icon={<FileTextOutlined />}
            >
              生成摘要
            </Button>
          </Space>
        </div>

        {result && (
          <Card style={{ background: '#fafafa' }}>
            <Title level={4}>摘要结果</Title>
            <Paragraph style={{ fontSize: '16px', lineHeight: '1.8' }}>
              {result.summary}
            </Paragraph>
            
            <Divider />
            
            <Space size="large">
              <span>原文长度：{result.original_length} 字符</span>
              <span>摘要长度：{result.length} 字符</span>
              <span>压缩比：{(result.compression_ratio * 100).toFixed(1)}%</span>
            </Space>
          </Card>
        )}
      </Card>
    </div>
  );
};

export default SummaryGeneration; 