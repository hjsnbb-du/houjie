import { useState } from 'react'
import {
  DashboardOutlined,
  InboxOutlined,
  UserOutlined,
  ShoppingCartOutlined,
  SettingOutlined,
  LogoutOutlined
} from '@ant-design/icons'
import { Layout, Menu, Button, Table, Card, theme, Form, Input, Select, Badge, Tabs } from 'antd'
import { useAuth } from './contexts/AuthContext'
import { LoginForm } from './components/auth/LoginForm'
import { RegisterForm } from './components/auth/RegisterForm'
import Dashboard from './components/dashboard/Dashboard'

const { Header, Sider, Content } = Layout
const { useToken } = theme

const modules = [
  { id: 'dashboard', name: '仪表盘', icon: <DashboardOutlined /> },
  { id: 'inventory', name: '库存管理', icon: <InboxOutlined /> },
  { id: 'users', name: '用户管理', icon: <UserOutlined /> },
  { id: 'orders', name: '订单管理', icon: <ShoppingCartOutlined /> },
  { id: 'settings', name: '系统设置', icon: <SettingOutlined /> }
]

// Sample data for tables
const inventoryData = [
  { key: '1', name: '示例产品 1', sku: 'SKU001', quantity: 100, price: '¥299.00', status: '正常' },
  { key: '2', name: '示例产品 2', sku: 'SKU002', quantity: 50, price: '¥199.00', status: '低库存' },
]

const userData = [
  { key: '1', name: '张三', email: 'zhangsan@example.com', role: '管理员', status: '活跃', registerDate: '2024-01-18' },
  { key: '2', name: '李四', email: 'lisi@example.com', role: '用户', status: '活跃', registerDate: '2024-01-17' },
]

const orderData = [
  { key: '1', orderNo: 'ORD20240118001', customer: '王五', amount: '¥599.00', status: '待发货', orderDate: '2024-01-18 14:30' },
  { key: '2', orderNo: 'ORD20240118002', customer: '赵六', amount: '¥899.00', status: '已完成', orderDate: '2024-01-18 15:45' },
]

