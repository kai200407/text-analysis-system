import React, { useState, useEffect } from 'react';
import { Layout, Menu, Card, Row, Col, Statistic, Typography, Button, message } from 'antd';
import { 
  DashboardOutlined, 
  HeartOutlined, 
  KeyOutlined, 
  FileTextOutlined,
  SwapOutlined,
  HistoryOutlined,
  BarChartOutlined,
  LogoutOutlined
} from '@ant-design/icons';
import { useNavigate, Outlet } from 'react-router-dom';
import api from '../utils/axios';

const { Header, Sider, Content } = Layout;
const { Title } = Typography;

const Dashboard = () => {
  const [collapsed, setCollapsed] = useState(false);
  const [stats, setStats] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    // ProtectedRoute已经处理了认证检查，这里直接获取统计数据
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await api.get('/api/stats');
      setStats(response.data);
    } catch (error) {
      // 如果获取统计数据失败，不强制跳转登录页，只显示错误信息
      console.error('获取统计数据失败:', error);
      message.error('获取统计数据失败');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    message.success('已退出登录');
    navigate('/login');
  };

  const menuItems = [
    {
      key: 'dashboard',
      icon: <DashboardOutlined />,
      label: '仪表板',
      onClick: () => navigate('/dashboard')
    },
    {
      key: 'sentiment',
      icon: <HeartOutlined />,
      label: '情感分析',
      onClick: () => navigate('/dashboard/sentiment')
    },
    {
      key: 'keywords',
      icon: <KeyOutlined />,
      label: '关键词提取',
      onClick: () => navigate('/dashboard/keywords')
    },
    {
      key: 'summary',
      icon: <FileTextOutlined />,
      label: '文本摘要',
      onClick: () => navigate('/dashboard/summary')
    },
    {
      key: 'similarity',
      icon: <SwapOutlined />,
      label: '相似度计算',
      onClick: () => navigate('/dashboard/similarity')
    },
    {
      key: 'history',
      icon: <HistoryOutlined />,
      label: '历史记录',
      onClick: () => navigate('/dashboard/history')
    },
    {
      key: 'stats',
      icon: <BarChartOutlined />,
      label: '统计分析',
      onClick: () => navigate('/dashboard/stats')
    }
  ];

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
        <div style={{ 
          height: 64, 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          color: 'white',
          fontSize: collapsed ? 16 : 18,
          fontWeight: 'bold'
        }}>
          {collapsed ? 'TA' : '文本分析'}
        </div>
        <Menu
          theme="dark"
          mode="inline"
          defaultSelectedKeys={['dashboard']}
          items={menuItems}
        />
      </Sider>
      
      <Layout>
        <Header style={{ 
          background: '#fff', 
          padding: '0 16px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <Title level={4} style={{ margin: 0 }}>智能文本分析系统</Title>
          <Button 
            type="primary" 
            icon={<LogoutOutlined />}
            onClick={handleLogout}
          >
            退出登录
          </Button>
        </Header>
        
        <Content style={{ margin: '24px 16px', padding: 24, background: '#fff', minHeight: 280 }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default Dashboard; 