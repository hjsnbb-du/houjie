import React from 'react';
import { Row, Col, Card, theme } from 'antd';
import StatisticCard from './StatisticCard';
import TrendChart from './TrendChart';
import { useDashboardData } from '../../hooks/useDashboardData';

const { useToken } = theme;

const Dashboard: React.FC = () => {
  const { stats, trends, loading, error } = useDashboardData();
  const { token } = useToken();

  if (error) {
    console.error('Dashboard error:', error);
  }

  return (
    <div className="dashboard-container" style={{ padding: '24px', background: token.colorBgContainer }}>
      {/* Work Order Statistics Row */}
      <Row gutter={[24, 24]}>
        <Col xs={24} sm={12} md={6}>
          <StatisticCard
            title="今日新工单"
            value={stats?.workOrders.newToday}
            loading={loading}
            type="default"
          />
        </Col>
        <Col xs={24} sm={12} md={6}>
          <StatisticCard
            title="今日完成工单"
            value={stats?.workOrders.completedToday}
            loading={loading}
            type="success"
          />
        </Col>
        <Col xs={24} sm={12} md={6}>
          <StatisticCard
            title="已完成工单"
            value={stats?.workOrders.totalCompleted}
            loading={loading}
            type="success"
          />
        </Col>
        <Col xs={24} sm={12} md={6}>
          <StatisticCard
            title="剩余工单"
            value={stats?.workOrders.remaining}
            loading={loading}
            type="warning"
          />
        </Col>
      </Row>

      {/* Customer Statistics and Work Order Statistics */}
      <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
        {/* Customer Statistics */}
        <Col xs={24} lg={12}>
          <Card title="客户统计" bordered={false}>
            <Row gutter={[16, 16]}>
              <Col span={12}>
                <StatisticCard
                  title="总客户数"
                  value={stats?.customers.total}
                  loading={loading}
                  type="default"
                />
              </Col>
              <Col span={12}>
                <StatisticCard
                  title="服务中客户数"
                  value={stats?.customers.active}
                  loading={loading}
                  type="success"
                />
              </Col>
              <Col span={12}>
                <StatisticCard
                  title="待跟进客户数"
                  value={stats?.customers.followUp}
                  loading={loading}
                  type="warning"
                />
              </Col>
              <Col span={12}>
                <StatisticCard
                  title="已到期客户数"
                  value={stats?.customers.expired}
                  loading={loading}
                  type="error"
                />
              </Col>
            </Row>
          </Card>
        </Col>

        {/* Work Order Statistics */}
        <Col xs={24} lg={12}>
          <Card title="工单统计" bordered={false}>
            <TrendChart
              title="工单趋势"
              data={trends?.workOrders || []}
              loading={loading}
              height={300}
            />
          </Card>
        </Col>
      </Row>

      {/* Trend Charts */}
      <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
        <Col xs={24}>
          <Card title="客户量趋势" bordered={false}>
            <TrendChart
              title="客户趋势"
              data={trends?.customers || []}
              loading={loading}
              height={300}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
