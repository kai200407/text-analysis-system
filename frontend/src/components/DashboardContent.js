import React from 'react';
import { Card, Row, Col, Statistic, Typography } from 'antd';
import { 
  DashboardOutlined, 
  HeartOutlined, 
  KeyOutlined, 
  FileTextOutlined
} from '@ant-design/icons';

const { Title } = Typography;

const DashboardContent = () => {
  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <Title level={4}>欢迎使用智能文本分析系统</Title>
        <p>本系统提供多种文本分析功能，帮助您更好地理解和处理文本数据。</p>
      </div>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总分析次数"
              value={0}
              prefix={<DashboardOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="情感分析"
              value={0}
              prefix={<HeartOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="关键词提取"
              value={0}
              prefix={<KeyOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="文本摘要"
              value={0}
              prefix={<FileTextOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={12}>
          <Card title="功能说明" style={{ height: 300 }}>
            <div style={{ lineHeight: 2 }}>
              <p><strong>情感分析：</strong>分析文本的情感倾向，判断为积极、消极或中性。</p>
              <p><strong>关键词提取：</strong>使用TF-IDF和TextRank算法提取文本中的关键词。</p>
              <p><strong>文本摘要：</strong>生成文本的摘要信息，帮助快速理解文本内容。</p>
              <p><strong>相似度计算：</strong>计算两段文本之间的相似度，用于文本比较。</p>
            </div>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="使用建议" style={{ height: 300 }}>
            <div style={{ lineHeight: 2 }}>
              <p>• 输入文本时，建议使用中文文本以获得更好的分析效果</p>
              <p>• 文本长度建议在50-2000字之间，过短或过长可能影响分析准确性</p>
              <p>• 系统会自动保存您的分析历史，方便后续查看</p>
              <p>• 可以通过统计分析功能查看您的使用情况</p>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default DashboardContent;
