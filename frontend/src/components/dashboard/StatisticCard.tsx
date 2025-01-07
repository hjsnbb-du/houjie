import React from 'react';
import { Card, Statistic, theme } from 'antd';
import { StatisticProps } from 'antd/es/statistic/Statistic';

interface StatisticCardProps extends Omit<StatisticProps, 'title'> {
  title: string;
  loading?: boolean;
  type?: 'default' | 'success' | 'warning' | 'error';
}

const StatisticCard: React.FC<StatisticCardProps> = ({
  title,
  value,
  loading = false,
  type = 'default',
  ...props
}) => {
  const { token } = theme.useToken();

  const getColorByType = () => {
    switch (type) {
      case 'success':
        return token.colorSuccess;
      case 'warning':
        return token.colorWarning;
      case 'error':
        return token.colorError;
      default:
        return token.colorPrimary;
    }
  };

  return (
    <Card loading={loading} bordered={false} style={{ height: '100%', boxShadow: token.boxShadowTertiary }}>
      <Statistic
        title={<span style={{ color: token.colorTextSecondary }}>{title}</span>}
        value={value}
        valueStyle={{ color: getColorByType(), fontSize: token.fontSizeLG }}
        {...props}
      />
    </Card>
  );
};

export default StatisticCard;