function App() {
  const { user, login, logout, register } = useAuth()
  const [activeModule, setActiveModule] = useState('dashboard')
  const { token } = useToken()

  if (!user) {
    return (
      <Layout style={{ minHeight: '100vh' }}>
        <Content style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          background: token.colorBgLayout
        }}>
          <Card style={{ width: 400 }}>
            <Tabs
              items={[
                { key: 'login', label: '登录', children: <LoginForm onLogin={login} /> },
                { key: 'register', label: '注册', children: <RegisterForm onRegister={register} /> }
              ]}
            />
          </Card>
        </Content>
      </Layout>
    )
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider theme="light" width={250} style={{ boxShadow: token.boxShadowTertiary }}>
        <div style={{ padding: 24, borderBottom: `1px solid ${token.colorBorder}` }}>
          <h1 style={{ margin: 0, fontSize: token.fontSizeHeading3, fontWeight: 600 }}>ERP系统</h1>
        </div>
        <Menu
          mode="inline"
          selectedKeys={[activeModule]}
          onClick={({ key }) => setActiveModule(key)}
          style={{ borderRight: 'none' }}
          items={modules.map(module => ({
            key: module.id,
            icon: module.icon,
            label: module.name,
          }))}
        />
        <div style={{
          position: 'absolute',
          bottom: 0,
          width: '100%',
          padding: '16px',
          borderTop: `1px solid ${token.colorBorder}`
        }}>
          <Button
            icon={<LogoutOutlined />}
            danger
            block
            style={{ height: '40px' }}
            onClick={logout}
          >
            退出登录
          </Button>
        </div>
      </Sider>
      <Layout>
        <Header style={{
          background: token.colorBgContainer,
          padding: '0 24px',
          borderBottom: `1px solid ${token.colorBorder}`,
          display: 'flex',
          alignItems: 'center',
          height: 64
        }}>
          <h2 style={{
            margin: 0,
            fontSize: token.fontSizeHeading4,
            fontWeight: 600
          }}>
            {modules.find(m => m.id === activeModule)?.name}
          </h2>
        </Header>
        <Content style={{ padding: 24, background: token.colorBgLayout }}>
          {activeModule === 'dashboard' && (
            <Dashboard />
          )}

          {activeModule === 'inventory' && (
            <Card title="库存列表">
              <Table
                dataSource={inventoryData}
                columns={[
                  { title: '产品名称', dataIndex: 'name', key: 'name', sorter: true },
                  { title: 'SKU', dataIndex: 'sku', key: 'sku' },
                  { title: '库存数量', dataIndex: 'quantity', key: 'quantity', sorter: true },
                  { title: '单价', dataIndex: 'price', key: 'price', sorter: true },
                  {
                    title: '状态',
                    dataIndex: 'status',
                    key: 'status',
                    render: (status) => (
                      <Badge
                        status={status === '正常' ? 'success' : 'warning'}
                        text={status}
                      />
                    )
                  },
                ]}
                pagination={{ pageSize: 10 }}
              />
            </Card>
          )}

          {activeModule === 'users' && (
            <Card title="用户列表">
              <Table
                dataSource={userData}
                columns={[
                  { title: '用户名', dataIndex: 'name', key: 'name', sorter: true },
                  { title: '邮箱', dataIndex: 'email', key: 'email' },
                  { title: '角色', dataIndex: 'role', key: 'role' },
                  {
                    title: '状态',
                    dataIndex: 'status',
                    key: 'status',
                    render: (status) => (
                      <Badge
                        status={status === '活跃' ? 'success' : 'default'}
                        text={status}
                      />
                    )
                  },
                  { title: '注册时间', dataIndex: 'registerDate', key: 'registerDate', sorter: true },
                ]}
                pagination={{ pageSize: 10 }}
              />
            </Card>
          )}

          {activeModule === 'orders' && (
            <Card title="订单列表">
              <Table
                dataSource={orderData}
                columns={[
                  { title: '订单号', dataIndex: 'orderNo', key: 'orderNo' },
                  { title: '客户', dataIndex: 'customer', key: 'customer', sorter: true },
                  { title: '金额', dataIndex: 'amount', key: 'amount', sorter: true },
                  {
                    title: '状态',
                    dataIndex: 'status',
                    key: 'status',
                    render: (status) => (
                      <Badge
                        status={
                          status === '已完成' ? 'success' :
                          status === '待发货' ? 'processing' :
                          'default'
                        }
                        text={status}
                      />
                    )
                  },
                  { title: '下单时间', dataIndex: 'orderDate', key: 'orderDate', sorter: true },
                ]}
                pagination={{ pageSize: 10 }}
              />
            </Card>
          )}

          {activeModule === 'settings' && (
            <Card title="系统设置">
              <Form layout="vertical" style={{ maxWidth: 600 }}>
                <Form.Item label="公司名称" name="companyName">
                  <Input placeholder="请输入公司名称" />
                </Form.Item>
                <Form.Item label="系统语言" name="language">
                  <Select
                    placeholder="请选择系统语言"
                    options={[
                      { value: 'zh', label: '中文' },
                      { value: 'en', label: 'English' },
                    ]}
                  />
                </Form.Item>
                <Form.Item label="时区" name="timezone">
                  <Select
                    placeholder="请选择时区"
                    options={[
                      { value: 'Asia/Shanghai', label: '中国标准时间 (UTC+8)' },
                      { value: 'UTC', label: '协调世界时 (UTC)' },
                    ]}
                  />
                </Form.Item>
                <Form.Item>
                  <Button type="primary">保存设置</Button>
                </Form.Item>
              </Form>
            </Card>
          )}
        </Content>
      </Layout>
    </Layout>
  )
}

export default App
